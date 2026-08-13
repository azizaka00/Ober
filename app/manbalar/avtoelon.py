"""Avtoelon.uz — O'zbekiston avtomobil va ehtiyot qismlar e'lonlari.

2026-08-13 da tekshirildi: sayt ochiq (HTTP 200), robots.txt e'lon
sahifalarini taqiqlamaydi (faqat /index/br, /index/click, /*change*,
/sendmess* va sh.k. xizmat yo'llari). SSR — oddiy HTTP yig'ish yetarli,
brauzer kerak emas.

Ikki bo'lim:
  /avto/        — avtomobillar (karta: `row list-item a-elem`)
  /zapchasti/   — ehtiyot qismlar va tovarlar (karta: `hot-item`)

Har karta ichida JSON-LD `unitPrice`, `city`, `lastUpdate` beradi —
ro'yxat sahifasining o'zidan tayyor tuzilma, shu sababli narx va
joyni alohida HTML parse qilish shart emas.

Narx `y.e.` (shartli birlik = AQSH dollari) da. Baza `narx_som` ni
kutadi — `baza.dollar_kursi()` orqali so'mga o'tkazamiz. Kurs olinmasa
`narx_som=None` (karta narxsiz chiqadi, qidiruv buzilmaydi).

E'lon identifikatori — `/a/show/{id}` URL'sidagi raqam (JSON-LD `id`).
"""

from __future__ import annotations

import json
import re
import time
import urllib.request

import baza

MANBA = "avtoelon"
NOM = "Avtoelon"
KUTISH = 1.2          # soniya, so'rovlar orasida (saytni urishmaymiz)
# To'liq (sutkalik) sikl nechta sahifa yig'adi — har bo'lim uchun.
# 2026-08-13: 3 -> 10 (bozor to'liq qamrovda bo'lsin). O'lchov:
# avto bo'limida har sahifa 30 karta; 10 sahifa = ~300 e'lon/bo'lim.
# E'lon sahifasi ham alohida olinadi (tavsif uchun) — 1.2s KUTISH bilan
# to'liq sikl ~25 daqiqa qo'shadi (OLX siklidan ancha kam).
CHUQUR_SAHIFA = 10
_TAYANCH = "https://avtoelon.uz"
_SARLAVHA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/126.0 Safari/537.36"}

_BO_LIMLAR = [
    ("/avto/", 1),        # avtomobillar — asosiy
    ("/zapchasti/", 1),   # ehtiyot qismlar — OBERning birinchi vertikali
]

# Shahar slug -> (viloyat, shahar). Sayt `gorod-tashkent` kabi slug
# beradi; OBER viloyat va shaharni alohida kutadi.
_JOY = {
    "tashkent": ("Toshkent", "Toshkent"),
    "andizhan": ("Andijon", "Andijon"),
    "fergana": ("Farg'ona", "Farg'ona"),
    "namangan": ("Namangan", "Namangan"),
    "samarkand": ("Samarqand", "Samarqand"),
    "buhara": ("Buxoro", "Buxoro"),
    "navoi": ("Navoiy", "Navoiy"),
    "dzhizak": ("Jizzax", "Jizzax"),
    "karshi": ("Qashqadaryo", "Qarshi"),
    "nukus": ("Qoraqalpog'iston", "Nukus"),
    "termez": ("Surxondaryo", "Termiz"),
    "urgench": ("Xorazm", "Urganch"),
    "kokand": ("Farg'ona", "Qo'qon"),
    "gulistan": ("Sirdaryo", "Guliston"),
    "almalyk": ("Toshkent", "Olmaliq"),
    "angren": ("Toshkent", "Angren"),
    "chirchik": ("Toshkent", "Chirchiq"),
}


def _sozla(html: str) -> str:
    """HTML matnini tozalaydi: `&nbsp;` -> bo'shliq, teglar tashlanadi."""
    matn = re.sub(r"<[^>]+>", " ", html)
    matn = matn.replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\s+", " ", matn).strip()


