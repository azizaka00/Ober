"""
OBER — TELEGRAM KANALLARI ADAPTERI

NEGA (Aziz, 2026-08-02: "hech kim qilmagan aqlli taktik yurish"):
O'zbekistonliklarning HAR TO'RTINCHISI Telegram orqali xarid qiladi,
OLX'dan esa 23% foydalanadi. Ya'ni Telegram savdosi OLX bilan teng.
Lekin TGStat va Telemetr KANALLARNI sanaydi, kanal ichidagi TOVARNI
emas. Bugun kerakli narsani izlagan odam 15 ta kanalga a'zo bo'lib,
qo'lda skroll qiladi. Bu — indekslanmagan yarim bozor.

NEGA BU OLX'DAN YAXSHIROQ MANBA:
  1. Barqaror. OLX'ni `__PRERENDERED_STATE__` orqali o'qiymiz — ular
     sahifani o'zgartirsa ertaga sinadi. `t.me/s/<kanal>` esa rasmiy,
     ochiq va yillar davomida o'zgarmagan ko'rinish.
  2. Toza. Ochiq kanal — ommaviy nashr, kirish uchun hisob kerak emas.
  3. Sotuvchi allaqachon shu yerda. Uni saytga taklif qilish shart emas.

TUZILISH (2026-08-02 da brauzerda o'z ko'zim bilan tekshirilgan,
taxmin emas):
  <div class="tgme_widget_message" data-post="kanal/3251">
  <div class="tgme_widget_message_text js-message_text"> ... matn
  <a class="tgme_widget_message_photo_wrap ..." style="...url('...')">
  <time class="time" datetime="2026-07-29T07:01:36+00:00">
  Keyingi sahifa: ?before=<eng kichik xabar raqami>

MUHIM CHEKLOV — HAMMA XABAR E'LON EMAS.
O'lchangan: `roboshopuz` kanalining 18 xabaridan 12 tasida matn bor,
lekin faqat yarmida narx bor. Qolganlari e'lon emas: podkast, video,
"hurmatli mijozlar" xabari. Ularni indeksga qo'shsak qidiruv axlatga
to'ladi. Shuning uchun qat'iy filtr: NARXI BO'LMAGAN XABAR OLINMAYDI.
Narx — "bu sotuv e'loni" degan eng ishonchli belgi.
"""

from __future__ import annotations

import html as _html
import re
import time
from urllib.request import Request, urlopen

import baza

MANBA = "telegram"
NOM = "Telegram"
UA = "OberBot/0.1 (+https://ober.uz; aloqa: uznaiza@gmail.com)"
KUTISH = 2.0                       # soniya, sahifalar orasida

_TEG = re.compile(r"<[^>]+>")
_BR = re.compile(r"<br\s*/?>", re.I)
# Emoji va bezak belgilar. Manba faylda maxsus belgi yozmaymiz — faqat
# kod nuqtalari: tahrirlovchi yoki kodlash o'zgarsa ham sinmaydi.
_EMOJI = re.compile(
    "["
    "\U0001F000-\U0001FAFF"      # emoji asosiy bloklari
    "←-⇿"              # strelkalar
    "⌀-➿"              # texnik belgilar, dingbats
    "⬀-⯿"              # qo'shimcha belgilar
    "☀-⛿"              # turli belgilar
    "️‍⃣︎"   # variant selektorlari, ZWJ
    "]+")


def yukla(url: str) -> str:
    req = Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "uz,ru;q=0.9",
    })
    with urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def _matn(s: str) -> str:
    """HTML -> toza matn. <br> qator ajratgichi sifatida saqlanadi.

    Teglar bo'shliqsiz olib tashlanadi: Telegram raqamni ham bezaydi
    ("100 <b>000</b>"), bo'shliq qo'ysak narx "100 000" o'rniga
    "100  000" bo'lib ketardi. Ortiqcha bo'shliq keyin siqiladi.
    """
    s = _BR.sub("\n", s)
    s = _TEG.sub("", s)
    s = _html.unescape(s)
    return "\n".join(re.sub(r"[ \t]+", " ", q).strip()
                     for q in s.split("\n")).strip()


