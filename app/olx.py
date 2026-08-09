"""
OBER — OLX ADAPTERI

Zond natijasi (2026-07-30): OLX sahifasida JSON blok YO'Q, lekin barqaror
`data-testid` belgilari bor. Ular QA uchun qo'yilgan va dizayn o'zgarsa ham
odatda saqlanadi — shuning uchun parser shularga tayanadi, CSS klassga emas
(css-blr5zl kabi klasslar har build'da o'zgaradi).

Belgilar:
  data-testid="l-card"        — bitta e'lon kartasi
  data-testid="ad-price"      — narx ("95 000 сум")
  data-testid="location-date" — "Ташкент, Чиланзарский район - 18 июля 2026 г."
  href="/d/obyavlenie/...-ID<kod>.html" — havola va ID
  <span title="Новый">        — holati

HIMOYA QOIDALARI (ober/docs/01-manbalar.md):
  - o'zimizni tanitamiz
  - so'rovlar orasida kutamiz (manbani yuklamaymiz)
  - faqat ochiq ko'rinadigan ma'lumot
"""

from __future__ import annotations

import html as _html
import json
import re
import time
from urllib.request import Request, urlopen

import baza

MANBA = "olx"
NOM = "OLX"
UA = "OberBot/0.1 (+https://ober.uz; aloqa: uznaiza@gmail.com)"
KUTISH = 2.5                       # soniya, sahifalar orasida

# ── Yordamchilar ─────────────────────────────────────────────────────────────

_TEG = re.compile(r"<[^>]+>")


def _matn(s: str) -> str:
    """HTML teglarni olib tashlaydi va bo'shliqlarni tozalaydi."""
    return re.sub(r"\s+", " ", _html.unescape(_TEG.sub(" ", s))).strip()


def yukla(url: str) -> str:
    req = Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "ru,uz;q=0.9",
    })
    with urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


# ── Narx ─────────────────────────────────────────────────────────────────────

# Ishonchli narx chegarasi. Bulardan tashqarisi — sotuvchi xatosi yoki bema'ni
# raqam (masalan 999999999). Ularni narx sifatida yozmaymiz.
NARX_MIN = 5_000
NARX_MAX = 2_000_000_000
USD_SOM = 11_960                   # 2026-07 rasmiy kurs atrofida


def soxta_narxmi(qiymat: int) -> bool:
    """'Qo'ng'iroq qiling' ma'nosidagi soxta raqammi?

    2026-08-01 da o'lchandi: "kobalt fara" so'rovida eng qimmat e'lon
    "Правая часть фары от кобалт Б/у — 9 999 999 so'm" edi. Bu narx emas,
    bu "narx yozgim kelmadi" degani. Bitta shunday raqam butun oraliqni
    buzadi: 200 000 – 6 600 000 degan foydasiz javob chiqadi.

    Belgilar: bir xil raqam takrori (999999, 111111), yoki 123456 kabi
    ketma-ketlik. Faqat 6 xonadan uzun sonlarga qo'llanadi — 55 000 yoki
    111 000 haqiqiy narx bo'lishi mumkin.
    """
    s = str(int(qiymat))
    if len(s) < 6:
        return False
    if len(set(s)) == 1:                       # 999999, 1111111
        return True
    if s.rstrip("0") and len(set(s.rstrip("0"))) == 1 and len(s.rstrip("0")) >= 6:
        return True
    ketma = "1234567890"
    return s in ketma or s in ketma[::-1]      # 123456, 654321


