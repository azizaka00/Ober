"""Takliflar va chat sahifasini ko‘z bilan sinash uchun qayta yaratiladigan demo."""

from __future__ import annotations

import baza

# 2026-08-06: demo rasm eski `/chat-uploads/demo-nexia-kolodka-v1.png` edi —
# fayl serverda yo'q va konsolda 404 berardi. Endi har doim mavjud bo'lgan
# brend rasm ishlatiladi (server `/brend/` fayllarini bir yil keshlaydi).
DEMO_RASM = "/brend/seller-navy-panel.webp"


def tozala() -> None:
    baza.init()
    with baza.ulan() as c:
        sotuvchilar = [r["id"] for r in c.execute(
            "SELECT id FROM sotuvchilar WHERE aloqa LIKE 'demo-chat-%'")]
        sorovlar = [r["id"] for r in c.execute(
            "SELECT id FROM sorovlar WHERE aloqa='demo-chat-buyer'")]
        if sorovlar:
            belgilar = ",".join("?" for _ in sorovlar)
            suhbatlar = [r["id"] for r in c.execute(
                f"SELECT id FROM suhbatlar WHERE sorov_id IN ({belgilar})", sorovlar)]
            if suhbatlar:
                sb = ",".join("?" for _ in suhbatlar)
                c.execute(f"DELETE FROM xabarlar WHERE suhbat_id IN ({sb})", suhbatlar)
                c.execute(f"DELETE FROM suhbatlar WHERE id IN ({sb})", suhbatlar)
            c.execute(f"DELETE FROM javoblar WHERE sorov_id IN ({belgilar})", sorovlar)
            c.execute(f"DELETE FROM sorovlar WHERE id IN ({belgilar})", sorovlar)
        if sotuvchilar:
            belgilar = ",".join("?" for _ in sotuvchilar)
            c.execute(f"DELETE FROM sotuvchilar WHERE id IN ({belgilar})", sotuvchilar)


def main() -> None:
    tozala()
    avto = baza.sotuvchi_yoz(
        "Avto Lider", "Nexia kolodka va tormoz qismlari", ["kolodka"],
        ["nexia"], "Chilonzor", "demo-chat-avto")
    gm = baza.sotuvchi_yoz(
        "GM Parts", "GM avtomobillari uchun kolodka", ["kolodka"],
        ["nexia"], "Sergeli", "demo-chat-gm")
    usta = baza.sotuvchi_yoz(
        "Nexia Usta", "Nexia ehtiyot qismlari va servis", ["kolodka"],
        ["nexia"], "Yunusobod", "demo-chat-usta")
    sorov = baza.sorov_yoz(
        "Nexia old kolodka", "Toshkent", "demo-chat-buyer", 210_000,
        ["nexia"], ["kolodka"])

    chat1 = baza.javob_yoz(
        sorov, avto, "bor", 185_000, "Narxi yakuniy, hozir bor.")
    baza.suhbat_xabar_yoz(
        chat1, "sotuvchi", avto,
        "Original GM kolodka bor, rasmini yubordim", DEMO_RASM)
    baza.javob_yoz(
        sorov, gm, "bor", 205_000, "Yetkazib berish ham bor, 20 daqiqada tayyor.")
    chat3 = baza.javob_yoz(
        sorov, usta, "bor", 170_000, "Ertaga olib ketsangiz bo‘ladi.")
    baza.suhbat_ol(chat3, "xaridor", sorov)

    print("OBER chat demosi tayyor")
    print(f"Xaridor: http://127.0.0.1:8800/takliflar?sorov={sorov}")
    print(f"Sotuvchi: http://127.0.0.1:8800/takliflar?rol=sotuvchi&seller={avto}")
    print(f"sorov_id={sorov} sotuvchi_id={avto} chat_id={chat1}")


if __name__ == "__main__":
    main()