# ── NARX ─────────────────────────────────────────────────────────────────
# Telegramda narx erkin matnda yoziladi. O'lchangan haqiqiy shakllar:
#   "💰 Narxi: 100 000 so'm"   "55 000 so‘m"   "12$"   "1.2 mln"
# Chegaralar OLX adapteridagi bilan bir xil mantiqda: bema'ni raqam
# (telefon, yil, 999999999) narx sifatida yozilmaydi.
DOLLAR_KURSI = 12800               # taxminiy; faqat tartiblash uchun
NARX_ENG_KAM = 1000
NARX_ENG_KOP = 5_000_000_000

# `сўм` - o'zbek kirillchasi (ў = U+045E). Ilgari faqat ruscha `сум`
# yozilgan edi va butun ko'chmas mulk kanali o'tib ketardi:
# "Нархи: 780 000 000 сўм" narx sifatida tanilmasdi (2026-08-03).
_NARX_SOM = re.compile(
    r"(\d[\d\s.,]{2,})\s*(so\s*['`’ʻ]?\s*m|с[ўуo]м|sum|som)", re.I)
_NARX_USD = re.compile(r"(?:\$|USD|у\.?е\.?)\s*(\d[\d\s.,]*)|"
                       r"(\d[\d\s.,]*)\s*(?:\$|USD|у\.?е\.?)", re.I)
# `ming` dan keyin `$` kelsa - bu DOLLAR, ming so'm emas.
# "10 ming$lik navorot" = 10 000 dollarlik ish (2026-08-03).
_NARX_MING = re.compile(r"(\d+[.,]?\d*)\s*(ming|минг)\b(?!\s*[$₽])", re.I)
_NARX_MLN = re.compile(r"(\d+[.,]?\d*)\s*(mln|млн|million|миллион)\b", re.I)
# Telefon raqamini narx deb o'qib qo'ymaslik uchun
_TELEFON = re.compile(r"(?:\+?998|\b9\d)[\s\-()]?\d[\s\-()\d]{6,}")


def _son(s: str) -> int:
    raqam = re.sub(r"[^\d]", "", s or "")
    return int(raqam) if raqam else 0


# Raqamli, lekin narx BO'LMAGAN qatorlar. Mashina va ko'chmas mulk
# e'lonlarida bular narxdan ko'p uchraydi.
_OLCHOV = re.compile(
    r"\bkm\b|probeg|пробег|\byil\b|\bгод\b|pozitsiya|позиция|"
    r"xona|комнат|qavat|этаж|sotix|сотих|соток|м2|m²|м²|kv\.?m|"
    r"\bkg\b|\bлитр\b|\bl\b|dvigatel|двигател|\byear\b", re.I)


def _dollar_son(xom: str) -> float:
    """"10,600" -> 10600.0,  "12.5" -> 12.5

    2026-08-03 XATO: mashina e'lonlari narxni "Narxi: 10,600$" deb
    yozadi - vergul MINGLIKLAR ajratgichi. Kod uni kasr nuqtasi deb
    o'qidi va 10 600 dollar 10.6 dollarga aylandi. Ya'ni bozordagi
    eng qimmat tovar - mashina - ming barobar arzon ko'rinardi va
    "avval arzoni" saralashini butunlay buzardi.

    Farqlash qoidasi oddiy: ajratgichdan keyin ANIQ 3 raqam bo'lsa -
    mingliklar ("10,600"), 1-2 raqam bo'lsa - kasr ("12.5").
    """
    s = (xom or "").strip().replace(" ", "")
    if not s:
        return 0.0
    # 10,600  yoki  1.250.000  -> mingliklar
    if re.fullmatch(r"\d{1,3}([.,]\d{3})+", s):
        return float(re.sub(r"[^\d]", "", s))
    # 12.5  yoki  12,5  -> kasr
    if re.fullmatch(r"\d+[.,]\d{1,2}", s):
        return float(s.replace(",", "."))
    raqam = re.sub(r"[^\d]", "", s)
    return float(raqam) if raqam else 0.0


