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

    print("\n  %d to'g'ri · %d xato  (%d tadan)" % (jami - xato, xato, jami))
    return 1 if xato else 0


if __name__ == "__main__":
    sys.exit(main())
