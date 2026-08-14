"""
OBER — MAHALLIY LUG'AT

Bu fayl loyihaning eng qimmatli qismi. Kod nusxalanadi, lug'at esa
vaqt va tajriba bilan yig'iladi — aynan shu bizning ustunligimiz.

Muammo (2026-07-30 jonli tekshiruvda o'lchangan): OLX'da "neksiya kolodka"
so'roviga 10 ta natija, shundan 4 tasi BOSHQA MASHINA (Трекер, Малибу,
Эквинокс). Sotuvchilar esa bitta so'zni 4 xil imloda yozadi
("chexol chehol chixol chihol"), chunki qidiruv ishlamaydi.

Shu yerda tuzatamiz.
"""

from __future__ import annotations

import re

# ── Kirill -> lotin (o'zbek va rus matnini bir shaklga keltirish) ────────────
KIRILL = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
    "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sh",
    "ъ": "", "ы": "i", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    "қ": "q", "ғ": "g", "ҳ": "h", "ў": "o", "ъ": "",
}


def lotinlash(s: str) -> str:
    return "".join(KIRILL.get(ch, ch) for ch in s.lower())


def normalla(s: str) -> str:
    """Har qanday matnni taqqoslash uchun bir shaklga keltiradi."""
    s = lotinlash(s)
    s = s.replace("'", "").replace("`", "").replace("ʻ", "").replace("’", "")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    # Ko'p uchraydigan imlo tebranishlari. O'zbek yozuvida bir tovush bir necha
    # xil yoziladi — ikkala tomon ham bir xil shaklga keltirilsa, taqqoslash
    # ishonchli bo'ladi. (2026-07-30: "Qoblt" kobalt deb tanilmagan edi.)
    s = re.sub(r"kh", "x", s)
    s = re.sub(r"ts", "s", s)
    s = s.translate(str.maketrans({
        "q": "k",      # qoblt / kobalt
        "w": "v",      # wolksvagen / volksvagen
        "y": "i",      # ekyunoks / ekvinoks
        "j": "z",      # jiguli / ziguli
        "c": "s",      # lacetti / lasetti
    }))
    s = re.sub(r"([a-z])\1+", r"\1", s)       # takroriy harf: "kkk" -> "k"
    s = re.sub(r"\s+", " ", s).strip()
    # ── O'ZBEKCHA↔RUSCHA KANONIK SINO.NIM (2026-08-13) ────────────────
    # Yangi manbalar (Shahar.uz, Glotr) RUSCHA nom olib keladi. O'zbekcha
    # so'rov ularni topa olmay qolgandi:
    #
    #   "zaryadka"      -> zariadka       "Зарядное устройство" -> zariadnoe
    #   "kvartira ijara" -> izara          "Аренда квартиры"    -> arenda
    #   "kir yuvish"     -> iuvish         "Стиральная машина"  -> stiralnaia
    #   "muzlatgich"     -> muzlatgish     "Холодильник"        -> xolodilnik
    #   "karavot"        -> karavot        "Кровать"            -> krovat
    #
    # FTS prefiks qidiruvi "zariadka*" bilan "zariadnoe"ni topa olmaydi
    # — ildiz bir, qo'shimcha boshqa. Yechim: ruscha shakl normallashganda
    # o'zbekcha KANONIK shaklga keladi. FTS indeksi ham shu normalla bilan
    # qurilgani uchun ikkala tomon bir xil bo'ladi — qidiruv ham, indeks ham.
    #
    # Ro'yxat QISQA va ANIQ — faqat o'lchangan, bir ma'noli juftliklar.
    # Kengaytirish shart emas: yangi manba qo'shilsa bozor_izi o'zi taniydi.
    if s:
        for rus, kanonik in _KANONIK.items():
            s = s.replace(" " + rus + " ", " " + kanonik + " ")
            if s.startswith(rus + " "):
                s = kanonik + s[len(rus):]
            if s.endswith(" " + rus):
                s = s[:-(len(rus) + 1)] + " " + kanonik
            if s == rus:
                s = kanonik
    return s


