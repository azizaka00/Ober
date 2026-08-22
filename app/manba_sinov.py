"""`manba_qorovul` sinovi — jonli bazaga tegmasdan, o'z vaqtinchalik bazasida.

ENG MUHIM SINOV: JIM QOLGAN MANBANI KO'RSIN.

2026-08-22 da to'rtta manba sakkiz kun jim turgan va buni hech kim
payqamagan edi. Qorovulning butun ma'nosi shu holatni ushlashda.
Sinovning yarmi "ushlasin", yarmi "bexuda shovqin qilmasin" ni
tekshiradi — noto'g'ri ogohlantirish ham xuddi shunday zararli,
chunki uni bir-ikki marta ko'rgan odam keyingisini o'qimay qo'yadi.

ISHLATISH
---------
    python3 app/manba_sinov.py
"""

from __future__ import annotations

import os
import shutil
import tempfile
import time
from pathlib import Path

import baza

JONLI = baza.DB
JONLI_HOLAT = ((JONLI.stat().st_mtime, JONLI.stat().st_size)
               if JONLI.exists() else None)

VAQTINCHA = Path(tempfile.mkdtemp(prefix="ober-manba-sinov-"))
baza.DB = VAQTINCHA / "sinov.db"

import manba_qorovul as mq                              # noqa: E402

jami = 0
xato = 0
SOAT = 3600.0


def tekshir(shart: bool, izoh: str) -> None:
    global jami, xato
    jami += 1
    if not shart:
        xato += 1
        print(f"  XATO  {izoh}")


def elon(manba: str, i: int, korildi_soat: float, olindi_soat: float,
         faol: int = 1) -> None:
    hozir = time.time()
    with baza.ulan() as c:
        c.execute(
            "INSERT INTO elonlar(manba, tashqi_id, nom, faol,"
            " oxirgi_korildi, olindi) VALUES(?,?,?,?,?,?)",
            (manba, f"{manba}-{i}", f"{manba} e'loni {i}", faol,
             hozir - korildi_soat * SOAT, hozir - olindi_soat * SOAT))
        c.commit()


