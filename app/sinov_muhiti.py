"""OBER — mahalliy sinov muhiti (2026-08-16).

NIMA UCHUN KERAK
----------------
Bugungacha har o'zgarish jonli saytga yuborilardi: deploy -> ~100
soniya kutish -> brauzerdan o'lchash. Bir kunda 15 marta takrorlandi,
ya'ni ~40 daqiqa faqat kutishga ketdi. Tepa paneldagi xato aynan
shuning uchun topilmadi — tez urinib ko'rishning iloji yo'q edi.

Bu skript jonli saytga TEGMASDAN to'liq serverni ko'taradi.

XAVFSIZLIK — ENG MUHIMI
-----------------------
Jonli baza (`data/ober.db`, 262 MB) haqiqiy foydalanuvchi
ma'lumotlari bilan: sotuvchilar telefon raqamlari, suhbatlar,
xabarlar. Unga YOZILMAYDI va u NUSXA OLINMAYDI.

Bu yerda qilinadigan ish:
  * jonli baza FAQAT O'QISH rejimida ochiladi (`mode=ro`);
  * undan faqat `elonlar` jadvalidan namuna olinadi;
  * `sotuvchilar`, `suhbatlar`, `xabarlar`, `sorovlar`, `javoblar`
    BO'SH qoladi — ya'ni shaxsiy ma'lumot umuman ko'chirilmaydi.

Natija ~6 MB, sinov uchun yetarli.

ISHLATISH
---------
    python app/sinov_muhiti.py            # baza tayyorlanadi
    python app/sinov_muhiti.py --ishga    # baza + server

Server `http://127.0.0.1:8811` da ko'tariladi.

`web/` papkasi NUSXA OLINMAYDI — jonli papkaga bog'lanadi. Ya'ni
HTML/CSS tahriri darhol ko'rinadi, qayta ishga tushirish shart emas.
"""

from __future__ import annotations

import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

ILDIZ = Path(__file__).resolve().parent.parent
JONLI_BAZA = ILDIZ / "data" / "ober.db"
MUHIT = Path(os.environ.get("OBER_SINOV_MUHITI") or "/tmp/ober-sinov")
PORT = os.environ.get("OBER_SINOV_PORT") or "8811"

# Namuna hajmi. 3000 ta e'lon qidiruvni sinash uchun yetarli va
# baza 6 MB atrofida qoladi. Kattaroq kerak bo'lsa oshiring.
NAMUNA = int(os.environ.get("OBER_SINOV_NAMUNA") or 3000)

# BU JADVALLAR HECH QACHON KO'CHIRILMAYDI. Ro'yxat ataylab qora
# ro'yxat emas, OQ ro'yxatning teskarisi: yangi jadval qo'shilsa u
# ham ko'chirilmaydi, chunki pastda faqat `elonlar` ko'chiriladi.
SHAXSIY = ("sotuvchilar", "suhbatlar", "xabarlar", "sorovlar",
           "javoblar", "yuborishlar", "push_obunalar")


def sxema_va_namuna() -> None:
    """Bo'sh sxema + faqat e'lonlar namunasi."""
    (MUHIT / "data").mkdir(parents=True, exist_ok=True)
    yangi = MUHIT / "data" / "ober.db"
    if yangi.exists():
        yangi.unlink()

    src = sqlite3.connect(f"file:{JONLI_BAZA}?mode=ro", uri=True)
    dst = sqlite3.connect(yangi)
    try:
        # FTS yordamchi jadvallari (`_data`, `_idx`, `_docsize`)
        # qo'lda yaratilmaydi — ular virtual jadval bilan birga
        # o'zi paydo bo'ladi.
        for (sql,) in src.execute(
                "SELECT sql FROM sqlite_master WHERE sql IS NOT NULL "
                "AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '%_fts_%'"):
            try:
                dst.execute(sql)
            except sqlite3.OperationalError as xato:
                print(f"    o'tkazildi: {str(xato)[:70]}")
        dst.commit()

        ustunlar = [r[1] for r in src.execute("PRAGMA table_info(elonlar)")]
        belgi = ",".join("?" * len(ustunlar))
        qatorlar = src.execute(
            "SELECT * FROM elonlar ORDER BY id DESC LIMIT ?",
            (NAMUNA,)).fetchall()
        dst.executemany(f"INSERT INTO elonlar VALUES ({belgi})", qatorlar)
        dst.commit()

        # Nazorat: shaxsiy jadvallar chindan bo'shmi?
        for nom in SHAXSIY:
            try:
                son = dst.execute(f"SELECT COUNT(*) FROM {nom}").fetchone()[0]
            except sqlite3.OperationalError:
                continue
            if son:
                raise SystemExit(
                    f"TO'XTATILDI: `{nom}` jadvalida {son} yozuv bor. "
                    "Shaxsiy ma'lumot sinov bazasiga tushmasligi kerak.")
    finally:
        src.close()
        dst.close()

    hajm = yangi.stat().st_size / 1e6
    print(f"  baza tayyor: {len(qatorlar)} e'lon, {hajm:.1f} MB")
    print(f"  shaxsiy jadvallar: bo'sh (tekshirildi)")


def bogla() -> None:
    """`app` nusxalanadi, `web` jonli papkaga bog'lanadi."""
    if (MUHIT / "app").exists():
        shutil.rmtree(MUHIT / "app")
    shutil.copytree(ILDIZ / "app", MUHIT / "app")

    # web NUSXA OLINMAYDI — bog'lanadi. Shunda CSS/HTML tahriri
    # darhol ko'rinadi va serverni qayta yoqish kerak bo'lmaydi.
    for nom in ("web", "brend"):
        manba = ILDIZ / nom
        nishon = MUHIT / nom
        if nishon.is_symlink() or nishon.exists():
            nishon.unlink() if nishon.is_symlink() else shutil.rmtree(nishon)
        if manba.exists():
            nishon.symlink_to(manba, target_is_directory=True)
    print(f"  app nusxalandi, web/brend bog'landi -> {MUHIT}")


def main() -> int:
    if not JONLI_BAZA.exists():
        print(f"  {JONLI_BAZA} topilmadi.")
        return 1
    print(f"\n  OBER sinov muhiti -> {MUHIT}\n")
    bogla()
    sxema_va_namuna()

    if "--ishga" in sys.argv:
        muhit = dict(os.environ,
                     OBER_PORT=PORT, OBER_HOST="127.0.0.1",
                     OBER_NO_BROWSER="1")
        print(f"\n  server: http://127.0.0.1:{PORT}\n")
        subprocess.run([sys.executable, "app/server.py"],
                       cwd=MUHIT, env=muhit)
    else:
        print(f"\n  ishga tushirish:\n"
              f"    cd {MUHIT} && OBER_PORT={PORT} OBER_NO_BROWSER=1 "
              f"python3 app/server.py\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