# _KANONIK — normalla() oxirida qo'llanadi (yuqoridagi izoh). Lug'at
# import paytida normalla() ni chaqiradi (TOXTA), shuning uchun bu ro'yxat
# normalla() TA'RIFIDAN KEYIN turishi shart — import tartibi buzilmasin.
_KANONIK = {
    "zariadnoe": "zariadka",     # зарядное  -> zaryadka
    "zariadnaia": "zariadka",    # зарядная  -> zaryadka
    "arenda": "izara",           # аренда    -> ijara
    "stiralnaia": "iuvish",      # стиральная -> yuvish
    "xolodilnik": "muzlatgish",  # холодильник -> muzlatgich
    "krovat": "karavot",         # кровать   -> karavot
    "kvartiri": "kvartira",      # квартиры  -> kvartira (kelishik)
    "kvartire": "kvartira",      # квартире  -> kvartira
    "kvartiru": "kvartira",      # квартиру  -> kvartira
    "prodaja": "sotish",         # продажа   -> sotish
    "prodaza": "sotish",         # продажа   -> sotish (ts->s qoidasi)
}


# ── SO'ROVNI TOZALASH ───────────────────────────────────────────────────────
#
# Aziz, 2026-08-03: xaridor erkin yozadi -
#   "menga soat kerak bambino 6, kim 800.000 so'mga beradi?"
# Bundan qidiruvga faqat SOAT va BAMBINO 6 ketishi kerak. "menga",
# "kerak", "kim", "beradi" - shovqin; "800 000 so'm" esa BYUDJET,
# mahsulot nomi emas. Ilgari hammasi indeksga yuborilardi va natija
# buzilardi.
#
# Ro'yxat xom holda yoziladi va import paytida normallashtiriladi -
# shunda `normalla()` qoidalari (q->k, y->i ...) qo'lda hisoblanmaydi.
_TOXTA_XOM = (
    # so'rash
    "menga", "menda", "bizga", "kerak", "kerakmi", "kere", "keremi",
    "bormi", "bor", "yoq", "yo'q", "topib", "top", "toping", "beradi",
    "beradimi", "bering", "berasiz", "sotadi", "sotasiz", "sotib",
    "olmoqchiman", "olmoqchi", "olaman", "izlayapman", "qidiryapman",
    "kim", "kimda", "kimdir", "qayerda", "qayerdan", "iltimos", "salom",
    "assalomu", "alaykum", "aka", "opa", "birodar",
    # SOTUVCHI FE'LLARI — 2026-08-10 da qo'shildi.
    # Sotuvchi o'zini "gilam sotaman", "mebel yasayman", "kir yuvish
    # mashinasi tuzataman" deb tanishtiradi. Bu fe'llar mahsulotni
    # bildirmaydi, lekin qidiruvni TORAYTIRADI: indeksda "gilam VA
    # sotaman" birga uchraydigan e'lon kam, "gilam" esa minglab.
    # Natijada "gilam sotaman" degan sotuvchi "gilam kerak" degan
    # xaridorni topa olmay qolgan edi.
    "sotaman", "sotamiz", "sotyapman", "sotuvda", "sotiladi",
    "yasayman", "yasaymiz", "qilaman", "qilamiz", "tuzataman",
    "tuzatamiz", "tamirlayman", "ishlayman", "ko'rsataman",
    "beraman", "beramiz", "chiqaraman", "tikaman", "pishiraman",
    "продаю", "продам", "делаю", "ремонтирую", "оказываю",
    # narx
    "narx", "narxi", "narxini", "qancha", "qanchaga", "pul", "puli",
    "so'm", "som", "sum", "dollar", "arzon", "arzonroq", "qimmat",
    # qo'shimchali shakllar - byudjet ifodasidan keyin qolib ketadi
    "so'mga", "so'mgacha", "so'mdan", "so'mni", "so'mlik", "so'mlar",
    "sumga", "sumgacha", "sumdan", "gacha", "atrofida", "chamasi",
    "dollarga", "dollargacha", "ming", "mln", "million",
    # bog'lovchi
    "uchun", "bilan", "yoki", "yana", "ham", "faqat", "juda", "eng",
    "shu", "bu", "ana", "mana", "qanday", "qanaqa", "nima", "necha",
    # ruscha
    "мне", "нужен", "нужна", "нужно", "надо", "есть", "кто", "сколько",
    "продам", "куплю", "ищу", "цена", "сум", "рублей", "пожалуйста",
)


def _toxta_royxat() -> set:
    return {normalla(w) for w in _TOXTA_XOM if normalla(w)}


TOXTA = _toxta_royxat()

# Byudjet: son + valyuta belgisi. "800.000 so'mga", "12 mln", "500$"
_BYUDJET = re.compile(
    r"(\d[\d\s.,]*)\s*(so\s*['`’ʻ]?\s*m|с[ўуo]м|sum|som|ming|минг|"
    r"mln|млн|million|миллион|\$|usd|у\.?е\.?)", re.I)


