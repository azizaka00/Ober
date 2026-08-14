"""Avizinfo.uz — O'zbekiston e'lonlar taxtasi (A tur: sotuvchi beradi).

2026-08-14 da tekshirildi: sayt serverdan ochiq (HTTP 200), robots.txt
e'lon sahifalarini taqiqlamaydi. SSR — oddiy HTTP yig'ish yetarli.

A TUR (e'lonlar taxtasi): sotuvchi o'zi e'lon qo'yadi. OBER uchun
qiymati — bozor taklifi, OLX'ga o'xshash lekin o'z auditoriyasi.

Har shahar alohida SUBDOMEN: tashkent.avizinfo.uz, andijan.avizinfo.uz...
Har birida bir xil kategoriya tuzilishi. Hozircha Toshkent (eng katta),
`_SHAHARLAR` ro'yxatiga qo'shish orqali boshqalari ham ochiladi.

URL tuzilishi (2026-08-14):
  Kategoriya:  /ru-i-ads-i-category-i-{slug}.html
  Pagination:  /ru-i-ads-i-page-i-{n}-1-i-category-i-{slug}.html
  E'lon:       /ru-i-offer-i-category-i-{slug}-i-id-i-{id}-i-{nom}.html

Karta tuzilishi (ro'yxat sahifasi):
  <a href="/ru-i-offer-...-i-id-i-538407-...html">
    <picture><source data-srcset=".../300-300-1/...jpg" alt="NOM #538407">
    <img data-src="https://tashkent.avizinfo.uz/content/c/300-300-1/...">
  <div class="product-info">
    <h3 class="item-title"><a href="...">NOM</a></h3>
    <div class="item-tag"><span>21.07.2026, 08:12</span></div>
    <ul class="entry-meta">
      <li><a href="...category...">Авто запчасти</a></li>
      <li><a href="...">Ташкент</a></li>
    <div class="item-price font-weight-bold ribbon3 green sm">
      2 500 000 сўм

Narx SO'MDA (`сўм` belgisi bilan) — konvertatsiya kerak emas.
ID — havoladagi `i-id-i-{id}` naqshi.
Rasm — `data-src` (300x300). E'lon sahifasida 800x600 kattaligi bor
(chuqur rejimda tavsif bilan birga olinadi).

E'lon sahifasi: `ad-text` klassida tavsif, `ai-ad-price` da narx,
`ad-gallery` da katta rasm (chuqur rejim uchun).
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request

import baza

MANBA = "avizinfo"
NOM = "Avizinfo"
KUTISH = 1.0          # soniya, so'rovlar orasida (saytni urishmaymiz)
# To'liq (sutkalik) sikl nechta sahifa yig'adi — har bo'lim uchun.
CHUQUR_SAHIFA = 10
_TAYANCH = "https://tashkent.avizinfo.uz"
_SARLAVHA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/126.0 Safari/537.36"}

# Shaharlar — har biri alohida subdomen, bir xil kategoriya tuzilishi.
# Toshkent eng katta; Andijon/Samarqand/Buxoro 2026-08-14 da qo'shildi
# (serverdan ochiq, bir xil karta tuzilishi). Kichik shaharlarda ba'zi
# bo'limlar bo'sh bo'lishi mumkin — bu xato emas, karta 0 chiqadi.
_SHAHARLAR = [
    ("tashkent", "Toshkent"),
    ("andijan", "Andijon"),
    ("samarkand", "Samarqand"),
    ("buhara", "Buxoro"),
]

# Bo'limlar — 1-daraja kategoriyalar. OBER vertikallariga mos bo'lganlari.
# `kategoriya` — qidiruvda ko'rinadigan o'zbekcha nom.
_BO_LIMLAR = [
    ("avtomobili", "Avtomobillar"),
    ("legkovye-avtomobili", "Yengil avtomobillar"),
    ("avto-zapchasti", "Avto ehtiyot qismlar"),
    ("moto-zapchasti", "Moto ehtiyot qismlar"),
    ("velosipedy", "Velosipedlar"),
    ("kompijutery-orgtehnika", "Kompyuterlar"),
    ("tehnika-dlja-doma", "Uy texnikasi"),
    ("mebeli-komfort", "Mebel"),
    ("stroitelistvo-remont", "Qurilish va ta'mirlash"),
    ("detskij-mir", "Bolalar dunyosi"),
    ("turizm-sport-otdyh", "Turizm va sport"),
    ("zdorovie-krasota", "Go'zallik va salomatlik"),
    ("rastenija-zhivotnye-ptitsy", "O'simlik va hayvonlar"),
    ("tovary-materialy", "Tovarlar"),
]


def _sozla(html: str) -> str:
    """HTML matnini tozalaydi: teglar va entitylar tashlanadi."""
    matn = re.sub(r"<[^>]+>", " ", html)
    matn = matn.replace("&nbsp;", " ").replace("&amp;", "&")
    matn = matn.replace("&quot;", '"').replace("&rsquo;", "'")
    matn = matn.replace("&lsquo;", "'").replace("&middot;", "·")
    return re.sub(r"\s+", " ", matn).strip()


def _sahifa_ol(yol: str, tayanch: str | None = None) -> str:
    """Sahifani oladi; HTTP xatosida '' qaytaradi.

    HTTPError/URLError tutib olinadi: bitta bo'lim yiqilsa qolgan
    bo'limlar davom etadi, xato sanoqqa tushadi.
    """
    baza_manzil = tayanch or _TAYANCH
    soz = urllib.request.Request(baza_manzil + yol, headers=_SARLAVHA)
    try:
        with urllib.request.urlopen(soz, timeout=20) as r:
            if r.status != 200:
                print(f"  [avizinfo] {yol} -> HTTP {r.status}")
                return ""
            return r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"  [avizinfo] {yol} -> HTTP {e.code} ({e.reason})")
        return ""
    except urllib.error.URLError as e:
        print(f"  [avizinfo] {yol} -> tarmoq xatosi: {e.reason}")
        return ""


def _kartalar(sahifa: str) -> list[tuple[str, str]]:
    """Ro'yxat sahifasidagi e'lonlar: (tashqi_id, karta HTML).

    Karta `ru-i-offer-...-i-id-i-{id}-...` havolasi bilan boshlanadi
    va keyingi `ru-i-offer` havolasigacha cho'ziladi. ID — havoladagi
    `i-id-i-` naqshidan keyingi raqam.
    """
    # Karta `product-info` klassidan boshlanadi (rasm bloki undan oldin
    # kelsa ham, nom/narx/sana shu yerda) va keyingi `product-info` gacha
    # cho'ziladi. ID — ichidagi `ru-i-offer-...-i-id-i-{id}` havolasidan.
    boshlar = [m.start() for m in re.finditer(r'class="product-info"', sahifa)]
    natija: list[tuple[str, str]] = []
    for i, bosh in enumerate(boshlar):
        tugash = boshlar[i + 1] if i + 1 < len(boshlar) else bosh + 20000
        blok = sahifa[bosh:tugash]
        m = re.search(r"i-id-i-(\d+)", blok)
        if m:
            natija.append((m.group(1), blok))
    return natija


def _ro_kat(sahifa: str, kategoriya: str, shahar: str) -> list[dict]:
    """Ro'yxat sahifasidagi e'lonlarni dict'ga aylantiradi."""
    natija: list[dict] = []
    for tashqi_id, blok in _kartalar(sahifa):
        # NOM — item-title (h3 ichidagi a) yoki rasm alt
        nom = ""
        m = re.search(r'class="item-title"[^>]*>\s*<a[^>]*>([^<]+)</a>', blok)
        if m:
            nom = m.group(1).strip()
        if not nom:
            m2 = re.search(r'alt="([^"]+)"', blok)
            if m2:
                # alt oxiridagi "#{id}" bezagini tashlaymiz
                nom = re.sub(r"\s*#\d+\s*$", "", m2.group(1)).strip()
        if not nom:
            continue

        # HAVOLA — to'liq URL (ru-i-offer...)
        havola = ""
        m3 = re.search(r'href="(https://[^"]*ru-i-offer[^"]*)"', blok)
        if not m3:
            m3 = re.search(r'href="(/[^"]*ru-i-offer[^"]*)"', blok)
        if m3:
            h = m3.group(1)
            havola = h if h.startswith("http") else _TAYANCH + h

        # NARX — item-price klassida, SO'MDA. Div ichida ko'p bo'shliq
        # va `&nbsp;` bo'lishi mumkin — butun div matnini tozalab olamiz.
        narx_som = None
        narx_asl = None
        m4 = re.search(r'class="item-price[^"]*"[^>]*>(.*?)</div>', blok, re.S)
        if m4:
            narx_matn = _sozla(m4.group(1))
            mraqam = re.search(r"([0-9][0-9 \u00a0]{2,18})", narx_matn)
            if mraqam:
                raqam = int(re.sub(r"[^\d]", "", mraqam.group(1)))
                if raqam > 0:
                    narx_som = raqam
                    narx_asl = f"{raqam:,}".replace(",", " ") + " so'm"

        # RASM — data-src (300x300)
        rasm = ""
        m5 = re.search(r'data-src="(https://[^"]+)"', blok)
        if m5:
            rasm = m5.group(1)
            # Kattaroq o'lcham (800x600 e'lon sahifasida, lekin ro'yxatda
            # 300x300 bor — shu qoladi, yig'ish yengil bo'lsin)
            rasm = rasm.replace("/c/300-300-", "/c/800-600-")

        # SANA — item-tag ichida "21.07.2026, 08:12"
        sana = ""
        m6 = re.search(r'class="item-tag"[^>]*>.*?<span>([^<]+)</span>', blok, re.S)
        if m6:
            sana = m6.group(1).strip()[:10]   # "21.07.2026"

        # SHAHAR — entry-meta ichidagi ikkinchi li (avval kategoriya)
        e_shahar = shahar
        m7 = re.findall(r'class="entry-meta[^"]*"[^>]*>(.*?)</ul>', blok, re.S)
        if m7:
            li = re.findall(r"<li[^>]*>(.*?)</li>", m7[0], re.S)
            if len(li) >= 2:
                joy = _sozla(li[1])
                if joy:
                    e_shahar = joy

        natija.append({
            "manba": MANBA, "tashqi_id": tashqi_id, "nom": nom,
            "narx_som": narx_som, "narx_asl": narx_asl,
            "viloyat": shahar, "shahar": e_shahar,
            "sana": sana, "havola": havola, "rasm": rasm,
            "kategoriya": kategoriya,
        })
    return natija