def _sahifa_ol(yol: str) -> str:
    """Sahifani oladi; HTTP xatosida '' qaytaradi."""
    soz = urllib.request.Request(_TAYANCH + yol, headers=_SARLAVHA)
    with urllib.request.urlopen(soz, timeout=20) as r:
        if r.status != 200:
            print(f"  [avtoelon] {yol} -> HTTP {r.status}")
            return ""
        return r.read().decode("utf-8", errors="replace")


def _narx_qiymat(raqam: int | None, birlik: str = "") -> tuple[int | None, str | None]:
    """y.e. narxni so'mga o'tkazadi.

    `birlik` — JSON-LD `unitPrice` uchun har doim y.e. (dollar). Kurs
    olinmasa narx_som=None (karta narxsiz chiqadi, qidiruv buzilmaydi).
    """
    if not raqam:
        return None, None
    narx_asl = f"{raqam:,}".replace(",", " ") + " y.e."
    kurs = baza.dollar_kursi()
    if not kurs or not kurs.get("kurs"):
        return None, narx_asl
    return raqam * kurs["kurs"], narx_asl


def _joy_ajrat(manzil: str) -> tuple[str, str]:
    """`/avto/gorod-tashkent/` -> ('Toshkent', 'Toshkent')."""
    m = re.search(r"gorod-([a-z-]+)", manzil)
    if m and m.group(1) in _JOY:
        return _JOY[m.group(1)]
    return "", ""


def _json_ld(blok: str) -> dict:
    """Karta ichidagi `listing.items.push({...})` JSON'ini o'qiydi.

    Ro'yxat sahifasi har karta uchun `unitPrice`, `city`, `lastUpdate`
    beradi — JSON-LD emas, JS obyekt, lekin json bilan o'qiladi.
    """
    m = re.search(r"listing\.items\.push\((\{.*?\})\)\s*;", blok, re.S)
    if not m:
        return {}
    try:
        d = json.loads(m.group(1))
        return d if isinstance(d, dict) else {}
    except Exception:                          # noqa: BLE001
        return {}


def _kartalar(sahifa: str) -> list[dict]:
    """Ro'yxat sahifasidagi barcha e'lonlarni o'qiydi.

    Karta chegarasi `data-id` atributi orqali ajratiladi (har kartada
    `data-id="1234567"` bor, keyingi kartagacha cho'ziladi). Ikkala
    bo'lim bir xil qolipda keladi, farq faqat karta tashqi ko'rinishida.
    """
    # Karta boshlanishi: `row list-item a-elem` yoki `hot-item` klasslari.
    boshlar = [m.start() for m in re.finditer(
        r'class="(?:row list-item a-elem|hot-item)[^"]*"', sahifa)]
    bloklar: list[str] = []
    for i, bosh in enumerate(boshlar):
        tugash = boshlar[i + 1] if i + 1 < len(boshlar) else bosh + 30000
        blok = sahifa[bosh:tugash]
        # ID — karta oxiridagi `id="advert-123"` yoki ichidagi havola
        tashqi_id = ""
        m = re.search(r'id="advert-(\d+)"', blok)
        if not m:
            m = re.search(r'href="/a/show/(\d+)"', blok)
        if m:
            tashqi_id = m.group(1)
        if tashqi_id:
            bloklar.append((tashqi_id, blok))
    return bloklar


