"""
OBER — BAZADAGI SOXTA NARXLARNI TOZALASH (bir martalik tuzatish)

`olx.soxta_narxmi()` filtri yangi yig'ishlarda ishlaydi, lekin bazada
allaqachon yozilgan soxta narxlar qoladi. Bu skript ularni tozalaydi.

2026-08-01 o'lchovi: "kobalt fara" so'rovida eng qimmat e'lon
"Правая часть фары от кобалт Б/у — 9 999 999 so'm" edi. Bu narx emas,
"qo'ng'iroq qiling" degani. Bitta shunday raqam butun narx oralig'ini
foydasiz qiladi.

E'lon O'CHIRILMAYDI — faqat `narx_som` bo'shatiladi. E'lon "kimda bor"
ro'yxatida qoladi, lekin narx hisobiga kirmaydi.
"""

from __future__ import annotations

import baza
from olx import soxta_narxmi


def main() -> None:
    baza.init()
    with baza.ulan() as c:
        qatorlar = c.execute(
            "SELECT id, nom, narx_som FROM elonlar"
            " WHERE narx_som IS NOT NULL").fetchall()

    soxta = [(r["id"], r["nom"], r["narx_som"]) for r in qatorlar
             if soxta_narxmi(r["narx_som"])]

    print("=" * 62)
    print("  OBER — soxta narxlarni tozalash")
    print("=" * 62)
    print(f"\n  Narxli e'lon: {len(qatorlar)}")
    print(f"  Soxta topildi: {len(soxta)}\n")

    for _, nom, narx in soxta[:15]:
        print(f"    {narx:>12,}  {nom[:44]}")
    if len(soxta) > 15:
        print(f"    ... yana {len(soxta) - 15} ta")

    if not soxta:
        print("\n  Tozalash kerak emas.\n")
        return

    with baza.ulan() as c:
        c.executemany("UPDATE elonlar SET narx_som=NULL WHERE id=?",
                      [(i,) for i, _, _ in soxta])

    print(f"\n  {len(soxta)} ta e'lonning narxi bo'shatildi.")
    print("  E'lonlar o'chirilmadi — ular 'kimda bor' ro'yxatida qoladi.\n")


if __name__ == "__main__":
    main()
