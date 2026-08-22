"""OBER — MCP serveri. `qidir` · `sorov_yubor` · `javoblar`.

NIMA BU
-------
AI agent (ChatGPT, Claude, Gemini) O'zbekiston bozoridan to'g'ridan-
to'g'ri qidira oladigan kirish nuqtasi.

Bugun kimdir agentdan "Toshkentdan 3 mln gacha divan top" desa —
javob yo'q. OLX'da agent interfeysi yo'q, Uzum CAPTCHA qo'yadi.
Bu fayl o'sha bo'shliqni yopadi. Sabab va reja: `AGENT-REJA.md`.

NISHA — HECH KIMDA YO'Q NARSA
-----------------------------
ACP (OpenAI+Stripe) ham, UCP (Google) ham faqat MAVJUD tovarni
sotadi. OBERda boshqasi: agent tovar topmasa, uni sotuvchilardan
SO'RAY oladi (`sorov_yubor`). Agentdan boshlanib jonli sotuvchiga
boradigan so'rov zanjiri — boshqa joyda yo'q.

TEXNIKA
-------
MCP — JSON-RPC 2.0, stdin/stdout orqali, har xabar bitta qatorda.
Kutubxona SHART EMAS, shuning uchun `pip install` yo'q — CLAUDE.md
qoidasi saqlanadi.

Server HTTP orqali emas, `qidiruv.qidir()` va `baza` ni TO'G'RIDAN
chaqiradi. Ya'ni tarmoq yo'q, javob millisekundlarda.

CHEGARA — BUZILMAYDI
--------------------
Agent SO'ROV QO'YADI va JAVOBLARNI O'QIYDI. Tanlash, savdolashish
va kelishuv — odamning ishi. Agent sotuvchiga javob yoza olmaydi:
bunday vosita YO'Q va qo'shilmaydi. OBER to'lov qilmaydi, va odam
nomidan majburiyat olish noto'g'ri.

TALAB YARATADIGAN VOSITA FAQAT BITTA — `sorov_yubor`. U hech narsa
o'chirmaydi, hech kimga pul o'tkazmaydi. `javoblar` yangi talab
yaratmaydi; u faqat ALLAQACHON RUXSAT BERILGAN tarqatishning
keyingi to'lqinini ochadi (sabab `javoblar_vosita` izohida).

MANBA — QAYSI BAZAGA GAPIRADI (2026-08-17)
------------------------------------------
Ikki rejim bor va ikkalasi ham kerak:

  HTTP (standart)  `OBER_API=https://ober.uz`
      Vositalar sayt API'siga boradi. Talab HAQIQIY sotuvchilarga
      yetadi, indeks to'liq va yangi.

  MAHALLIY         `OBER_API=` (bo'sh)
      `baza` va `qidiruv` to'g'ridan chaqiriladi. Tarmoq yo'q,
      javob millisekundlarda. Sinov (`mcp_sinov.py`) shu rejimda.

NEGA STANDART HTTP (2026-08-17 da o'lchandi). Ishchi kompyuterdagi
`data/ober.db` — production EMAS: 126 873 e'lon (saytda 523 000+),
13 sotuvchi, eng yangi e'lon 3 kun eski. Mahalliy rejimda
`sorov_yubor` o'sha nusxaga yozadi va ober.uz dagi sotuvchilar
hech narsa ko'rmaydi. Ya'ni zanjir sinovda ishlab, hayotda uzilgan
bo'lardi — eng yomon turdagi xato, chunki u jimgina.

ISHLATISH
---------
    python app/mcp_server.py

Klient sozlamasi (Claude Desktop / Cowork):
    {"command": "python", "args": ["D:/OBER/app/mcp_server.py"]}

Mahalliy baza bilan sinash uchun `env` ga `OBER_API` ni bo'sh qo'ying.
"""

from __future__ import annotations

import json
import os
import sys
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request

PROTOKOL = "2024-11-05"
NOM = "ober"
VERSIYA = "0.3.0"

# Bir so'rovda qaytariladigan eng ko'p natija. Agent kontekstini
# to'ldirib yubormaslik uchun ataylab kichik — agent kerak bo'lsa
# aniqroq so'rov beradi.
ENG_KOP = 20

# Talab 24 soat ochiq turadi (`baza.SOROV_MUDDATI`). Bu yerda faqat
# agentga aytish uchun — haqiqiy qiymat bazada.
MUDDAT_SOAT = 24

# TEZLIK CHEKLOVI — bitta agent butun sotuvchi bazasini spamlamasin.
#
# Sayt tomonida `/api/sorov` da soatiga 60 ta chegara bor
# (server.py `_TEZLIK_QOIDA`), lekin MCP HTTP orqali o'tmaydi — u
# `baza` ni to'g'ridan chaqiradi. Ya'ni o'sha chegara BU YERDA
# ISHLAMAYDI va qaytadan qo'yilishi shart.
#
# Sayt chegarasi butun IP uchun (bir uydagi hamma odam). Bu yerda
# esa bitta agent seansi — shuning uchun qattiqroq.
YOZISH_SOATIGA = 10
YOZISH_DAQIQADA = 3

# Bir xil talab ikki marta yozilmasin. Agent qayta urinsa (tarmoq
# uzildi, javob kech keldi) sotuvchiga bir xil xabar ikki marta
# bormaydi.
NUSXA_OYNASI = 3600


