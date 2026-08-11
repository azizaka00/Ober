"""OBER yo'nalishlari — sotuvchi va so'rovni bir-biriga ulash uchun.

MUHIM TAMOYIL (2026-08-04 da tuzatildi)
---------------------------------------
Bu lug'at — BONUS, SHART EMAS.

Ilgari bu faylda BITTA yo'nalish bor edi: banner va reklama. Natijada
OBER faqat ikki xil sotuvchini qabul qilardi — avtoehtiyot qism sotuvchi
va bannerchi. Mebelchi, tikuvchi, usta, fotograf, kandolatchi, shifokor,
repetitor — hammasi ro'yxatdan o'tmoqchi bo'lganda 422 xato olardi:
"Yo'nalishni hali aniq tushunmadik."

Aziz, 2026-08-04: *"Hali men har xil turdagi sotuvchi va xizmat
ko'rsatuvchilarga demak OBER ni tavsiya qila olmas ekanmanda."*

Aynan shu saboq 2026-08-02 da QIDIRUV tomonida allaqachon o'rganilgan
edi ("lug'at shart emas, bonus" — `OBER-DIZAYN-QOIDALARI.md`, 10-bo'lim),
lekin sotuvchi halqasiga ko'chirilmagan ekan.

Endi qoida bitta va ikkala tomonga baravar tegishli:

    Lug'at tanisa — moslik ANIQ bo'ladi.
    Tanimasa — odamning O'Z SO'ZLARI bo'yicha ishlaydi.
    Hech kim rad etilmaydi.

Yo'nalish qo'shish
------------------
Yangi yo'nalish faqat REAL sotuvchi kelganda qo'shiladi, kitobdan
ko'chirib emas. Ibora — odam O'ZI yozadigan so'z bo'lsin ("kir yuvish
mashinasi"), rasmiy kategoriya nomi emas ("Maishiy texnika xizmatlari").

Ibora yozish qoidasi
--------------------
Bir so'zli ibora so'z BOSHI bo'yicha qidiriladi: "mebel" -> "mebellar",
"mebelchi" ham tutiladi. Bu o'zbek tilida zarur, chunki qo'shimchalar
ko'p.

Lekin qisqa so'zlarda bu xatoga olib keladi. 2026-08-04 o'lchov:
  "kafe"  -> "KAFEL teraman"  ni oshxona deb tanidi
  "tort"  -> "setka TORTISH"  ni kandolat deb tanidi
Bunday so'z oldiga `=` qo'yiladi — u faqat TO'LIQ so'z sifatida
qidiriladi: `"=kafe"`.
"""

from __future__ import annotations

import re

from lugat import normalla


