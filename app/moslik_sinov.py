"""
MOSLIK SINOVI — sotuvchi va xaridor bir-birini topadimi?

Nega bu fayl bor
----------------
`relevans_sinov.py` QIDIRUV natijasini tekshiradi (xaridor nima
ko'radi). Bu fayl esa MOSLIKNI tekshiradi: so'rov to'g'ri sotuvchiga
boradimi. Ikkalasi boshqa narsa va ikkalasi ham alohida buzilgan.

Har qator — bir marta HAQIQATAN buzilgan holat:

  gilam        60 ta namuna gilam sotuvchisini ko'rsatmagan (2026-08-10)
  oyna         mebelchiga avto oynasi so'rovi kelgan   (2026-08-09)
  kitob        ikkinchi so'z namunani 299 dan 1 ga tushirgan (2026-08-10)
  abcdefg      ma'nosiz matn "Transport" olgan         (2026-08-10)
  123 456      yalang'och raqam "Transport" olgan      (2026-08-10)

Ishga tushirish:  python3 moslik_sinov.py
"""

from __future__ import annotations

import sys

import baza
from yonalishlar import belgilar

# ---------------------------------------------------------------- #
# 1. MA'NOSIZ MATN HECH QANDAY KATEGORIYA OLMAYDI
#
# Noto'g'ri kategoriyadan ko'ra kategoriyasiz yaxshiroq: noto'g'ri
# kategoriya begona sotuvchiga so'rov yuboradi va u tizimga ishonchini
# yo'qotadi.
# ---------------------------------------------------------------- #
MANOSIZ = [
    "abcdefg qwerty",
    "zzzz xxxx yyyy",
    "asdf jkl",
    "qqq www eee",
    "hjkhjk mnbmnb",
    "salom qalaysiz",
    "...",
    "123 456",
    "998901234567",
]

# ---------------------------------------------------------------- #
# 2. SOTUVCHI <-> XARIDOR
#
# (sotuvchi o'zi haqida yozgani, xaridor so'rovi, mos kelishi kerakmi)
# ---------------------------------------------------------------- #
JUFTLAR = [
    # --- MOS KELISHI SHART -------------------------------------- #
    ("gilam sotaman", "gilam kerak 3x4", True),
    ("mebel yasayman divan shkaf", "shkaf kerak", True),
    ("avto ehtiyot qism fara stop", "lacettiga labavoy oyna kerak", True),
    ("velosiped sotaman", "velosiped kerak bolalar uchun", True),
    ("kir yuvish mashinasi tuzataman", "muzlatgich tuzatasizmi", True),
    ("zargarlik uzuk sirga yasayman", "uzuk kerak oltin", True),
    ("kaptar sotaman", "kaptar kerak", True),
    ("fotograf toy suratga olaman", "toyga fotograf kerak", True),
    ("kompyuter noutbuk sotaman", "noutbuk kerak oyin uchun", True),
    ("qurilish gisht sement", "sement kerak 50 qop", True),
    ("santexnik ustaman", "kran oqyapti usta kerak", True),
    ("kitob sotaman", "kitob kerak darslik", True),

    # --- MOS KELMASLIGI SHART ----------------------------------- #
    # Mebelchiga avto so'rovi bormaydi. Bu xato ikki marta, ikki
    # boshqa sababdan takrorlangan — shuning uchun ikki qator.
    ("mebel yasayman divan shkaf", "lacettiga labavoy oyna kerak", False),
    ("mebel yasayman divan shkaf karavot", "nexia 3 bamper kerak", False),
    ("tort pishiraman", "kobalt fara kerak", False),
    ("tikuvchiman koylak tikaman", "divan kerak charm", False),
    ("kir yuvish mashinasi tuzataman", "nexia bamper kerak", False),

    # "KIMDA BOR" — O'ZBEKCHADA ENG TABIIY SO'RASH USULI.
    # 2026-08-10 gacha bunday so'rovlarning HAMMASI tikuvchiga
    # ketardi: `normalla("kiyim")` -> "kim", qolip esa so'z boshi
    # bo'yicha qidirib "kimda" ni tutardi.
    ("tikuvchiman koylak tikaman",
     "Nexia 2 fara 300000 somga kimda bor", False),
    ("tikuvchiman koylak tikaman",
     "Samsung s24 ultralar kimda nech pul", False),
    # Haqiqiy kiyim so'rovi esa ishlashda davom etsin.
    ("tikuvchiman koylak tikaman", "koylak kerak erkaklar uchun", True),
]