def narx_tahlil(matn: str, kurs: int = USD_SOM) -> tuple[int | None, str, bool]:
    """'95 000 сум Договорная' -> (95000, 'som', True)
       '75 у.е.'               -> (900000, 'usd', False)
    Qaytaradi: (so'mdagi narx, valyuta, kelishiladimi)"""
    kelishiladi = bool(re.search(r"Договорн|Kelishil", matn, re.I))
    raqamlar = re.findall(r"[\d\s ]+", matn)
    if not raqamlar:
        return None, "", kelishiladi
    son = re.sub(r"[^\d]", "", max(raqamlar, key=len))
    if not son:
        return None, "", kelishiladi
    if len(son) > 12:
        return None, "", kelishiladi
    qiymat = int(son)
    valyuta = "som"
    if re.search(r"у\.?\s?е|y\.?\s?e|\$|USD", matn, re.I):
        qiymat *= kurs
        valyuta = "usd"
    # Ishonchsiz raqamni bazaga yozmaymiz — asl matn baribir saqlanadi.
    # Sotuvchilar ba'zan 999999999 kabi bema'ni narx yozadi; ular o'rtacha
    # narxni buzadi va butun tahlilni yaroqsiz qiladi.
    if not (NARX_MIN <= qiymat <= NARX_MAX) or soxta_narxmi(qiymat):
        return None, valyuta, kelishiladi
    return qiymat, valyuta, kelishiladi


def joy_tahlil(matn: str) -> tuple[str, str, str]:
    """'Ташкент, Чиланзарский район - 18 июля 2026 г.'
       -> ('Ташкент', 'Чиланзарский район', '18 июля 2026 г.')"""
    joy, _, sana = matn.partition(" - ")
    shahar, _, tuman = joy.partition(", ")
    return shahar.strip(), tuman.strip(), sana.strip()


# ── Parser ───────────────────────────────────────────────────────────────────

def kartalarni_ajrat(html: str) -> list[str]:
    """Sahifani e'lon kartalariga bo'ladi."""
    joylar = [m.start() for m in re.finditer(r'data-testid="l-card"', html)]
    if not joylar:
        return []
    joylar.append(len(html))
    return [html[joylar[i]:joylar[i + 1]] for i in range(len(joylar) - 1)]


# ── ASOSIY MANBA: sahifaning ichidagi holat (PRERENDERED_STATE) ─────────────
#
# 2026-07-30, uchinchi urinish. Tarix:
#   1) HTML kartalardan o'qidik      -> rasm 12%, tuman 8%
#   2) ld+json qo'shdik              -> faqat 1-sahifada ishladi (Aziz ko'rdi)
#   3) SHU: sahifada window.__PRERENDERED_STATE__ bor va unda HAR sahifadagi
#      HAR e'lonning to'liq ma'lumoti turadi — rasm, shahar, TUMAN, tavsif,
#      qism turi, do'konmi, sotuvchi, aniq narx va sana.
#
# O'lchandi (2-sahifa, 52 e'lon): rasm 51/52, shahar 52/52, tuman 38/52.
# Ya'ni e'lon sahifasini alohida ochish (3 soniya har biriga) endi kerak
# emas — hammasi bitta so'rovda keladi. Telefon esa bu yerda ham YO'Q:
# faqat "phone: true" degan belgi bor, raqamning o'zi emas.

_HOLAT_RE = re.compile(r'PRERENDERED_STATE__\s*=\s*("(?:[^"\\]|\\.)*")')


def _lugat(x) -> dict:
    """Faqat lug'atni qaytaradi. OLX maydonlari ba'zan matn yoki ro'yxat
    bo'lib keladi — bitta shunday hol butun yig'ishni to'xtatgan edi."""
    return x if isinstance(x, dict) else {}


def _param_qiymat(p: dict) -> str:
    q = p.get("value")
    if isinstance(q, dict):
        q = q.get("label") or q.get("value") or q.get("key") or ""
    return str(q or "").strip()


def _param(ad: dict, kalit: str) -> str:
    for p in ad.get("params") or []:
        if isinstance(p, dict) and p.get("key") == kalit:
            return _param_qiymat(p)
    return ""