def _yalangoch_narx(matn: str) -> tuple[int | None, str]:
    """Valyutasiz, yolg'iz turgan raqam - narx.

    2026-08-03 o'lchov: `avto_gm_zapchastt` kanalining 15 xabaridan
    BITTASI ham olinmadi, chunki ular narxni shunday yozadi:

        Matiz torpeda
        310000

    Valyuta ham, "narxi" so'zi ham yo'q. Bu O'zbek Telegram savdosida
    keng tarqalgan yozuv va aynan bizning o'zak kategoriyamiz - avto
    ehtiyot qism. Ularsiz Telegram indeksining ma'nosi qolmaydi.

    XAVFSIZLIK: faqat qator DEYARLI RAQAMDAN IBORAT bo'lsa olinadi
    ("1kom. 255000" - ha, "2 xona, 8 qavatli uy" - yo'q). Va eng kami
    5 xonali: 4 xonali son yil bo'lishi mumkin (2026), 5 xonalisi esa
    haqiqiy narx.
    """
    for qator in matn.split("\n"):
        q = qator.strip()
        if not q or len(q) > 40:
            continue
        # O'LCHOV BIRLIGI NARX EMAS.
        # 2026-08-03: "Probeg: 22.000 km" narx deb o'qildi va Trailblazer
        # 10 000 so'mga tushdi. Mashina e'lonida raqamli qator ko'p:
        # probeg, yil, qavat, xona, sotix. Ularning hech biri narx emas.
        if _OLCHOV.search(q):
            continue
        raqamlar = re.findall(r"\d[\d\s.,]*\d|\d", q)
        if not raqamlar:
            continue
        # Qatorda raqamdan boshqa nima bor? Narx qatorida deyarli
        # hech narsa bo'lmaydi ("310000", "1kom. 255000").
        qolgani = re.sub(r"[\d\s.,:\-]", "", q)
        if len(qolgani) > 5:
            continue                        # bu jumla, narx emas
        nomzod = max((_son(r) for r in raqamlar), default=0)
        if 10_000 <= nomzod <= NARX_ENG_KOP:
            return nomzod, q[:40]
    return None, ""


# "Narxi:", "Нархи:", "Цена:", "💲" - narx SHU QATORDA yozilgan degan
# ishonchli belgi. Boshqa qatorlardagi raqamlar tavsif bo'lishi mumkin.
_NARX_YORLIG = re.compile(r"narx|нарх|цена|price|💲|narhi", re.I)


def narx_top(matn: str) -> tuple[int | None, str]:
    """(so'mdagi narx, asl yozuv). Topilmasa (None, "").

    AVVAL YORLIQLI QATOR. 2026-08-03 xato: Trailblazer e'lonida
    "💲Narxi: 22,200$" bor edi, lekin tavsifda "10 ming$lik navorot
    qilingan" degan gap ham bor edi. Kod butun matndan qidirib,
    "10 ming" ni narx deb oldi va 22 200 dollarlik mashina 10 000
    so'mga tushdi.

    Yechim: narx yorlig'i bo'lgan qator bo'lsa, FAQAT o'shani o'qiymiz.
    Yorliq yo'q bo'lsagina butun matnga qaraymiz.
    """
    for qator in matn.split("\n"):
        if _NARX_YORLIG.search(qator):
            n, asl = _narx_qatordan(qator)
            if n:
                return n, asl
    return _narx_qatordan(matn)