def byudjet_top(matn: str) -> int | None:
    """So'rovdagi narx chegarasini ajratadi. Topilmasa None."""
    m = _BYUDJET.search(matn or "")
    if not m:
        return None
    son = re.sub(r"[^\d]", "", m.group(1))
    if not son:
        return None
    n = int(son)
    birlik = m.group(2).lower()
    if birlik.startswith(("ming", "минг")):
        n *= 1_000
    elif birlik.startswith(("mln", "млн", "milli", "милли")):
        n *= 1_000_000
    elif birlik.startswith(("$", "usd", "у")):
        n *= 12_800
    return n if 1_000 <= n <= 50_000_000_000 else None


def sorovni_tozala(matn: str) -> tuple[list, int | None]:
    """Erkin so'rovdan izlanadigan so'zlar va byudjetni ajratadi.

    Qaytaradi: (so'zlar, byudjet)
    """
    byudjet = byudjet_top(matn)
    # Byudjet ifodasini matndan olib tashlaymiz - uning raqami
    # mahsulot nomiga aralashmasin ("bambino 6" dagi 6 esa qoladi).
    toza = _BYUDJET.sub(" ", matn or "")
    sozlar = []
    for w in normalla(toza).split():
        if w in TOXTA:
            continue
        if len(w) > 2 or w.isdigit():
            sozlar.append(w)
    return sozlar, byudjet