def _ro_kat(sahifa: str, manzil: str) -> list[dict]:
    """Ro'yxat sahifasidagi e'lonlarni dict'ga aylantiradi."""
    natija: list[dict] = []
    viloyat, shahar = _joy_ajrat(manzil)
    for tashqi_id, blok in _kartalar(sahifa):
        # JSON-LD — eng ishonchli manba
        ld = _json_ld(blok)

        nom = _sozla(ld.get("title") or "") or ""
        if not nom:
            mnom = re.search(r'class="a-info-top[^"]*"[^>]*>(.*?)</', blok, re.S)
            if mnom:
                nom = _sozla(mnom.group(1))
        if not nom:
            mimg = re.search(r'<img[^>]*alt="([^"]+)"', blok)
            if mimg:
                nom = re.sub(r"\s+id\d+\s*$", "", mimg.group(1))
        if not nom:
            continue

        # NARX — JSON-LD unitPrice (y.e.) yoki ro'yxat matnidagi narx
        narx_som, narx_asl = None, None
        ld_narx = ld.get("unitPrice")
        if isinstance(ld_narx, (int, float)) and ld_narx:
            narx_som, narx_asl = _narx_qiymat(int(ld_narx))
        else:
            # Hot kartada narx `<nobr>~19 802 y.e.</nobr>` ichida — eng
            # ishonchli joy. `bot` matnidan to'g'ridan-to'g'ri olish
            # xavfli: "BYD e2 2026" dagi "2 2026" raqamini ham oladi.
            # `_sozla` `&nbsp;`ni bo'shliqqa aylantiradi (HTML entity
            # regex `\u00a0` bilan tushmaydi).
            # Hot kartada narx `<nobr>~19 802 y.e.</nobr>` ichida — eng
            # ishonchli joy. `bot` matnidan to'g'ridan-to'g'ri olish
            # xavfli: "BYD e2 2026" dagi "2 2026" raqamini ham oladi.
            # `_sozla` `&nbsp;`ni bo'shliqqa aylantiradi (HTML entity
            # regex `\u00a0` bilan tushmaydi).
            mnarx = re.search(r'<nobr>(.*?)</nobr>', blok, re.S)
            if not mnarx:
                mnarx = re.search(r'class="price"[^>]*>.*?</span>(.*?)</span>',
                                  blok, re.S)
            if mnarx:
                txt = _sozla(mnarx.group(1))
                mraq = re.search(r"~?\s*([\d\s]{3,})\s*(y\.e\.|сом|сум|so\.m|млн|тыс)?", txt)
                if mraq:
                    raqam = int(re.sub(r"\s", "", mraq.group(1)))
                    birlik = (mraq.group(2) or "").lower()
                    if "y.e" in birlik:
                        narx_som, narx_asl = _narx_qiymat(raqam)
                    elif "млн" in birlik:
                        narx_som, narx_asl = raqam * 1_000_000, f"{raqam} млн"
                    elif "тыс" in birlik:
                        narx_som, narx_asl = raqam * 1_000, f"{raqam} тыс"
                    else:
                        narx_som, narx_asl = raqam, txt

        # JOY — JSON-LD city slug yoki ro'yxat matni
        # Slug `gorod-tashkent` — `_JOY` kaliti `tashkent`, prefiks
        # tashlanadi (kalitlarni `gorod-` bilan to'ldirish shart emas).
        e_viloyat, e_shahar = viloyat, shahar
        ld_city = re.sub(r"^gorod-", "", ld.get("city") or "")
        if ld_city and ld_city in _JOY:
            e_viloyat, e_shahar = _JOY[ld_city]
        if not e_shahar:
            mjoy = re.search(r'class="a-info-text__region[^"]*"[^>]*>(.*?)</', blok, re.S)
            if mjoy:
                e_shahar = _sozla(mjoy.group(1))
            else:
                mjoy2 = re.search(r'<span class="top"[^>]*>(.*?)<span', blok, re.S)
                if mjoy2:
                    e_shahar = _sozla(mjoy2.group(1))

        # SANA — JSON-LD lastUpdate ISO
        sana = ""
        ls = ld.get("lastUpdate") or ""
        if isinstance(ls, str) and len(ls) >= 10:
            sana = ls[:10]
        if not sana:
            mhot = re.search(r'class="hot-time[^"]*">\s*([^<]{10,25}?)\s*</div>', blok)
            if mhot:
                sana = mhot.group(1).strip()[:10]

        # RASM — ro'yxatdagi kichik rasm (kattaroq o'lchamga)
        # HTML tuzilma: `<img ... src="..." ... class="a-elem__image">`
        # — src class'dan OLDIN keladi. Karta klassiga qarab qaraymiz:
        # `a-elem__image` (avto) yoki `hot-small-img` (zapchasti).
        rasm = ""
        if "a-elem__image" in blok or "hot-small-img" in blok:
            mrasm = re.search(r'<img[^>]*src="(https://[^"]+)"', blok)
            if mrasm:
                rasm = mrasm.group(1).replace("-120x90", "-240x180")
                rasm = rasm.replace("-160x120", "-320x240")

        natija.append({
            "manba": MANBA, "tashqi_id": tashqi_id, "nom": nom,
            "narx_som": narx_som, "narx_asl": narx_asl,
            "viloyat": e_viloyat, "shahar": e_shahar,
            "sana": sana, "havola": f"{_TAYANCH}/a/show/{tashqi_id}",
            "rasm": rasm,
        })
    return natija