def barcha_paramlar(ad: dict) -> list[dict]:
    """E'lonning BARCHA tavsiflari.

    2026-08-02 saboq: biz faqat `part_type` ni olardik va qolganini
    tashlardik. Holbuki OLX har e'longa o'z tavsiflarini qo'yib beradi:
    kvartira uchun xona soni, qavat, maydon; telefon uchun model,
    xotira, holat.

    Ya'ni HAR KATEGORIYA UCHUN LUG'AT QO'LDA YOZISH SHART EMAS —
    OLX allaqachon yozib qo'ygan, biz uni olmayotgan edik.

    Bu ma'lumot bilan qidiruv ham, narx sahifalari ham har kategoriyada
    ishlaydi: "2 xonali kvartira Chilonzor", "iphone 128 gb".
    """
    natija = []
    for p in ad.get("params") or []:
        if not isinstance(p, dict):
            continue
        qiymat = _param_qiymat(p)
        kalit = str(p.get("key") or "").strip()
        if not qiymat or not kalit:
            continue
        natija.append({"k": kalit,
                       "n": str(p.get("name") or "").strip(),
                       "q": qiymat,
                       # normalizedValue TILGA BOG'LIQ EMAS — ruscha va
                       # o'zbekcha sahifadagi bir xil tavsifni shu orqali
                       # juftlashtiramiz.
                       "nq": str(p.get("normalizedValue") or "").strip()})
    return natija


def atamalarni_juftla(uz_sahifa: str, ru_sahifa: str) -> list[tuple]:
    """Bitta sahifaning o'zbekcha va ruscha variantidan atama lug'ati.

    Aziz savoli (2026-08-02): "ruschada qidirsa ham chiqadimi?"
    Sarlavhalar aralash yozilgani uchun chiqadi, lekin OLX BERGAN
    tavsiflar (Yangi / Новый) faqat bitta tilda bo'lardi.

    Ikkala tilni to'liq yig'ish vaqtni ikki barobar oshiradi. O'rniga:
    har kategoriyaning FAQAT BIRINCHI sahifasi ikki tilda o'qiladi va
    atamalar juftligi yozib olinadi. Keyin indeksga ikkala til ham
    qo'shiladi — qidiruv ikki tilda ishlaydi, yig'ish esa sekinlashmaydi.

    Juftlash `key` + `normalizedValue` bo'yicha — ular tilga bog'liq emas.
    """
    def _paramlar(sahifa: str) -> dict:
        m = _HOLAT_RE.search(sahifa)
        if not m:
            return {}
        try:
            ads = json.loads(json.loads(m.group(1)))["listing"]["listing"]["ads"]
        except Exception:                        # noqa: BLE001
            return {}
        chiqdi = {}
        for a in ads:
            if not isinstance(a, dict):
                continue
            for p in barcha_paramlar(a):
                if p["nq"]:
                    chiqdi[(p["k"], p["nq"])] = (p["n"], p["q"])
        return chiqdi

    uz, ru = _paramlar(uz_sahifa), _paramlar(ru_sahifa)
    juftlar = []
    for kalit, (uz_nom, uz_qiymat) in uz.items():
        ru_juft = ru.get(kalit)
        if not ru_juft:
            continue
        ru_nom, ru_qiymat = ru_juft
        if uz_qiymat and ru_qiymat and uz_qiymat != ru_qiymat:
            juftlar.append((kalit[0], uz_qiymat, ru_qiymat))
        if uz_nom and ru_nom and uz_nom != ru_nom:
            juftlar.append((kalit[0], uz_nom, ru_nom))
    return juftlar


def holatdan_oqi(sahifa: str, viloyat: str = "") -> list[dict]:
    """Sahifadagi holat blokidan e'lonlarni o'qiydi. Topilmasa — bo'sh."""
    m = _HOLAT_RE.search(sahifa)
    if not m:
        return []
    try:
        holat = json.loads(json.loads(m.group(1)))
        elonlar = holat["listing"]["listing"]["ads"]
    except Exception:                            # noqa: BLE001
        return []

    natija = []
    xato = 0
    for a in elonlar:
        try:
            e = _elondan(a, viloyat)
        except Exception:                        # noqa: BLE001
            xato += 1                            # bitta g'alati e'lon
            continue                             # butun yig'ishni to'xtatmasin
        if e:
            natija.append(e)
    if xato:
        print(f"      ({xato} ta e'lon o'qilmadi — o'tkazib yuborildi)")
    return natija


