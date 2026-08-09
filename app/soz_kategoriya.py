"""SO'Z -> KATEGORIYA LUG'ATI, INDEKSNING O'ZIDAN QURILADI.

MUAMMO
------
Aziz, 2026-08-04: *"Barcha turdagi mahsulotni sotish kerak, 100 000 xil
bo'lsa hammasini. Va barcha turdagi xizmatlarni ham."*

`yonalishlar.py` — qo'lda yozilgan ro'yxat. U 20 ta keng yo'nalishni
biladi. Qo'lda yozilgan ro'yxat hech qachon 100 000 xil tovarni
qoplay olmaydi: har yangi mahsulot uchun kod yozib o'tirish kerak
bo'ladi.

So'zma-so'z moslikning ham teshigi bor:

    sotuvchi:  "mebel yasayman"
    xaridor:   "shkaf kerak"
    umumiy so'z: YO'Q

Ikkalasi bir narsa haqida gapiryapti, lekin tizim buni ko'rmaydi.

YECHIM — LUG'ATNI YOZMAYMIZ, HISOBLAYMIZ
---------------------------------------
Bizda 267 000 haqiqiy e'lon bor va HAR BIRINING KATEGORIYASI ma'lum.
Bu tayyor lug'at: "shkaf" so'zi qaysi kategoriyadagi e'lonlarda
uchrashini sanab chiqsak, uni qo'lda yozish shart emas.

    shkaf     -> Uy va bog'          (e'lonlarning 89% i)
    kolodka   -> Avto ehtiyot qism   (97%)
    tort      -> Oziq-ovqat          (71%)

Shundan keyin "mebel yasayman" ham, "shkaf kerak" ham bir xil
kategoriya belgisini oladi va bir-birini topadi.

NEGA BU ISHONCHLI
-----------------
1. Ma'lumot haqiqiy — o'zbek bozorining o'z so'zlari, o'z imlosi.
2. O'zi o'sadi: yig'uvchi yangi tovar olib kelsa, lug'at ham kengayadi.
3. Kod o'zgarmaydi. Yangi mahsulot turi chiqsa hech kim hech narsa
   yozmaydi.

CHEKLOV — buni bilib turish kerak
---------------------------------
Indeks asosan TOVAR. `Xizmatlar` kategoriyasida atigi ~4 000 e'lon
bor. Demak xizmatlar uchun bu lug'at kuchsiz va `yonalishlar.py`
hamda so'zma-so'z moslik asosiy bo'lib qoladi. Sotuvchilar ko'paygan
sari xizmat tomoni ham yaxshilanadi.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
FAYL = BASE / "data" / "soz-kategoriya.json"

# So'z kategoriya belgisini olishi uchun shartlar. Ular ATAYLAB qattiq:
# noto'g'ri belgi sotuvchini begona so'rov bilan bezovta qiladi va u
# OBER'ni o'chirib qo'yadi. Kam, lekin to'g'ri belgilagan afzal.
ENG_KAM_UCHRASH = 8        # so'z kamida shuncha e'londa uchrasin
ENG_KAM_ULUSH = 0.55       # va ularning kamida 55% i bitta kategoriyada
ENG_QISQA_SOZ = 3          # 2 harfli so'zlar shovqin

# Hamma joyda uchraydigan so'zlar hech narsani ajratmaydi.
_UMUMIY = {
    "sotiladi", "sotaman", "sotuv", "yangi", "arzon", "sifatli", "zor",
    "holati", "yaxshi", "kerak", "bor", "narxi", "narx", "dona", "ta",
    "uchun", "bilan", "va", "hamda", "toshkent", "shahri", "tumani",
    "viloyati", "prodam", "prodaetsya", "novi", "sostoyanie", "otlichnoe",
    "srochno", "shoshilinch", "originalni", "original", "kafolat",
    "dostavka", "yetkazib", "berish", "aksiya", "chegirma", "arzonlashdi",
}


def _tokenlar(matn: str) -> set[str]:
    from lugat import normalla
    n = normalla(matn or "")
    return {w for w in re.split(r"[^\w]+", n)
            if len(w) >= ENG_QISQA_SOZ and not w.isdigit() and w not in _UMUMIY}


def _yuqori_kategoriya(kat: str) -> str:
    return (kat or "").split("/")[0].strip()


def qur(chop: bool = True) -> dict:
    """Indeksni bir marta o'qib, so'z -> kategoriya jadvalini yasaydi."""
    import baza

    boshi = time.time()
    sanoq: dict[str, dict[str, int]] = {}
    jami = 0

    baza.init()
    with baza.ulan() as c:
        for r in c.execute(
                "SELECT nom, kategoriya FROM elonlar"
                "  WHERE faol=1 AND kategoriya IS NOT NULL AND kategoriya<>''"):
            kat = _yuqori_kategoriya(r["kategoriya"])
            if not kat:
                continue
            jami += 1
            for w in _tokenlar(r["nom"]):
                d = sanoq.get(w)
                if d is None:
                    d = sanoq[w] = {}
                d[kat] = d.get(kat, 0) + 1

    lugat: dict[str, str] = {}
    for soz, katlar in sanoq.items():
        hammasi = sum(katlar.values())
        if hammasi < ENG_KAM_UCHRASH:
            continue
        eng_kat, eng_soni = max(katlar.items(), key=lambda x: x[1])
        if eng_soni / hammasi >= ENG_KAM_ULUSH:
            lugat[soz] = eng_kat

    FAYL.parent.mkdir(parents=True, exist_ok=True)
    FAYL.write_text(json.dumps(
        {"qurilgan": time.time(), "elon": jami, "sozlar": lugat},
        ensure_ascii=False), encoding="utf-8")

    if chop:
        print(f"  [soz-kat] {jami} e'londan {len(sanoq)} so'z ko'rildi, "
              f"{len(lugat)} tasi kategoriyaga bog'landi "
              f"({time.time() - boshi:.1f}s)")
    return lugat


_LUGAT: dict[str, str] | None = None
_YUKLANGAN = 0.0


def lugat() -> dict[str, str]:
    """Fayldan o'qiydi. Fayl yo'q bo'lsa bo'sh — bu XATO EMAS."""
    global _LUGAT, _YUKLANGAN
    if _LUGAT is not None and time.time() - _YUKLANGAN < 600:
        return _LUGAT
    try:
        d = json.loads(FAYL.read_text(encoding="utf-8"))
        _LUGAT = d.get("sozlar") or {}
    except (OSError, ValueError):
        _LUGAT = {}
    _YUKLANGAN = time.time()
    return _LUGAT


def kategoriyalarni_top(matn: str) -> set[str]:
    """Erkin matndan kategoriya belgilarini topadi.

    Belgi `kat:` bilan boshlanadi — qo'lda yozilgan yo'nalishlar bilan
    aralashib ketmasin.
    """
    L = lugat()
    if not L:
        return set()
    return {"kat:" + L[w] for w in _tokenlar(matn) if w in L}


if __name__ == "__main__":
    qur()
