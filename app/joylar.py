"""
OBER — JOY LUG'ATI (O'zbekiston geografiyasi)

MUAMMO (2026-07-30, Aziz ko'rsatdi): joy ro'yxati aralash chiqardi —
"Риштан", "Коканд", "Чиланзарский район". Ma'lumot OLX'dan ruscha keladi,
biz esa uni qanday kelsa shunday ko'rsatardik. Natijada bitta ro'yxatda
kirill, lotin va ruscha nomlar aralashib ketdi va ro'yxat juda uzun edi.

YECHIM: bu yerda O'zbekistonning O'ZI TO'G'RI yozilgan geografiyasi turadi.
OLX'dan kelgan har qanday yozuv shu yerga solishtiriladi va TOZA
o'zbekcha nomga aylantiriladi. Ro'yxat ma'lumotdan emas, SHU FAYLDAN
tuziladi — shuning uchun u har doim toza va bir xil.

Tuzilma: viloyat -> shahar/tuman. Har biriga ruscha variantlari yozilgan,
chunki tanish faqat shu orqali bo'ladi.
"""

from __future__ import annotations

# ── Viloyat -> [(o'zbekcha nom, ruscha variantlari...)] ─────────────────────
# Ruscha variantda "-ский район" yozilmaydi: u avtomatik olib tashlanadi.
GEO: dict[str, list[tuple[str, ...]]] = {
    "Toshkent shahri": [
        ("Bektemir", "бектемир"),
        ("Chilonzor", "чиланзар"),
        ("Mirobod", "мирабад"),
        ("Mirzo Ulug'bek", "мирзо-улугбек", "мирзо улугбек"),
        ("Olmazor", "алмазар"),
        ("Sergeli", "сергели"),
        ("Shayxontohur", "шайхантахур", "шайхантаур"),
        ("Uchtepa", "учтепа", "учтепинск"),
        ("Yakkasaroy", "яккасарай"),
        ("Yangihayot", "янгихаёт", "янгихает"),
        ("Yashnobod", "яшнабад"),
        ("Yunusobod", "юнусабад"),
    ],
    "Toshkent viloyati": [
        ("Angren", "ангрен"),
        ("Bekobod", "бекабад"),
        ("Bo'ka", "бука", "букинск"),
        ("Bo'stonliq", "бостанлык", "бостанлик"),
        ("Chinoz", "чиназ"),
        ("Chirchiq", "чирчик"),
        ("Nurafshon", "нурафшан", "нурафшон"),
        ("Ohangaron", "ахангаран"),
        ("Olmaliq", "алмалык", "алмалик"),
        ("Parkent", "паркент"),
        ("Piskent", "пскент"),
        ("Qibray", "кибрай"),
        ("Quyi Chirchiq", "куйичирчик", "куйи чирчик"),
        ("O'rta Chirchiq", "урта чирчик", "уртачирчик"),
        ("Yuqori Chirchiq", "юкоричирчик", "юкори чирчик"),
        ("Yangiyo'l", "янгиюль", "янгийул"),
        ("Zangiota", "зангиата", "зангиота"),
        ("Oqqo'rg'on", "аккурган"),
        ("Toshkent tumani", "ташкентский"),
    ],
    "Samarqand": [
        ("Samarqand", "самарканд"),
        ("Kattaqo'rg'on", "каттакурган"),
        ("Urgut", "ургут"),
        ("Bulung'ur", "булунгур"),
        ("Ishtixon", "иштыхан", "иштихан"),
        ("Jomboy", "джамбай", "жомбой"),
        ("Payariq", "пайарык", "паярык"),
        ("Nurobod", "нурабад"),
        ("Oqdaryo", "акдарья"),
        ("Past Darg'om", "пастдаргом", "паст даргом"),
        ("Toyloq", "тайлак"),
        ("Narpay", "нарпай"),
    ],
    "Buxoro": [
        ("Buxoro", "бухара"),
        ("Kogon", "каган"),
        ("G'ijduvon", "гиждуван"),
        ("Vobkent", "вабкент"),
        ("Romitan", "ромитан"),
        ("Shofirkon", "шафиркан"),
        ("Olot", "алат"),
        ("Qorako'l", "каракуль"),
        ("Jondor", "жондор", "джандар"),
        ("Peshku", "пешку"),
        ("Qorovulbozor", "караулбазар"),
    ],
    "Farg'ona": [
        ("Farg'ona", "фергана"),
        ("Qo'qon", "коканд"),
        ("Marg'ilon", "маргилан"),
        ("Quvasoy", "кувасай"),
        ("Rishton", "риштан"),
        ("Quva", "кува"),
        ("Beshariq", "бешарык", "бешарик"),
        ("Bog'dod", "багдад"),
        ("Buvayda", "бувайда"),
        ("Dang'ara", "дангара"),
        ("Furqat", "фуркат"),
        ("Oltiariq", "алтыарык", "олтиарик"),
        ("So'x", "сох"),
        ("Toshloq", "ташлак"),
        ("Uchko'prik", "учкуприк"),
        ("Yozyovon", "язъяван", "языван"),
    ],
    "Andijon": [
        ("Andijon", "андижан"),
        ("Asaka", "асака"),
        ("Xonobod", "ханабад", "хонабад"),
        ("Shahrixon", "шахрихан"),
        ("Marhamat", "мархамат"),
        ("Paxtaobod", "пахтаабад"),
        ("Baliqchi", "балыкчи"),
        ("Bo'ston", "бустан"),
        ("Buloqboshi", "булакбаши"),
        ("Izboskan", "избаскан"),
        ("Jalaquduq", "джалакудук"),
        ("Qo'rg'ontepa", "кургантепа"),
        ("Oltinko'l", "алтынкуль"),
        ("Ulug'nor", "улугнор"),
    ],
    "Namangan": [
        ("Namangan", "наманган"),
        ("Chust", "чуст"),
        ("Chortoq", "чартак"),
        ("Kosonsoy", "касансай", "косонсой"),
        ("Pop", "пап"),
        ("To'raqo'rg'on", "туракурган"),
        ("Uchqo'rg'on", "учкурган"),
        ("Uychi", "уйчи"),
        ("Yangiqo'rg'on", "янгикурган"),
        ("Mingbuloq", "мингбулак"),
        ("Norin", "нарын", "норин"),
    ],
    "Qashqadaryo": [
        ("Qarshi", "карши"),
        ("Shahrisabz", "шахрисабз"),
        ("Kitob", "китаб"),
        ("Yakkabog'", "яккабаг"),
        ("G'uzor", "гузар"),
        ("Koson", "касан", "косон"),
        ("Kamashi", "камаши"),
        ("Muborak", "мубарек"),
        ("Chiroqchi", "чиракчи"),
        ("Dehqonobod", "дехканабад"),
        ("Kasbi", "касби"),
        ("Mirishkor", "миришкор"),
        ("Nishon", "нишан"),
    ],
    "Surxondaryo": [
        ("Termiz", "термез"),
        ("Denov", "денау"),
        ("Sherobod", "шерабад"),
        ("Boysun", "байсун"),
        ("Sariosiyo", "сариасия"),
        ("Jarqo'rg'on", "джаркурган"),
        ("Qumqo'rg'on", "кумкурган"),
        ("Sho'rchi", "шурчи"),
        ("Angor", "ангор"),
        ("Muzrabot", "музрабад"),
        ("Oltinsoy", "алтынсай"),
        ("Bandixon", "бандихан"),
        ("Qiziriq", "кизирик"),
        ("Uzun", "узун"),
    ],
    "Xorazm": [
        ("Urganch", "ургенч"),
        ("Xiva", "хива"),
        ("Xazorasp", "хазарасп"),
        ("Gurlan", "гурлен"),
        ("Pitnak", "питнак"),
        ("Shovot", "шават"),
        ("Bog'ot", "багат"),
        ("Qo'shko'pir", "кошкупыр"),
        ("Yangiariq", "янгиарык"),
        ("Yangibozor", "янгибазар"),
        ("Xonqa", "ханка"),
    ],
    "Navoiy": [
        ("Navoiy", "навои"),
        ("Zarafshon", "зарафшан"),
        ("Uchquduq", "учкудук"),
        ("Karmana", "кармана"),
        ("Qiziltepa", "кызылтепа"),
        ("Nurota", "нурата"),
        ("Xatirchi", "хатырчи"),
        ("Konimex", "канимех"),
        ("Tomdi", "тамды"),
    ],
    "Jizzax": [
        ("Jizzax", "джизак"),
        ("G'allaorol", "галляарал"),
        ("Zomin", "заамин"),
        ("Do'stlik", "дустлик"),
        ("Paxtakor", "пахтакор"),
        ("Baxmal", "бахмаль"),
        ("Sharof Rashidov", "шараф рашидов"),
        ("Mirzacho'l", "мирзачуль"),
        ("Yangiobod", "янгиабад"),
        ("Forish", "фариш"),
        ("Zafarobod", "зафарабад"),
    ],
    "Sirdaryo": [
        ("Guliston", "гулистан"),
        ("Yangiyer", "янгиер"),
        ("Shirin", "ширин"),
        ("Sirdaryo", "сырдарья"),
        ("Boyovut", "баяут"),
        ("Sayxunobod", "сайхунабад"),
        ("Oqoltin", "акалтын"),
        ("Mirzaobod", "мирзаабад"),
        ("Xovos", "хаваст"),
    ],
    "Qoraqalpog'iston": [
        ("Nukus", "нукус"),
        ("Xo'jayli", "ходжейли"),
        ("Chimboy", "чимбай"),
        ("To'rtko'l", "турткуль"),
        ("Beruniy", "беруни"),
        ("Qo'ng'irot", "кунград"),
        ("Mo'ynoq", "муйнак"),
        ("Amudaryo", "амударья"),
        ("Ellikqal'a", "элликкала"),
        ("Kegeyli", "кегейли"),
        ("Qanliko'l", "канлыкуль"),
        ("Shumanay", "шуманай"),
        ("Taxtako'pir", "тахтакупыр"),
        ("Taxiatosh", "тахиаташ"),
    ],
}