# ── MANBA: HTTP yoki mahalliy ────────────────────────────────────────

# `OBER_API` berilmagan bo'lsa — sayt. Bo'sh satr berilsa — mahalliy
# baza. Ya'ni "unutib qoldirish" xavfsiz tomonga tushadi: standart
# holatda talab haqiqiy sotuvchilarga boradi.
ODATIY_API = "https://ober.uz"
API = os.environ.get("OBER_API", ODATIY_API).strip().rstrip("/")

# Sayt qidiruvi 4+ so'zli so'rovda ~200 ms, tarmoq bilan ~1 s.
# 20 soniya — sayt qayta yuklanayotgan paytga ham yetadi.
KUTISH = 20


class ApiXato(Exception):
    """Sayt bilan gaplashishda muammo — agentga matn bo'lib qaytadi."""


def _api(yol: str, tana: dict | None = None, **parametr) -> dict:
    """Sayt API'si. `tana` berilsa POST, aks holda GET."""
    manzil = API + yol
    if parametr:
        toza = {k: v for k, v in parametr.items() if v not in (None, "", 0)}
        if toza:
            manzil += "?" + urllib.parse.urlencode(toza)
    ma_lumot = None
    sarlavha = {"Accept": "application/json",
                # Kim kelayotgani jurnalda ko'rinsin — sayt tomonida
                # agent trafigini oddiy odamdan ajratish uchun.
                "User-Agent": f"ober-mcp/{VERSIYA}"}
    if tana is not None:
        ma_lumot = json.dumps(tana, ensure_ascii=False).encode()
        sarlavha["Content-Type"] = "application/json"
    so_rov = urllib.request.Request(manzil, data=ma_lumot,
                                    headers=sarlavha)
    try:
        with urllib.request.urlopen(so_rov, timeout=KUTISH) as j:
            return json.loads(j.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as x:
        # Sayt o'z xatosini JSON'da tushuntiradi — uni yo'qotmaymiz.
        try:
            d = json.loads(x.read().decode("utf-8") or "{}")
        except Exception:                            # noqa: BLE001
            d = {}
        izoh = d.get("xato") or x.reason
        if x.code == 429:
            raise ApiXato("Sayt tezlik chegarasi: biroz kuting.") from x
        raise ApiXato(f"ober.uz {x.code}: {izoh}") from x
    except urllib.error.URLError as x:
        raise ApiXato(f"ober.uz ga ulanib bo'lmadi: {x.reason}") from x
    except TimeoutError as x:
        raise ApiXato(f"ober.uz {KUTISH} soniyada javob bermadi.") from x


def _qidir_xom(sorov: str, viloyat: str, narx_gacha: int) -> dict:
    """Qidiruv natijasi — ikkala rejimda BIR XIL shaklda.

    `/api/qidir` `qidiruv.qidir()` javobini o'zgartirmasdan qaytaradi,
    ya'ni `_ishonchli` va `sozlar` ikkala yo'lda ham bor va ishonch
    chegarasi bir xil ishlaydi.
    """
    if API:
        return _api("/api/qidir", q=sorov, tuman=viloyat,
                    narx_gacha=narx_gacha)
    import qidiruv
    return qidiruv.qidir(sorov, viloyat, limit=ENG_KOP,
                         narx_gacha=narx_gacha)


def _ochiqmi(sorov: dict) -> bool:
    """Talab hali javob qabul qiladimi.

    Mahalliy rejimda `baza.sorov_ochiqmi` bor, HTTP'da yo'q — lekin
    ikkala yo'l ham `holat` va `yaratildi` ni qaytaradi, shuning uchun
    qoida bitta joyda yoziladi.
    """
    if (sorov.get("holat") or "") not in ("yangi", "yuborildi", "javob_bor"):
        return False
    yaratildi = float(sorov.get("yaratildi") or 0)
    return (time.time() - yaratildi) < MUDDAT_SOAT * 3600


# ── ISHONCH CHEGARASI ────────────────────────────────────────────────
#
# MUAMMO (2026-08-16 da o'lchangan, 2026-08-17 da qayta tasdiqlangan):
#
#     qidir("zzqqxx yoq narsa")  -> 181 ta begona e'lon
#     qidir("blorptak mashinasi") -> 154 ta begona e'lon
#     qidir("qwertyuiop")         -> 4 ta ("Qwertyuiopasdf12")
#
# Sabab: indeksda hech narsa aniq mos kelmasa `fts_erkin` "kamida
# bitta so'z" (OR) bosqichiga tushadi. "narsa" — haqiqiy o'zbekcha
# so'z, shuning uchun 181 ta e'lon topiladi.
#
# ODAM buni ko'rib "bu men so'raganim emas" deydi va o'zi filtrlaydi.
# AGENT esa buni haqiqiy javob deb foydalanuvchiga uzatadi. Ya'ni
# agentli savdo bu xatoni bir necha barobar jiddiylashtiradi — bu
# endi bezovtalik emas, YOLG'ON MA'LUMOT.
#
# QOIDA — yangi ballash yozilmaydi, `qidiruv.py` ning o'z belgilari
# o'qiladi. Ikkita shart:
#
#   1. `sozlar` bo'sh bo'lmasin. Bo'sh bo'lsa so'rovdan hech qanday
#      mazmunli so'z chiqmagan, lekin lug'at tasodifan model
#      tanigan bo'lishi mumkin. O'lchov: `qidir("zzz vvv yyy")` ->
#      1404 natija, chunki "vvv" lug'atda `volkswagen` ga bog'langan;
#      hammasi bir xil ball (68.7) oladi va `_ishonchli` YOLG'ONDAN
#      True bo'ladi (model yo'lida u standart qiymat).
#
#   2. Kamida bitta natijada `_ishonchli=True` bo'lsin. Bu bayroq
#      `qidiruv._yakunla` da qo'yiladi va "so'rovning HAMMA so'zi
#      sarlavhada ANIQ (prefiks emas) uchradi" degani. Aynan shu
#      erkin rejimdagi OR bosqichini kesadi.
#
# O'LCHOV (2026-08-17, jonli indeks — 500 000+ e'lon):
#
#   12 ta yolg'on so'rov  -> 12 tasi rad etildi, 0 ta xato qabul
#   24 ta haqiqiy so'rov  -> 21 tasi qabul qilindi
#
# Rad etilgan 3 ta "haqiqiy" so'rov tekshirildi va uchalasi ham
# TO'G'RI rad etilgan:
#
#   "usta santexnik"              -> indeksda santexnik yo'q
#                                    (1-natija: gaz balon o'rnatish)
#   "divan charm"                 -> divan bor, charm divan yo'q
#   "2 xonali kvartira chilonzor" -> yagona natija 4 xonali
#
# Uchalasi ham aynan `sorov_yubor` uchun tug'ilgan holat: indeksda
# yo'q — sotuvchidan so'raladi. Ya'ni chegara natijani kesmaydi,
# uni TO'G'RI YO'LGA burib yuboradi.

def _ishonchli_natijalar(javob: dict) -> list:
    """`qidir()` javobidan ishonsa bo'ladigan natijalar.

    Yangi mantiq yo'q — `qidiruv.py` qo'ygan belgilar o'qiladi.
    """
    if not javob.get("sozlar"):
        return []                    # mazmunli so'z chiqmadi
    return [x for x in (javob.get("natijalar") or []) if x.get("_ishonchli")]


VOSITALAR = [{
    "name": "qidir",
    "description": (
        "O'zbekiston bozoridan mahsulot qidiradi. OLX va ochiq Telegram "
        "kanallaridan yig'ilgan 500 000 dan ortiq e'lon indeksidan "
        "izlaydi (har 45 daqiqada yangilanadi). Erkin matn qabul "
        "qiladi — kategoriya tanlash shart emas. Masalan: "
        "'divan charm', 'nexia kolodka', '2 xonali kvartira Chilonzor'. "
        "Har natijada asl e'lon havolasi bo'ladi. "
        "MUHIM: aniq moslik topilmasa vosita BO'SH ro'yxat qaytaradi "
        "va `holat` maydonida buni aytadi — yaqin, lekin boshqa "
        "tovarlarni javob sifatida bermaydi. Shunday holatda "
        "`sorov_yubor` bilan talabni jonli sotuvchilarga yuborish "
        "mumkin. DIQQAT: OBER to'lov va yetkazib berishni bajarmaydi, "
        "faqat topadi va bog'laydi."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "sorov": {
                "type": "string",
                "description": "Nima qidirilyapti — erkin matn, "
                               "o'zbekcha yoki ruscha.",
            },
            "viloyat": {
                "type": "string",
                "description": "Ixtiyoriy. Masalan 'Toshkent shahri', "
                               "'Samarqand'. Bu QAT'IY FILTR EMAS — "
                               "shu joydagi e'lonlar yuqoriroq chiqadi, "
                               "lekin boshqa joydagilar ham qaytishi "
                               "mumkin. Har natijada `viloyat` bor.",
            },
            "narx_max": {
                "type": "integer",
                "description": "Ixtiyoriy. So'mda eng yuqori narx. "
                               "Narxi ko'rsatilmagan e'lonlar chiqmaydi.",
            },
            "soni": {
                "type": "integer",
                "description": f"Ixtiyoriy. Nechta natija (1-{ENG_KOP}).",
            },
        },
        "required": ["sorov"],
    },
}, {
    "name": "sorov_yubor",
    "description": (
        "Indeksda yo'q tovar yoki xizmatni JONLI SOTUVCHILARDAN "
        "so'raydi. OBER talabni mos sotuvchilarga tarqatadi, ular "
        "narx, muddat va rasm bilan javob beradi. "
        "QACHON: `qidir` `holat` maydonida 'aniq_moslik_yoq' yoki "
        "'topilmadi' qaytarganda, yoki foydalanuvchi ataylab "
        "sotuvchidan so'rashni istaganda. "
        "CHEGARA — BUZILMAYDI: bu vosita faqat SO'ROV QO'YADI. "
        "Javoblarni ODAM o'qiydi va o'zi tanlaydi. Agent sotuvchi "
        "bilan savdolashmaydi, narx kelishmaydi, buyurtmani "
        "yakunlamaydi va foydalanuvchi nomidan majburiyat olmaydi. "
        "`aloqa` — foydalanuvchining haqiqiy telefon raqami; uni "
        "FOYDALANUVCHIDAN SO'RANG, o'zingiz to'qimang. Raqamsiz "
        "so'rov yubormang."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "matn": {
                "type": "string",
                "description": "Nima kerakligi — foydalanuvchining o'z "
                               "so'zlari bilan. Masalan: 'charm divan, "
                               "3 o'rinli, Toshkent'. Sotuvchi aynan "
                               "shu matnni ko'radi.",
            },
            "aloqa": {
                "type": "string",
                "description": "Foydalanuvchining telefon raqami "
                               "(998XXXXXXXXX yoki XXXXXXXXX). "
                               "FOYDALANUVCHIDAN so'ralsin — "
                               "to'qib yozilmasin.",
            },
            "tuman": {
                "type": "string",
                "description": "Ixtiyoriy. Joy — shu yerdagi "
                               "sotuvchilar oldin xabar oladi.",
            },
            "byudjet": {
                "type": "integer",
                "description": "Ixtiyoriy. So'mda. Sotuvchi javob "
                               "berishdan oldin narxni biladi.",
            },
            "ism": {
                "type": "string",
                "description": "Ixtiyoriy. Sotuvchi chatda "
                               "'Xaridor · Ism' deb ko'radi.",
            },
        },
        "required": ["matn", "aloqa"],
    },
}, {
    "name": "javoblar",
    "description": (
        "`sorov_yubor` bilan qo'yilgan talabning holatini ko'rsatadi: "
        "nechta sotuvchiga bordi, nechtasi javob berdi, narxlar "
        "qanday. Sotuvchi javobi ikki xil bo'ladi — `aynan` (aynan "
        "shu tovar bor) va `oxshash` (o'xshashi bor). Bu ikkisini "
        "ARALASHTIRMANG: `oxshash` javobni 'topildi' deb aytish "
        "foydalanuvchini chalg'itadi. "
        "CHEGARA: agent javoblarni faqat O'QIYDI va odamga aytadi. "
        "Tanlash, savdolashish va kelishuv — odamning ishi, u "
        "`kuzatish` havolasi orqali OBER chatida qiladi. Sotuvchiga "
        "javob yozadigan vosita yo'q."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "kalit": {
                "type": "string",
                "description": "`sorov_yubor` qaytargan `kuzatish` "
                               "havolasi yoki undagi kalit. Raqamli "
                               "ID ishlamaydi — begona odamning "
                               "takliflari ochilib qolmasin.",
            },
        },
        "required": ["kalit"],
    },
}]