# ── MASHINA MODELLARI ───────────────────────────────────────────────────────
# Kalit — standart nom. Qiymat — bozorda uchraydigan barcha yozilishlar.
# Normallashtirilgandan keyin taqqoslanadi, shuning uchun kirill ham ishlaydi.
MODELLAR: dict[str, list[str]] = {
    "nexia":     ["nexia", "neksiya", "neksia", "neksya", "nekseya", "nekcia",
                  "nexia2", "nexia3", "neksiya2", "neksiya3", "dons", "donc",
                  "sons", "sonc", "dohc"],      # bozorda shunday ham yoziladi
    "cobalt":    ["cobalt", "kobalt", "kabalt", "kobolt"],
    "gentra":    ["gentra", "jentra", "jentura"],
    "lacetti":   ["lacetti", "lasetti", "laseti", "lachetti"],
    "spark":     ["spark", "sparek", "isparka"],
    "matiz":     ["matiz", "matis"],
    "damas":     ["damas", "damaz"],
    "labo":      ["labo"],
    "tico":      ["tico", "tiko"],
    "malibu":    ["malibu", "malibu2"],
    "captiva":   ["captiva", "kaptiva"],
    "tracker":   ["tracker", "treker"],
    "onix":      ["onix", "oniks"],
    "monza":     ["monza"],
    # Ko'rilgan variant lug'atга yoziladi. Taxminiy topishni bo'shatish
    # xavfli (yolg'on moslik chiqadi) — aniq yozish har doim yaxshiroq.
    "equinox":   ["equinox", "ekvinoks", "ekyunoks", "ekvinox", "ekvnoks"],
    "tahoe":     ["tahoe", "taxo"],
    "orlando":   ["orlando"],
    "epica":     ["epica", "epika"],
    "byd":       ["byd", "chazor", "song", "yuan", "seal", "han"],
    "chery":     ["chery", "cheri", "tiggo", "arizo"],
    "kia":       ["kia", "sonet", "seltos", "sportage", "sorento", "carens",
                  "k5", "bongo", "carnival", "karnival", "rio", "cerato"],
    "hongqi":    ["hongqi", "hongki", "xongqi"],
    "foton":     ["foton", "fotton"],
    "starex":    ["starex", "grand starex", "staryeks"],
    "hyundai":   ["hyundai", "xyundai", "sonata", "elantra", "creta", "accent",
                  "santafe", "tucson", "porter"],
    "lada":      ["lada", "jiguli", "vaz", "priora", "granta", "niva", "xray"],
    "gaz":       ["gazel", "gazell", "gaz", "volga"],
    "uaz":       ["uaz", "uazik", "patriot", "hunter", "buxanka"],
    "zaz":       ["zaz", "forza", "tavria", "slavuta"],
    "yamaha":    ["yamaha", "yamaxa", "yammaxa"],
    "mercedes":  ["mercedes", "merc", "mers", "benz"],
    "bmw":       ["bmw", "bmv"],
    "toyota":    ["toyota", "camry", "corolla", "prado", "lexus"],
    "land_rover": ["land rover", "range rover", "rang rover", "rangerover",
                   "discovery", "defender", "evoque", "velar"],
    "bentley":   ["bentley", "bentayga", "continental", "flying spur"],
    "genesis":   ["genesis", "gv70", "gv80", "g70", "g80", "g90"],
    "infiniti":  ["infiniti", "fx35", "fx37", "qx50", "qx60", "qx70", "qx80"],
    "tesla":     ["tesla", "model3", "modely", "models", "modelx"],
    "buick":     ["buick", "velite", "encore", "enclave", "envision", "lacrosse"],
    "cadillac":  ["cadillac", "escalade", "xts", "ct5", "ct6", "lyriq"],
    "jeep":      ["jeep", "wrangler", "cherokee", "grand cherokee", "compass",
                  "renegade"],
    "mazda":     ["mazda"],
    "ford":      ["ford", "sierra", "focus", "mustang", "mondeo", "escape"],
    "jac":       ["jac"],
    "changan":   ["changan", "changancenter"],
    "isuzu":     ["isuzu"],
    # 2026-07-30 sinovda topilgan yetishmovchilik: bu modellar lug'atda
    # bo'lmagani uchun "modeli yo'q" deb hisoblandi va noto'g'ri natijaga
    # tushdi ("matiz bamper" so'roviga Haval bamperi chiqdi).
    "haval":     ["haval", "jolion", "dargo", "f7", "h6", "m6"],
    "jetour":    ["jetour", "jetur", "x70", "x90", "dashing"],
    "shineray":  ["shineray", "chinerai", "chineray", "shinerey"],
    "ravon":     ["ravon", "r2", "r3", "r4"],
    "chevrolet": ["chevrolet", "shevrole", "shevrolet", "cruze", "kruz",
                  "aveo", "nubira", "rezzo", "trailblazer", "traverse", "travers"],
    "daewoo":    ["daewoo", "deu", "prince", "espero", "leganza", "nexia1"],
    "geely":     ["geely", "jili", "coolray", "emgrand", "atlas", "monjaro"],
    "exeed":     ["exeed", "eksid", "txl", "vx", "lx"],
    "lifan":     ["lifan"],
    "faw":       ["faw", "bestune"],
    "dongfeng":  ["dongfeng", "donfeng", "aeolus", "aelous", "shine"],
    "leapmotor": ["leapmotor", "lipmotor"],
    "xpeng":     ["xpeng", "ikspeng"],
    "zeekr":     ["zeekr", "ziker"],
    "lixiang":   ["lixiang", "lisyan", "l7", "l9"],
    "wuling":    ["wuling", "hongguang"],
    "nissan":    ["nissan", "almera", "qashqai", "serena", "teana", "murano",
                  "xtrail", "patrol"],
    "honda":     ["honda", "civic", "accord", "crv"],
    "volkswagen": ["volkswagen", "folksvagen", "vw", "passat", "polo", "tiguan",
                   "caddy", "kaddi", "golf", "touareg", "teramont"],
    "audi":      ["audi", "avdi", "q5", "a4", "a6"],
    "skoda":     ["skoda", "octavia", "rapid"],
    "renault":   ["renault", "reno", "logan", "duster"],
    "mitsubishi": ["mitsubishi", "mitsubisi", "lancer", "outlander", "pajero"],
    "subaru":    ["subaru"],
    "ssangyong": ["ssangyong", "rexton", "actyon"],
    "hafei":     ["hafei", "hafey"],
    "byd_song":  [],           # BYD variantlari yuqorida
    "kamaz":     ["kamaz", "maz", "zil", "kraz"],
    "daf":       ["daf", "man", "scania", "volvo", "iveco", "howo", "shacman"],
}