def _narx_qatordan(matn: str) -> tuple[int | None, str]:
    """Berilgan matndan narxni ajratadi."""
    toza = _TELEFON.sub(" ", matn)          # raqamlar chalkashmasin
    m = _NARX_SOM.search(toza)
    if m:
        n = _son(m.group(1))
        if NARX_ENG_KAM <= n <= NARX_ENG_KOP:
            return n, m.group(0).strip()
    m = _NARX_MLN.search(toza)
    if m:
        n = int(float(m.group(1).replace(",", ".")) * 1_000_000)
        if NARX_ENG_KAM <= n <= NARX_ENG_KOP:
            return n, m.group(0).strip()
    m = _NARX_MING.search(toza)
    if m:
        n = int(float(m.group(1).replace(",", ".")) * 1000)
        if NARX_ENG_KAM <= n <= NARX_ENG_KOP:
            return n, m.group(0).strip()
    m = _NARX_USD.search(toza)
    if m:
        d = _dollar_son((m.group(1) or m.group(2) or ""))
        if 1 <= d <= 1_000_000:
            return int(d * DOLLAR_KURSI), m.group(0).strip()
    # Oxirgi urinish: valyutasiz yolg'iz raqam
    return _yalangoch_narx(_TELEFON.sub(" ", matn))


# ── SARLAVHA ─────────────────────────────────────────────────────────────
# Birinchi mazmunli qator. Emoji va reklama bezaklari olib tashlanadi.
_AXLAT_QATOR = re.compile(
    r"^\s*(?:https?://|t\.me/|@\w+|[\W_]*)\s*$", re.I)


# E'lon xususiyatlarining yorliqlari. Sarlavha SHULARGACHA tugaydi.
# 2026-08-03: ba'zi xabarlarda qator ajratgich yo'q va butun e'lon
# bitta qatorga tushadi. Natijada sarlavha shunday chiqardi:
# "Moshina modeli: #Nexia 1 Kraska: Polniy Rangi: Oq Yil: 1999
#  Probeg: xxxx Benzin gaz Narxi: 600$ Tel: ..." - o'qib bo'lmaydi.
_XUSUSIYAT = re.compile(
    r"\s(kraska|rangi|yil|probeg|narx|нарх|цена|tel|тел|pozitsiya|"
    r"pozitsiyasi|holati|benzin|manzil|joylashuv)\s*:", re.I)


def sarlavha_top(matn: str) -> str:
    for qator in matn.split("\n"):
        q = _EMOJI.sub(" ", qator)
        q = re.sub(r"\s+", " ", q).strip(" .,:;-–—*_|")
        if len(q) < 4 or _AXLAT_QATOR.match(q):
            continue
        # Ikkinchi yorliqdan boshlab kesamiz: birinchisi sarlavhaning
        # o'zi bo'lishi mumkin ("Moshina modeli: #Nexia").
        kesim = list(_XUSUSIYAT.finditer(q))
        if len(kesim) > 1:
            q = q[:kesim[1].start()].strip(" .,:;-–—*_|")
        return q[:140]
    return ""


# ── E'LONMI? ─────────────────────────────────────────────────────────────
# Kanal xabarlarining yarmi e'lon emas. Filtr qat'iy: narxsiz olinmaydi.
_REKLAMA = re.compile(
    r"a[’'`]?zo bo|obuna bo|kanalga qo|подпис|reklama|admin kerak|"
    r"shogird ol|kanal topdim|joinchat", re.I)

# SOTILGAN TOVAR KO'RSATILMAYDI.
# 2026-08-03: indeksga "#Sotildi" belgili mashinalar tushdi. Xaridor
# bosib borsa, tovar allaqachon yo'q. Bir marta shunday bo'lsa ishonch
# ketadi - bu OBER'ning butun ma'nosiga qarshi.
_SOTILGAN = re.compile(
    r"#\s*sotildi|\bsotildi\b|сотилди|продано|продан\b|\bsold\b|"
    r"band qilindi|бант қилинди", re.I)


