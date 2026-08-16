"""
OBER — TO'LQINLI YUBORISH SINOVI

Tekshiradi:
  1. So'rov faqat MOS sotuvchilarga boradi (banner sotuvchisiga fara emas)
  2. Qaytadigan son HAQIQIY (15 ta bo'lsa 15, "30 ta" deb yozilmaydi)
  3. Sotuvchi faqat o'ziga yuborilgan so'rovni ko'radi
  4. Tushunilmagan so'rov hech kimga bormaydi

Sinov o'z ma'lumotini yaratadi va oxirida tozalaydi — asosiy bazaga
tegmaydi.
"""

from __future__ import annotations

import baza
from lugat import modellarni_top, qismlarni_top
from yonalishlar import yonalishlarni_top

XATO = 0


def tekshir(shart: bool, izoh: str) -> None:
    global XATO
    print(f"    {'OK  ' if shart else 'XATO'}  {izoh}")
    if not shart:
        XATO += 1


def sorov_yarat(matn: str, tuman: str = "") -> int:
    return baza.sorov_yoz(matn, tuman, "sinov-xaridor", None,
                          sorted(modellarni_top(matn)),
                          sorted(qismlarni_top(matn)),
                          sorted(yonalishlarni_top(matn)))


def main() -> None:
    baza.init()
    print("=" * 62)
    print("  OBER — to'lqinli yuborish sinovi")
    print("=" * 62)

    yaratilgan_sotuvchilar = []
    yaratilgan_sorovlar = []

    try:
        # ── Sotuvchilar: 3 ta fara, 1 ta banner
        for i in range(3):
            sid = baza.sotuvchi_yoz(
                f"Sinov Fara {i}", "fara, stop", ["fara"], [],
                "Chilonzor", f"+99890000000{i}", [])
            yaratilgan_sotuvchilar.append(sid)
        banner_id = baza.sotuvchi_yoz(
            "Sinov Banner", "banner, poligrafiya", [], [],
            "Chilonzor", "+998900000099", ["banner_reklama"])
        yaratilgan_sotuvchilar.append(banner_id)

        # ── 1. Fara so'rovi
        print("\n  1) 'kobalt fara' so'rovi")
        s1 = sorov_yarat("kobalt fara", "Chilonzor")
        yaratilgan_sorovlar.append(s1)
        n1 = baza.tolqin_yubor(s1)

        tekshir(n1["yuborildi"] >= 3,
                f"mos sotuvchilarga yetdi (yuborildi={n1['yuborildi']})")
        tekshir(n1["yuborildi"] == n1["mos"],
                f"haqiqiy son ko'rsatilyapti ({n1['yuborildi']} = mos {n1['mos']})")
        tekshir(n1["yuborildi"] <= baza.CHEGARA_BOSHLANGICH,
                f"chegaradan oshmadi (<= {baza.CHEGARA_BOSHLANGICH})")

        # Banner sotuvchisi fara so'rovini KO'RMASLIGI kerak
        banner_korgani = [x["id"] for x in baza.sotuvchi_sorovlari(banner_id)]
        tekshir(s1 not in banner_korgani,
                "banner sotuvchisiga fara so'rovi BORMADI")

        fara_korgani = [x["id"] for x in
                        baza.sotuvchi_sorovlari(yaratilgan_sotuvchilar[0])]
        tekshir(s1 in fara_korgani, "fara sotuvchisi so'rovni ko'rdi")

        # ── 2. Banner so'rovi
        print("\n  2) '25 m banner kerak' so'rovi")
        s2 = sorov_yarat("25 m2 banner kerak", "Chilonzor")
        yaratilgan_sorovlar.append(s2)
        n2 = baza.tolqin_yubor(s2)
        tekshir(n2["yuborildi"] >= 1, "banner sotuvchisiga yetdi")

        fara_korgani2 = [x["id"] for x in
                         baza.sotuvchi_sorovlari(yaratilgan_sotuvchilar[0])]
        tekshir(s2 not in fara_korgani2,
                "fara sotuvchisiga banner so'rovi BORMADI")

        # ── 3. Tushunilmagan so'rov
        print("\n  3) tushunilmagan so'rov")
        s3 = sorov_yarat("qwerty zxcvb", "")
        yaratilgan_sorovlar.append(s3)
        n3 = baza.tolqin_yubor(s3)
        tekshir(n3["yuborildi"] == 0,
                "hech kimga yuborilmadi — sotuvchi bezovta qilinmadi")

        # ── 4. Takroriy chaqiruv qo'shimcha yubormasin
        print("\n  4) takroriy chaqiruv")
        n1b = baza.tolqin_yubor(s1)
        tekshir(n1b["yuborildi"] == n1["yuborildi"],
                "ikkinchi chaqiruvda takror yuborilmadi")

    finally:
        with baza.ulan() as c:
            for sid in yaratilgan_sorovlar:
                c.execute("DELETE FROM yuborishlar WHERE sorov_id=?", (sid,))
                c.execute("DELETE FROM sorovlar WHERE id=?", (sid,))
        # Sotuvchilar alohida — `sotuvchi_ochir` o'z ulanishini ochadi;
        # yuqoridagi ochiq tranzaksiya ichida ikkinchi yozuvchi qulfni
        # kutib qolardi (database is locked).
        for sid in yaratilgan_sotuvchilar:
            baza.sotuvchi_ochir(sid)

    print("\n" + "-" * 62)
    print("  HAMMASI JOYIDA\n" if not XATO else f"  {XATO} TA XATO\n")


if __name__ == "__main__":
    main()