# ---------------------------------------------------------------- #
# 3. E'LON KATEGORIYASI — sotuvchidan so'ramay, indeksdan aniqlanadi
#
# Matnlar HAQIQIY e'lon shaklida: `ober_elon_yoz` nom va tavsifni
# birga beradi, uch so'zli sarlavhani emas. Qisqa matn bilan sinash
# tizimni haqiqatda uchramaydigan holatga moslashtirib qo'yardi.
# ---------------------------------------------------------------- #
KATEGORIYALAR = [
    ("3 kishilik burchak divan sotiladi holati yaxshi",
     "Uy va bog'"),
    ("Nexia 3 uchun fara sotiladi original",
     "Transport"),
    ("iPhone 13 128gb sotiladi karobka hujjati bilan",
     "Elektr jihozlari"),
    ("Kvartira ijaraga beriladi 2 xonali Chilonzor",
     "Ko'chmas mulk"),
    ("Bolalar velosipedi 5 yoshdan 8 yoshgacha",
     "Bolalar dunyosi"),
    ("Gilam sotiladi 3x4 yangi hech ishlatilmagan",
     "Uy va bog'"),
    ("Oltin uzuk 585 proba ayollar uchun",
     "Moda va stil"),
    ("Kir yuvish mashinasi LG avtomat sotiladi",
     "Elektr jihozlari"),
    ("Kitob sotiladi badiiy adabiyot toplami",
     "Xobbi, dam olish sport"),
    ("Kitoblar sotiladi darsliklar",
     "Xobbi, dam olish sport"),
    # BIR MAHSULOT, TURLI IBORA. 2026-08-10 da jonli oqim testida
    # ko'rindi: test bir iborada o'tib, deyarli bir xil ikkinchisida
    # yiqilgan edi ("uyda turgan" qo'shilishi kategoriyani
    # "Elektr jihozlari" ga o'zgartirgan). Endi uchalasi ham qulflangan.
    ("Gilam sotiladi 3x4 yangi Hech ishlatilmagan, uyda turgan",
     "Uy va bog'"),
    ("Gilam 3x4 arzon narxda beriladi",
     "Uy va bog'"),
    ("Divan sotiladi yangi holati yaxshi",
     "Uy va bog'"),
    ("iPhone 14 Pro sotiladi yangi hech ishlatilmagan",
     "Elektr jihozlari"),
    ("Muzlatgich Artel sotiladi holati zor",
     "Elektr jihozlari"),
    ("Kaptar sotiladi juftligi",
     "Hayvonlar"),
    ("Erkaklar kurtkasi charm olcham 52",
     "Moda va stil"),
    ("Nexia 2 kolodka old orqa original",
     "Transport"),
    ("Tomorqa sotiladi 6 sotix Zangiota",
     "Ko'chmas mulk"),
    # Ishonch yetmasa — bo'sh. Noto'g'ri kategoriya e'lonni umrbod
    # noto'g'ri bo'limda qoldiradi.
    ("abcdefg qwerty", ""),
    ("123 456", ""),
    ("zzzz xxxx yyyy", ""),
]