# ISH E'LONI — OYLIK NARX EMAS.
#
# 2026-08-04, Aziz bosh sahifani telefonda suratga oldi. "Hozir bozorda"
# lentasida quyidagilar turardi:
#
#     ISHGA TAKLIF QILAMIZ ‼            11 400 000 so'm
#     ЭНАГА (НЯНЯ) КЕРАК                 6 000 000 so'm
#     Logistika Dispatcher kerak       312 180 973 so'm
#
# Bular ish e'lonlari, raqamlar esa OYLIK MAOSH. Narx maydoniga tushgani
# uchun ular tovar bo'lib ko'rinadi: "arzonidan" saralaganda ish e'loni
# divan bilan aralashadi, oxirgi misolda esa telefon raqami narx bo'lib
# olingan.
#
# Maosh — narx emas. Ish e'loni indeksda QOLADI (OBER "mahsulot, xizmat
# va ishlarni" topadi), lekin narxsiz.
# Ikkita alohida tekshiruv, chunki ular boshqacha xavf tug'diradi.
#
# 1) ANIQ BELGILAR — bu so'zlar tovar e'lonida deyarli uchramaydi,
#    shuning uchun ularni yolg'iz o'zi yetarli deb olamiz.
_ISH_ANIQ = re.compile(
    r"ishga taklif|ish taklif|иш таклиф|ishga olamiz|"
    r"\bvakansiya\b|вакансия|требует[сяь]|ищем\s|"
    r"приглашаем на работу|\bрезюме\b|ish o[’'`]?rni|"
    r"ish haqi|иш хақи|oylik maosh|ойлик маош|"
    r"заработная плата|зарплата|ish vaqti|иш вақти|яшаб ишлаш",
    re.I)

# 2) KASB + "KERAK" — "kerak" yolg'iz o'zi ISHONCHSIZ belgi.
#    "Kobalt fara kerak" — bu xaridorning talabi, ish e'loni emas.
#    Shuning uchun oldida ANIQ KASB nomi turishi shart.
_ISH_KASB = re.compile(
    r"(?:xodim|ходим|ishchi|ишчи|yordamchi|ёрдамчи|farrosh|фаррош|"
    r"oshpaz|ошпаз|ofitsiant|официант|qorovul|қоровул|охранник|"
    r"haydovchi|ҳайдовчи|водител\w*|kuryer|курьер|dispatcher|диспетчер|"
    r"repetitor|репетитор|тренер|повар|няня|энага|нянь\w*|"
    r"рабочи\w*|менеджер|сотрудник|sotuvchi-konsultant|sartarosh)"
    r"[\w’'`ʻ]*\s*(?:\([^)]{0,30}\)\s*)?(?:[^\s]+\s+){0,3}?"
    r"(?:kerak|керак|talab qilinadi|талаб қилинади)",
    re.I)


def ishmi(matn: str) -> bool:
    """Ish e'lonimi? Sarlavha va matn boshiga qaraydi.

    Ish e'loni indeksdan CHIQARILMAYDI — faqat narxi olib tashlanadi,
    chunki undagi raqam maosh. OBER "mahsulot, xizmat va ishlarni"
    topadi, demak ish e'loni qidiruvda qolishi kerak.
    """
    bosh = matn[:600]
    return bool(_ISH_ANIQ.search(bosh) or _ISH_KASB.search(bosh))


def elonmi(matn: str, narx: int | None) -> bool:
    if not narx:
        return False                        # narxsiz — e'lon emas
    if _SOTILGAN.search(matn):
        return False                        # allaqachon sotilgan
    if _REKLAMA.search(matn):
        return False                        # boshqa kanal reklamasi
    havolalar = len(re.findall(r"https?://|t\.me/", matn))
    return havolalar <= 3                   # havola tiqilgan post — spam


# ── SAHIFANI O'QISH ──────────────────────────────────────────────────────

_XABAR = re.compile(
    r'<div class="tgme_widget_message[^"]*"[^>]*data-post="([^"]+)"(.*?)'
    r'(?=<div class="tgme_widget_message\b|</section>|\Z)', re.S)