YO_NALISHLAR: dict[str, dict] = {
    # ── SAVDO ────────────────────────────────────────────────────────
    "banner_reklama": {
        "nom": "Banner va tashqi reklama",
        "iboralar": (
            "banner", "baner", "баннер", "poligrafiya", "полиграфия",
            "tashqi reklama", "наружная реклама", "reklama stend",
            "plakat", "poster", "vizitka", "flayer", "flyer",
            "chop etish", "pechat", "печать", "chop qilish",
            "lightbox", "obemniy harf", "oracal", "orakal",
        ),
    },
    "mebel": {
        "nom": "Mebel",
        "iboralar": (
            "mebel", "мебель", "divan", "диван", "shkaf", "шкаф",
            "karavot", "кровать", "krovat", "stol stul", "стол стул",
            "oshxona mebeli", "кухонный гарнитур", "garnitur",
            "yumshoq mebel", "мягкая мебель", "matras", "матрас",
            "komod", "комод", "tumba", "тумба", "kreslo", "кресло",
        ),
    },
    "kiyim": {
        "nom": "Kiyim va poyabzal",
        "iboralar": (
            "kiyim", "одежда", "koylak", "куйлак", "платье", "futbolka",
            "shim", "брюки", "kurtka", "куртка", "palto", "пальто",
            "poyabzal", "обувь", "tufli", "туфли", "krossovka", "кроссовки",
            "tikuvchi", "tikaman", "ateliye", "ателье", "швея",
            "trikotaj", "трикотаж", "forma tikish", "milliy libos",
        ),
    },
    "bolalar": {
        "nom": "Bolalar tovarlari",
        "iboralar": (
            "bolalar kiyimi", "детская одежда", "oyinchoq", "игрушк",
            "kolyaska", "коляска", "beshik", "детская кроват",
            "bolalar mebeli", "avtokreslo", "автокресло", "pampers",
        ),
    },
    "oziq_ovqat": {
        "nom": "Oziq-ovqat va kulinariya",
        "iboralar": (
            # "=" — faqat to'liq so'z. "tort\w*" bo'lsa "setka TORTISH"
            # ni, "kafe\w*" bo'lsa "KAFEL teraman" ni tutib olardi.
            "=tort", "tortlar", "=торт", "shirinlik", "сладост", "kandolat",
            "non yopish", "выпечк", "pishiriq", "=kafe", "=кафе",
            "milliy taom", "osh buyurtma", "плов на заказ",
            "keyterin", "кейтеринг", "banket", "банкет", "dostavka ovqat",
            "quruq meva", "сухофрукт", "asal", "мёд",
        ),
    },

    # ── XIZMAT ───────────────────────────────────────────────────────
    "qurilish_tamir": {
        "nom": "Qurilish va ta'mirlash",
        "iboralar": (
            # "tamirlash" va "remont" ATAYLAB yo'q: ular juda umumiy.
            # "Kompyuter tamirlash" ni ham qurilish deb tanib olardi.
            # Ta'mir qaysi sohaga tegishli ekanini OBYEKT belgilaydi
            # (kompyuter / muzlatgich / kvartira), "ta'mir" so'zi emas.
            "qurilish", "строительств", "ремонт квартир", "kvartira tamiri",
            "kafel", "кафель", "плитк", "malyarka", "маляр",
            "gipsokarton", "гипсокартон", "shpaklovka", "шпаклевк",
            "santexnik", "сантехник", "elektrik", "электрик",
            "svarka", "сварк", "payvandlash", "beton", "бетон",
            "tom yopish", "кровл", "eshik ornatish", "deraza ornatish",
            "plastik deraza", "пластиковые окна", "natyajnoy potolok",
            "натяжной потолок", "fasad", "фасад", "travertin",
        ),
    },
    "maishiy_tamir": {
        "nom": "Maishiy texnika ta'miri",
        "iboralar": (
            "muzlatgich", "холодильник", "kir yuvish", "стиральн",
            "konditsioner", "кондиционер", "televizor tamir",
            "mikroto'lqin", "микроволнов", "changyutgich", "пылесос",
            "gaz plita", "газовая плита", "boyler", "бойлер",
            "maishiy texnika", "бытовая техника",
        ),
    },
    "avto_xizmat": {
        "nom": "Avto xizmat",
        "iboralar": (
            "avtoservis", "автосервис", "moy almashtirish", "замена масла",
            "shinomontaj", "шиномонтаж", "balanslash", "балансировк",
            "kuzov", "кузовн", "rihtovka", "рихтовк", "pokraska",
            "tonirovka", "тонировк", "avto kimyoviy", "химчистка авто",
            "diagnostika avto", "avto elektrik", "автоэлектрик",
            "avtomoyka", "автомойка", "signalizatsiya ornatish",
        ),
    },
    "kompyuter_it": {
        "nom": "Kompyuter va IT",
        "iboralar": (
            "kompyuter", "компьютер", "noutbuk", "ноутбук",
            "printer", "принтер", "kartrij", "картридж",
            "zapravka", "заправк", "sayt yasash", "создание сайт",
            "dastur", "программир", "setka tortish", "локальная сет",
            "videokuzatuv", "видеонаблюден", "kamera ornatish",
        ),
    },
    "telefon": {
        "nom": "Telefon va aksessuar",
        "iboralar": (
            "telefon", "телефон", "smartfon", "смартфон",
            "ekran almashtirish", "замена экран", "displey",
            "telefon tamir", "ремонт телефон", "chexol", "чехол",
            "quloqchin", "наушник", "zaryadnik", "зарядк",
        ),
    },
    "gozallik": {
        "nom": "Go'zallik va salomatlik",
        "iboralar": (
            "sartarosh", "парикмахер", "soch olish", "стрижк",
            "manikyur", "маникюр", "pedikyur", "педикюр",
            "kosmetolog", "косметолог", "massaj", "массаж",
            "gozallik saloni", "салон красоты", "kirpik", "ресниц",
            "makiyaj", "макияж", "epilyatsiya", "эпиляц",
        ),
    },
    "tashish": {
        "nom": "Yuk tashish va yetkazib berish",
        "iboralar": (
            "yuk tashish", "грузоперевоз", "gruzchik", "грузчик",
            "pereezd", "переезд", "kochirish xizmati", "kuryer",
            "курьер", "dostavka", "доставк", "yetkazib berish",
            "manzilga yetkazish", "taksi", "такси", "evakuator",
            "эвакуатор", "refrijerator",
        ),
    },
    "tadbir": {
        "nom": "To'y va tadbirlar",
        "iboralar": (
            "toy xizmati", "свадебн", "fotograf", "фотограф",
            "videograf", "видеосъемк", "video suratga", "tamada",
            "тамада", "boshlovchi", "ведущий", "dj", "диджей",
            "shar bezash", "шары", "dekor", "декор", "arenda zal",
            "toyxona", "sozanda", "artist", "аниматор", "animator",
        ),
    },
    "talim": {
        "nom": "Ta'lim va kurslar",
        "iboralar": (
            "repetitor", "репетитор", "oqituvchi", "kurs", "курсы",
            "ingliz tili", "английский", "rus tili", "matematika",
            "математик", "haydovchilik kursi", "автошкол",
            "dasturlash kursi", "buxgalteriya kursi", "ielts",
            "onlayn dars", "онлайн урок",
        ),
    },
    "kochmas_mulk": {
        "nom": "Ko'chmas mulk",
        "iboralar": (
            "kvartira", "квартир", "uy sotish", "продажа дом",
            "ijara", "аренда", "arenda", "rieltor", "риэлтор",
            "ofis ijara", "офис аренда", "yer uchastka", "участок",
            "novostroyka", "новостройк", "dacha", "дача",
        ),
    },
    "hujjat_moliya": {
        "nom": "Hujjat, moliya va yuridik",
        "iboralar": (
            "buxgalter", "бухгалтер", "notarius", "нотариус",
            "tarjima", "перевод документ", "yuridik", "юридическ",
            "advokat", "адвокат", "soliq hisoboti", "налогов",
            "biznes royxatdan", "регистрация ооо", "sertifikat olish",
        ),
    },
    "sogliq": {
        "nom": "Sog'liq va optika",
        "iboralar": (
            "dorixona", "аптек", "tibbiy", "медицинск", "shifokor",
            "врач", "koz oynak", "kozoynak", "очки", "optika", "оптик",
            "ortoped", "ортопед", "stomatolog", "стоматолог",
            "tish davolash", "massajchi", "analiz",
        ),
    },
    "hayvonlar": {
        "nom": "Hayvonlar",
        "iboralar": (
            "veterinar", "ветеринар", "it sotiladi", "mushuk",
            "кошк", "собак", "quyon", "tovuq", "parranda",
            "hayvon yemi", "корм для", "akvarium", "аквариум",
        ),
    },
    "bogdorchilik": {
        "nom": "Bog'dorchilik va o'simlik",
        "iboralar": (
            "kochat", "саженц", "urug", "семен", "ogit", "удобрен",
            "gul sotish", "цветы", "landshaft", "ландшафт",
            "gazon", "газон", "issiqxona", "теплиц",
        ),
    },
    "sport": {
        "nom": "Sport va hobbi",
        "iboralar": (
            "velosiped", "велосипед", "trenajyor", "тренажер",
            "sport anjom", "спортивн", "fitnes", "фитнес",
            "murabbiy", "тренер", "turizm anjom", "palatka",
            "baliq ovi", "рыбалк",
        ),
    },
}


