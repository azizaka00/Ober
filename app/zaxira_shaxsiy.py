"""OBER — QAYTA TIKLAB BO'LMAYDIGAN ma'lumot zaxirasi (2026-08-17).

NEGA ALOHIDA ZAXIRA KERAK
-------------------------
Kunlik to'liq zaxira allaqachon bor (`data/zaxira/ober-1..7.db`,
har biri ~1.3 GB). Lekin ularning HAMMASI o'sha serverning o'zida
turadi. Disk yoki server yiqilsa baza ham, zaxira ham birga
yo'qoladi — ya'ni zaxira faqat "o'chirib yubordim" holatidan
himoya qiladi, "server yo'q bo'ldi" holatidan emas.

1.3 GB ni har kuni tashqariga ko'chirish qimmat. Lekin kerak ham
emas, chunki bazaning katta qismi QAYTA YIG'SA BO'LADI:

    elonlar        683 995 qator   OLX va Telegramdan qayta yig'iladi
    yigish_holati    3 354 qator   ish holati, qiymati yo'q
    elonlar_fts                    indeks, qayta quriladi

QAYTA TIKLAB BO'LMAYDIGANI ikkitasi:

    narx_tarix   1 084 944 qator   HECH QACHON qayta yig'ilmaydi —
                                   kechagi narxni bugun o'lchab
                                   bo'lmaydi. `baza.py` buni
                                   "bizning asosiy aktivimiz" deydi
    foydalanuvchi ma'lumoti        sotuvchilar, so'rovlar, javoblar,
                                   suhbatlar, xabarlar — bir necha
                                   yuz qator, lekin ular ODAMLAR

Shuning uchun bu skript ikkita ALOHIDA fayl beradi: biri kichkina
(odamlar), ikkinchisi kattaroq (narx tarixi). Kichkinasini har kuni
tashqariga chiqarish arzon.

ISHLATISH
---------
    python3 app/zaxira_shaxsiy.py            # data/zaxira-tashqi/ ga
    python3 app/zaxira_shaxsiy.py --qayerga /yol

Jonli bazaga FAQAT O'QISH rejimida tegadi (`mode=ro`).
"""

from __future__ import annotations

import gzip
import sqlite3
import sys
import time
from pathlib import Path

ILDIZ = Path(__file__).resolve().parent.parent
BAZA = ILDIZ / "data" / "ober.db"
QAYERGA = ILDIZ / "data" / "zaxira-tashqi"

# ODAMLAR — kichik, lekin o'rnini hech narsa bosmaydi.
ODAM_JADVALLARI = (
    "sotuvchilar", "sorovlar", "javoblar", "suhbatlar", "xabarlar",
    "yuborishlar", "push_obunalar", "sozlama", "qidiruvlar",
)

# SESSIYA VA KIRISH KODLARI ATAYLAB YO'Q. Ular vaqtinchalik sirlar:
# zaxirada yotgan token — bu qo'shimcha xavf, foyda esa nol
# (muddati baribir tugaydi va odam qaytadan kiradi).

NARX_JADVALI = "narx_tarix"

# Nechta kunlik nusxa saqlanadi. Fayl kichik, lekin cheksiz o'smasin.
SAQLASH_KUNI = 14


def _ulan() -> sqlite3.Connection:
    c = sqlite3.connect(f"file:{BAZA}?mode=ro", uri=True)
    c.row_factory = sqlite3.Row
    return c


def _sxema(c: sqlite3.Connection, jadval: str) -> str | None:
    r = c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
                  (jadval,)).fetchone()
    return r["sql"] if r and r["sql"] else None


def _qiymat(x) -> str:
    if x is None:
        return "NULL"
    if isinstance(x, (int, float)):
        return repr(x)
    if isinstance(x, bytes):
        return "X'" + x.hex() + "'"
    return "'" + str(x).replace("'", "''") + "'"


def _jadvalni_yoz(c, jadval: str, yoz) -> int:
    sxema = _sxema(c, jadval)
    if not sxema:
        return 0
    yoz(f"DROP TABLE IF EXISTS {jadval};\n")
    yoz(sxema.rstrip().rstrip(";") + ";\n")
    n = 0
    # `fetchmany` — 1 mln qatorli `narx_tarix` xotiraga sig'masin.
    imzo = c.execute(f"SELECT * FROM {jadval} LIMIT 0")
    ustunlar = [d[0] for d in imzo.description]
    kursor = c.execute(f"SELECT * FROM {jadval}")
    boshi = f"INSERT INTO {jadval} ({','.join(ustunlar)}) VALUES "
    while True:
        qatorlar = kursor.fetchmany(2000)
        if not qatorlar:
            break
        yoz(boshi + ",".join(
            "(" + ",".join(_qiymat(q[u]) for u in ustunlar) + ")"
            for q in qatorlar) + ";\n")
        n += len(qatorlar)
    return n


def _eskilarini_kamayt(papka: Path) -> int:
    """Eng yangi `SAQLASH_KUNI` tadan boshqasini o'chiradi."""
    ochirildi = 0
    for naqsh in ("ober-odamlar-*.sql.gz", "ober-narx-*.sql.gz"):
        fayllar = sorted(papka.glob(naqsh), reverse=True)
        for f in fayllar[SAQLASH_KUNI:]:
            try:
                f.unlink()
                ochirildi += 1
            except OSError:
                pass
    return ochirildi


def main() -> int:
    global QAYERGA
    if "--qayerga" in sys.argv:
        QAYERGA = Path(sys.argv[sys.argv.index("--qayerga") + 1])
    if not BAZA.exists():
        print(f"  {BAZA} topilmadi.")
        return 1
    QAYERGA.mkdir(parents=True, exist_ok=True)
    kun = time.strftime("%Y%m%d")

    c = _ulan()
    try:
        natija = []
        for nom, jadvallar in (("odamlar", ODAM_JADVALLARI),
                               ("narx", (NARX_JADVALI,))):
            yol = QAYERGA / f"ober-{nom}-{kun}.sql.gz"
            jami = 0
            with gzip.open(yol, "wt", encoding="utf-8", compresslevel=9) as f:
                f.write(f"-- OBER zaxira ({nom}) {time.strftime('%Y-%m-%d %H:%M')}\n")
                f.write("PRAGMA foreign_keys=OFF;\nBEGIN;\n")
                for j in jadvallar:
                    jami += _jadvalni_yoz(c, j, f.write)
                f.write("COMMIT;\n")
            natija.append((nom, yol, jami, yol.stat().st_size))
    finally:
        c.close()

    print("=" * 58)
    print("  OBER — tashqi zaxira (qayta tiklab bo'lmaydigan qism)")
    print("=" * 58)
    for nom, yol, qator, bayt in natija:
        print(f"  {nom:8} {qator:>9} qator   {bayt/1e6:6.2f} MB   {yol.name}")
    ochirildi = _eskilarini_kamayt(QAYERGA)
    if ochirildi:
        print(f"  eski nusxalar o'chirildi: {ochirildi}")
    print()
    print("  DIQQAT: bu fayllar hamon SHU serverda. Zaxira faqat")
    print("  boshqa mashinaga ko'chirilgandan keyin zaxira bo'ladi.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