def main() -> int:
    baza.init()
    xato = 0
    jami = 0

    print("=== 1. MA'NOSIZ MATN KATEGORIYA OLMAYDI ===")
    for matn in MANOSIZ:
        jami += 1
        natija = baza.bozor_izi(matn)
        if natija:
            xato += 1
            print("  XATO %-26s -> %s" % (matn[:24], sorted(natija)))
        else:
            print("  OK   %-26s" % matn[:24])

    print("\n=== 2. SOTUVCHI <-> XARIDOR ===")
    for sotuvchi, xaridor, kutilgan in JUFTLAR:
        jami += 1
        a = set(belgilar(sotuvchi))
        b = set(belgilar(xaridor))
        mos = bool(a & b)
        if mos != kutilgan:
            xato += 1
            print("  XATO %-34s <-> %-28s kutilgan %s, chiqdi %s"
                  % (sotuvchi[:32], xaridor[:26], kutilgan, mos))
        else:
            print("  OK   %-34s <-> %-28s %s"
                  % (sotuvchi[:32], xaridor[:26], sorted(a & b) or "-"))

    print("\n=== 3. E'LON KATEGORIYASI ===")
    for matn, kutilgan in KATEGORIYALAR:
        jami += 1
        natija = baza.taxminiy_kategoriya(matn)
        if natija != kutilgan:
            xato += 1
            print("  XATO %-30s kutilgan %-18s chiqdi %s"
                  % (matn[:28], kutilgan or "(bo'sh)", natija or "(bo'sh)"))
        else:
            print("  OK   %-30s -> %s" % (matn[:28], natija or "(bo'sh)"))

    # ── 4. O'ZINGGA O'Z SO'ROVING KELMASIN (2026-08-15) ──────────────
    #
    # Aziz topgan xato: u telefon sotuvchisi bo'lib ro'yxatdan o'tgan,
    # keyin o'zi telefon so'ragan va bildirishnoma o'ziga kelgan.
    # Kichik bozorda bu odatiy holat — sotuvchi ham xaridor bo'ladi.
    #
    # Bog'lovchi belgi telefon raqami. Format turlicha bo'lgani uchun
    # oxirgi 9 raqam solishtiriladi: +998901234567, 998901234567 va
    # 901234567 — bitta odam.
    print("\n=== 4. SOTUVCHI O'Z SO'ROVINI OLMASIN ===")

    class _Qator(dict):
        def __getitem__(self, k):
            return self.get(k)

    holatlar = [
        ("+998901234567", "+998901234567", True,  "aynan bir xil"),
        ("+998901234567", "998901234567",  True,  "+ belgisisiz"),
        ("+998901234567", "901234567",     True,  "faqat 9 xona"),
        ("+998901234567", "+998901234568", False, "boshqa raqam"),
        ("+998901234567", "",              False, "sotuvchida raqam yo'q"),
        ("",             "+998901234567",  False, "so'rovda raqam yo'q"),
    ]
    for sorov_aloqa, sotuvchi_aloqa, kutilgan, izoh in holatlar:
        jami += 1
        o9 = lambda x: (lambda r: r[-9:] if len(r) >= 9 else "")(
            "".join(ch for ch in str(x or "") if ch.isdigit()))
        chetlanadi = bool(o9(sorov_aloqa)) and o9(sotuvchi_aloqa) == o9(sorov_aloqa)
        if chetlanadi != kutilgan:
            xato += 1
            print("  XATO %-24s kutilgan %s, chiqdi %s"
                  % (izoh, kutilgan, chetlanadi))
        else:
            print("  OK   %-24s chetlanadi=%s" % (izoh, chetlanadi))

    print("\n=== 5. ERKIN QIDIRUV — OR NOMZODLARINI BALLASH ===")
    t, x = _erkin_qidiruv_sinovlari()
    jami += t
    xato += x

    print("\n  %d to'g'ri · %d xato  (%d tadan)" % (jami - xato, xato, jami))
    return 1 if xato else 0


# ---------------------------------------------------------------- #
# 5. ERKIN QIDIRUV — OR BOSQICHI NOMZODLARINI PYTHON BALLASHI
#
# 2026-08-16: OR bosqichi `ORDER BY rank` dan `rowid DESC` ga o'tdi
# (tezlik: 458-1167 ms -> 5-9 ms). Endi nomzodlar QANDAY TARTIBDA
# kelsa ham sifat Python ballashiga bog'liq — bu bo'lim shuni qattiq
# qo'riqlaydi. `relevans_sinov` faqat model yo'lini qamraydi, erkin
# yo'l (lug'at tanimagan so'rov) shu yerda tekshiriladi.
#
# Nomzodlar deterministik — haqiqiy baza va FTS tartibidan mustaqil.
# ---------------------------------------------------------------- #