# Bir so'zli iboralar uchun so'z BOSHI bo'yicha ham qidiramiz:
# sotuvchi "mebellar", "mebelchi", "tortlar" deb yozishi mumkin.
# Ko'p so'zli iboralar to'liq ketma-ketlik sifatida qidiriladi.
def _tayyorla() -> list[tuple[str, re.Pattern]]:
    from lugat import TOXTA

    natija = []
    tashlangan = []
    for kalit, d in YO_NALISHLAR.items():
        boshlar, aniqlar, iboralar = [], [], []
        for xom in d["iboralar"]:
            aniq = xom.startswith("=")
            n = normalla(xom[1:] if aniq else xom)
            if not n:
                continue
            # NORMALLASHGACH TO'XTASH SO'ZIGA AYLANGAN IBORA — IBORA EMAS.
            #
            # 2026-08-10, jonli so'rovlarda topildi:
            #
            #     "Nexia 2 fara 300000 so'mga kimda bor"  -> kiyim
            #     "Samsung s24 ultralar kimda nech pul?"  -> kiyim
            #
            # Sabab: `normalla("kiyim")` -> "kim" (y->i va takror
            # unlilar qisqaradi). Qolip esa so'z BOSHI bo'yicha
            # qidiradi — `\bkim\w*` "kimda", "kimga", "kimdir" ni ham
            # tutadi. "Kimda bor?" esa o'zbekchada eng tabiiy so'rash
            # usuli, ya'ni bunday so'rovlarning HAMMASI tikuvchiga
            # ketardi.
            #
            # Qoida qo'lda yozilmaydi: to'xtash so'zlari ro'yxati
            # allaqachon bor va u savol so'zlarini biladi. Kelajakda
            # boshqa ibora shunday to'qnashsa — o'zi tashlanadi.
            if " " not in n and n in TOXTA:
                tashlangan.append((kalit, xom, n))
                continue
            if " " in n:
                iboralar.append(re.escape(n))
            elif aniq:
                aniqlar.append(re.escape(n))
            else:
                boshlar.append(re.escape(n))
        qismlar = []
        if boshlar:
            # so'z boshi: "mebel" -> "mebellar", "mebelchi" ham tutiladi
            qismlar.append(r"\b(?:" + "|".join(boshlar) + r")\w*")
        if aniqlar:
            # faqat to'liq so'z: "kafe" bor, "kafel" yo'q
            qismlar.append(r"\b(?:" + "|".join(aniqlar) + r")\b")
        if iboralar:
            qismlar.append(r"(?:" + "|".join(iboralar) + r")")
        if qismlar:
            natija.append((kalit, re.compile("|".join(qismlar))))
    if tashlangan:
        _TASHLANGAN.extend(tashlangan)
    return natija


