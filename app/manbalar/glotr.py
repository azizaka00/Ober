"""Glotr.uz — O'zbekiston onlayn do'koni (B tur: tayanch narx).

2026-08-13 da tekshirildi: sayt serverdan ochiq (HTTP 200, Asaxiy'dan
farqli — blok yo'q), robots.txt faqat /search ni taqiqlaydi (kategoriya
va tovar sahifalari ochiq). SSR — oddiy HTTP yig'ish yetarli.

B TUR (do'kon): sotuvchi emas, NARX beradi. OBER uchun qiymati —
"bozor narxi qancha" degan savolga tayanch dalil. Kartada `biznes=1`
belgilanadi va "Glotr" manba belgisi bilan chiqadi.

Kategoriya sahifasi: /{bo'lim}/ — har sahifada ~56 karta. Pagination:
?page=2 ... (2026-08-13 tekshirildi, page=2 -> 200, boshqa tovarlar).

Karta tuzilishi (2026-08-13):
  <div class='product-card__header'>
    <a href="/{slug}-p-{id}/" class='product-card__swiper ...'>
      <img ... data-src='https://files.glotr.uz/...' title='NOM'>
  ...
    <div class="price-retail proposal-price"> 244 000 <span>сум / шт.</span>

Narx SO'MDA (B tur uchun bevosita narx_som, konvertatsiya kerak emas).
NOM — rasm `title` atributida. HAVOLA — `-p-{id}` naqshidagi slug.
ID — havola oxiridagi raqam.

Tovar sahifasi: /{slug}-p-{id}/ — `description` meta tegi tavsif beradi
(2026-08-13 tekshirildi). Chuqur rejimda tavsif olinadi.
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request

import baza

MANBA = "glotr"
NOM = "Glotr"
KUTISH = 1.2          # soniya, so'rovlar orasida (saytni urishmaymiz)
# To'liq (sutkalik) sikl nechta sahifa yig'adi — har bo'lim uchun.
# Avtoelon/Shahar bilan bir xil: 10 sahifa x ~56 karta = ~560 e'lon/bo'lim.
CHUQUR_SAHIFA = 10
_TAYANCH = "https://glotr.uz"
_SARLAVHA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/126.0 Safari/537.36"}

# Bo'limlar — Glotr katalogi (2026-08-13 bosh sahifadan olingan).
# OBER vertikallariga mos bo'lganlari tanlandi. `kategoriya` — qidiruvda
# ko'rinadigan o'zbekcha nom.
_BO_LIMLAR = [
    ("avtotovari", "Avto tovarlar"),
    ("transport", "Transport"),
    ("telefoni-i-plansheti", "Telefon va planshetlar"),
    ("kompyuteri", "Kompyuterlar"),
    ("fototexnika", "Foto va video"),
    ("bitovaya-texnika", "Maishiy texnika"),
    ("videotexnika", "Video va audio"),
    ("audiotexnika", "Audio texnika"),
    ("instrumenti", "Asboblar"),
    ("stroymateriali", "Qurilish materiallari"),
    ("tovari-dlya-remonta", "Ta'mirlash uchun"),
    ("dlya-doma-i-sada", "Uy va bog'"),
    ("mebel", "Mebel"),
    ("detskie-tovari", "Bolalar tovarlari"),
    ("sporttovari", "Sport tovarlari"),
    ("knigi", "Kitoblar"),
    ("zootovari", "Hayvonlar uchun"),
    ("zdorove-i-krasota", "Go'zallik va salomatlik"),
    ("sumki-i-chemodani", "Sumka va chamadonlar"),
    ("ukrasheniya", "Taqinchoqlar"),
    ("galantereya", "Galantereya"),
]


def _sozla(html: str) -> str:
    """HTML matnini tozalaydi: teglar va entitylar tashlanadi."""
    matn = re.sub(r"<[^>]+>", " ", html)
    matn = matn.replace("&nbsp;", " ").replace("&amp;", "&")
    matn = matn.replace("&quot;", '"').replace("&rsquo;", "'")
    matn = matn.replace("&lsquo;", "'").replace("&middot;", "·")
    return re.sub(r"\s+", " ", matn).strip()


def _sahifa_ol(yol: str) -> str:
    """Sahifani oladi; HTTP xatosida '' qaytaradi.

    HTTPError/URLError tutib olinadi: bitta bo'lim yiqilsa qolgan
    bo'limlar davom etadi, xato sanoqqa tushadi. (Asaxiy'dagi kabi
    alohida `_Bloklandi` kerak emas — Glotr serverdan ochiq, 403
    kutilmaydi.)
    """
    soz = urllib.request.Request(_TAYANCH + yol, headers=_SARLAVHA)
    try:
        with urllib.request.urlopen(soz, timeout=20) as r:
            if r.status != 200:
                print(f"  [glotr] {yol} -> HTTP {r.status}")
                return ""
            return r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"  [glotr] {yol} -> HTTP {e.code} ({e.reason})")
        return ""
    except urllib.error.URLError as e:
        print(f"  [glotr] {yol} -> tarmoq xatosi: {e.reason}")
        return ""


def _kartalar(sahifa: str) -> list[tuple[str, str]]:
    """Ro'yxat sahifasidagi tovarlar: (tashqi_id, karta HTML).

    Karta chegarasi `product-card__header` boshlanishi orqali
    ajratiladi (har kartada bittadan bor). ID — havoladagi `-p-{id}`
    naqshining oxiridagi raqam.
    """
    boshlar = [m.start() for m in re.finditer(r"product-card__header", sahifa)]
    natija: list[tuple[str, str]] = []
    for i, bosh in enumerate(boshlar):
        tugash = boshlar[i + 1] if i + 1 < len(boshlar) else bosh + 20000
        blok = sahifa[bosh:tugash]
        m = re.search(r'href="/([^"]*?)-p-(\d+)/"', blok)
        if m:
            natija.append((m.group(2), blok))
    return natija


def _ro_kat(sahifa: str, kategoriya: str) -> list[dict]:
    """Ro'yxat sahifasidagi tovarlarni dict'ga aylantiradi."""
    natija: list[dict] = []
    for tashqi_id, blok in _kartalar(sahifa):
        # NOM — rasm `title` atributida (yagona toza joy, 2026-08-13)
        # Qavs ichida TO'LIQ qiymat olinadi: `title='Склад телефон...'`
        # Non-greedy qolip birinchi 5 belgida to'xtab qolgandi —
        # "Склад", "Брасл" kabi kesilgan nomlar yig'ildi (2026-08-13
        # o'lchov: 8 ta namunadan 6 tasi kesilgan edi).
        nom = ""
        m = re.search(r'title=["\']([^"\']+)["\']', blok)
        if m:
            nom = m.group(1).strip()
        if not nom:
            m2 = re.search(r'<h3[^>]*>([^<]+)</h3>', blok)
            if m2:
                nom = m2.group(1).strip()
        if not nom:
            continue

        # HAVOLA — tovar sahifasi (slug)
        havola = ""
        m3 = re.search(r'href="(/[^"]*-p-\d+/)"', blok)
        if m3:
            havola = _TAYANCH + m3.group(1)

        # NARX — price-retail klassida, SO'MDA (B tur, bevosita)
        narx_som = None
        narx_asl = None
        m4 = re.search(r'price-retail[^>]*>\s*([0-9][0-9 ]{2,20})', blok)
        if m4:
            narx_som = int(re.sub(r"\s", "", m4.group(1)))
            narx_asl = f"{narx_som:,}".replace(",", " ") + " so'm"

        # RASM — files.glotr.uz dagi tovar rasmi (data-src)
        rasm = ""
        m5 = re.search(r'data-src="(https://files\.glotr\.uz/[^"]+)"', blok)
        if not m5:
            m5 = re.search(r'data-src=\'(https://files\.glotr\.uz/[^\']+)\'', blok)
        if m5:
            rasm = m5.group(1)

        natija.append({
            "manba": MANBA, "tashqi_id": tashqi_id, "nom": nom,
            "narx_som": narx_som, "narx_asl": narx_asl,
            "viloyat": "Toshkent", "shahar": "Toshkent",
            "sana": "", "havola": havola, "rasm": rasm,
            "biznes": 1, "kategoriya": kategoriya,
        })
    return natija


def _tavsif_ol(tashqi_id: str, slug: str) -> dict:
    """Tovar sahifasidan tavsif va katta rasmni oladi."""
    sahifa = _sahifa_ol(f"/{slug}-p-{tashqi_id}/")
    natija: dict = {}
    if not sahifa:
        return natija
    # Tavsif — meta description tegi (2026-08-13 tekshirildi):
    # "Купить ... в Ташкенте ⚡️ Цена 216 000 сум ⚡️ Наличие, фото ..."
    m = re.search(r'name="description"\s+content="([^"]+)"', sahifa)
    if m:
        tavsif = m.group(1)
        # "Купить X в Ташкенте" bezagini tashlaymiz — toza tavsif qolsin
        tavsif = re.sub(r"^Купить\s+.{0,120}?\s+в\s+[А-ЯЁа-яё]+(?:е)?,\s*"
                        r"Узбекистане\s*[⚡️|]*\s*Цена\s+[\d\s]+\s+сум\s*"
                        r"[⚡️|]*\s*", " ", tavsif, flags=re.S)
        natija["tavsif"] = _sozla(tavsif)[:2000]
    mrasm = re.search(r'<img[^>]*class="[^"]*main-photo[^"]*"[^>]*'
                      r'src="(https://[^"]+)"', sahifa)
    if not mrasm:
        mrasm = re.search(r'<meta property="og:image"\s+content="([^"]+)"', sahifa)
    if mrasm:
        natija["rasm"] = mrasm.group(1)
    return natija


def bosh(cheklov: int = 1, faqat: str = "") -> dict:
    """Tez yig'ish: har bo'limdan birinchi sahifa.

    E'lonlarni yangilaydi, hech narsani nofaol qilmaydi.
    """
    sikl = baza.sikl_boshlash(MANBA)
    natija = {"yangi": 0, "yangilandi": 0, "ozgarmadi": 0, "xato": 0}
    for slug, kategoriya in _BO_LIMLAR:
        if faqat and faqat not in slug:
            continue
        html = _sahifa_ol(f"/{slug}/")
        if not html:
            natija["xato"] += 1
            continue
        for e in _ro_kat(html, kategoriya):
            holat = baza.saqla(e, sikl)
            natija[holat] = natija.get(holat, 0) + 1
        time.sleep(KUTISH)
    return natija


def chuqur(sahifalar: int | None = None, faqat: str = "") -> dict:
    """To'liq yig'ish: ko'p sahifa + tovar tavsiflari.

    `sahifalar` — har bo'limdan nechta sahifa (default: CHUQUR_SAHIFA).
    Tovar tavsifi alohida sahifadan olinadi (baza mavjud ma'lumotni
    saqlab qoladi).
    """
    if sahifalar is None:
        sahifalar = CHUQUR_SAHIFA
    sikl = baza.sikl_boshlash(MANBA)
    natija = {"yangi": 0, "yangilandi": 0, "ozgarmadi": 0, "xato": 0}
    for slug, kategoriya in _BO_LIMLAR:
        if faqat and faqat not in slug:
            continue
        for sahifa in range(1, max(1, sahifalar) + 1):
            manzil = f"/{slug}/?page={sahifa}" if sahifa > 1 else f"/{slug}/"
            html = _sahifa_ol(manzil)
            if not html:
                natija["xato"] += 1
                continue
            for e in _ro_kat(html, kategoriya):
                # Slug havoladan olinadi (tavsif sahifasi uchun)
                slug_tovar = ""
                m = re.search(r"/glotr\.uz/([^/]+?)-p-\d+/$",
                              e.get("havola") or "")
                if not m:
                    m = re.search(r"/([^/]+?)-p-\d+/$", e.get("havola") or "")
                if m:
                    slug_tovar = m.group(1)
                if slug_tovar:
                    e.update(_tavsif_ol(e["tashqi_id"], slug_tovar))
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
