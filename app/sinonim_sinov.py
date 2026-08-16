"""SINONIM SINOVI — o'zbekcha va ruscha mahsulot nomlari bir-birini topadimi?

Nega bu fayl bor
----------------
Yangi manbalar (Glotr, Shahar.uz) RUSCHA nom olib keladi, xaridor esa
O'ZBEKCHA yozadi: "zaryadka" so'rovi "Зарядное устройство"ni, "kitob"
"Книга"ni topishi kerak. Yechim `lugat.normalla()` ichidagi `_KANONIK`
xaritasi: ruscha shakl normallashganda o'zbekcha kanonik shaklga keladi,
FTS indeksi ham shu normalla bilan qurilgani uchun ikkala tomon bir xil.

Bu sinov `_KANONIK` ni qo'riqlaydi. Har juftlik ASL yozuvdan (kirillcha
ruscha + lotincha o'zbekcha) normallashganda TENG bo'lishi shart.
Qo'lda hisoblangan kalit xato bo'lsa (masalan "часы" -> "chasi" deb
yozilsa, aslida "shasi" — ch->sh qoidasi bor) sinov yiqiladi.

Ishga tushirish:  python3 sinonim_sinov.py
"""

from __future__ import annotations

import sys

from lugat import normalla, _KANONIK

# (ruscha asl yozuv, o'zbekcha asl yozuv). Ikkalasi ham normallashganda
# BIR XIL bo'lishi kerak. Ro'yxat production o'lchovidan (2026-08-16):
# har qator bir marta HAQIQATAN topilmay qolgan so'rov.
JUFtLIKLAR = [
    ("Зарядное устройство", "zaryadka"),
    ("Зарядная", "zaryadka"),
    ("Аренда", "ijara"),
    ("Аренда квартиры", "kvartira ijara"),
    ("Стиральная машина", "kir yuvish mashinasi"),
    ("Газовая плита", "gaz plita"),
    ("Холодильник", "muzlatgich"),
    ("Кровать", "karavot"),
    ("Книга", "kitob"),
    ("Книги", "kitob"),
    ("Часы", "soat"),
    ("Ковер", "gilam"),
    ("Ковры", "gilam"),
    ("Подушка", "yostiq"),
    ("Дверь", "eshik"),
    ("Двери", "eshik"),
    ("Окно", "deraza"),
    ("Окна", "deraza"),
    ("Кирпич", "g'isht"),
    ("Краска", "bo'yoq"),
    ("Труба", "quvur"),
    ("Трубы", "quvur"),
    ("Казан", "qozon"),
    ("Чайник", "choynak"),
    ("Чайники", "choynak"),
    ("Серьги", "zirak"),
    ("Браслет", "bilaguzuk"),
    ("Очки", "ko'zoynak"),
    ("Полотенце", "sochiq"),
    ("Рубашка", "ko'ylak"),
    ("Платье", "ko'ylak"),
    ("Обувь", "poyabzal"),
    ("Утюг", "dazmol"),
    ("Пылесос", "changyutgich"),
    ("Фен", "parmaxona"),
    ("Тетрадь", "daftar"),
    ("Мыло", "sovun"),
    ("Обогреватель", "isitgich"),
    ("Зонт", "soyabon"),
    ("Перчатки", "qo'lqop"),
    ("Брюки", "shim"),
    ("Карандаш", "qalam"),
    ("Цепочка", "zanjir"),
    ("sovutgich", "muzlatgich"),   # uz-uz sinonimi — ruscha emas
]


def main() -> int:
    print("=" * 64)
    print("  OBER — SINONIM QATLAMI (o'zbekcha <-> ruscha)")
    print("=" * 64)

    def bir_birini_topadi(a: str, b: str) -> bool:
        """a so'zlarining HAR BIRI b ning biror so'ziga prefiks bo'lsa.

        FTS prefiks qidiruvi bilan aynan shunday ishlaydi: "zaryadka"
        so'rovi "zariadka ustroistvo" (Зарядное устройство) e'lonini
        topadi, chunki "zariadka*" tokeniga mos keladi. To'liq tenglik
        shart emas — qisqa tomon so'zlari uzun tomonning prefiksi bo'lsa
        yetarli.
        """
        a_soz, b_soz = a.split(), b.split()
        # Qisqa tomon so'zlari uzun tomonning biror so'ziga mos kelsin.
        qisqa, uzun = (a_soz, b_soz) if len(a_soz) <= len(b_soz) \
            else (b_soz, a_soz)
        return all(any(u.startswith(k) for u in uzun) for k in qisqa)

    xato = 0
    jami = 0
    for ru, uz in JUFtLIKLAR:
        jami += 1
        n_ru, n_uz = normalla(ru), normalla(uz)
        # 1) Ikkala til bir-birini topishi shart (ikkala yo'nalishda).
        if not (bir_birini_topadi(n_ru, n_uz)
                and bir_birini_topadi(n_uz, n_ru)):
            xato += 1
            print("  XATO %-24s -> %r <-> %r"
                  % (f"{ru!r} / {uz!r}", n_ru, n_uz))
            continue
        # 2) Idempotentlik: xarita natijasi yana xaritaga tushmasligi kerak.
        #    Aks holda ikkita qoida zanjir bo'lib bir-birini chaqiradi.
        if normalla(n_ru) != n_ru:
            xato += 1
            print("  XATO %-24s idempotent emas: %r -> %r"
                  % (f"{ru!r}", n_ru, normalla(n_ru)))
            continue
        print("  OK   %-24s -> %r" % (f"{ru!r} = {uz!r}", n_ru))

    # 3) Qoida kalitlari qidiruv tozalagichidan o'tishi shart
    #    (`sorovni_tozala` 2 harfdan qisqa so'zni tashlaydi).
    qisqa = sorted(k for k in _KANONIK if len(k) <= 2)
    if qisqa:
        xato += 1
        print("  XATO 2 harfdan qisqa kalitlar (qidiruv ularni tashlaydi):",
              qisqa)
    else:
        print("  OK   barcha kalitlar uzunligi 3+")

    # 4) Qiymat ham kalit bo'lmasin — zanjirli almashtirish xavfi.
    qadriyat_kalit = sorted(set(_KANONIK.values()) & set(_KANONIK))
    if qadriyat_kalit:
        xato += 1
        print("  XATO qiymat ham kalit bo'lib qolgan (zanjir xavfi):",
              qadriyat_kalit)
    else:
        print("  OK   qiymatlar kalitlar bilan kesishmaydi")

    print("-" * 64)
    print(f"  NATIJA: {jami - xato} to'g'ri · {xato} xato ({jami} juftlik"
          f" + {len(_KANONIK)} kalit)")
    return 1 if xato else 0


if __name__ == "__main__":
    sys.exit(main())
