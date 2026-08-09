"""
OBER — BAZANI TOZALASH

Narx cheklovi keyinroq qo'shilgani uchun eski ma'lumotda bema'ni
raqamlar qolgan (2 400 000 000 · 57 630 720 000 kabi).

Ular o'rtacha narxni buzadi va butun tahlilni yaroqsiz qiladi —
shuning uchun narx sifatida o'chiriladi. Asl matn (narx_asl) saqlanadi.
"""

from __future__ import annotations

import baza
from olx import NARX_MAX, NARX_MIN


def main() -> None:
    baza.init()
    with baza.ulan() as c:
        shubhali = c.execute(
            "SELECT COUNT(*) n FROM elonlar WHERE narx_som IS NOT NULL "
            "AND (narx_som < ? OR narx_som > ?)", (NARX_MIN, NARX_MAX)
        ).fetchone()["n"]

        print("=" * 60)
        print("  OBER — bazani tozalash")
        print("=" * 60)
        print(f"\n  Ishonchli oraliq: {NARX_MIN:,} – {NARX_MAX:,} so'm")
        print(f"  Undan tashqarida: {shubhali} ta e'lon")

        if shubhali:
            print("\n  Namuna (eng qimmat 5 tasi):")
            for r in c.execute(
                    "SELECT nom, narx_som, narx_asl FROM elonlar "
                    "WHERE narx_som > ? ORDER BY narx_som DESC LIMIT 5",
                    (NARX_MAX,)):
                print(f"    {r['narx_som']:>18,}  {r['nom'][:40]}")

            c.execute(
                "UPDATE elonlar SET narx_som = NULL "
                "WHERE narx_som IS NOT NULL AND (narx_som < ? OR narx_som > ?)",
                (NARX_MIN, NARX_MAX))
            c.execute(
                "DELETE FROM narx_tarix WHERE narx_som < ? OR narx_som > ?",
                (NARX_MIN, NARX_MAX))
            print(f"\n  {shubhali} ta narx o'chirildi (asl matn saqlanib qoldi)")
        else:
            print("\n  Tozalash kerak emas.")

        qoldi = c.execute("SELECT COUNT(*) n FROM elonlar "
                          "WHERE narx_som IS NOT NULL").fetchone()["n"]
        eng = c.execute("SELECT MAX(narx_som) m FROM elonlar").fetchone()["m"]
        print(f"\n  Narxi bor: {qoldi} ta · eng yuqori: {eng:,} so'm\n"
              if eng else "")


if __name__ == "__main__":
    main()