# Viloyatning o'zi ham tanilishi kerak ("Ташкент" -> Toshkent shahri)
VILOYAT_RU: dict[str, tuple[str, ...]] = {
    "Toshkent shahri": ("ташкент", "тошкент", "toshkent"),
    "Toshkent viloyati": ("ташкентская область", "ташкентская"),
    "Samarqand": ("самарканд", "самаркандская"),
    "Buxoro": ("бухара", "бухарская"),
    "Farg'ona": ("фергана", "ферганская"),
    "Andijon": ("андижан", "андижанская"),
    "Namangan": ("наманган", "наманганская"),
    "Qashqadaryo": ("кашкадарья", "кашкадарьинская"),
    "Surxondaryo": ("сурхандарья", "сурхандарьинская"),
    "Xorazm": ("хорезм", "хорезмская"),
    "Navoiy": ("навои", "навоийская"),
    "Jizzax": ("джизак", "джизакская"),
    "Sirdaryo": ("сырдарья", "сырдарьинская"),
    "Qoraqalpog'iston": ("каракалпакстан", "каракалпакия"),
}

# ── Tanish jadvali ──────────────────────────────────────────────────────────
_OLIB_TASHLANADI = (
    "ский район", "ская область", "ский р-н", " район", " р-н", " область",
    " туман", " tumani", " shahri", " viloyati", " tuman",
)