def _tavsif_ol(tashqi_id: str) -> dict:
    """E'lon sahifasidan tavsif, parametrlar va katta rasmni oladi."""
    sahifa = _sahifa_ol(f"/a/show/{tashqi_id}")
    natija: dict = {}
    if not sahifa:
        return natija
    m = re.search(r'class="description-text"[^>]*>(.*?)</div>', sahifa, re.S)
    if m:
        natija["tavsif"] = _sozla(m.group(1))[:2000]
    params = {}
    for dt, dd in re.findall(r'<dt class="value-title">([^<]+)</dt>\s*'
                             r'<dd class="value[^"]*">(.*?)</dd>', sahifa, re.S):
        params[_sozla(dt)] = _sozla(dd)
    if params:
        natija["xususiyatlar"] = json.dumps(params, ensure_ascii=False)
    mrasm = re.search(r'class="main-photo"[^>]*>.*?src="(https://[^"]+)"', sahifa, re.S)
    if mrasm:
        natija["rasm"] = mrasm.group(1)
    return natija


def bosh(cheklov: int = 1, faqat: str = "") -> dict:
    """Tez yig'ish: birinchi sahifalar (avto + zapchasti).

    E'lonlarni yangilaydi, hech narsani nofaol qilmaydi.
    """
    sikl = baza.sikl_boshlash(MANBA)
    natija = {"yangi": 0, "yangilandi": 0, "ozgarmadi": 0, "xato": 0}
    for yol, _ in _BO_LIMLAR:
        if faqat and faqat not in yol:
            continue
        html = _sahifa_ol(yol)
        if not html:
            natija["xato"] += 1
            continue
        for e in _ro_kat(html, yol):
            holat = baza.saqla(e, sikl)
            natija[holat] = natija.get(holat, 0) + 1
        time.sleep(KUTISH)
    return natija


def chuqur(sahifalar: int | None = None, faqat: str = "") -> dict:
    """To'liq yig'ish: ko'p sahifa + har e'lon sahifasidan tavsif.

    `sahifalar` — har bo'limda nechta sahifa (default: CHUQUR_SAHIFA).
    E'lon sahifasi ma'lumoti (tavsif, parametrlar) alohida olinadi —
    baza mavjud ma'lumotni saqlab qoladi (bo'sh qiymat bilan ustidan
    yozmaydi).
    """
    if sahifalar is None:
        sahifalar = CHUQUR_SAHIFA
    sikl = baza.sikl_boshlash(MANBA)
    natija = {"yangi": 0, "yangilandi": 0, "ozgarmadi": 0, "xato": 0}
    for yol, _ in _BO_LIMLAR:
        if faqat and faqat not in yol:
            continue
        for sahifa in range(1, max(1, sahifalar) + 1):
            manzil = f"{yol}?page={sahifa}" if sahifa > 1 else yol
            html = _sahifa_ol(manzil)
            if not html:
                natija["xato"] += 1
                continue
            for e in _ro_kat(html, yol):
                e.update(_tavsif_ol(e["tashqi_id"]))
                holat = baza.saqla(e, sikl)
                natija[holat] = natija.get(holat, 0) + 1
                time.sleep(KUTISH)
            time.sleep(KUTISH)
    baza.sikl_yakunla(MANBA, sikl, toliq=bool(not faqat))
    return natija


if __name__ == "__main__":
    import sys
    rejim = sys.argv[1] if len(sys.argv) > 1 else "bosh"
    # `n` berilmagan bo'lsa `chuqur` CHUQUR_SAHIFA (10) ni ishlatadi
    n = int(sys.argv[2]) if len(sys.argv) > 2 else None
    f = sys.argv[3] if len(sys.argv) > 3 else ""
    if rejim == "chuqur":
        print(chuqur(n, f))
    else:
        print(bosh(n or 1, f))
