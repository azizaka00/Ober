"""
OBER — QIDIRUV TEZLIGI O'LCHOVI

Serverga bog'liq emas: to'g'ridan-to'g'ri `qidiruv.qidir()` ni o'lchaydi.
Shu sababli natija toza — tarmoq va brauzer aralashmaydi.
"""

from __future__ import annotations

import time

import baza
import qidiruv

SO_ROVLAR = [
    "kobalt fara", "akumlyator", "neksiya kolodka", "bamper",
    "spark rul", "matiz dvigatel", "lasetti amortizator",
    "gazel most", "tormoz disk", "kapot",
]


def main() -> None:
    baza.init()
    print("=" * 60)
    print("  OBER — qidiruv tezligi")
    print("=" * 60)
    print(f"\n  Indeks (FTS5): {'BOR' if baza.FTS_BOR else 'YO`Q'}")

    with baza.ulan() as c:
        jami = c.execute("SELECT COUNT(*) n FROM elonlar WHERE faol=1").fetchone()["n"]
        idx = (c.execute("SELECT COUNT(*) n FROM elonlar_fts").fetchone()["n"]
               if baza.FTS_BOR else 0)
    print(f"  Faol e'lon: {jami} · indeksda: {idx}\n")

    qidiruv.qidir("isitish")          # birinchi chaqiruv hisobga olinmaydi

    vaqtlar = []
    for s in SO_ROVLAR:
        t = time.time()
        n = qidiruv.qidir(s)
        ms = (time.time() - t) * 1000
        vaqtlar.append(ms)
        belgi = "  " if ms < 300 else ("! " if ms < 1000 else "!!")
        print(f"  {belgi}{s:24} {ms:7.0f} ms   {n['jami']:6} natija")

    vaqtlar.sort()
    print("\n" + "-" * 60)
    print(f"  o'rtacha {sum(vaqtlar)/len(vaqtlar):.0f} ms · "
          f"eng sekini {vaqtlar[-1]:.0f} ms")
    if vaqtlar[-1] > 1000:
        print("\n  DIQQAT: 1 soniyadan sekin so'rov bor.")
    else:
        print("\n  Tezlik joyida.")
    print()


if __name__ == "__main__":
    main()