def _erkin_elon(tashqi_id: str, nom: str, sana: str = "2026-08-10",
                kategoriya: str = "") -> dict:
    return {
        "id": 0, "manba": "olx", "tashqi_id": tashqi_id, "nom": nom,
        "narx_som": 250_000, "narx_asl": "", "holat": "yangi",
        "viloyat": "Toshkent shahri", "shahar": "Toshkent",
        "tuman": "Chilonzor", "sana": sana,
        "havola": f"https://example.test/{tashqi_id}",
        "rasm": "", "biznes": 0, "qism_turi": "",
        "sotuvchi_nomi": "Sinov", "kategoriya": kategoriya,
        "tan_modellar": None, "tan_qismlar": None, "tan_nom_qismlar": None,
    }


def _erkin_qidiruv_sinovlari() -> tuple[int, int]:
    """Erkin yo'l sifatini deterministik nomzod to'plamida tekshiradi."""
    import qidiruv

    # "divan charm" so'rovi OR bosqichidan shu nomzodlarni oldi deb
    # olaylik (tartib ATABAY aralash — Python qayta ballashi shart):
    #   a — aniq "divan" sarlavhada  (xaridor shuni ko'rishi kerak)
    #   b — faqat "charm" PREFIKSI    (Charmhoo — begona brend)
    #   c — ikkala so'z               (eng yuqori ball)
    #   d — hech biri yo'q            (filtrlanishi shart)
    #   e — faqat KATEGORIYAda "divan" (qoladi, lekin pastda)
    nomzodlar = [
        _erkin_elon("a", "Audit divan yangi 2 orinli"),
        _erkin_elon("b", "Charmhoo cotecho R13"),
        _erkin_elon("c", "Yumshoq divan zamonaviy charm"),
        _erkin_elon("d", "Kir yuvish mashinasi 10 kg"),
        _erkin_elon("e", "Yumshoq mebel", kategoriya="Uy va bog'/Divanlar"),
    ]
    for i, x in enumerate(nomzodlar, 1):
        x["id"] = i
    idlar = list(range(1, len(nomzodlar) + 1))

    eski_fts = baza.fts_erkin
    eski_idlardan = baza.elonlar_idlardan
    baza.fts_erkin = lambda sozlar, limit=900, faqat_birga=False: idlar
    baza.elonlar_idlardan = lambda lst: [x for x in nomzodlar if x["id"] in lst]
    try:
        natija = qidiruv.qidir("divan charm", limit=10)
    finally:
        baza.fts_erkin = eski_fts
        baza.elonlar_idlardan = eski_idlardan

    tartib = [x["tashqi_id"] for x in natija["natijalar"]]
    ballar = {x["tashqi_id"]: x["ball"] for x in natija["natijalar"]}

    holatlar = [
        # Eng muhimi: "d" (hech qanday so'z yo'q) UMUMAN chiqmaydi.
        ("d" not in tartib, "ma'nosiz nomzod (hech bir so'z yo'q) filtrlansin"),
        # "c" ikkala so'zni sarlavhada saqlaydi — eng yuqori.
        (tartib and tartib[0] == "c", "ikkala so'zli sarlavha birinchi bo'lsin"),
        # Aniq "divan" prefiks-mosdan (Charmhoo) yuqori turadi.
        (ballar.get("a", 0) > ballar.get("b", 0),
         "aniq so'z prefiks-mosdan yuqori ball olsin"),
        # Kategoriyadagi so'z sarlavhadagidan past ball oladi, lekin qoladi.
        ("e" in tartib and ballar.get("e", 10**9) < ballar.get("c", 0),
         "kategoriya mosligi sarlavha mosligidan past bo'lsin"),
    ]
    for shart, nom in holatlar:
        if shart:
            print("  OK   %s" % nom)
        else:
            print("  XATO %s  (tartib: %s, ballar: %s)"
                  % (nom, tartib, ballar))
    return len(holatlar) - sum(not s for s, _ in holatlar), \
        sum(not s for s, _ in holatlar)


# 5-bo'lim asosiy main() ichidan chaqiriladi — oxirgi umumiy sanashdan
# oldin. `_erkin_qidiruv_sinovlari` o'z holatlarini bosadi, qaytaradi:
# (to'g'ri, xato).

if __name__ == "__main__":
    sys.exit(main())
