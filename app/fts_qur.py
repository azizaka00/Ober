"""
OBER — FTS5 INDEKSINI QURISH (bir martalik)

Mavjud e'lonlar uchun to'liq-matn indeksini to'ldiradi. Bundan keyin
`tahlil.py` uni o'zi yangilab boradi.

Nega kerak: qidiruv ilgari hamma e'lonni xotiraga yuklardi. 11 500 da
bu ishlardi, 100 000 da xotira yetmaydi. Indeks bilan xotiraga hech
narsa yuklanmaydi.
"""

from __future__ import annotations

import time

import baza
from lugat import normalla


def main() -> None:
    baza.init()
    print("=" * 60)
    print("  OBER — qidiruv indeksini qurish")
    print("=" * 60)

    if not baza.FTS_BOR:
        print("\n  DIQQAT: bu Python'da FTS5 yo'q.")
        print("  Qidiruv eski usulda ishlaydi (hammasi xotirada).")
        print("  Baza kattalashsa sekinlashadi.\n")
        return

    boshlandi = time.time()
    with baza.ulan() as c:
        qatorlar = c.execute(
            "SELECT id, nom, qism_turi, tan_modellar, tan_qismlar"
            " FROM elonlar WHERE faol=1 AND tan_qismlar IS NOT NULL").fetchall()
        c.execute("DELETE FROM elonlar_fts")

    print(f"\n  {len(qatorlar)} ta e'lon indekslanmoqda...\n")

    to_plam, n = [], 0
    for r in qatorlar:
        matn = f"{r['nom']} {r['qism_turi'] or ''}"
        teg = " ".join(x for x in
                       ((r["tan_modellar"] or "").split(",")
                        + (r["tan_qismlar"] or "").split(",")) if x)
        to_plam.append((r["id"], normalla(matn), teg))
        if len(to_plam) >= 2000:
            baza.fts_yoz(to_plam)
            n += len(to_plam)
            to_plam = []
            print(f"    {n}/{len(qatorlar)}")
    if to_plam:
        baza.fts_yoz(to_plam)
        n += len(to_plam)

    with baza.ulan() as c:
        jami = c.execute("SELECT COUNT(*) n FROM elonlar_fts").fetchone()["n"]

    print(f"\n  Tayyor — {time.time() - boshlandi:.1f} soniya")
    print(f"  Indeksda: {jami} ta e'lon")
    print("\n  Endi qidiruv xotiraga yuklamaydi — baza qanchalik katta")
    print("  bo'lsa ham tez ishlaydi.\n")


if __name__ == "__main__":
    main()