def _tavsif_ol(tashqi_id: str, havola: str) -> dict:
    """E'lon sahifasidan tavsif va katta rasmni oladi."""
    # Havola TO'LIQ URL (shahar subdomeni bilan) — `_sahifa_ol` tayanch
    # qo'shmasdan ochishi uchun domenni ajratamiz. 2026-08-14: boshqa
    # shaharlar (andijan, samarkand...) qo'shildi — faqat tashkent emas.
    import re as _re
    m = _re.match(r"(https://[^/]+)(/.*)", havola or "")
    if not m:
        return {}
    tayanch, yol = m.group(1), m.group(2)
    sahifa = _sahifa_ol(yol, tayanch)
    natija: dict = {}
    if not sahifa:
        return natija
    # TAVSIF — ad-text klassida (xususiyatlar bilan birga keladi)
    m = re.search(r'class="ad-text[^"]*"[^>]*>(.*?)</div>', sahifa, re.S)
    if m:
        tavsif = _sozla(m.group(1))
        # "Тип объявления:" kabi xususiyat sarlavhalarini tozalaymiz
        tavsif = re.sub(r"(?:Тип объявления|Тип|Категория|Описание)\s*:?\s*",
                        " ", tavsif)
        natija["tavsif"] = tavsif[:2000]
    # KATTA RASM — ad-gallery ichida
    mrasm = re.search(r'class="ad-gallery[^"]*"[^>]*>.*?'
                      r'src="(https://[^"]+)"', sahifa, re.S)
    if mrasm:
        natija["rasm"] = mrasm.group(1)
    return natija


