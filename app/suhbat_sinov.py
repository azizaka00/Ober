"""OBER ichki taklif/chat halqasi uchun deterministik regressiya testi."""

from __future__ import annotations

import base64
import tempfile
from pathlib import Path

import baza
import server


def tekshir(shart: bool, nom: str) -> None:
    if not shart:
        raise AssertionError(nom)
    print(f"  OK  {nom}")


def main() -> None:
    eski_db, eski_uploads = baza.DB, server.UPLOADS
    # sqlite3 context manager commit qiladi, lekin Windowsda fayl handle'i
    # interpreter GC'sigacha ochiq qolishi mumkin; sinov natijasini cleanup
    # timingiga bog'lamaymiz.
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as papka:
        ildiz = Path(papka)
        baza.DB = ildiz / "ober-test.db"
        server.UPLOADS = ildiz / "uploads"
        baza._INIT_QILINDI.clear()
        try:
            baza.init()
            sotuvchi = baza.sotuvchi_yoz(
                "Avto Lider", "Nexia kolodka", ["kolodka"], ["nexia"],
                "Chilonzor", "+998901112233")
            sorov = baza.sorov_yoz(
                "Nexia old kolodka", "Chilonzor", "+998909998877",
                200_000, ["nexia"], ["kolodka"])
            xaridor_token = baza.sorov_tokeni(sorov)
            sotuvchi_token = baza.sessiya_yarat(sotuvchi)
            tekshir(bool(xaridor_token) and not xaridor_token.isdigit(),
                    "xaridor uchun yopiq sessiya tokeni yaratildi")
            tekshir(baza.sorov_id_token(xaridor_token) == sorov,
                    "xaridor tokeni faqat o'z so'roviga yechiladi")
            tekshir(server._actor_ident({"actor": [str(sorov)]},
                                        "xaridor") == 0,
                    "raqamli so'rov ID autentifikatsiya bo'lmaydi")
            tekshir(server._actor_ident({"actor": [xaridor_token]},
                                        "xaridor") == sorov,
                    "xaridor tokeni chat aktorini tasdiqlaydi")
            tekshir(server._sotuvchi_ident({"id": [str(sotuvchi)]}) == 0,
                    "raqamli sotuvchi ID autentifikatsiya bo'lmaydi")
            tekshir(server._sotuvchi_ident({"id": [sotuvchi_token]}) == sotuvchi,
                    "sotuvchi sessiya tokeni kabinetni tasdiqlaydi")
            suhbat = baza.javob_yoz(
                sorov, sotuvchi, "bor", 185_000,
                "Original GM kolodka bor, rasmini yubordim",
                "/chat-uploads/seller.webp")
            tekshir(bool(suhbat), "ijobiy taklif suhbat yaratadi")

            lenta = baza.sorov_takliflari(sorov)
            taklif = lenta["takliflar"][0]
            tekshir(taklif["oqilmagan"] == 1,
                    "xaridor chatga kirmasdan yangi xabarni ko‘radi")
            tekshir("aloqa" not in taklif and "+998" not in str(lenta),
                    "telefon raqamlari taklif lentasiga chiqmaydi")
            tekshir(taklif["oxirgi_rasm"].endswith("seller.webp"),
                    "sotuvchi rasmi previewda ko‘rinadi")
            buyer_notice = baza.bildirishnomalar_ol("xaridor", sorov)
            tekshir(buyer_notice["jami"] == 1 and
                    buyer_notice["bildirishnomalar"][0]["sarlavha"] ==
                    "Sotuvchi · Avto Lider",
                    "xaridor markazida sotuvchi bildirishnomasi ko‘rinadi")
            tekshir("+998" not in str(buyer_notice),
                    "bildirishnoma markazi telefonni oshkor qilmaydi")

            ochildi = baza.suhbat_ol(suhbat, "xaridor", sorov)
            tekshir(len(ochildi["xabarlar"]) == 1,
                    "xaridor suhbatni ochadi")
            tekshir(baza.sorov_takliflari(sorov)["takliflar"][0]["oqilmagan"] == 0,
                    "ochilgan xabar o‘qildi bo‘ladi")
            tekshir(baza.bildirishnomalar_ol("xaridor", sorov)["jami"] == 0,
                    "chat ochilganda xaridor badge’i tozalanadi")
            tekshir(baza.suhbat_ol(suhbat, "xaridor", sorov + 99) is None,
                    "begona xaridor suhbatga kirmaydi")

            tanlangan = baza.taklif_tanla(sorov, taklif["javob_id"])
            tekshir(tanlangan == suhbat, "xaridor taklifni tanlaydi")
            baza.suhbat_xabar_yoz(
                suhbat, "xaridor", sorov, "Manzilingizni yuboring",
                "/chat-uploads/buyer.jpg")
            sotuvchi_lenta = baza.sotuvchi_suhbatlari(sotuvchi)
            tekshir(sotuvchi_lenta[0]["oqilmagan"] == 1,
                    "sotuvchi xaridorning yangi xabarini ko‘radi")
            tekshir(sotuvchi_lenta[0]["oxirgi_rasm"].endswith("buyer.jpg"),
                    "xaridor ham rasm yubora oladi")
            seller_notice = baza.bildirishnomalar_ol("sotuvchi", sotuvchi)
            tekshir(seller_notice["jami"] == 1 and
                    seller_notice["bildirishnomalar"][0]["suhbat_id"] == suhbat,
                    "sotuvchi markazida xaridor xabari ko‘rinadi")
            tekshir(baza.bildirishnomalar_ol("begona", sotuvchi)["jami"] == 0,
                    "noto‘g‘ri rol bildirishnoma olmaydi")
            tekshir(baza.bildirishnomalar_oqildi("sotuvchi", sotuvchi) == 1 and
                    baza.bildirishnomalar_ol("sotuvchi", sotuvchi)["jami"] == 0,
                    "sotuvchi barcha bildirishnomani o‘qilgan qiladi")

            baza.suhbat_ol(suhbat, "sotuvchi", sotuvchi)
            baza.suhbat_xabar_yoz(
                suhbat, "sotuvchi", sotuvchi, "Joylashuvni yubordim",
                "/chat-uploads/location.png")
            tekshir(baza.sorov_takliflari(sorov)["takliflar"][0]["oqilmagan"] == 1,
                    "sotuvchi javobi xaridorga unread bo‘ladi")
            tekshir(baza.bildirishnomalar_ol("xaridor", sorov)["jami"] == 1,
                    "sotuvchi javobi xaridor markaziga keladi")
            tekshir(baza.bildirishnomalar_oqildi("xaridor", sorov) == 1 and
                    baza.bildirishnomalar_ol("xaridor", sorov)["jami"] == 0,
                    "xaridor barcha bildirishnomani o‘qilgan qiladi")
            tekshir(baza.suhbat_xabar_yoz(
                suhbat, "sotuvchi", sotuvchi + 1, "Begona", "") is None,
                "begona sotuvchi xabar yubora olmaydi")

            # 1x1 PNG: server faqat ruxsatli rasm formatini va hajmini qabul qiladi.
            png = base64.b64encode(
                b"\x89PNG\r\n\x1a\n" + b"OBER-test-image").decode()
            manzil = server.Ishlovchi._rasm_saqla(
                None, "data:image/png;base64," + png)
            tekshir(manzil.startswith("/chat-uploads/") and
                    (server.UPLOADS / manzil.rsplit("/", 1)[-1]).is_file(),
                    "rasm UUID nom bilan lokal saqlanadi")
            try:
                server.Ishlovchi._rasm_saqla(
                    None, "data:text/plain;base64," + base64.b64encode(b"x").decode())
                raise AssertionError("matn fayli qabul qilindi")
            except ValueError:
                print("  OK  rasm bo‘lmagan fayl rad etiladi")

            print("\nSUHBAT VA BILDIRISHNOMA SINOVI: 28/28")
        finally:
            baza.DB = eski_db
            server.UPLOADS = eski_uploads
            baza._INIT_QILINDI.clear()


if __name__ == "__main__":
    main()