# ── QISM TURLARI ────────────────────────────────────────────────────────────
QISMLAR: dict[str, list[str]] = {
    "kolodka":      ["kolodka", "kaladka", "kalodka", "tormoz kolodka",
                     "tormoznaya kolodka", "tormozniy kolodka"],
    "disk_tormoz":  ["tormoz disk", "tormoznoy disk", "disk tormoz"],
    "amortizator":  ["amortizator", "amartizator", "stoyka", "stoyk", "aylanma"],
    # FARA va TUMANKA — BOSHQA narsa (2026-08-01).
    # Ilgari "tumanka" fara ichida edi va "kobalt fara" so'roviga tuman
    # chirog'i birinchi bo'lib chiqardi. Ular boshqa mahsulot, boshqa
    # narx: fara 200-900 ming, tumanka 100-250 ming.
    # "svet" OLIB TASHLANDI (2026-08-02).
    # O'zbek e'lonlarida "svet" — RANG, chiroq emas: "oq svet",
    # "кора свет". Shu tufayli "kobalt fara" so'roviga butun mashinalar
    # chiqardi: "Кобалт 2019 ок свет — 135 000 000". Narx oralig'i
    # 200 ming – 1.4 mln bo'lib buzilgan edi.
    "fara":         ["fara", "far", "faralar", "farasi"],
    "tumanka":      ["tumanka", "tumanki", "protivotuman", "protivotumanka",
                     "туманка", "tuman chirogi", "tuman farasi"],
    # Lug'atda yo'q so'z eng yaqin NOTO'G'RI yozuvga yopishadi — shuning uchun
    # qamrov muhim. (2026-07-30: "galofka" -> "kalodka" deb tanilgan edi.)
    "lampa":        ["lampa", "lampochka", "galogenka", "galofka", "galopka",
                     "ksenon", "led lampa", "lampalar"],
    "suport":       ["suport", "support", "sopport"],
    "opora":        ["opora", "oporniy", "opornik", "opora podshipnik"],
    "katushka":     ["katushka", "katuska", "kotushka", "svecha katushka"],
    "granata":      ["granata", "granat", "shrus", "shrys"],
    "tablo":        ["tablo", "panel pribor", "shitok pribor"],
    "klimat":       ["klimat", "klimat kontrol", "pechka", "otopitel"],
    "oblisovka":    ["oblisovka", "oblitsovka", "oblisofka", "nakladka"],
    "stop":         ["stop", "stopsignal", "zadniy stop", "orqa fara"],
    "bamper":       ["bamper", "bamfer", "bampir", "bufer", "buper"],
    "kapot":        ["kapot", "kaput"],
    "krilo":        ["krilo", "krlo", "krelo", "krylo"],
    "eshik":        ["eshik", "dver", "dverka"],
    "oyna":         ["oyna", "steklo", "lobovoy", "lobovoe", "avtooyna",
                     "shisha", "steklopodyomnik"],
    "rul":          ["rul", "rull", "rulevoy"],
    # "kolonka/kalonka" fuzzy moslikda "kolodka"ga yopishib, tormoz
    # qidiruviga rul kolonkalari chiqayotgan edi. Alohida tur bo‘lsa aniq
    # moslik fuzzy bosqichini to‘xtatadi va ikki qism aralashmaydi.
    "rul_kolonka":  ["kolonka", "kalonka", "qalonka", "rul kolonka",
                     "rulavoy kalonka", "rulovoy kolonka", "rulevaya kolonka",
                     "rulevoy kolonka"],
    "akkumulyator": ["akkumulyator", "akumlyator", "akumulyator", "akum",
                     "akb", "batareya"],
    "starter":      ["starter", "startyor"],
    "generator":    ["generator", "genератор", "gen"],
    "radiator":     ["radiator", "radyator", "radiyator"],
    "nasos":        ["nasos", "pompa", "benzonasos", "toplivniy nasos"],
    "filtr":        ["filtr", "filter", "moy filtr", "vozdushniy filtr"],
    "sveча":        ["svecha", "svecha zajiganiya", "shamcha"],
    "dvigatel":     ["dvigatel", "dvigatil", "motor", "matr"],
    "karobka":      ["karobka", "korobka", "kpp", "akpp", "transmissiya"],
    "sepleniye":    ["sepleniye", "ssepleniye", "diskcepleniya", "sceplenie"],
    "gilza":        ["gilza", "porshen", "porshin", "kolso"],
    "shina":        ["shina", "balon", "rezina", "pokrishka"],
    "disk":         ["disk", "diska", "diskalar", "titan disk"],
    "chexol":       ["chexol", "chehol", "chixol", "chihol", "chekhol", "chexollar"],
    "polik":        ["polik", "kovrik"],
    "signal":       ["signalizatsiya", "signal", "signalizatsia", "starline"],
    "magnitola":    ["magnitola", "magnitafon", "manitor", "monitor", "avtozvuk"],
    "kondensioner": ["konditsioner", "konditsoner", "kondey", "kompressor"],
    "glushitel":    ["glushitel", "glushitil", "pryamotok", "vixlop"],
    "podshipnik":   ["podshipnik", "podshibnik", "stupitsa", "stupica"],
    "ressor":       ["ressor", "pruzhina", "padushka"],
    "gaz_ballon":   ["ballon", "propan", "metan", "gaz ballon", "ustanovka",
                     "ballonlar", "reduktor"],
    # 2026-07-30: LUGAT-TOLDIR.bat ma'lumotdan topgan haqiqiy qismlar.
    # Men o'ylab topmadim — e'lonlar ko'rsatdi.
    "bagaj":        ["bagaj", "bagajnik", "bagaz", "bagajnigi", "kryshka bagajnika"],
    "kuzov":        ["kuzov", "kuzav", "kuzovnoy", "kuzovnaya", "kuzovnie detali"],
    "bort":         ["bort", "borti", "bortlar", "bortovoy"],
    "rama":         ["rama", "ramasi", "shassi"],
    "most":         ["most", "mosti", "zadniy most", "reduktor most"],
    "injektor":     ["injektor", "inzektor", "forsunka", "forsunki"],
    "blok":         ["blok", "blok upravleniya", "blok tsilindrov", "eb blok"],
    "bakavoy":      ["bakavoy", "bokovoy", "bokoviy", "yon panel"],
    "spidometr":    ["spidometr", "spedometr", "panel pribor", "shchitok"],
    "ftulka":       ["ftulka", "vtulka", "vtulki", "saylentblok"],
    "podushka":     ["podushka", "padushka", "podushka motor", "opora dvigatel"],
    "deska":        ["deska", "doska", "torpedo", "torpeda"],
    # 2026-07-30, ikkinchi bosqich — ma'lumot topgan qismlar
    "kabina":       ["kabina", "kabinasi", "kabin"],
    "richag":       ["richag", "rishak", "richak", "rychag", "rychagi"],
    "krishka":      ["krishka", "krыshka", "kryshka", "qopqoq"],
    "sidenie":      ["sidenie", "sidenya", "sidenlar", "kreslo", "o'rindiq"],
    "zaslonka":     ["zaslonka", "drossel", "drosel"],
    "katalizator":  ["katalizator", "katalizatr", "katalizator"],
    "trambler":     ["trambler", "tramblyor", "tramblor", "raspredelitel"],
    "tent":         ["tent", "tenti", "chodir"],
    "silindr":      ["silindr", "tsilindr", "cilindr", "glavniy tormoznoy"],
    "remen":        ["remen", "remin", "ryemen", "rolik", "natyajnoy rolik"],
    "furgon":       ["furgon", "fura", "budka", "kuzov furgon"],
}