def _elondan(a: dict, viloyat: str) -> dict | None:
    """Holat blokidagi bitta e'lonni bizning ko'rinishga o'giradi."""
    if not isinstance(a, dict):
        return None
    havola = str(a.get("url") or "")
    mid = re.search(r"-ID([A-Za-z0-9]+)\.html", havola)
    if not mid or not a.get("title"):
        return None

    # Narx
    narx_som = valyuta = None
    p = _lugat(a.get("price"))
    r = _lugat(p.get("regularPrice"))
    narx_asl = str(p.get("displayValue") or "")
    kelishiladi = bool(r.get("negotiable"))
    qiymat = r.get("value")
    if isinstance(qiymat, (int, float)):
        kod = str(r.get("currencyCode") or "UZS").upper()
        qiymat = int(qiymat * (USD_SOM if kod == "USD" else 1))
        valyuta = "usd" if kod == "USD" else "som"
        if NARX_MIN <= qiymat <= NARX_MAX and not soxta_narxmi(qiymat):
            narx_som = qiymat

    # Holati: "Б/у" / "Новый"
    h = _param(a, "state").lower()
    holati = "yangi" if "нов" in h or "yangi" in h else ("b_u" if h else "")

    joy = _lugat(a.get("location"))
    foydalanuvchi = _lugat(a.get("user"))

    # photos uch xil ko'rinishda uchraydi: matn, matnlar ro'yxati yoki
    # obyektlar ro'yxati. 2026-07-31 da ro'yxat[matn] ko'rinishi butun
    # yig'ishni to'xtatgan edi — endi uchalasi ham qabul qilinadi.
    rasm = a.get("photos")
    if isinstance(rasm, list):
        rasm = rasm[0] if rasm else ""
    if isinstance(rasm, dict):
        rasm = rasm.get("link") or rasm.get("url") or rasm.get("filename") or ""
    rasm = str(rasm or "").replace("{width}", "640").replace("{height}", "480")

    return {
        "manba": MANBA, "tashqi_id": mid.group(1),
        "nom": _matn(str(a.get("title") or "")),
        "narx_som": narx_som, "narx_asl": narx_asl, "valyuta": valyuta,
        "kelishiladi": kelishiladi, "holat": holati,
        "viloyat": viloyat,
        "shahar": str(joy.get("cityName") or ""),
        "tuman": str(joy.get("districtName") or ""),
        "sana": str(a.get("lastRefreshTime")
                    or a.get("createdTime") or "")[:10],
        "havola": havola, "rasm": rasm,
        "biznes": bool(a.get("isBusiness")),
        "qism_turi": _param(a, "part_type"),
        # BARCHA tavsiflar — har kategoriya uchun avtomatik lug'at
        "xususiyatlar": json.dumps(barcha_paramlar(a), ensure_ascii=False),
        "olx_kategoriya": str((a.get("category") or {}).get("id") or "")
        if isinstance(a.get("category"), dict) else "",
        "tavsif": _matn(str(a.get("description") or ""))[:2000],
        "sotuvchi_id": str(foydalanuvchi.get("id") or ""),
        "sotuvchi_nomi": str(foydalanuvchi.get("name")
                             or _lugat(a.get("contact")).get("name") or ""),
    }