# Qaysi iboralar to'xtash so'ziga to'qnashgani uchun tashlandi.
# Sinov shu ro'yxatni tekshiradi — jimgina yo'qolib qolmasin.
_TASHLANGAN: list[tuple[str, str, str]] = []


_QOLIP = _tayyorla()


def yonalishlarni_top(matn: str) -> set[str]:
    """Erkin matndan yo'nalish belgilarini topadi.

    IKKI MANBA:
      1. Yuqoridagi qo'lda yozilgan ro'yxat — 20 ta keng yo'nalish.
      2. `soz_kategoriya` — 267 000 haqiqiy e'londan HISOBLANGAN
         lug'at. U qo'lda yozilmaydi, o'zi o'sadi va 100 000 xil
         tovarni qoplaydi. Belgilari `kat:` bilan boshlanadi.

    Hech narsa topilmasligi — XATO EMAS. Bu holatda tizim odamning
    o'z so'zlari bo'yicha ishlaydi (`baza._mos_sotuvchilar`).
    """
    n = normalla(matn or "")
    if not n:
        return set()
    # 2026-08-10: bu yerda `soz_kategoriya.kategoriyalarni_top` ham
    # chaqirilardi — HAR SO'Z uchun bitta kategoriya beradigan
    # hisoblangan lug'at. U olib tashlandi.
    #
    # Sabab: u so'zni YOLG'IZ ko'radi. `oyna` mebel e'lonlarida ko'p
    # uchraydi -> "Uy va bog'". Natijada "lacettiga labavoy oyna kerak"
    # mebelchiga borardi (jonli testda ko'rildi).
    #
    # O'rniga `baza.bozor_izi` ishlatiladi: u butun matnni indeksdan
    # o'tkazadi, ya'ni so'zlarni BIRGALIKDA ko'radi. Qo'shilishi va
    # tozalanishi quyidagi `belgilar()` da — chaqiruvchida emas.
    return {kalit for kalit, qolip in _QOLIP if qolip.search(n)}