def _teskari(lug: dict[str, list[str]]) -> dict[str, str]:
    """{'nexia': [...]} -> {'neksiya': 'nexia', ...} (normallashtirilgan)"""
    t: dict[str, str] = {}
    for kalit, variantlar in lug.items():
        t[normalla(kalit)] = kalit
        for v in variantlar:
            t[normalla(v)] = kalit
    return t


MODEL_INDEKS = _teskari(MODELLAR)
QISM_INDEKS = _teskari(QISMLAR)


# ── O'XSHASHLIK BO'YICHA MOSLASHTIRISH (fuzzy) ──────────────────────────────
# 2026-07-30 sinovda aniqlandi: qo'lda yozilgan variantlar YETMAYDI.
# Bozorda "Ковальт", "Qoblt", "Koblt", "экюнокс", "Nexi" kabi cheksiz xato
# yozilishlar bor. Ularni sanab chiqib bo'lmaydi — o'xshashlik bilan
# taqqoslash kerak.
# O'LCHOV: NECHTA HARF FARQ QILADI (tahrir masofasi), foiz emas.
#
# 2026-07-30 da ikki xil xato ketma-ket chiqdi va sabab bitta edi —
# noto'g'ri o'lchov. Foizli o'xshashlik bu ikkisini ajrata olmaydi:
#   koblt  -> kobalt   bitta harf TUSHIB QOLGAN     = imlo xatosi   (kerak)
#   gelivi -> geli     ikkita harf QO'SHILGAN       = boshqa so'z   (kerak emas)
# Ikkalasi ham ~0.80 o'xshashlik beradi. Tahrir masofasi esa aniq ajratadi:
# birinchisida 1 ta farq, ikkinchisida 2 ta.
#
# Ruxsat: 8 harfgacha 1 ta farq, 9+ harfda 2 ta.
# (2026-07-30: 7 harfda 2 ta farqqa ruxsat bergandim — "galofka" (chiroq
# lampasi) "kalodka" deb tanildi. Ikki farq juda erkin ekan.)
def _ruxsat(n: int) -> int:
    return 1 if n <= 8 else 2