def _son(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


# ── `qidir` ──────────────────────────────────────────────────────────

def qidir_vosita(arg: dict) -> dict:
    sorov = str(arg.get("sorov") or "").strip()
    if not sorov:
        return {"xato": "`sorov` bo'sh — nima qidirilishini yozing."}

    soni = _son(arg.get("soni")) or 10
    soni = max(1, min(ENG_KOP, soni))
    narx_max = _son(arg.get("narx_max")) or 0
    viloyat = str(arg.get("viloyat") or "").strip()

    # Narx chegarasi `qidir` ning O'ZIGA beriladi, natijadan keyin
    # kesilmaydi: ichkarida u ballashdan oldin qo'llanadi, ya'ni
    # chegaraga sig'adigan e'lonlar TOP dan tushib qolmaydi.
    #
    # `limit` har doim ENG_KOP: ishonch chegarasi natijani kesadi,
    # shuning uchun `soni` ta so'ralganda `soni` ta ballangan e'lon
    # olish yetmaydi — ishonchlisi pastroqda qolib ketishi mumkin.
    try:
        javob = _qidir_xom(sorov, viloyat, narx_max)
    except ApiXato as x:
        return {"xato": str(x)}

    ishonchli = _ishonchli_natijalar(javob)

    # NARX SABABMI? Bo'sh natijada agentga "bunday tovar yo'q" deb
    # aytish YOLG'ON bo'lishi mumkin — tovar bor, faqat qimmatroq.
    # Shuning uchun narx chegarasi berilgan va natija bo'sh bo'lsa,
    # qidiruv narxsiz qayta yuriladi (~100-200 ms) va agentga
    # HAQIQIY eng arzon narx aytiladi.
    narx_sababmi = False
    eng_arzon = None
    if not ishonchli and narx_max:
        try:
            keng = _qidir_xom(sorov, viloyat, 0)
        except ApiXato:
            keng = {}
        keng_ishonchli = _ishonchli_natijalar(keng)
        if keng_ishonchli:
            narx_sababmi = True
            narxlar = [x["narx_som"] for x in keng_ishonchli
                       if x.get("narx_som")]
            eng_arzon = min(narxlar) if narxlar else None
            javob = keng

    chiqish = []
    for e in ishonchli[:soni]:
        # HAVOLA HAR DOIM BO'LISHI SHART (2026-08-16 birinchi sinovda
        # topildi). OBER'ning O'Z e'lonlarida `havola` bo'sh — ular
        # tashqi saytda emas, OBERning o'zida yashaydi. Agent bunday
        # yozuvni foydalanuvchiga bera olmaydi: "mana divan, lekin
        # qayerdaligini aytolmayman" degan javob foydasiz.
        havola = e.get("havola")
        if not havola and e.get("id"):
            havola = f"https://ober.uz/elon/{e['id']}"
        chiqish.append({
            "nom": e.get("nom"),
            "narx_som": e.get("narx_som"),
            "viloyat": e.get("viloyat"),
            "shahar": e.get("shahar"),
            "kategoriya": e.get("kategoriya"),
            "sana": e.get("sana"),
            "havola": havola,
            "manba": e.get("manba"),
        })

    if chiqish:
        return {
            "sorov": sorov,
            "holat": "topildi",
            "topildi": len(chiqish),
            "elonlar": chiqish,
            "izoh": ("Narxlar so'mda. Havola asl e'lonni ochadi. "
                     "To'lov va yetkazib berish OBER orqali "
                     "bajarilmaydi."),
        }

    # ── ANIQ MOSLIK YO'Q ──────────────────────────────────────────
    #
    # `elonlar` ATAYLAB bo'sh. Ballash bergan "yaqin" e'lonlar
    # javobga tushmaydi, chunki agent ularni haqiqiy topilma deb
    # uzatib yuboradi.
    #
    # `soralgani_emas` — faqat NOM. Narx yo'q, HAVOLA YO'Q. Havolasiz
    # e'lonni taklif sifatida ko'rsatib bo'lmaydi, lekin agent
    # foydalanuvchiga aniq gapira oladi: "OBER'da divan bor, charm
    # divan yo'q — sotuvchilardan so'raymi?"
    yaqin = [e.get("nom") for e in (javob.get("natijalar") or [])[:3]
             if e.get("nom")]

    if narx_sababmi:
        holat = "narx_boyicha_yoq"
    elif javob.get("jami"):
        holat = "aniq_moslik_yoq"
    else:
        holat = "topilmadi"

    if narx_sababmi:
        izoh = (f"«{sorov}» bor, lekin {narx_max} so'mgacha emas"
                + (f" — eng arzoni {eng_arzon} so'm." if eng_arzon
                   else ".")
                + " `sorov_yubor` bilan byudjetni aytib "
                  "sotuvchilardan so'rash mumkin: kimdir arzonroq "
                  "taklif qilishi mumkin.")
    elif holat == "aniq_moslik_yoq":
        izoh = (f"«{sorov}» indeksda ANIQ topilmadi. Yaqin, lekin "
                f"boshqa tovarlar bor — ular javob sifatida "
                f"berilmaydi. `sorov_yubor` bilan talabni jonli "
                f"sotuvchilarga yuborish mumkin; buning uchun "
                f"foydalanuvchidan telefon raqamini so'rang.")
    else:
        izoh = (f"«{sorov}» indeksda yo'q. `sorov_yubor` bilan "
                f"talabni jonli sotuvchilarga yuborish mumkin; "
                f"buning uchun foydalanuvchidan telefon raqamini "
                f"so'rang.")

    natija = {
        "sorov": sorov,
        "holat": holat,
        "topildi": 0,
        "elonlar": [],
        "keyingi_qadam": "sorov_yubor",
        "izoh": izoh,
    }
    if eng_arzon:
        natija["eng_arzon_som"] = eng_arzon
    if yaqin and not narx_sababmi:
        natija["soralgani_emas"] = yaqin
        natija["ogohlantirish"] = (
            "`soralgani_emas` — bu so'ralgan tovar EMAS, faqat "
            "indeksda nima borligini ko'rsatadi. Foydalanuvchiga "
            "topilma sifatida berilmasin.")
    # Qidiruv o'zi qisqaroq so'z taklif qilgan bo'lsa — foydali.
    if javob.get("taklif"):
        natija["qisqaroq_sorov"] = javob["taklif"]
    return natija


# ── `sorov_yubor` ────────────────────────────────────────────────────

_YOZISH_VAQTLARI: list = []          # oxirgi yozishlar (time.time())


def _tezlik_ok() -> str:
    """Chegaradan chiqilgan bo'lsa — sabab matni, aks holda "" ."""
    hozir = time.time()
    _YOZISH_VAQTLARI[:] = [t for t in _YOZISH_VAQTLARI if hozir - t < 3600]
    if len(_YOZISH_VAQTLARI) >= YOZISH_SOATIGA:
        return (f"Soatiga {YOZISH_SOATIGA} tadan ko'p so'rov "
                f"yuborilmaydi — sotuvchilar bezovta bo'lmasin.")
    daqiqada = sum(1 for t in _YOZISH_VAQTLARI if hozir - t < 60)
    if daqiqada >= YOZISH_DAQIQADA:
        return (f"Daqiqasiga {YOZISH_DAQIQADA} tadan ko'p so'rov "
                f"yuborilmaydi. Biroz kuting.")
    return ""


def _telefon_tozala(aloqa: str) -> str:
    """Raqamni bir xil shaklga keltiradi — server.py bilan bir xil.

    Sotuvchi ro'yxatdan o'tganda ham shu shakl ishlatiladi, ya'ni
    `baza._mos_sotuvchilar` dagi "o'zingga o'z so'roving kelmasin"
    tekshiruvi (oxirgi 9 raqam) to'g'ri ishlaydi.
    """
    raqam = "".join(ch for ch in (aloqa or "") if ch.isdigit())
    if len(raqam) == 9 and raqam.startswith("9"):
        return "998" + raqam
    if len(raqam) == 12 and raqam.startswith("998"):
        return raqam
    return raqam


# Yaqinda yozilgan talablar: (matn, aloqa) -> (vaqt, sorov_id, kalit).
# HTTP rejimida bazani so'rab bo'lmaydi, shuning uchun nusxa shu yerda
# ushlanadi. Jarayon qayta ishga tushsa yo'qoladi — lekin nusxa xavfi
# ham aynan bitta seans ichida: agent javobni kutmay qayta urinadi.
_YOZILGANLAR: dict = {}


def _nusxa_top(matn: str, aloqa: str):
    kalit = (matn, aloqa)
    yozuv = _YOZILGANLAR.get(kalit)
    if yozuv and time.time() - yozuv[0] < NUSXA_OYNASI:
        return yozuv[1], yozuv[2]
    if API:
        return None, None
    # Mahalliy rejimda baza aniqroq javob beradi: jarayon qayta ishga
    # tushgan bo'lsa ham nusxa tutiladi.
    import baza
    with baza.ulan() as c:
        r = c.execute(
            "SELECT id FROM sorovlar WHERE aloqa=? AND matn=? AND yaratildi > ?"
            " ORDER BY id DESC LIMIT 1",
            (aloqa, matn, time.time() - NUSXA_OYNASI)).fetchone()
    if not r:
        return None, None
    return r["id"], baza.sorov_tokeni(r["id"])


def _talab_yoz(matn: str, aloqa: str, tuman: str, byudjet, ism) -> dict:
    """Talabni yozadi va birinchi to'lqinni yuboradi.

    Qaytaradi: {"sorov_id", "kalit", "yuborildi", "mos"}.
    """
    if API:
        j = _api("/api/sorov", {"matn": matn, "aloqa": aloqa,
                                "tuman": tuman, "byudjet": byudjet,
                                "ism": ism})
        if not j.get("ok"):
            raise ApiXato(j.get("xato") or "sayt so'rovni qabul qilmadi")
        return {"sorov_id": j.get("id"), "kalit": j.get("token") or "",
                "yuborildi": j.get("yuborildi") or 0,
                "mos": j.get("mos_sotuvchi") or 0}

    import baza
    from lugat import modellarni_top, qismlarni_top
    from yonalishlar import belgilar as yonalishlar_belgilar
    baza.init()
    # YO'NALISH INDEKSDAN ANIQLANADI, lug'atdan emas — sayt bilan bir
    # xil yo'l (`baza.bozor_izi` orqali). Sotuvchi ham shu usulda
    # belgilangan, shuning uchun ikkalasi bir-birini topa oladi.
    sid = baza.sorov_yoz(matn, tuman, aloqa, byudjet,
                         sorted(modellarni_top(matn)),
                         sorted(qismlarni_top(matn)),
                         yonalishlar_belgilar(matn), ism)
    # Birinchi to'lqin darhol ketadi. Qaytadigan son — HAQIQIY son.
    tarqatish = baza.tolqin_yubor(sid)
    return {"sorov_id": sid, "kalit": baza.sorov_tokeni(sid),
            "yuborildi": tarqatish["yuborildi"], "mos": tarqatish["mos"]}


def sorov_yubor_vosita(arg: dict) -> dict:
    try:
        from lugat import byudjet_top
    except ImportError:                              # noqa: BLE001
        def byudjet_top(_):
            return None

    matn = str(arg.get("matn") or "").strip()[:500]
    if len(matn) < 3:
        return {"xato": "`matn` juda qisqa — nima kerakligini yozing.",
                "maslahat": "Masalan: «charm divan, 3 o'rinli, Toshkent»."}

    aloqa = _telefon_tozala(arg.get("aloqa") or "")
    if len(aloqa) < 9:
        return {
            "xato": "`aloqa` — haqiqiy telefon raqami kerak.",
            "maslahat": ("Foydalanuvchidan raqamini SO'RANG (masalan "
                         "998901234567). Raqam to'qib yozilmasin: "
                         "sotuvchi shu raqam orqali bog'lanadi."),
        }
    if len(set(aloqa[-9:])) <= 1:
        return {"xato": "`aloqa` haqiqiy raqamga o'xshamaydi.",
                "maslahat": "Foydalanuvchidan raqamini so'rang."}

    tuman = str(arg.get("tuman") or "").strip()[:60]
    ism = str(arg.get("ism") or "").strip()[:40] or None
    byudjet = _son(arg.get("byudjet"))
    # Byudjet matnning o'zidan ham olinadi — sayt shunday qiladi
    # ("kim 800.000 so'mga beradi?").
    if not byudjet:
        byudjet = byudjet_top(matn)

    # NUSXA. Chegaradan OLDIN tekshiriladi: qayta urinish chegarani
    # yeb qo'ymasin.
    eski, eski_kalit = _nusxa_top(matn, aloqa)
    if eski:
        return {
            "ok": True,
            "holat": "allaqachon_yuborilgan",
            "sorov_id": eski,
            "kalit": eski_kalit,
            "kuzatish": f"https://ober.uz/takliflar?kalit={eski_kalit}",
            "keyingi_qadam": "javoblar",
            "izoh": ("Aynan shu talab yaqinda yuborilgan — takrori "
                     "yozilmadi. Holatni `javoblar` bilan tekshiring."),
        }

    sabab = _tezlik_ok()
    if sabab:
        return {"xato": sabab, "holat": "tezlik_chegarasi"}

    try:
        y = _talab_yoz(matn, aloqa, tuman, byudjet, ism)
    except ApiXato as x:
        return {"xato": str(x)}

    sid, kalit = y["sorov_id"], y["kalit"]
    yuborildi, mos = y["yuborildi"], y["mos"]
    _YOZISH_VAQTLARI.append(time.time())
    _YOZILGANLAR[(matn, aloqa)] = (time.time(), sid, kalit)

    if yuborildi:
        izoh = (f"Talab {yuborildi} ta mos sotuvchiga yuborildi. "
                f"Ular narx va rasm bilan javob beradi. Javob "
                f"KELISHINI KUTISH KERAK — darhol kelmaydi. Holatni "
                f"`javoblar` vositasi bilan `kalit` orqali "
                f"tekshiring. Tanlash va savdolashish odamning ishi: "
                f"foydalanuvchiga kuzatish havolasini bering.")
    else:
        izoh = (f"Talab yozildi, lekin hozircha bu yo'nalishda mos "
                f"sotuvchi topilmadi. So'rov {MUDDAT_SOAT} soat ochiq "
                f"turadi — shu vaqtda ro'yxatdan o'tgan sotuvchiga "
                f"ham boradi. Holatni `javoblar` bilan tekshiring.")

    return {
        "ok": True,
        "holat": "yuborildi" if yuborildi else "sotuvchi_kutilmoqda",
        "sorov_id": sid,
        "yuborildi": yuborildi,
        "mos_sotuvchi": mos,
        "byudjet": byudjet,
        "muddat_soat": MUDDAT_SOAT,
        # `javoblar` shu kalitni so'raydi. Raqamli `sorov_id` emas —
        # u ketma-ket va taxmin qilinadi.
        "kalit": kalit,
        "kuzatish": f"https://ober.uz/takliflar?kalit={kalit}",
        "keyingi_qadam": "javoblar",
        "izoh": izoh,
    }


# ── `javoblar` ───────────────────────────────────────────────────────

# Sotuvchi javobining ichki holati -> agent tushunadigan so'z.
# `bor` va `oxshash` ni ARALASHTIRIB bo'lmaydi: birinchisi "aynan shu
# tovar bor", ikkinchisi "o'xshashi bor". Agent ikkinchisini birinchisi
# deb aytsa — bu yana o'sha yolg'on ma'lumot muammosi, faqat endi
# indeksdan emas, jonli sotuvchidan kelgani.
JAVOB_TURI = {"bor": "aynan", "oxshash": "oxshash"}


def _kalit_ol(xom: str) -> str:
    """Kalitni matndan ajratadi.

    Agent ko'pincha butun havolani qaytaradi
    (`https://ober.uz/takliflar?kalit=...`) — uni rad etish behuda
    ishqalanish, kalit o'sha yerda turibdi.
    """
    xom = str(xom or "").strip()
    if "kalit=" in xom:
        xom = xom.split("kalit=", 1)[1]
    return xom.split("&", 1)[0].split("#", 1)[0].strip()


def _takliflar_ol(kalit: str) -> dict | None:
    """Talab va unga kelgan takliflar. Topilmasa — None.

    HTTP yo'lida sayt `/api/sorov/takliflar` ni bergan paytda
    KEYINGI TO'LQINNI O'ZI ochadi (`ochiq_sorovlarni_yurit`) —
    bu saytning mavjud xatti-harakati, biz uni boshqara olmaymiz.
    Mahalliy yo'lda esa ataylab faqat SHU so'rovning to'lqini
    ochiladi: o'qish vositasi begona talablarga tegmasligi kerak.
    """
    if API:
        try:
            j = _api("/api/sorov/takliflar", id=kalit)
        except ApiXato as x:
            if "401" in str(x) or "topilmadi" in str(x):
                return None
            raise
        if not j.get("sorov"):
            return None
        return j

    import baza
    baza.init()
    sid = baza.sorov_id_token(kalit)
    if not sid:
        return None
    if baza.sorov_ochiqmi(sid):
        baza.tolqin_yubor(sid)
    d = baza.sorov_takliflari(sid)
    if not d.get("sorov"):
        return None
    d["yuborildi"] = baza.yuborilgan_soni(sid)
    return d


def javoblar_vosita(arg: dict) -> dict:
    kalit = _kalit_ol(arg.get("kalit"))
    if not kalit:
        return {"xato": "`kalit` bo'sh.",
                "maslahat": "`sorov_yubor` qaytargan `kuzatish` "
                            "havolasini bering."}
    if kalit.isdigit():
        # Raqamli ID ketma-ket, ya'ni TAXMIN QILSA BO'LADI. Sayt ham
        # faqat tokenni qabul qiladi (`server._xaridor_ident`) —
        # bu yo'l ham teshik bo'lib qolmasin.
        return {"xato": "Raqamli ID qabul qilinmaydi.",
                "maslahat": "`kuzatish` havolasidagi kalitni bering."}

    try:
        d = _takliflar_ol(kalit)
    except ApiXato as x:
        return {"xato": str(x)}
    if d is None:
        return {"xato": "Bunday talab topilmadi — kalit noto'g'ri "
                        "yoki eskirgan."}

    sorov = dict(d.get("sorov") or {})
    ochiq = _ochiqmi(sorov)
    yuborildi = d.get("yuborildi") or 0

    javoblar = []
    for t in d.get("takliflar") or []:
        # ATAYLAB TANLAB OLINADI, `**t` YOZILMAYDI. `sorov_takliflari`
        # ichki maydonlarni ham qaytaradi (`sotuvchi_id`, `suhbat_id`,
        # `javob_id`) — ular agentga kerak emas. Yangi ustun
        # qo'shilganda u o'zi javobga sizib chiqmasin.
        javoblar.append({
            "sotuvchi": t.get("nom") or "Sotuvchi",
            "joy": t.get("tuman") or "",
            "turi": JAVOB_TURI.get(t.get("holat"), t.get("holat")),
            "narx_som": t.get("narx"),
            "izoh": t.get("izoh") or "",
            "oxirgi_xabar": t.get("oxirgi_xabar") or "",
            "vaqt": t.get("oxirgi_vaqt") or "",
            "oqilmagan": t.get("oqilmagan") or 0,
        })

    narxlar = sorted(x["narx_som"] for x in javoblar if x["narx_som"])
    kuzatish = f"https://ober.uz/takliflar?kalit={kalit}"

    if javoblar:
        holat = "javob_bor"
        izoh = (f"{len(javoblar)} ta sotuvchi javob berdi. Narx va "
                f"shartlarni ODAM tanlaydi — foydalanuvchiga "
                f"kuzatish havolasini bering, yozishma o'sha yerda "
                f"davom etadi. `aynan` va `oxshash` javoblarni "
                f"ajratib ayting.")
    elif ochiq:
        holat = "kutilmoqda"
        izoh = (f"Hali javob yo'q. Talab {yuborildi} ta sotuvchida "
                f"turibdi va {MUDDAT_SOAT} soat ochiq. Biroz kutib "
                f"qayta so'rash mumkin.")
    else:
        holat = "yopilgan"
        izoh = ("Talab muddati tugagan va javob kelmagan. Kerak "
                "bo'lsa `sorov_yubor` bilan qaytadan yuborish "
                "mumkin.")

    natija = {
        "ok": True,
        "holat": holat,
        "talab": sorov.get("matn") or "",
        "byudjet": sorov.get("byudjet"),
        "yuborildi": yuborildi,
        "javob_soni": len(javoblar),
        "javoblar": javoblar,
        "kuzatish": kuzatish,
        "izoh": izoh,
    }
    if narxlar:
        natija["eng_arzon_som"] = narxlar[0]
    return natija


ISHLOVCHILAR = {
    "qidir": qidir_vosita,
    "sorov_yubor": sorov_yubor_vosita,
    "javoblar": javoblar_vosita,
}


# ── JSON-RPC ────────────────────────────────────────────────────────

def _javob(id_, natija=None, xato=None) -> dict:
    j = {"jsonrpc": "2.0", "id": id_}
    if xato is not None:
        j["error"] = xato
    else:
        j["result"] = natija
    return j


def ishla(xabar: dict):
    usul = xabar.get("method")
    id_ = xabar.get("id")

    if usul == "initialize":
        return _javob(id_, {
            "protocolVersion": PROTOKOL,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": NOM, "version": VERSIYA},
        })

    # Bildirishnomalarda `id` yo'q — javob qaytarilmaydi.
    if usul in ("notifications/initialized", "initialized"):
        return None

    if usul == "tools/list":
        return _javob(id_, {"tools": VOSITALAR})

    if usul == "tools/call":
        p = xabar.get("params") or {}
        nom = p.get("name")
        arg = p.get("arguments") or {}
        ishlovchi = ISHLOVCHILAR.get(nom)
        if ishlovchi is None:
            return _javob(id_, xato={"code": -32601,
                                     "message": f"noma'lum vosita: {nom}"})
        try:
            natija = ishlovchi(arg)
        except Exception as x:                       # noqa: BLE001
            # Xato agentga MATN sifatida qaytadi, protokol xatosi
            # emas — agent buni o'qib qayta urina oladi.
            return _javob(id_, {
                "content": [{"type": "text",
                             "text": f"Xato: {type(x).__name__}: {x}"}],
                "isError": True,
            })
        return _javob(id_, {
            "content": [{"type": "text",
                         "text": json.dumps(natija, ensure_ascii=False,
                                            indent=1)}],
            # Vosita darajasidagi xato protokol xatosi emas: agent uni
            # o'qib tuzatadi (masalan raqam so'raydi).
            "isError": bool(natija.get("xato")),
        })

    if id_ is None:
        return None
    return _javob(id_, xato={"code": -32601,
                             "message": f"noma'lum usul: {usul}"})


def main() -> int:
    for qator in sys.stdin:
        qator = qator.strip()
        if not qator:
            continue
        try:
            xabar = json.loads(qator)
        except json.JSONDecodeError:
            continue
        try:
            javob = ishla(xabar)
        except Exception:                            # noqa: BLE001
            traceback.print_exc(file=sys.stderr)
            javob = _javob(xabar.get("id"),
                           xato={"code": -32603, "message": "ichki xato"})
        if javob is not None:
            sys.stdout.write(json.dumps(javob, ensure_ascii=False) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