def _kalit(matn: str) -> str:
    """Solishtirish uchun sodda ko'rinish."""
    s = (matn or "").strip().lower().replace("ё", "е")
    for q in _OLIB_TASHLANADI:
        if s.endswith(q):
            s = s[: -len(q)]
            break
    return (s.replace("'", "").replace("`", "").replace("’", "")
             .replace("-", " ").replace("ъ", "").strip())


def _jadval() -> tuple[dict, dict]:
    """joy_kaliti -> (viloyat, joy_nomi)   va   viloyat_kaliti -> viloyat."""
    joy, vil = {}, {}
    for v, royxat in GEO.items():
        vil[_kalit(v)] = v
        for ru in VILOYAT_RU.get(v, ()):
            vil[_kalit(ru)] = v
        for yozuv in royxat:
            uz = yozuv[0]
            for nom in yozuv:
                joy[_kalit(nom)] = (v, uz)
    return joy, vil


_JOY, _VIL = _jadval()


def tani(shahar: str = "", tuman: str = "", viloyat: str = "") -> tuple[str, str]:
    """OLX yozuvidan (viloyat, joy) toza o'zbekcha nomlarni qaytaradi.

    Topilmasa joy bo'sh qoladi — o'ylab topmaymiz, aralash ro'yxat
    aynan shundan paydo bo'lgan edi."""
    for x in (tuman, shahar):
        t = _JOY.get(_kalit(x))
        if t:
            return t
    v = _VIL.get(_kalit(viloyat)) or _VIL.get(_kalit(shahar)) or ""
    return (v, "")


def daraxt() -> list[dict]:
    """Tanlov uchun tayyor ro'yxat — ma'lumotdan emas, shu fayldan."""
    return [{"viloyat": v, "joylar": [y[0] for y in royxat]}
            for v, royxat in GEO.items()]


def moslikmi(tanlangan: str, viloyat: str, joy: str) -> bool:
    """Tanlangan joy shu e'longa mos keladimi (viloyat ham, tuman ham).

    DIQQAT: viloyat nomlari _kalit() bilan solishtirilmaydi. Sabab —
    _kalit " shahri" va " viloyati" qo'shimchasini olib tashlaydi va
    "Toshkent shahri" bilan "Toshkent viloyati" bir xil bo'lib qoladi.
    Bu ikkisi esa butunlay boshqa joy."""
    if not tanlangan:
        return True
    t = tanlangan.strip().lower()
    return t == (viloyat or "").strip().lower() or _kalit(tanlangan) == _kalit(joy)