def _masofa(a: str, b: str, chek: int) -> int:
    """Tahrir masofasi (Levenshtein). `chek`dan oshsa erta to'xtaydi."""
    if abs(len(a) - len(b)) > chek:
        return chek + 1
    oldingi = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        joriy = [i]
        eng_kichik = i
        for j, cb in enumerate(b, 1):
            narx = min(oldingi[j] + 1,          # o'chirish
                       joriy[j - 1] + 1,        # qo'shish
                       oldingi[j - 1] + (ca != cb))   # almashtirish
            joriy.append(narx)
            eng_kichik = min(eng_kichik, narx)
        if eng_kichik > chek:                    # bu qatorda umid yo'q
            return chek + 1
        oldingi = joriy
    return oldingi[-1]


_MIN_UZUNLIK = 4           # qisqa so'zlarda taqqoslash yolg'on natija beradi

# ── FAQAT ANIQ YOZILGANDA TANILADIGAN VARIANTLAR ─────────────────────
#
# 2026-08-10 o'lchov. `bamper` qidiruvida motor moyi va shlagbaum
# chiqardi. Sabab noaniq moslikda emas — chegaramiz allaqachon qattiq
# (8 harfgacha atigi 1 farq). Sabab AYNAN IKKI VARIANTDA:
#
#     super  ->  buper    1 harf farq
#     bufet  ->  bufer    1 harf farq
#
# `bufer` va `buper` — haqiqiy imlolar (буфер). Lekin ikkalasi ham
# o'zbek e'lonlarida eng ko'p uchraydigan ikki so'zga bir harf qolgan:
# "super" (SUPER NARX, супер цена — har qadamda) va "bufet" (oshxona
# bufeti — mebelda).
#
# Bunday variantni noaniq moslikdan chiqaramiz. Aniq yozilsa —
# topiladi; taxmin qilinmaydi. Yo'qotish kichik: bu imlolar kam
# uchraydi. Yutuq katta: minglab yolg'on moslik yo'qoladi.
#
# Yangi variant qo'shayotganda o'ylang: u keng tarqalgan boshqa so'zga
# bir harf qolganmi? Qolgan bo'lsa shu ro'yxatga qo'shing.
FUZZYSIZ = frozenset({
    "bufer",   # ~ bufet (oshxona bufeti)
    "buper",   # ~ super (SUPER NARX)
})


# XATO EDI: birinchi harf bo'yicha guruhlagandim — lekin xato ko'pincha
# AYNAN birinchi harfda bo'ladi ("Qoblt" / "kobalt"). Endi uzunlik bo'yicha
# filtrlaymiz va keshlaymiz — bu tezlik uchun yetarli.
def _royxat(indeks: dict[str, str]) -> dict[int, list[tuple[str, str]]]:
    """Fuzzy variantlarni uzunligi bo‘yicha kichik savatlarga ajratadi.

    `FUZZYSIZ` dagilar bu yerga TUSHMAYDI — ular faqat aniq moslikda
    ishlaydi. Aniq moslik alohida yo'l bilan, indeksdan to'g'ridan-to'g'ri
    tekshiriladi, shuning uchun ular yo'qolib qolmaydi.
    """
    natija: dict[int, list[tuple[str, str]]] = {}
    for variant, kalit in indeks.items():
        if len(variant) >= _MIN_UZUNLIK and variant not in FUZZYSIZ:
            natija.setdefault(len(variant), []).append((variant, kalit))
    return natija


_MODEL_ROYXAT = _royxat(MODEL_INDEKS)
_QISM_ROYXAT = _royxat(QISM_INDEKS)
_KESH: dict[tuple[str, bool], str | None] = {}


