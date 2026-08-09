"""
OBER — OLX KATEGORIYALARI (to'liq ro'yxat)

Manba: `ober/docs/04-universal-bozor-kategoriyalari.md`

NEGA SUBKATEGORIYA KERAK:
OLX bitta so'rov uchun sahifalashni ~25 sahifa bilan cheklaydi (~1 300
e'lon). Ya'ni "nedvizhimost" ni butunlay o'qib bo'lmaydi. Lekin
"kvartira sotish", "kvartira ijara", "uy", "yer" alohida-alohida
o'qilsa, har biri o'z 25 sahifasini beradi. Shuning uchun ro'yxat
subkategoriyalarga bo'lingan — qamrov shundan bir necha barobar oshadi.

Har yozuv: (yo'l, o'zbekcha nom)
Yo'l OLX URL'idagi bo'lak: https://www.olx.uz/<yol>/<viloyat>/
"""

from __future__ import annotations

KATEGORIYALAR: list[tuple[str, str]] = [
    # ── TRANSPORT ────────────────────────────────────────────────────────
    ("transport/avtozapchasti-i-aksessuary/avtozapchasti", "Avto ehtiyot qism"),
    ("transport/avtozapchasti-i-aksessuary/shiny-diski-i-kolesa", "Shina va disk"),
    ("transport/avtozapchasti-i-aksessuary/avtoaksessuary", "Avto aksessuar"),
    ("transport/avtozapchasti-i-aksessuary/avtozvuk-i-video", "Avto audio"),
    ("transport/legkovye-avtomobili", "Yengil avtomobil"),
    ("transport/gruzovye-avtomobili", "Yuk mashinasi"),
    ("transport/moto", "Mototsikl"),
    ("transport/avtobusy", "Avtobus"),
    ("transport/pritsepy", "Tirkama"),
    ("transport/spetstehnika", "Maxsus texnika"),
    ("transport/selhoztehnika", "Qishloq xo'jaligi texnikasi"),
    ("transport/vodnyy-transport", "Suv transporti"),

    # ── KO'CHMAS MULK ────────────────────────────────────────────────────
    ("nedvizhimost/kvartiry/prodazha", "Kvartira sotish"),
    ("nedvizhimost/kvartiry/arenda", "Kvartira ijara"),
    ("nedvizhimost/doma/prodazha", "Uy sotish"),
    ("nedvizhimost/doma/arenda", "Uy ijara"),
    ("nedvizhimost/zemlya", "Yer"),
    ("nedvizhimost/kommercheskaya-nedvizhimost", "Tijorat binosi"),
    ("nedvizhimost/garazhy-parkovki", "Garaj va parking"),
    ("nedvizhimost/posutochno-pochasovo", "Sutkalik ijara"),
    ("nedvizhimost/dachi", "Dacha"),

    # ── ELEKTRONIKA ──────────────────────────────────────────────────────
    ("elektronika/telefony-i-aksessuary", "Telefon va aksessuar"),
    ("elektronika/kompyutery-i-komplektuyuschie", "Kompyuter"),
    ("elektronika/noutbuki-i-aksessuary", "Noutbuk"),
    ("elektronika/foto-video", "Foto va video"),
    ("elektronika/televizory-i-videotehnika", "Televizor"),
    ("elektronika/audiotehnika", "Audio texnika"),
    ("elektronika/igry-i-igrovye-pristavki", "O'yin va pristavka"),
    ("elektronika/bytovaya-tehnika", "Maishiy texnika"),
    ("elektronika/klimaticheskoe-oborudovanie", "Iqlim texnikasi"),
    ("elektronika/umnye-ustroystva", "Aqlli qurilma"),

    # ── UY VA BOG' ───────────────────────────────────────────────────────
    ("dom-i-sad/mebel", "Mebel"),
    ("dom-i-sad/interer", "Interyer"),
    ("dom-i-sad/remont-i-stroitelstvo", "Qurilish va ta'mirlash"),
    ("dom-i-sad/instrumenty", "Asboblar"),
    ("dom-i-sad/posuda-i-kuhonnye-prinadlezhnosti", "Idish-tovoq"),
    ("dom-i-sad/rasteniya", "O'simlik"),
    ("dom-i-sad/produkty-pitaniya", "Oziq-ovqat"),
    ("dom-i-sad/sad-ogorod", "Bog' va tomorqa"),

    # ── BOLALAR DUNYOSI ──────────────────────────────────────────────────
    ("detskiy-mir/detskaya-odezhda", "Bolalar kiyimi"),
    ("detskiy-mir/detskaya-obuv", "Bolalar oyoq kiyimi"),
    ("detskiy-mir/detskie-kolyaski", "Kolyaska"),
    ("detskiy-mir/avtokresla", "Avto o'rindiq"),
    ("detskiy-mir/detskaya-mebel", "Bolalar mebeli"),
    ("detskiy-mir/igrushki", "O'yinchoq"),
    ("detskiy-mir/detskiy-transport", "Bolalar transporti"),
    ("detskiy-mir/tovary-dlya-kormleniya", "Oziqlantirish"),
    ("detskiy-mir/tovary-dlya-shkolnikov", "Maktab mahsulotlari"),

    # ── MODA VA STIL ─────────────────────────────────────────────────────
    ("moda-i-stil/odezhda", "Kiyim"),
    ("moda-i-stil/obuv", "Oyoq kiyim"),
    ("moda-i-stil/svadebnyy-salon", "To'y salon"),
    ("moda-i-stil/chasy", "Soat"),
    ("moda-i-stil/aksessuary", "Aksessuar"),
    ("moda-i-stil/krasota-i-zdorove", "Go'zallik va salomatlik"),

    # ── XIZMATLAR ────────────────────────────────────────────────────────
    ("uslugi/remont-i-stroitelstvo", "Ta'mirlash va qurilish"),
    ("uslugi/avto-moto", "Avto-moto xizmat"),
    ("uslugi/krasota-zdorove", "Go'zallik xizmati"),
    ("uslugi/uborka", "Tozalash"),
    ("uslugi/bytovye-uslugi", "Maishiy xizmat"),
    ("uslugi/perevozki-arenda-transporta", "Tashish va transport ijarasi"),
    ("uslugi/obrazovanie", "Ta'lim"),
    ("uslugi/foto-video-uslugi", "Foto va video xizmat"),
    ("uslugi/reklama-poligrafiya", "Reklama va poligrafiya"),
    ("uslugi/yuridicheskie-uslugi", "Yuridik xizmat"),
    ("uslugi/finansovye-uslugi", "Moliyaviy xizmat"),
    ("uslugi/perevody-teksty", "Tarjima va matn"),
    ("uslugi/dostavka-edy", "Taom yetkazish"),
    ("uslugi/oborudovanie-i-biznes", "Uskuna va biznes"),

    # ── ISH ──────────────────────────────────────────────────────────────
    ("rabota/vakansii", "Vakansiya"),
    ("rabota/rezyume", "Rezyume"),

    # ── HAYVONLAR ────────────────────────────────────────────────────────
    ("zhivotnye/sobaki", "It"),
    ("zhivotnye/koshki", "Mushuk"),
    ("zhivotnye/ptitsy", "Qush"),
    ("zhivotnye/akvariumnye-rybki", "Akvarium baliqlari"),
    ("zhivotnye/selskohozyaystvennye-zhivotnye", "Qishloq xo'jaligi hayvonlari"),
    ("zhivotnye/tovary-dlya-zhivotnyh", "Hayvonlar uchun mahsulot"),

    # ── XOBBI, SPORT, DAM OLISH ──────────────────────────────────────────
    ("hobbi-otdyh-i-sport/sport-otdyh", "Sport va dam olish"),
    ("hobbi-otdyh-i-sport/velosipedy", "Velosiped"),
    ("hobbi-otdyh-i-sport/muzykalnye-instrumenty", "Musiqa asboblari"),
    ("hobbi-otdyh-i-sport/knigi-zhurnaly", "Kitob va jurnal"),
    ("hobbi-otdyh-i-sport/antikvariat-kollektsii", "Antikvariat"),
    ("hobbi-otdyh-i-sport/bilety", "Chipta"),

    # ── BOSHQA ───────────────────────────────────────────────────────────
    ("otdam-darom", "Tekinga beraman"),
    ("obmen-barter", "Ayirboshlash"),
]