def bosh(cheklov: int = 1, faqat: str = "") -> dict:
    """Tez yig'ish: har bo'limdan birinchi sahifa (Toshkent).

    E'lonlarni yangilaydi, hech narsani nofaol qilmaydi.
    """
    sikl = baza.sikl_boshlash(MANBA)
    natija = {"yangi": 0, "yangilandi": 0, "ozgarmadi": 0, "xato": 0}
    for shahar_slug, shahar in _SHAHARLAR:
        tayanch = f"https://{shahar_slug}.avizinfo.uz"
        for slug, kategoriya in _BO_LIMLAR:
            if faqat and faqat not in slug:
                continue
            html = _sahifa_ol(f"/ru-i-ads-i-category-i-{slug}.html", tayanch)
            if not html:
                natija["xato"] += 1
                continue
            for e in _ro_kat(html, kategoriya, shahar):
                holat = baza.saqla(e, sikl)
                natija[holat] = natija.get(holat, 0) + 1
            time.sleep(KUTISH)
    return natija


def chuqur(sahifalar: int | None = None, faqat: str = "") -> dict:
    """To'liq yig'ish: ko'p sahifa + har e'lon sahifasidan tavsif."""
    if sahifalar is None:
        sahifalar = CHUQUR_SAHIFA
    sikl = baza.sikl_boshlash(MANBA)
    natija = {"yangi": 0, "yangilandi": 0, "ozgarmadi": 0, "xato": 0}
    for shahar_slug, shahar in _SHAHARLAR:
        tayanch = f"https://{shahar_slug}.avizinfo.uz"
        for slug, kategoriya in _BO_LIMLAR:
            if faqat and faqat not in slug:
                continue
            for sahifa in range(1, max(1, sahifalar) + 1):
                if sahifa == 1:
                    manzil = f"/ru-i-ads-i-category-i-{slug}.html"
                else:
                    manzil = (f"/ru-i-ads-i-page-i-{sahifa}-1-i-category-i-"
                              f"{slug}.html")
                html = _sahifa_ol(manzil, tayanch)
                if not html:
                    natija["xato"] += 1
                    continue
                for e in _ro_kat(html, kategoriya, shahar):
                    # Tavsif — faqat havola to'liq bo'lsa (alohida sahifa)
                    if e.get("havola"):
                        e.update(_tavsif_ol(e["tashqi_id"], e["havola"]))
                    holat = baza.saqla(e, sikl)
                    natija[holat] = natija.get(holat, 0) + 1
                    time.sleep(KUTISH)
                time.sleep(KUTISH)
    baza.sikl_yakunla(MANBA, sikl, toliq=bool(not faqat))
    return natija


if __name__ == "__main__":
    import sys
    rejim = sys.argv[1] if len(sys.argv) > 1 else "bosh"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else None
    f = sys.argv[3] if len(sys.argv) > 3 else ""
    if rejim == "chuqur":
        print(chuqur(n, f))
    else:
        print(bosh(n or 1, f))
