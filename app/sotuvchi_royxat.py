"""
OBER — SOTUVCHILARNI JALB QILISH RO'YXATI

Thumbtack aynan shundan boshlagan: kataloglarni yig'ib, ta'minotchilarni
TOPIB, o'zi bordi. Talab isbotini kutmadi.

Bizda ham xuddi shu boylik bor va biz uni ishlatmayapmiz. Yig'ilgan
e'lonlarda sotuvchi nomi, do'konmi-yo'qmi, nechta e'loni bori va nima
sotishi yozilgan. Ya'ni "kimni OBER'ga taklif qilish kerak" degan
ro'yxat allaqachon bazamizda.

Natija: `data/jalb-qilish.txt` — eng katta va faol sotuvchilar,
tartib bilan.

  python sotuvchi_royxat.py            -- 100 ta eng yirik sotuvchi
  python sotuvchi_royxat.py 300        -- 300 ta
  python sotuvchi_royxat.py 100 fara   -- faqat fara sotuvchilari
"""

from __future__ import annotations

import sys

import baza


def main(limit: int = 100, yonalish: str = "") -> int:
    baza.init()

    shart = "WHERE faol=1 AND sotuvchi_nomi IS NOT NULL AND sotuvchi_nomi <> ''"
    parametrlar: list = []
    if yonalish:
        shart += " AND (tan_qismlar LIKE ? OR nom LIKE ?)"
        parametrlar += [f"%{yonalish}%", f"%{yonalish}%"]

    with baza.ulan() as c:
        qatorlar = c.execute(
            f"""SELECT sotuvchi_nomi, sotuvchi_id,
                       COUNT(*) elon_soni,
                       MAX(biznes) dokon,
                       COUNT(DISTINCT tuman) hudud,
                       MIN(narx_som) eng_arzon,
                       MAX(narx_som) eng_qimmat,
                       MAX(havola) namuna,
                       GROUP_CONCAT(DISTINCT kategoriya) yonalishlar
                FROM elonlar {shart}
                GROUP BY sotuvchi_nomi
                HAVING elon_soni >= 2
                ORDER BY dokon DESC, elon_soni DESC
                LIMIT ?""", parametrlar + [limit]).fetchall()

        jami_sotuvchi = c.execute(
            "SELECT COUNT(DISTINCT sotuvchi_nomi) n FROM elonlar"
            " WHERE faol=1 AND sotuvchi_nomi <> ''").fetchone()["n"]
        dokonlar = c.execute(
            "SELECT COUNT(DISTINCT sotuvchi_nomi) n FROM elonlar"
            " WHERE faol=1 AND biznes=1 AND sotuvchi_nomi <> ''").fetchone()["n"]

    print("=" * 66)
    print("  OBER — jalb qilish uchun sotuvchilar ro'yxati")
    print("=" * 66)
    print(f"\n  Bazada jami sotuvchi: {jami_sotuvchi}")
    print(f"  Ulardan do'kon (biznes): {dokonlar}")
    print(f"  Ro'yxatga olindi: {len(qatorlar)}\n")

    if not qatorlar:
        print("  Ma'lumot yo'q. Avval yig'ish kerak.\n")
        return 1

    satrlar = [
        "# OBER — jalb qilish ro'yxati",
        "# Manba: yig'ilgan e'lonlar. Eng ko'p e'lonli va do'kon maqomidagilar tepada.",
        "# Ustunlar: nom | e'lon soni | do'konmi | hududlar | yo'nalish | namuna havola",
        "",
    ]
    print(f"  {'SOTUVCHI':<28} {'E`LON':>6} {'DO`KON':>7}  YO`NALISH")
    print("  " + "-" * 62)
    for r in qatorlar:
        nom = (r["sotuvchi_nomi"] or "")[:28]
        yon = (r["yonalishlar"] or "")[:40]
        dokon = "ha" if r["dokon"] else "-"
        print(f"  {nom:<28} {r['elon_soni']:>6} {dokon:>7}  {yon}")
        satrlar.append(
            f"{r['sotuvchi_nomi']} | {r['elon_soni']} | {dokon} | "
            f"{r['hudud']} | {yon} | {r['namuna'] or ''}")

    fayl = baza.DB.with_name("jalb-qilish.txt")
    fayl.write_text("\n".join(satrlar) + "\n", encoding="utf-8")

    print("\n" + "-" * 66)
    print(f"  Fayl: {fayl}")
    print("\n  QANDAY ISHLATILADI:")
    print("   1. Ro'yxatdagi do'konlarni OLX havolasidan topib, bog'laning")
    print("   2. Ayting: 'OBER'da sizning yo'nalishingizda so'rovlar bor'")
    print("   3. Telegramga ulanish havolasini bering — 30 soniyalik ish")
    print("\n  Eslatma: bu sotuvchilar sizga OLX'da pul to'layapti.")
    print("  OBER'da esa hozircha bepul va so'rov o'zi keladi.\n")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    n = int(args[0]) if args and args[0].isdigit() else 100
    y = args[1] if len(args) > 1 else ""
    raise SystemExit(main(n, y))