_MATN = re.compile(
    r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', re.S)
_RASM = re.compile(r"background-image:url\('([^']+)'\)")
_VAQT = re.compile(r'<time[^>]+datetime="([^"]+)"')


def sahifadan_oqi(html: str, kanal_nomi: str = "") -> list[dict]:
    """t.me/s/<kanal> sahifasidan e'lonlarni ajratadi."""
    natija = []
    for post, tana in _XABAR.findall(html):
        m = _MATN.search(tana)
        if not m:
            continue
        matn = _matn(m.group(1))
        narx, asl = narx_top(matn)
        if not elonmi(matn, narx):
            continue
        nom = sarlavha_top(matn)
        if not nom:
            continue
        # Ish e'loni bo'lsa raqam — maosh, narx emas. Indeksda qoladi,
        # lekin narxsiz: aks holda "arzonidan" saralaganda ish e'loni
        # tovarlar orasiga tushib qoladi. (2026-08-04)
        if ishmi(matn):
            narx, asl = None, ""
        rasm = _RASM.search(tana)
        vaqt = _VAQT.search(tana)
        kanal = post.split("/")[0]
        natija.append({
            "manba": MANBA,
            "tashqi_id": post,                       # "kanal/3251" — noyob
            "nom": nom,
            "narx_som": narx,
            "narx_asl": asl,
            "valyuta": "UZS",
            "havola": f"https://t.me/{post}",
            "rasm": rasm.group(1) if rasm else None,
            "sana": (vaqt.group(1)[:10] if vaqt else None),
            "tavsif": matn[:2000],
            "sotuvchi_id": kanal,
            "sotuvchi_nomi": kanal_nomi or kanal,
            "biznes": 1,                             # kanal = do'kon
            "viloyat": None, "shahar": None, "tuman": None,
        })
    return natija


def eng_kichik_id(html: str) -> int:
    """Sahifadagi eng eski xabar raqami — keyingi sahifa uchun."""
    raqamlar = [int(p.split("/")[1]) for p, _ in _XABAR.findall(html)
                if p.split("/")[-1].isdigit()]
    return min(raqamlar) if raqamlar else 0


# ── KANAL YIG'ISH ────────────────────────────────────────────────────────

def kanal(nom: str, sahifalar: int = 1, sikl: str = "") -> dict:
    """Bitta kanalni o'qiydi. `sahifalar` — nechta 'ortga' qadam."""
    hisob = {"korildi": 0, "elon": 0, "yangi": 0, "yangilandi": 0,
             "qaytdi": 0, "ozgarmadi": 0, "xato": 0}
    oldin = 0
    for _ in range(max(1, sahifalar)):
        url = f"https://t.me/s/{nom}"
        if oldin:
            url += f"?before={oldin}"
        try:
            html = yukla(url)
        except Exception:                            # noqa: BLE001
            hisob["xato"] += 1
            break
        elonlar = sahifadan_oqi(html, nom)
        hisob["korildi"] += len(_XABAR.findall(html))
        hisob["elon"] += len(elonlar)
        for e in elonlar:
            try:
                hisob[baza.saqla(e, sikl)] += 1
            except Exception:                        # noqa: BLE001
                hisob["xato"] += 1
        keyingi = eng_kichik_id(html)
        if not keyingi or keyingi == oldin:
            break
        oldin = keyingi
        time.sleep(KUTISH)
    return hisob


def kanallar_royxati() -> list[str]:
    """`data/telegram-kanallar.txt` — har qatorda bitta kanal nomi."""
    fayl = baza.DB.with_name("telegram-kanallar.txt")
    try:
        satrlar = fayl.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    nomlar = []
    for s in satrlar:
        s = s.strip()
        if not s or s.startswith("#"):
            continue
        s = s.split("|")[0].strip().lstrip("@")
        s = s.replace("https://t.me/", "").replace("t.me/", "").strip("/")
        if s:
            nomlar.append(s)
    return nomlar