def ldjson_oqi(sahifa: str) -> dict[str, dict]:
    """havola_yo'li -> {'rasm':..., 'joy':..., 'narx':...}"""
    natija: dict[str, dict] = {}
    for m in re.finditer(
            r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
            sahifa, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception:                        # noqa: BLE001
            continue
        takliflar = ((d.get("offers") or {}).get("offers")
                     if isinstance(d, dict) else None)
        if not isinstance(takliflar, list):
            continue
        for t in takliflar:
            if not isinstance(t, dict):
                continue
            url = str(t.get("url") or "")
            mid = re.search(r"-ID([A-Za-z0-9]+)\.html", url)
            if not mid:
                continue
            rasm = t.get("image")
            if isinstance(rasm, list):
                rasm = rasm[0] if rasm else ""
            joy = (t.get("areaServed") or {})
            natija[mid.group(1)] = {
                "rasm": str(rasm or ""),
                "joy": str(joy.get("name") or "") if isinstance(joy, dict) else "",
                "joy_turi": str(joy.get("@type") or "") if isinstance(joy, dict) else "",
                "narx": t.get("price"),
            }
    return natija


def kartani_oqi(karta: str, viloyat: str = "") -> dict | None:
    m = re.search(r'href="(/d/obyavlenie/[^"]+)"', karta)
    if not m:
        return None
    yol = m.group(1)
    havola = "https://www.olx.uz" + yol

    mid = re.search(r"-ID([A-Za-z0-9]+)\.html", yol)
    if not mid:
        return None
    tashqi_id = mid.group(1)

    # Nom: h4/h6 ichida yoki havola matnida
    nom = ""
    mn = re.search(r"<h[46][^>]*>(.*?)</h[46]>", karta, re.S)
    if mn:
        nom = _matn(mn.group(1))
    if not nom:
        ma = re.search(r'href="' + re.escape(yol) + r'"[^>]*>(.*?)</a>', karta, re.S)
        if ma:
            nom = _matn(ma.group(1))
    if not nom:
        return None

    # Narx
    narx_som = valyuta = None
    narx_asl = ""
    kelishiladi = False
    mp = re.search(r'data-testid="ad-price"[^>]*>(.*?)</p>', karta, re.S)
    if mp:
        narx_asl = _matn(mp.group(1))
        narx_som, valyuta, kelishiladi = narx_tahlil(narx_asl)

    # Joy va sana
    shahar = tuman = sana = ""
    ml = re.search(r'data-testid="location-date"[^>]*>(.*?)</p>', karta, re.S)
    if ml:
        shahar, tuman, sana = joy_tahlil(_matn(ml.group(1)))

    # Holati
    holat = ""
    mh = re.search(r'title="(Новый|Б/у)"', karta)
    if mh:
        holat = "yangi" if mh.group(1) == "Новый" else "b_u"

    # Rasm
    rasm = ""
    mr = re.search(r'<img[^>]+src="(https://[^"]+)"', karta)
    if mr:
        rasm = mr.group(1)

    return {
        "manba": MANBA, "tashqi_id": tashqi_id, "nom": nom,
        "narx_som": narx_som, "narx_asl": narx_asl, "valyuta": valyuta,
        "kelishiladi": kelishiladi, "holat": holat,
        "viloyat": viloyat, "shahar": shahar, "tuman": tuman, "sana": sana,
        "havola": havola, "rasm": rasm,
    }


# ── Yig'ish ──────────────────────────────────────────────────────────────────

KATEGORIYA = "https://www.olx.uz/oz/transport/avtozapchasti-i-aksessuary/avtozapchasti/"

# OLX tuzilishi: viloyat -> shahar -> tuman.
# Viloyat e'lon matnida YO'Q, shuning uchun URL orqali bilamiz.
# Sonlar — 2026-07-30 holatiga ko'ra butun kategoriya bo'yicha.
VILOYATLAR: list[tuple[str, str, int]] = [
    # (URL bo'lagi, o'zbekcha nom, taxminiy e'lon soni)
    ("toshkent-oblast",        "Toshkent viloyati",   46966),
    ("samarkandskaya-oblast",  "Samarqand",            4156),
    ("buharskaya-oblast",      "Buxoro",               3215),
    ("ferganskaya-oblast",     "Farg'ona",             2282),
    ("horezmskaya-oblast",     "Xorazm",               1587),
    ("kashkadarinskaya-oblast","Qashqadaryo",          1460),
    ("navoijskaya-oblast",     "Navoiy",               1088),
    ("andizhanskaya-oblast",   "Andijon",               909),
    ("karakalpakstan",         "Qoraqalpog'iston",      811),
    ("namanganskaya-oblast",   "Namangan",              665),
    ("dzhizakskaya-oblast",    "Jizzax",                645),
    ("surhandarinskaya-oblast","Surxondaryo",           645),
    ("syrdarinskaya-oblast",   "Sirdaryo",              485),
]


def viloyat_url(bolak: str) -> str:
    return f"{KATEGORIYA}{bolak}/"


def yigish(url: str, viloyat: str, sahifalar: int = 3, sikl: str = "") -> dict:
    hisob = {"korildi": 0, "yangi": 0, "yangilandi": 0, "qaytdi": 0,
             "ozgarmadi": 0, "xato": 0}

    for n in range(1, sahifalar + 1):
        manzil = url if n == 1 else f"{url}?page={n}"
        try:
            html = yukla(manzil)
        except Exception as e:                              # noqa: BLE001
            print(f"      [{n}] XATO: {type(e).__name__}: {e}")
            hisob["xato"] += 1
            continue

        # ASOSIY YO'L: sahifa ichidagi holat bloki (to'liq ma'lumot).
        # Zaxira: eski HTML karta parseri — holat bloki yo'qolsa ishlaydi.
        elonlar = holatdan_oqi(html, viloyat)
        manba_nomi = "holat"
        if not elonlar:
            elonlar = [x for x in (kartani_oqi(k, viloyat)
                                   for k in kartalarni_ajrat(html)) if x]
            manba_nomi = "karta"

        rasmli = sum(1 for e in elonlar if e.get("rasm"))
        tumanli = sum(1 for e in elonlar if e.get("tuman"))
        print(f"      [{n}] {len(elonlar)} e'lon ({manba_nomi}) · "
              f"rasm {rasmli} · tuman {tumanli}")

        if not elonlar:                                     # sahifalar tugadi
            break

        for e in elonlar:
            hisob["korildi"] += 1
            try:
                hisob[baza.saqla(e, sikl)] += 1
            except Exception as ex:                         # noqa: BLE001
                print(f"      saqlash xatosi: {ex}")
                hisob["xato"] += 1

        if n < sahifalar:
            time.sleep(KUTISH)

    return hisob


def main(sahifalar: int = 3, faqat: str = "", toliq: bool = False) -> dict:
    print("=" * 62)
    print("  OBER — OLX yig'uvchi (viloyat -> shahar -> tuman)")
    print("=" * 62)
    baza.init()
    sikl = baza.sikl_boshlash(MANBA)

    ruyxat = VILOYATLAR
    if faqat:
        ruyxat = [v for v in VILOYATLAR if faqat.lower() in v[1].lower()]

    jami = {"korildi": 0, "yangi": 0, "yangilandi": 0, "qaytdi": 0,
            "ozgarmadi": 0, "xato": 0}
    for bolak, nom, soni in ruyxat:
        print(f"\n  {nom}  (~{soni:,} e'lon mavjud)")
        h = yigish(viloyat_url(bolak), nom, sahifalar, sikl)
        for k in jami:
            jami[k] += h[k]
        print(f"      yangi {h['yangi']} · yangilandi {h['yangilandi']} · "
              f"qaytdi {h['qaytdi']} · o'zgarmadi {h['ozgarmadi']}")
        time.sleep(KUTISH)

    print("\n" + "-" * 62)
    print(f"  JAMI — ko'rildi {jami['korildi']} · yangi {jami['yangi']} · "
          f"yangilandi {jami['yangilandi']} · qaytdi {jami['qaytdi']} · "
          f"xato {jami['xato']}")

    # Faqat barcha viloyatlar xatosiz tugagan chuqur sikl ko‘rinmagan
    # e’lonlarni sanaydi. Sinov yoki xatoli sikl hech narsani nofaol qilmaydi.
    hayot = baza.sikl_yakunla(
        MANBA, sikl, toliq=bool(toliq and not faqat and jami["xato"] == 0))
    if hayot["toliq"]:
        print(f"  FAOLLIK — bu safar yo‘q {hayot['otkazildi']} · "
              f"3 marta yo‘qolib nofaol {hayot['nofaol_qilindi']}")
    else:
        print("  FAOLLIK — sinov yoki xatoli sikl; nofaollashtirish o‘tkazilmadi")

    s = baza.statistika()
    print(f"\n  BAZADA: faol {s['faol']} · nofaol {s['nofaol']} · "
          f"jami {s['jami']} · narxli {s['narxli']} · "
          f"{s['tumanlar']} tuman")
    for v, n in s["viloyatlar"].items():
        print(f"      {v:22} {n}")
    print(f"\n  Fayl: {baza.DB}\n")
    return {**jami, "hayot": hayot}


if __name__ == "__main__":
    import sys
    args = [x for x in sys.argv[1:] if x != "--toliq"]
    sahifalar = int(args[0]) if args else 3
    faqat = args[1] if len(args) > 1 else ""
    main(sahifalar, faqat, toliq="--toliq" in sys.argv)