def _fayldan() -> list[tuple[str, str]]:
    """`data/kategoriyalar.txt` — OLX'dan avtomatik topilgan ro'yxat.

    Bu ASOSIY manba. Quyidagi qo'lda yozilgan ro'yxat faqat zaxira,
    chunki qo'lda yozilgani xato bo'lishi mumkin (2026-08-01: 14 tadan
    6 tasi noto'g'ri edi).
    """
    import baza
    fayl = baza.DB.with_name("kategoriyalar.txt")
    try:
        satrlar = fayl.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    natija = []
    for s in satrlar:
        s = s.strip()
        if not s or s.startswith("#") or "|" not in s:
            continue
        yol, _, nom = s.partition("|")
        yol, nom = yol.strip().strip("/"), nom.strip()
        if yol:
            natija.append((yol, nom or yol))
    return natija


def royxat(faqat: str = "") -> list[tuple[str, str]]:
    """Kategoriyalar. `faqat` berilsa nom yoki yo'l bo'yicha filtrlaydi."""
    hammasi = _fayldan() or list(KATEGORIYALAR)
    if not faqat:
        return hammasi
    f = faqat.lower()
    return [k for k in hammasi if f in k[0].lower() or f in k[1].lower()]


def manba() -> str:
    return "OLX'dan topilgan" if _fayldan() else "qo'lda yozilgan (zaxira)"
