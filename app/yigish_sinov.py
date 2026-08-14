"""Faol/nofaol sikl va adapter interfeysi uchun xavfsiz lokal sinov."""

from __future__ import annotations

import tempfile
from pathlib import Path

import baza
import qidiruv
import tahlil
import yigish

OK = 0
XATO = 0


def tek(shart: bool, nom: str) -> None:
    global OK, XATO
    if shart:
        OK += 1
        print(f"  [OK  ] {nom}")
    else:
        XATO += 1
        print(f"  [XATO] {nom}")


def elon(tashqi_id: str, nom: str) -> dict:
    return {
        "manba": "olx", "tashqi_id": tashqi_id, "nom": nom,
        "narx_som": 250_000, "narx_asl": "250 000 so‘m", "valyuta": "som",
        "viloyat": "Toshkent viloyati", "shahar": "Toshkent",
        "tuman": "Sergeli", "sana": "2026-07-31",
        "havola": f"https://example.uz/{tashqi_id}", "rasm": "rasm.webp",
        "qism_turi": "Tormoz tizimi",
    }


def main() -> None:
    global OK, XATO
    asl_db = baza.DB
    with tempfile.TemporaryDirectory(prefix="ober-yigish-") as papka:
        baza.DB = Path(papka) / "sinov.db"
        try:
            baza.init()
            with baza.ulan() as c:
                ustunlar = {r["name"] for r in c.execute("PRAGMA table_info(elonlar)")}
            tek({"faol", "korilmadi", "oxirgi_sikl"} <= ustunlar,
                "faollik migratsiyasi yaratildi")

            s1 = baza.sikl_boshlash("olx")
            tek(baza.saqla(elon("a1", "Nexia kolodka old"), s1) == "yangi",
                "yangi e’lon siklga yozildi")
            tek(baza.sikl_yakunla("olx", s1, True)["toliq"],
                "to‘liq sikl yakunlandi")

            # Issiq va to'liq yig'uvchilar alohida jarayonda ishlaydi.
            # Issiq sikl bo'sh belgi bilan e'lonni yangilaganda to'liq
            # siklning belgisi yo'qolmasligi kerak.
            baza.saqla(elon("a1", "Nexia kolodka old"), "")
            with baza.ulan() as c:
                belgi = c.execute(
                    "SELECT oxirgi_sikl FROM elonlar WHERE tashqi_id='a1'"
                ).fetchone()["oxirgi_sikl"]
            tek(belgi == s1, "issiq sikl to'liq sikl belgisini saqladi")

            for kutilgan in (1, 2, 3):
                s = baza.sikl_boshlash("olx")
                # Manba ishlayapti, lekin a1 yo‘qolgan: nol natijali umumiy
                # nosozlik bilan haqiqiy yo‘qolishni adashtirmaymiz.
                baza.saqla(elon("anchor", "Cobalt fara tayanch"), s)
                baza.sikl_yakunla("olx", s, True)
                with baza.ulan() as c:
                    r = c.execute("SELECT faol, korilmadi FROM elonlar WHERE tashqi_id='a1'").fetchone()
                tek(r["korilmadi"] == kutilgan,
                    f"ko‘rinmaslik hisoblandi: {kutilgan}/3")

            tek(r["faol"] == 0, "uch sikldan keyin e’lon nofaol bo‘ldi")

            # Partial sikl boshqa e’lonlarning hisobini oshirmaydi.
            partial = baza.sikl_boshlash("olx")
            baza.sikl_yakunla("olx", partial, False)
            with baza.ulan() as c:
                p = c.execute("SELECT korilmadi FROM elonlar WHERE tashqi_id='a1'").fetchone()
            tek(p["korilmadi"] == 3, "partial sikl nofaollikni o‘zgartirmadi")

            aktiv = baza.sikl_boshlash("olx")
            baza.saqla(elon("a2", "Nexia kolodka yangi"), aktiv)
            tahlil.main()
            qidiruv._KESH = []
            qidiruv._KESH_VAQT = -1
            natija = qidiruv.qidir("neksiya kolodka")
            idlar = {r["tashqi_id"] for r in natija["natijalar"]}
            tek("a2" in idlar and "a1" not in idlar,
                "qidiruv faqat faol e’lonni ko‘rsatdi")

            qaytish = baza.sikl_boshlash("olx")
            tek(baza.saqla(elon("a1", "Nexia kolodka old"), qaytish) == "qaytdi",
                "qayta ko‘ringan e’lon faollashdi")
            with baza.ulan() as c:
                r = c.execute("SELECT faol, korilmadi FROM elonlar WHERE tashqi_id='a1'").fetchone()
            tek(r["faol"] == 1 and r["korilmadi"] == 0,
                "qaytgan e’lon hisoblagichi tozalandi")

            adapterlar = yigish.adapterlar()
            tek("olx" in adapterlar, "OLX umumiy adapterdan topildi")
            # Yangi manba qo'shilgach sinov uni ham tekshiradi: shartnoma
            # (MANBA, NOM, bosh, chuqur) buzilsa — darhol ko'rinadi.
            # 2026-08-13/14: avtoelon, asaxiy, shahar, glotr, avizinfo.
            for nomi, manba in (("avtoelon", "avtoelon"),
                                ("asaxiy", "asaxiy"),
                                ("shahar", "shahar"),
                                ("glotr", "glotr"),
                                ("avizinfo", "avizinfo")):
                tek(nomi in adapterlar, f"{nomi} adapteri topildi")
                if nomi in adapterlar:
                    a = adapterlar[nomi]
                    tek(a.MANBA == manba and callable(a.bosh)
                        and callable(a.chuqur),
                        f"{nomi} shartnomasi to'g'ri (MANBA/bosh/chuqur)")

            # 403-blok xulqi (2026-08-13): sayt IP'ni bloklaganda adapter
            # birinchi xatoda to'xtaydi — 16 bo'limni urib saytni bosmaydi.
            # Bu xulq buzilsa (masalan, 403 '' qaytarib davom etsa) sinov
            # tutib qoladi.
            if "asaxiy" in adapterlar:
                import manbalar.asaxiy as asaxiy
                asl_ol = asaxiy._sahifa_ol

                def _blok(yol: str) -> str:  # har so'rov 403
                    raise asaxiy._Bloklandi(f"{yol} -> test 403")

                asaxiy._sahifa_ol = _blok
                try:
                    natija = asaxiy.bosh(1)
                finally:
                    asaxiy._sahifa_ol = asl_ol
                tek(natija.get("xato") == 1 and natija.get("yangi") == 0,
                    "asaxiy 403'da to'xtaydi (sayt urilmaydi)")
        finally:
            # sqlite connection context manager commit qiladi, lekin Windowsda
            # obyektga oxirgi reference qolsa temp faylni darhol bo‘shatmaydi.
            if "c" in locals():
                c.close()
            baza.DB = asl_db
            qidiruv._KESH = []
            qidiruv._KESH_VAQT = -1

    print(f"\n  NATIJA: {OK} to‘g‘ri · {XATO} xato")
    if XATO:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