def main() -> int:
    print("\n  MANBA QOROVULI SINOVI\n" + "-" * 54)
    baza.init()

    # ── SINOV BAZASI ───────────────────────────────────────────────
    # Har manba 2026-08-22 dagi HAQIQIY holatni takrorlaydi.
    elon("olx", 1, korildi_soat=0.1, olindi_soat=0.1)      # tirik
    elon("olx", 2, korildi_soat=0.2, olindi_soat=200)
    elon("telegram", 1, korildi_soat=0.5, olindi_soat=1)   # tirik
    elon("glotr", 1, korildi_soat=188, olindi_soat=400)    # JIM 7.8 kun
    elon("glotr", 2, korildi_soat=190, olindi_soat=400)
    elon("shahar", 1, korildi_soat=212, olindi_soat=400)   # JIM 8.8 kun
    elon("yangi_manba", 1, korildi_soat=40, olindi_soat=5)  # yosh
    elon("ober", 1, korildi_soat=300, olindi_soat=400)     # yig'ilmaydi

    KUTILGAN = {"olx", "telegram", "glotr", "shahar",
                "yangi_manba", "yoq_manba"}

    h = mq.holat()
    nomlar = {x["manba"] for x in h}
    tekshir(nomlar == {"olx", "telegram", "glotr", "shahar",
                       "yangi_manba", "ober"},
            f"holat() barcha manbani ko'rsin ({sorted(nomlar)})")

    olx = next(x for x in h if x["manba"] == "olx")
    tekshir(olx["faol"] == 2, f"olx faol soni ({olx['faol']})")
    tekshir(olx["jim_soat"] < 1, f"olx jim emas ({olx['jim_soat']:.1f})")
    tekshir(olx["yangi24"] == 1,
            f"24 soatlik yangi to'g'ri sanalsin ({olx['yangi24']})")

    # ── 1. JIM MANBA USHLANSIN — ASOSIY SINOV ──────────────────────
    m = mq.muammolar(h, KUTILGAN)
    matn = " | ".join(m)
    tekshir(any("glotr" in x for x in m), f"glotr jim — ushlansin ({matn})")
    tekshir(any("shahar" in x for x in m), "shahar jim — ushlansin")
    tekshir(any("188" in x or "18" in x for x in m),
            "necha soat jim turgani aytilsin")
    tekshir(any("e'lon eskirmoqda" in x for x in m),
            "nechta e'lon eskirayotgani aytilsin — zarar ko'rinsin")

    # ── 2. BEXUDA SHOVQIN BO'LMASIN ────────────────────────────────
    tekshir(not any("olx" in x for x in m), "tirik olx haqida shovqin yo'q")
    tekshir(not any("telegram" in x for x in m), "tirik telegram — jim")

    # TELEGRAM ADAPTERSIZ, LEKIN QOROVUL UNI KO'RISHI SHART.
    # Birinchi jonli yugurishda (2026-08-22) u "kutilmagan" deb
    # chetlab o'tilgan edi — ya'ni Telegram to'xtasa hech kim
    # bilmasdi. Sinov shu bo'shliqni qo'riqlaydi.
    tekshir("telegram" in mq.ADAPTERSIZ,
            "telegram adaptersiz manba sifatida ro'yxatda bo'lsin")
    jim_tg = [{"manba": "telegram", "faol": 3000, "nofaol": 0,
               "yangi24": 0, "jim_soat": 200, "yosh_soat": 900}]
    tekshir(any("telegram" in x for x in
                mq.muammolar(jim_tg, mq.kutilgan_manbalar())),
            "telegram to'xtasa — ushlansin")
    tekshir(not any("yangi_manba" in x for x in m),
            "yosh manbaga birinchi sutkada tegilmasin")
    tekshir(not any(x.startswith("ober:") for x in m),
            "`ober` yig'ilmaydi — u haqda ogohlantirilmasin")

    # ── 2b. MA'LUM CHEKLOV — OGOHLANTIRMASIN, LEKIN KO'RINSIN ──────
    #
    # `asaxiy` adapteri to'g'ri, lekin asaxiy.uz 403 qaytaradi
    # (2026-08-22 o'lchovi). Har kuni "NOSOZ" bo'lib turgan tekshiruv
    # odamni qizilga ko'niktiradi — o'shanda haqiqiy nosozlik ham
    # e'tiborsiz qoladi.
    tekshir("asaxiy" in mq.MA_LUM_CHEKLOV,
            "asaxiy ma'lum cheklov sifatida belgilangan")
    tekshir(len(mq.MA_LUM_CHEKLOV.get("asaxiy", "")) > 30,
            "cheklov SABABI yozilgan — keyin eslash uchun")
    cheklangan = [{"manba": "asaxiy", "faol": 0, "nofaol": 0, "yangi24": 0,
                   "jim_soat": 900, "yosh_soat": 900}]
    tekshir(not mq.muammolar(cheklangan, {"asaxiy"}),
            "cheklangan manba 900 soat jim tursa ham ogohlantirmasin")
    tekshir(not mq.muammolar([], {"asaxiy"}),
            "cheklangan manba bazada umuman bo'lmasa ham jim")
    # Lekin cheklov RO'YXATDA turishi shart — yashirilmasin.
    mq_matn = Path(mq.__file__).read_text(encoding="utf-8")
    tekshir("MA'LUM CHEKLOV (ogohlantirilmaydi" in mq_matn,
            "cheklanganlar chiqishda alohida ko'rsatilsin")

    # ── 3. ADAPTERI BOR, E'LONI YO'Q ───────────────────────────────
    tekshir(any("yoq_manba" in x for x in m),
            "adapteri bor, lekin bitta ham e'loni yo'q — aytilsin")

    # ── 4. CHEGARA MA'NOLI BO'LSIN ─────────────────────────────────
    tekshir(24 <= mq.CHEGARA_SOAT <= 72,
            f"chegara kunlik yig'ishga mos ({mq.CHEGARA_SOAT} soat)")
    tekshir(mq.CHEGARA_SOAT > 24,
            "chegara 24 soatdan katta — bitta o'tkazib yuborish "
            "darhol signal bermasin")

    # ── 5. CHEGARANING IKKI TOMONI ─────────────────────────────────
    chegarada = [{"manba": "x", "faol": 5, "nofaol": 0, "yangi24": 0,
                  "jim_soat": mq.CHEGARA_SOAT - 1, "yosh_soat": 500}]
    tekshir(not mq.muammolar(chegarada, {"x"}),
            "chegaradan bir soat berida — muammo emas")
    chegarada[0]["jim_soat"] = mq.CHEGARA_SOAT + 1
    tekshir(mq.muammolar(chegarada, {"x"}),
            "chegaradan bir soat narida — muammo")

    # ── 6. KUTILGAN MANBALAR RO'YXATI QO'LDA YOZILMASIN ────────────
    #
    # Yangi adapter qo'shilib, qorovul ro'yxatiga yozish unutilsa —
    # qorovul aynan yangi manbani ko'rmay qoladi. Shuning uchun
    # ro'yxat `yigish.adapterlar()` dan olinadi.
    manba_matni = Path(mq.__file__).read_text(encoding="utf-8")
    tekshir("yigish.adapterlar()" in manba_matni,
            "kutilgan manbalar `yigish.adapterlar()` dan olinsin")

    # ── 7. JURNAL ──────────────────────────────────────────────────
    mq.JURNAL = VAQTINCHA / "manba-jurnali.tsv"
    mq._jurnalga(h, m)
    satr = mq.JURNAL.read_text(encoding="utf-8").splitlines()
    tekshir(satr[0].startswith("sana\tmanba"), "jurnal sarlavhasi")
    tekshir(len(satr) == len(h) + 1,
            f"har manba uchun bitta satr ({len(satr)-1}/{len(h)})")
    tekshir(any("\tNOSOZ" in s and "glotr" in s for s in satr),
            "jim manba jurnalda NOSOZ deb belgilansin")
    tekshir(any("\tok" in s and "olx" in s for s in satr),
            "tirik manba jurnalda ok")
    mq._jurnalga(h, m)
    satr2 = mq.JURNAL.read_text(encoding="utf-8").splitlines()
    tekshir(len(satr2) == len(satr) + len(h),
            "jurnal qo'shib boriladi, ustidan yozilmaydi")
    tekshir(satr2.count(satr[0]) == 1, "sarlavha bir marta yoziladi")

    # ── 8. JONLI BAZAGA TEGILMAGANMI ───────────────────────────────
    if JONLI_HOLAT:
        tekshir((JONLI.stat().st_mtime, JONLI.stat().st_size) == JONLI_HOLAT,
                "JONLI BAZA O'ZGARMASIN")
    tekshir(str(baza.DB).startswith(str(VAQTINCHA)),
            "sinov o'z vaqtinchalik bazasida yurdi")

    shutil.rmtree(VAQTINCHA, ignore_errors=True)
    print("-" * 54)
    print(f"  NATIJA: {jami - xato} to'g'ri · {xato} xato  ({jami} tadan)\n")
    return 1 if xato else 0


if __name__ == "__main__":
    raise SystemExit(main())
