"""
OBER — NOMA'LUM SO'ZLAR

Lug'atni qo'lda to'ldirish cheksiz ish. Buning o'rniga MA'LUMOTDAN
o'rganamiz: e'lonlarda tez-tez uchraydigan, lekin lug'atга tushmayotgan
so'zlarni topamiz.

Shunday qilib lug'at taxmin bilan emas, HAQIQIY EHTIYOJ bo'yicha to'ladi.
Har safar ma'lumot ko'paysa, ro'yxat aniqroq bo'ladi.
"""

from __future__ import annotations

import re
from collections import Counter

import baza
from lugat import (MODEL_INDEKS, QISM_INDEKS, modellarni_top, normalla, ozak,
                   qismlarni_top)

# Bularni tashlab ketamiz — savdo so'zlari, ma'no bermaydi.
# DIQQAT: taqqoslash normallashtirilgandan keyin bo'ladi, shuning uchun
# ro'yxat ham normallashtiriladi (pastda). Aks holda "orqa" -> "orka"
# bo'lib mos kelmay qoladi (2026-07-30 da shu xato topilgan edi).
_SHOVQIN_XOM = {
    "sotiladi", "satiladi", "sotilади", "prodam", "prodaetsya", "prodayetsya",
    "novый", "noviy", "yangi", "yani", "ideal", "holati", "sostoyanie",
    "narxi", "narx", "sena", "tsena", "dogovornaya", "kelishiladi",
    "bor", "yoq", "bar", "juda", "zor", "arzon", "optom", "roznitsa",
    "dostavka", "dastavka", "yetkazib", "berish", "olib", "kelamiz",
    "uchun", "bilan", "vaa", "ham", "hamda", "vsex", "vse", "dlya", "pod",
    "avto", "avtomobil", "mashina", "moshina", "mashinasi", "zapchast",
    "zapchasti", "ehtiyot", "qism", "qismlar", "original", "orginal",
    "arginal", "originalniy", "radnoy", "zavod", "korea", "koreya", "kitay",
    "yaxshi", "toza", "tozza", "kafolat", "garantiya", "aksiya", "aktsiya",
    "hech", "qanaqa", "ayb", "aybi", "komplekt", "kamplekt", "sht", "dona",
    "chap", "ong", "oldi", "orqa", "old", "zadniy", "peredniy", "levыy",
    "praviy", "vernyaya", "nijnyaya", "verxniy", "nijniy", "taraf", "tomon",
    "ming", "million", "mln", "som", "sum", "sumga", "ye", "yer",
    "telefon", "tel", "murojaat", "aloqa", "manzil", "adres",
    # 2026-07-30 ro'yxatidan qo'shildi
    "srochno", "sroshno", "assalomu", "aleykum", "alekum", "bizda",
    "kuzovnie", "kuzovnoy", "detali", "detal", "shtuk", "tasi", "tali",
    "bilan", "ega", "kuchiga", "gacha", "hamma", "barcha", "sifatli",
    "urilmagan", "yawi", "yaxwi", "ishlagan", "yurgan", "kelgan",
    "narxda", "narxlar", "arzonroq", "chegirma", "aksiyada",
    # 2026-07-30, ikkinchi bosqich
    "talik", "xolati", "ornatish", "rodnoy", "rabochiy", "raboshi",
    "avtomat", "mexanika", "plus", "premier", "style", "lux", "full",
    "xamma", "hamma", "yevro", "evro", "zavodskoy", "zavatskoy",
    "ishlaydi", "ishlatilgan", "yechilgan", "urilmagan", "moylisi",
    "xitoy", "kitay", "amerika", "yaponiya", "germaniya", "turkiya",
    "upravlenie", "peredniye", "perednie", "zadniye", "avlod", "yili",
    "buyum", "buyumlar", "mavjud", "mavjut", "keladi", "boradi",
}

SHOVQIN = {normalla(w) for w in _SHOVQIN_XOM}


def main(limit: int = 40) -> None:
    baza.init()
    with baza.ulan() as c:
        qatorlar = c.execute("SELECT nom, qism_turi FROM elonlar").fetchall()

    sanoq: Counter[str] = Counter()
    misol: dict[str, str] = {}

    for r in qatorlar:
        matn = f"{r['nom']} {r['qism_turi'] or ''}"
        # Bu e'londa nima tanildi?
        tanilgan = modellarni_top(matn) | qismlarni_top(matn)
        n = normalla(matn)

        for soz in n.split():
            if len(soz) < 4 or soz.isdigit():
                continue
            # Qo'shimchali shakl ham tekshiriladi: "zapchastlari" -> "zapchast"
            # (2026-07-30: shu tufayli allaqachon bilgan so'zlar ro'yxatda
            # qolib ketayotgan edi)
            ozaklar = ozak(soz)
            if any(o in SHOVQIN for o in ozaklar):
                continue
            if any(o in MODEL_INDEKS or o in QISM_INDEKS for o in ozaklar):
                continue
            # Bu so'z tufayli biror narsa tanilgan bo'lishi mumkin —
            # lekin biz aynan TANILMAGAN so'zlarni qidiryapmiz
            if modellarni_top(soz) or qismlarni_top(soz):
                continue
            sanoq[soz] += 1
            misol.setdefault(soz, r["nom"][:50])

    hisobot = baza.BASE / "data" / "nomalum-sozlar.txt"
    s: list[str] = []

    def q(x: str = "") -> None:
        print(x)
        s.append(x)

    q("=" * 66)
    q("  OBER — NOMA'LUM SO'ZLAR")
    q("  (e'lonlarda tez uchraydi, lekin lug'atда yo'q)")
    q("=" * 66)
    q(f"\n  {len(qatorlar)} e'lon ko'rildi · {len(sanoq)} xil noma'lum so'z\n")
    q(f"  {'SO`Z':22} {'SONI':>5}   MISOL")
    q("  " + "-" * 62)

    for soz, n in sanoq.most_common(limit):
        q(f"  {soz:22} {n:5}   {misol[soz][:34]}")

    q("")
    q("  Bu ro'yxatdan haqiqiy qism/brend nomlarini lugat.py ga qo'shing.")
    q("  Qolganini SHOVQIN ro'yxatiga qo'shsa — keyingi safar chiqmaydi.")
    q("")

    hisobot.parent.mkdir(parents=True, exist_ok=True)
    hisobot.write_text("\n".join(s), encoding="utf-8")
    print(f"  Saqlandi: {hisobot}\n")


if __name__ == "__main__":
    import sys
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 40)