def _oxshashini_top(soz: str, royxat: dict[int, list[tuple[str, str]]],
                    model: bool) -> str | None:
    """So'zga eng o'xshash lug'at yozuvini topadi (yoki None)."""
    kalit_kesh = (soz, model)
    if kalit_kesh in _KESH:
        return _KESH[kalit_kesh]

    natija = None
    if len(soz) >= _MIN_UZUNLIK:
        eng_yaqin = 99
        variantlar = []
        for uzunlik in range(max(_MIN_UZUNLIK, len(soz) - 2), len(soz) + 3):
            variantlar.extend(royxat.get(uzunlik, ()))
        for variant, kalit in variantlar:
            # JUDA QISQA yozuvlar uchun taxminiy moslik XAVFLI.
            # "geely" normallashgach "geli" (4 harf) bo'ladi va "gelvi"
            # (gel akkumulyator) undan atigi 1 harf farq qiladi.
            # Bunday qisqa nomlar aniq yozilishi kerak.
            if len(variant) <= 4:
                continue
            if abs(len(variant) - len(soz)) > _ruxsat(min(len(soz), len(variant))):
                continue
            # Ruxsat qisqa so'z bo'yicha olinadi — u qat'iyroq
            chek = _ruxsat(min(len(soz), len(variant)))
            m = _masofa(soz, variant, chek)
            if m <= chek and m < eng_yaqin:
                eng_yaqin, natija = m, kalit
                if m == 0:
                    break
    _KESH[kalit_kesh] = natija
    return natija


# O'zbek va rus tilida so'zga qo'shimcha qo'shiladi: fara -> farasi,
# eshik -> eshiklar, zapchast -> zapchastlari. Har shaklni lug'atга yozish
# cheksiz ish. Buning o'rniga qo'shimchani tanib, o'zagini taqqoslaymiz.
_QOSHIMCHA = (
    "lari", "lars", "lar", "ning", "dan", "ga", "da", "ni", "si", "i", "ii",
    "im", "iz", "asi", "sini", "larini", "lardan", "niki",
    "ы", "и",           # ruscha ko'plik (lotinlashgach: i)
    "ie", "oy", "iy", "ni", "nie", "noy",
)


def ozak(soz: str) -> list[str]:
    """So'zning bo'lishi mumkin bo'lgan o'zaklari (qo'shimchasiz).

    Eng qisqa o'zak 3 harf — "fari" (ruscha "фары") -> "far" shundan chiqadi.
    O'zbekchada undosh yumshaydi ham: eshik -> eshigi, shuning uchun
    oxirgi g/b/d ni k/p/t ga qaytarib ham sinaymiz."""
    natija = [soz]
    for q in _QOSHIMCHA:
        if len(soz) - len(q) >= 3 and soz.endswith(q):
            oz = soz[: -len(q)]
            natija.append(oz)
            # undosh yumshashi: eshig -> eshik, kitob -> kitop
            if oz and oz[-1] in "gbd":
                natija.append(oz[:-1] + {"g": "k", "b": "p", "d": "t"}[oz[-1]])
    return natija


_ozak = ozak          # ichki nom (eski chaqiruvlar uchun)


def _topish(matn: str, indeks: dict,
            royxat: dict[int, list[tuple[str, str]]], model: bool) -> set[str]:
    n = normalla(matn)
    topildi = set()
    sozlar = n.split()

    # 1) Aniq moslik: har variant uchun regex yuritmaymiz. Matndagi qisqa
    # n-gramlarni indeksdan to‘g‘ridan-to‘g‘ri topish ko‘p marta tezroq.
    for uzunlik in range(1, min(4, len(sozlar)) + 1):
        for i in range(len(sozlar) - uzunlik + 1):
            variant = " ".join(sozlar[i:i + uzunlik])
            if variant in indeks:
                topildi.add(indeks[variant])

    for soz in sozlar:
        if soz in indeks:
            continue

        # 2) Qo'shimchali shakl: "farasi" -> "fara", "eshiklar" -> "eshik"
        topildi_qoshimcha = False
        for oz in _ozak(soz)[1:]:            # birinchisi so'zning o'zi
            if oz in indeks:
                topildi.add(indeks[oz])
                topildi_qoshimcha = True
                break
        if topildi_qoshimcha:
            continue

        # 3) Imlo xatosi: o'xshashlik bo'yicha
        k = _oxshashini_top(soz, royxat, model)
        if k:
            topildi.add(k)

    return topildi


def modellarni_top(matn: str) -> set[str]:
    """Matndan mashina modellarini ajratadi (xato yozilgan bo'lsa ham)."""
    return _topish(matn, MODEL_INDEKS, _MODEL_ROYXAT, True)


def qismlarni_top(matn: str) -> set[str]:
    """Matndan ehtiyot qism turlarini ajratadi (xato yozilgan bo'lsa ham)."""
    return _topish(matn, QISM_INDEKS, _QISM_ROYXAT, False)
