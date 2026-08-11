"""OBER ichki taklif/chat halqasi uchun deterministik regressiya testi."""

from __future__ import annotations

import base64
import tempfile
from pathlib import Path

import baza
import server
import tg


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
            for i in range(12):
                baza.saqla({
                    "manba": "olx", "tashqi_id": f"vitrina-{i}",
                    "nom": f"Sinov divan {i}", "narx_som": 1_000_000 + i,
                    "narx_asl": "", "valyuta": "UZS", "kelishiladi": 0,
                    "holat": "yangi", "viloyat": "Toshkent shahri",
                    "shahar": "Toshkent", "tuman": "Chilonzor",
                    "sana": "2026-08-11", "havola": f"https://example.com/{i}",
                    "rasm": "/brend/icon.png", "telefon": "", "biznes": 0,
                    "qism_turi": "", "tavsif": "", "sotuvchi_id": "",
                    "sotuvchi_nomi": "", "kategoriya": f"Sinov bo‘lim {i % 4}",
                    "xususiyatlar": "[]", "olx_kategoriya": "Mebel",
                })
            baza._YANGI_KESH.update({"vaqt": 0.0, "n": 0, "royxat": []})
            tekshir(len(baza.yangi_elonlar(12)) == 12,
                    "vitrina xilma-xillikdan keyin zaxira kartalar bilan to‘ladi")

            sotuvchi = baza.sotuvchi_yoz(
                "Avto Lider", "Nexia kolodka", ["kolodka"], ["nexia"],
                "Chilonzor", "+998901112233")
            sorov = baza.sorov_yoz(
                "Nexia old kolodka", "Chilonzor", "+998909998877",
                200_000, ["nexia"], ["kolodka"])
            baza.tolqin_yubor(sorov)
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

            # Telegram xato qaytarsa bildirishnoma yo'qolmasin; muvaffaqiyatli
            # urinishdan keyingina belgilansin va qayta yuborilmasin.
            with baza.ulan() as c:
                c.execute("UPDATE sotuvchilar SET telegram_id=? WHERE id=?",
                          ("tg-test-1", sotuvchi))
            eski_yubor = tg.yubor
            yuborilgan_tg = []
            try:
                tg.yubor = lambda *args, **kwargs: False
                tekshir(tg.kutayotganlarni_yubor() == 0 and
                        len(baza.yuborilmagan_xabarlar()) == 1,
                        "Telegram xatosida yangi so‘rov navbatda qoladi")
                def tg_qabul(*args, **kwargs):
                    yuborilgan_tg.append((args, kwargs))
                    return True
                tg.yubor = tg_qabul
                tekshir(tg.kutayotganlarni_yubor() == 1 and
                        not baza.yuborilmagan_xabarlar(),
                        "yangi so‘rov Telegramga muvaffaqiyatli yuboriladi")
                tekshir(tg.kutayotganlarni_yubor() == 0 and
                        len(yuborilgan_tg) == 1,
                        "yangi so‘rov Telegramga takror yuborilmaydi")
                tekshir("Nexia old kolodka" in yuborilgan_tg[0][0][1] and
                        yuborilgan_tg[0][0][2],
                        "Telegram bildirishnomasida so‘rov va javob tugmalari bor")
            finally:
                tg.yubor = eski_yubor

            # Chiquvchi bildirishlar `getUpdates` long-pollidan mustaqil
            # siklda yuradi. Sikl ikkala navbatni ham bir aylanishda ko'radi.
            eski_sorov_bildir = tg.kutayotganlarni_yubor
            eski_chat_bildir = tg.kutayotgan_chatlarni_yubor
            bildirish_chaqirildi = []
            try:
                tg.kutayotganlarni_yubor = lambda: bildirish_chaqirildi.append(
                    "sorov") or 1
                tg.kutayotgan_chatlarni_yubor = lambda: bildirish_chaqirildi.append(
                    "chat") or 2
                tekshir(tg.bildirish_sikli() == 3 and
                        bildirish_chaqirildi == ["sorov", "chat"],
                        "Telegram chiquvchi sikli ikki navbatni long-polldan mustaqil tekshiradi")
            finally:
                tg.kutayotganlarni_yubor = eski_sorov_bildir
                tg.kutayotgan_chatlarni_yubor = eski_chat_bildir

            tg_tashxis = baza.tg_holat()
            tekshir("ulanganlar" not in tg_tashxis and
                    tg_tashxis["telegramga_ulangan"] == 1,
                    "ochiq Telegram tashxisi sotuvchi ma'lumotini oshkor qilmaydi")

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
            tekshir("aloqa" not in str(ochildi) and "+998" not in str(ochildi),
                    "buyer chat API sotuvchi telefonini oshkor qilmaydi")
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

            # Xaridor xabari ham sotuvchiga Telegram orqali yetadi. API
            # yiqilsa belgi qo'yilmaydi va keyingi aylanish qayta urinadi.
            eski_yubor = tg.yubor
            chat_tg = []
            try:
                tg.yubor = lambda *args, **kwargs: False
                tekshir(tg.kutayotgan_chatlarni_yubor() == 0 and
                        len(baza.tg_kutayotgan_chat()) == 1,
                        "Telegram xatosida xaridor xabari navbatda qoladi")
                def tg_chat_qabul(*args, **kwargs):
                    chat_tg.append((args, kwargs))
                    return True
                tg.yubor = tg_chat_qabul
                tekshir(tg.kutayotgan_chatlarni_yubor() == 1 and
                        not baza.tg_kutayotgan_chat(),
                        "xaridor xabari sotuvchining Telegramiga yuboriladi")
                tekshir("Manzilingizni yuboring" in chat_tg[0][0][1] and
                        "OBER chatini ochish" in str(chat_tg[0][0][2]),
                        "Telegram xabarida matn va chatga o‘tish tugmasi bor")
                tekshir(tg.kutayotgan_chatlarni_yubor() == 0 and
                        len(chat_tg) == 1,
                        "xaridor xabari Telegramga takror yuborilmaydi")
            finally:
                tg.yubor = eski_yubor

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

            # Valid sessiya tokeni sorov_id ni taxmin qilishga ruxsat emas.
            tekshir(baza.javob_yoz(
                sorov + 999, sotuvchi, "bor", 1, "") is None,
                "taxmin qilingan so'rovga javob berilmaydi")
            begona_sotuvchi = baza.sotuvchi_yoz(
                "Mebelchi", "divan shkaf", [], [], "Chilonzor", "+998900001111")
            tekshir(baza.javob_yoz(
                sorov, begona_sotuvchi, "bor", 1, "") is None,
                "tayinlanmagan sotuvchi javob bera olmaydi")
            tekshir(baza.javob_yoz(
                sorov, sotuvchi, "bor", 1, "") is None,
                "bir sotuvchi takroriy javob bera olmaydi")

            expired = baza.sorov_yoz(
                "Nexia kolodka muddati", "Chilonzor", "+998909998878",
                210_000, ["nexia"], ["kolodka"])
            baza.tolqin_yubor(expired)
            with baza.ulan() as c:
                c.execute("UPDATE sorovlar SET yopiladi=? WHERE id=?",
                          (0, expired))
            tekshir(baza.javob_yoz(
                expired, sotuvchi, "bor", 1, "") is None,
                "muddati tugagan so'rovga javob berilmaydi")

            rad_etildi = baza.sorov_yoz(
                "Nexia kolodka boshqa", "Chilonzor", "+998909998879",
                220_000, ["nexia"], ["kolodka"])
            baza.tolqin_yubor(rad_etildi)
            tekshir(baza.javob_yoz(
                rad_etildi, sotuvchi, "yoq", None, "") == 0,
                "valid yo'q javobi invalid urinishdan ajratiladi")

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

            # ── TOPISH NATIJASI (2026-08-10) ─────────────────────────
            # OBER to'lovni bajarmaydi. Xaridor kerakli narsani OBER
            # qidiruvi orqali yoki boshqa joydan topganini hisobga olamiz.
            tekshir(not baza.natija_yoz(sorov, "boshqa-narsa"),
                    "notanish natija qabul qilinmaydi")
            tekshir(not baza.natija_yoz(sorov + 9999, "ober"),
                    "yo'q so'rov natijasi saqlandi deb aytilmaydi")
            tekshir(baza.natija_yoz(sorov, "tashqarida"),
                    "boshqa joydan topilgan natija yozib olinadi")
            with baza.ulan() as c:
                r = c.execute("SELECT natija FROM sorovlar WHERE id=?",
                              (sorov,)).fetchone()
            tekshir(r["natija"] == "tashqarida",
                    "natija bazada saqlandi")
            tekshir(baza.natija_yoz(sorov, "ober"),
                    "natijani keyin o'zgartirish mumkin")
            sanoq = baza.natija_sanogi()
            tekshir(sanoq.get("ober") == 1,
                    "natija sanog'i to'g'ri hisoblaydi")

            # ── ESKIRGAN BILDIRISHNOMA YUBORILMAYDI (2026-08-11) ─────
            # Savdo bildirishnomalari qayta yoqilganda navbatda 7
            # KUNLIK xabarlar turgan edi. Ularni endi yuborish
            # sotuvchini chalg'itadi — xabar emas, shovqin.
            import time as _t
            with baza.ulan() as c:
                c.execute("UPDATE sotuvchilar SET telegram_id='111222333'"
                          " WHERE id=?", (sotuvchi,))
                c.execute("UPDATE xabarlar SET rol='xaridor', tg_yuborildi=0,"
                          " vaqt=? WHERE suhbat_id=?",
                          (_t.time() - 200 * 3600, suhbat))
            tekshir(len(baza.tg_kutayotgan_chat()) == 0,
                    "7 kunlik chat xabari Telegramga uzatilmaydi")
            with baza.ulan() as c:
                c.execute("UPDATE xabarlar SET vaqt=? WHERE suhbat_id=?",
                          (_t.time() - 60, suhbat))
            tekshir(len(baza.tg_kutayotgan_chat()) > 0,
                    "yangi chat xabari esa uzatiladi")

            # ── 403 CHEKSIZ TAKRORLANMASIN (2026-08-11) ──────────────
            # Jonli serverda bildirishnomalar yoqilganda jurnal har 2
            # soniyada "HTTP 403 (sendMessage)" bilan to'lgan edi:
            # sotuvchi botni ochmagan, xabar belgilanmagan, halqa esa
            # to'xtovsiz qayta urinaverган.
            eski_sorov, eski_savdo = tg._sorov, tg.SAVDO_XABARLARI
            try:
                tg.SAVDO_XABARLARI = True
                chaqirildi = {"soni": 0}

                def _soxta_403(usul, _timeout=35, **maydonlar):
                    chaqirildi["soni"] += 1
                    tg._OXIRGI_KOD["kod"] = 403
                    return None

                tg._sorov = _soxta_403
                oldin = len(baza.tg_kutayotgan_chat())
                tekshir(oldin > 0, "sinovdan oldin navbatda xabar bor")
                tg.kutayotgan_chatlarni_yubor()
                tekshir(len(baza.tg_kutayotgan_chat()) == 0,
                        "403 dan keyin xabar navbatdan chiqadi")
                urinish = chaqirildi["soni"]
                tg.kutayotgan_chatlarni_yubor()
                tekshir(chaqirildi["soni"] == urinish,
                        "403 dan keyin qayta urinilmaydi")
            finally:
                tg._sorov, tg.SAVDO_XABARLARI = eski_sorov, eski_savdo

            print("\nSUHBAT VA BILDIRISHNOMA SINOVI: 56/56")
        finally:
            baza.DB = eski_db
            server.UPLOADS = eski_uploads
            baza._INIT_QILINDI.clear()


if __name__ == "__main__":
    main()