def tozalangan(matn: str, modellar, qismlar) -> set[str]:
    """Yo'nalishlar, ANIQ signal bilan tozalangan.

    MUAMMO (2026-08-09, jonli testda topildi)
    -----------------------------------------
    Mebelchi bo'lib ro'yxatdan o'tdim ("mebel yasayman divan shkaf
    karavot"). Kabinetda birinchi ko'rgan xaridor so'rovim:

        "lacettiga labavoy oyna kerak"

    Lacetti mashinasining old oynasi. Mebelga aloqasi yo'q.

    Sabab: `soz_kategoriya` — 258 000 e'londan HISOBLANGAN lug'at.
    Unda `oina` so'zi "Uy va bog'" ga bog'langan, chunki mebel
    e'lonlarida oyna (ko'zgu, shisha) juda ko'p uchraydi. Statistika
    to'g'ri — lekin bu so'rovda yonida `lacetti` (mashina modeli) va
    `oyna` (avto qismi) turibdi.

    QOIDA: aniq signal statistik taxmindan ustun.
    Lug'at model VA qismni birga tanigan bo'lsa — bu avto so'rovi.
    Hisoblangan lug'at qo'shgan boshqa kategoriyalar shovqin, ular
    olib tashlanadi. Avto yo'nalishlari va qo'lda yozilgan yorliqlar
    qoladi.

    Nega ikkalasi birga shart: `modellarni_top` yolg'iz o'zi
    ishonchsiz — "Divan Ugalok TESLA" ni ham tesla deb tanigan edi.
    Model + qism birgalikda esa kuchli dalil.
    """
    return _avto_qoidasi(yonalishlarni_top(matn), modellar, qismlar)


AVTO_KAT = ("kat:Transport", "kat:Avto ehtiyot qism")


def _avto_qoidasi(teglar: set[str], modellar, qismlar) -> set[str]:
    """Model VA qism birga tanilgan bo'lsa — avto bo'lmagan kat: ni olib tashla."""
    if not (modellar and qismlar):
        return teglar
    return {k for k in teglar
            if not k.startswith("kat:") or k in AVTO_KAT}


def belgilar(matn: str) -> list[str]:
    """Matnning YAKUNIY yorliqlari. Xaridor ham, sotuvchi ham shu yerdan.

    NEGA BITTA JOYDA (2026-08-10)
    -----------------------------
    Ilgari server ikki joyda shunday yozardi:

        tozalangan(matn, modellar, qismlar) | baza.bozor_izi(matn)

    Ko'rinishi to'g'ri, lekin tozalash `|` dan OLDIN bo'lgani uchun
    `bozor_izi` natijasi tozalanmay o'tib ketardi. Ya'ni 2026-08-09 da
    tuzatilgan xato boshqa eshikdan qaytib kelgan edi:

        "lacettiga labavoy oyna kerak" -> kat:Uy va bog'  (mebelchiga!)

    Sabab: indeksda `oyna` so'zi uy oynasi bilan to'lgan. Statistika
    to'g'ri, lekin yonida `lacetti` (model) va `oyna` (avto qismi)
    turibdi — aniq signal statistik taxmindan ustun.

    Endi tozalash BUTUN to'plamga qo'llanadi va u faqat shu funksiyada
    bajariladi. Chaqiruvchi tartibni buza olmaydi.
    """
    import baza
    from lugat import modellarni_top, qismlarni_top

    modellar = modellarni_top(matn)
    qismlar = qismlarni_top(matn)
    hammasi = (yonalishlarni_top(matn) | baza.bozor_izi(matn)
               | baza._yashirin_taxonomiya(matn))
    return sorted(_avto_qoidasi(hammasi, modellar, qismlar))


def yonalish_nomlari(kalitlar) -> list[str]:
    """Ichki belgilarni odamga tushunarli nomga aylantiradi."""
    nomlar = []
    for k in sorted(kalitlar):
        if k in YO_NALISHLAR:
            nomlar.append(YO_NALISHLAR[k]["nom"])
        elif k.startswith("kat:"):
            nomlar.append(k[4:])
    return nomlar
