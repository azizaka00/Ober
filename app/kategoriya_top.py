"""
OBER — KATEGORIYALARNI OLX'NING O'ZIDAN TOPISH

2026-08-01 saboq: kategoriya manzillarini TAXMIN qilib yozgandik.
8 tadan 4 tasi 404 chiqdi (`zemlya` emas `zemlja`, `rabota/vakansii`
umuman yo'q...). Noto'g'ri manzil 0 e'lon qaytaradi va tizim uni
"tugadi" deb belgilaydi — butun bo'lim JIMGINA yo'qoladi.

Yechim: ro'yxat qo'lda yozilmaydi va menyudan ham qirqilmaydi.
OLX bosh sahifasining `PRERENDERED_STATE` blokida BUTUN kategoriya
daraxti turadi — 915 yozuv, har birida aniq `path`. Uni o'qib olamiz.

Nomlar o'zbekcha (`/oz/` sahifasidan) va ota-bobosi bilan yoziladi:
"Ko'chmas mulk / Yer / Sotish".

Natija `data/kategoriyalar.txt`:

    yol|nom

  python kategoriya_top.py       -- yaproq (eng chuqur) kategoriyalar
  python kategoriya_top.py 2     -- 2-darajagacha (tezroq, kengroq qamrov)

OLX kategoriyani o'zgartirsa — shu skriptni qayta yuritish yetarli.
"""

from __future__ import annotations

import json
import re
import sys

import baza
import olx

FAYL = "kategoriyalar.txt"
HOLAT = re.compile(r'PRERENDERED_STATE__\s*=\s*("(?:[^"\\]|\\.)*")')


def daraxtni_ol(til: str = "oz") -> list[dict]:
    """OLX bosh sahifasidagi to'liq kategoriya daraxti."""
    url = f"https://www.olx.uz/{til}/" if til else "https://www.olx.uz/"
    m = HOLAT.search(olx.yukla(url))
    if not m:
        raise RuntimeError("kategoriya daraxti topilmadi")
    royxat = json.loads(json.loads(m.group(1)))["categories"]["list"]
    return list(royxat.values()) if isinstance(royxat, dict) else list(royxat)


def main(maks_daraja: int = 0) -> int:
    baza.init()
    print("=" * 64)
    print("  OBER — kategoriyalarni OLX'dan o'qish")
    print("=" * 64)

    try:
        hammasi = daraxtni_ol("oz")
    except Exception as e:                        # noqa: BLE001
        print(f"\n  Xato: {type(e).__name__}: {e}\n")
        return 1

    kim = {int(k["id"]): k for k in hammasi if k.get("id") is not None}

    def toliq_nom(k: dict) -> str:
        bolaklar, joriy, chuqur = [], k, 0
        while joriy is not None and chuqur < 5:
            bolaklar.append(str(joriy.get("name") or "").strip())
            joriy = kim.get(int(joriy.get("parentId") or 0))
            chuqur += 1
        return " / ".join(x for x in reversed(bolaklar) if x)

    # OTA KATEGORIYA OLINMAYDI, agar bolalari olinsa.
    # Otaning e'lonlari — bolalarining e'lonlari. Ikkalasini ham yig'ish
    # bir ishni ikki marta qilish va OLX'ni bekorga yuklash bo'lardi.
    tanlangan = []
    for k in hammasi:
        yol = str(k.get("path") or "").strip("/")
        if not yol:
            continue
        daraja = int(k.get("level") or 1)
        if maks_daraja:
            if daraja > maks_daraja:
                continue
        elif k.get("children"):
            continue                              # faqat yaproqlar
        tanlangan.append((yol, toliq_nom(k), daraja))

    korilgan, toza = set(), []
    for yol, nom, daraja in tanlangan:
        if yol in korilgan:
            continue
        korilgan.add(yol)
        toza.append((yol, nom, daraja))

    # TARTIB — MUHIM. Yig'ish soatlab davom etadi va yarmida to'xtashi
    # mumkin. Shuning uchun eng qimmatlisi birinchi bo'lsin: bizning
    # nishamiz (avto), keyin hajmi katta bo'limlar.
    USTUVORLIK = ["transport", "elektronika", "nedvizhimost", "dom-i-sad",
                  "moda-i-stil", "detskiy-mir", "uslugi", "rabota",
                  "hobbi-otdyh-i-sport", "zhivotnye", "otdam-darom",
                  "obmen-barter"]

    def _tartib(x):
        bosh = x[0].split("/")[0]
        try:
            u = USTUVORLIK.index(bosh)
        except ValueError:
            u = len(USTUVORLIK)
        return (u, x[0])

    toza.sort(key=_tartib)

    # BUTUN DARAXTNI faylga yozamiz — ko'z bilan tekshirish uchun.
    # "Hammasi olindimi?" degan savolga javob shu faylda bo'lsin.
    daraxt_satrlari = ["# OLX kategoriya daraxti (to'liq)",
                       f"# Jami: {len(hammasi)}", ""]
    for k in sorted(hammasi, key=lambda x: str(x.get("path") or "")):
        yol = str(k.get("path") or "")
        if not yol:
            continue
        daraja = int(k.get("level") or 1)
        bolalar = len(k.get("children") or [])
        belgi = "  " * (daraja - 1) + ("+ " if bolalar else "- ")
        daraxt_satrlari.append(
            f"{belgi}{k.get('name') or ''}"
            f"{'  (' + str(bolalar) + ' ta bolasi)' if bolalar else ''}"
            f"\n{'  ' * (daraja - 1)}    {yol}")
    baza.DB.with_name("olx-daraxt.txt").write_text(
        "\n".join(daraxt_satrlari) + "\n", encoding="utf-8")

    fayl = baza.DB.with_name(FAYL)
    satrlar = ["# OBER — OLX kategoriyalari (avtomatik topilgan)",
               "# Qo'lda tahrirlamang: kategoriya_top.py qayta yozadi.",
               f"# Jami: {len(toza)}", ""]
    satrlar += [f"{yol}|{nom}" for yol, nom, _ in toza]
    fayl.write_text("\n".join(satrlar) + "\n", encoding="utf-8")

    viloyat = len(olx.VILOYATLAR)
    juft = len(toza) * viloyat
    soat = juft * olx.KUTISH / 3600

    # Bo'limlar bo'yicha nechtadan olindi — hech biri tushib qolmasin
    bolim: dict[str, int] = {}
    for yol, _, _ in toza:
        bosh = yol.split("/")[0]
        bolim[bosh] = bolim.get(bosh, 0) + 1

    print(f"\n  OLX daraxtida: {len(hammasi)} kategoriya")
    tur = "yaproqlar" if not maks_daraja else f"{maks_daraja}-darajagacha"
    print(f"  Tanlandi:      {len(toza)}  ({tur})")
    print(f"  Ro'yxat:       {fayl}")
    print(f"  To'liq daraxt: {baza.DB.with_name('olx-daraxt.txt')}")
    print("\n  BO'LIMLAR BO'YICHA:")
    for b, n in sorted(bolim.items(), key=lambda x: -x[1]):
        print(f"    {b:24} {n:>4}")
    print(f"\n  {len(toza)} kategoriya x {viloyat} viloyat = {juft} juftlik")
    print(f"  Faqat 1-sahifadan o'tishga ~{soat:.0f} soat ketadi")
    if soat > 12:
        print("\n  DIQQAT: bu juda uzoq.")
        print("  Avval keng qamrov uchun:  python kategoriya_top.py 2")
    print()
    return 0


if __name__ == "__main__":
    d = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 0
    raise SystemExit(main(d))
