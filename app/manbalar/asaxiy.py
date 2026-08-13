"""Asaxiy.uz — O'zbekiston onlayn do'koni (B tur: tayanch narx).

2026-08-13 da tekshirildi: sayt ochiq (HTTP 200), robots.txt faqat
xizmat yo'llarini taqiqlaydi (admin, cart, ajax, sort, profile).
SSR — oddiy HTTP yig'ish yetarli, brauzer kerak emas.

B TUR (do'kon): sotuvchi emas, NARX beradi. OBER uchun qiymati —
"bozor narxi qancha" degan savolga tayanch dalil. Kartada `biznes=1`
belgilanadi va "Asaxiy" manba belgisi bilan chiqadi.

Kategoriya sahifasi: /product/{bo'lim} — har sahifada 24 ta tovar
(SSR HTML ichida). Pagination: /product/{bo'lim}/page=2 ... (2026-08-13
tekshirildi, `page=2` -> 200, boshqa tovarlar).

Karta tuzilishi (2026-08-13):
  <div class="product__item ..." data-actual-price="5379000">
    <span class="product__item__info-title">Samsung Galaxy A57 8/256 GB</span>
    <a href="/product/smartfon-...">  (tovar sahifasi)
    <img src="https://cdn.asaxiy.uz/...">
  Narx `data-actual-price` — SO'MDA (B tur uchun bevosita narx_som).

Tovar sahifasi: /product/{slug} — `description__item` ichida tavsif
(HTML), `data-price` da narx. Chuqur rejimda tavsif olinadi.

E'lon identifikatori — `data-product-id` (raqam).
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request

import baza

MANBA = "asaxiy"
NOM = "Asaxiy"
KUTISH = 1.2          # soniya, so'rovlar orasida (saytni urishmaymiz)
_TAYANCH = "https://asaxiy.uz"
_SARLAVHA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/126.0 Safari/537.36"}

# Bo'limlar — 1-daraja kategoriyalar. OBER vertikallariga mos
# (avtoqism, elektronika, uy-ro'zg'or). `kategoriya` — qidiruvda
# ko'rinadigan o'zbekcha nom.
_BO_LIMLAR = [
    ("instrumenty-i-avtotovary", "Asboblar va avto"),
    ("telefony-i-gadzhety", "Telefon va gadjetlar"),
    ("kompyutery-i-orgtehnika", "Kompyuterlar"),
    ("bytovaya-tehnika", "Maishiy texnika"),
    ("televizory-video-i-audio", "Televizor va audio"),
    ("klimaticheskaya-tehnika", "Iqlim texnikasi"),
    ("dlya-doma", "Uy uchun"),
    ("mebel", "Mebel"),
    ("posuda", "Idish-tovoq"),
    ("sport-i-otdyh", "Sport va dam olish"),
    ("detskiye-tovari", "Bolalar tovarlari"),
    ("krasota-i-zdorove", "Go'zallik va salomatlik"),
    ("odejda-obuv-i-aksessuari", "Kiyim va aksessuarlar"),
    ("kancelyarskie-tovary", "Kanselyariya"),
    ("knigi", "Kitoblar"),
    ("suvi", "Sovg'alar"),
]


def _sozla(html: str) -> str:
    """HTML matnini tozalaydi: teglar va entitylar tashlanadi."""
    matn = re.sub(r"<[^>]+>", " ", html)
    matn = matn.replace("&nbsp;", " ").replace("&amp;", "&")
    matn = matn.replace("&quot;", '"').replace("&rsquo;", "'")
    matn = matn.replace("&lsquo;", "'").replace("&middot;", "·")
    return re.sub(r"\s+", " ", matn).strip()


class _Bloklandi(Exception):
    """Sayt bizni butunlay bloklagan (403) — qolgan bo'limlarni urmaymiz.

    2026-08-13 o'lchovi: Hetzner IP (77.42.123.90) Asaxiy tomonidan
    bloklangan — IPv4 ham, IPv6 ham 403 (saytning o'z retro-403 sahifasi,
    Cloudflare emas). Bitta 403 tasodif emas: 16 ta bo'limni ketma-ket
    urib saytni bosish yomon odat. Birinchi 403'da to'xtaymiz va sabab
    aniq ko'rinadi.
    """


def _sahifa_ol(yol: str) -> str:
    """Sahifani oladi; HTTP xatosida '' qaytaradi.

    2026-08-13: serverdan 403 kelganda urlopen HTTPError ko'tarardi va
    butun sikl to'xtab qolardi (`[yigish:asaxiy] xato` — sabab shu).
    Endi HTTPError/URLError tutib olinadi: bitta bo'lim yiqilsa qolgan
    bo'limlar davom etadi, xato sanoqqa tushadi. 403 esa alohida —
    sayt bizni butunlay bloklaganini bildiradi, `_Bloklandi` ko'tariladi.
    """
    soz = urllib.request.Request(_TAYANCH + yol, headers=_SARLAVHA)
    try:
        with urllib.request.urlopen(soz, timeout=20) as r:
            if r.status != 200:
                print(f"  [asaxiy] {yol} -> HTTP {r.status}")
                return ""
            return r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            raise _Bloklandi(f"{yol} -> HTTP 403 (sayt IP'ni bloklagan)") from e
        print(f"  [asaxiy] {yol} -> HTTP {e.code} ({e.reason})")
        return ""
    except urllib.error.URLError as e:
        print(f"  [asaxiy] {yol} -> tarmoq xatosi: {e.reason}")
        return ""


def _kartalar(sahifa: str) -> list[tuple[str, str]]:
    """Ro'yxat sahifasidagi tovarlar: (product-id, karta HTML).

    Karta chegarasi `class="product__item ` boshlanishi orqali
    ajratiladi. `product__item` so'zi karta ICHIDA ham uchraydi
    (class atributining o'zi) — shuning uchun chegarani qo'shish
    noto'g'ri bo'ladi, keyingi `class="product__item ` gacha kesamiz.
    """
    boshlar = [m.start() for m in re.finditer(r'class="product__item ', sahifa)]
    natija: list[tuple[str, str]] = []
    for i, bosh in enumerate(boshlar):
        tugash = boshlar[i + 1] if i + 1 < len(boshlar) else bosh + 20000
        blok = sahifa[bosh:tugash]
        m = re.search(r'data-product-id="(\d+)"', blok)
        if m:
            natija.append((m.group(1), blok))
    return natija


def _ro_kat(sahifa: str, kategoriya: str) -> list[dict]:
    """Ro'yxat sahifasidagi tovarlarni dict'ga aylantiradi."""
    natija: list[dict] = []
    for tashqi_id, blok in _kartalar(sahifa):
        # NOM — product__item__info-title (ro'yxatdagi yagona toza joy)
        nom = ""
        m = re.search(r'product__item__info-title[^>]*>\s*([^<]+?)\s*<', blok)
        if m:
            nom = m.group(1).strip()
        if not nom:
            m2 = re.search(r'product-name[^>]*>\s*([^<]+?)\s*<', blok)
            if m2:
                nom = m2.group(1).strip()
        if not nom:
            continue

        # HAVOLA — tovar sahifasi
        havola = ""
        m3 = re.search(r'href="(/product/[^"]+)"', blok)
        if m3:
            havola = _TAYANCH + m3.group(1)

        # NARX — data-actual-price, SO'MDA (B tur, bevosita)
        narx_som = None
        narx_asl = None
        m4 = re.search(r'data-actual-price="(\d+)"', blok)
        if m4:
            narx_som = int(m4.group(1))
            narx_asl = f"{narx_som:,}".replace(",", " ") + " so'm"

        # RASM — tovar rasmi (yurak/taqqoslash ikonkalari emas)
        rasm = ""
        rasmlar = re.findall(r'<img[^>]*?src="([^"]+)"', blok)
        for r in rasmlar:
            if "heart" in r or "compare" in r or "fav" in r:
                continue
            if r.startswith("http"):
                rasm = r
                break
            if r.startswith("//"):
                rasm = "https:" + r
                break
            if r.startswith("/"):
                rasm = _TAYANCH + r
                break

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
    sahifa = _sahifa_ol(f"/product/{slug}")
    natija: dict = {}
    if not sahifa:
        return natija
    m = re.search(r'class="description__item[^"]*"[^>]*>(.*?)</div>'
                  r'\s*</div>\s*</div>', sahifa, re.S)
    if m:
        tavsif = _sozla(m.group(1))
        # "Mahsulot ta'rifi" sarlavhasi va boshqa bezaklarni tashlaymiz
        tavsif = re.sub(r"Mahsulot ta'rifi|Mahsulot haqida|Описание", " ", tavsif)
        natija["tavsif"] = tavsif[:2000]
    mrasm = re.search(r'class="product__item__image[^"]*"[^>]*>.*?'
                      r'src="(https://[^"]+)"', sahifa, re.S)
    if not mrasm:
        mrasm = re.search(r'<img[^>]*src="(https://cdn\.asaxiy[^"]+)"', sahifa)
    if mrasm:
        natija["rasm"] = mrasm.group(1)
    return natija


def bosh(cheklov: int = 1, faqat: str = "") -> dict:
    """Tez yig'ish: har bo'limdan birinchi sahifa.

    E'lonlarni yangilaydi, hech narsani nofaol qilmaydi.
    """
    sikl = baza.sikl_boshlash(MANBA)
    natija = {"yangi": 0, "yangilandi": 0, "ozgarmadi": 0, "xato": 0}
    try:
        for slug, kategoriya in _BO_LIMLAR:
            if faqat and faqat not in slug:
                continue
            html = _sahifa_ol(f"/product/{slug}")
            if not html:
                natija["xato"] += 1
                continue
            for e in _ro_kat(html, kategoriya):
                holat = baza.saqla(e, sikl)
                natija[holat] = natija.get(holat, 0) + 1
            time.sleep(KUTISH)
    except _Bloklandi as b:
        print(f"  [asaxiy] BLOKLANDI: {b}")
        natija["xato"] += 1
    return natija


def chuqur(sahifalar: int = 3, faqat: str = "") -> dict:
    """To'liq yig'ish: ko'p sahifa + tovar tavsiflari.

    `sahifalar` — har bo'limdan nechta sahifa. Tovar tavsifi alohida
    sahifadan olinadi (baza mavjud ma'lumotni saqlab qoladi).
    """
    sikl = baza.sikl_boshlash(MANBA)
    natija = {"yangi": 0, "yangilandi": 0, "ozgarmadi": 0, "xato": 0}
    try:
        for slug, kategoriya in _BO_LIMLAR:
            if faqat and faqat not in slug:
                continue
            for sahifa in range(1, max(1, sahifalar) + 1):
                manzil = f"/product/{slug}/page={sahifa}" if sahifa > 1 \
                    else f"/product/{slug}"
                html = _sahifa_ol(manzil)
                if not html:
                    natija["xato"] += 1
                    continue
                for e in _ro_kat(html, kategoriya):
                    # Tavsif uchun slug havoladan olinadi
                    slug_tovar = ""
                    m = re.search(r"/product/([^/]+)$", e.get("havola") or "")
                    if m:
                        slug_tovar = m.group(1)
                    if slug_tovar:
                        e.update(_tavsif_ol(e["tashqi_id"], slug_tovar))
                    holat = baza.saqla(e, sikl)
                    natija[holat] = natija.get(holat, 0) + 1
                    time.sleep(KUTISH)
                time.sleep(KUTISH)
    except _Bloklandi as b:
        print(f"  [asaxiy] BLOKLANDI: {b}")
        natija["xato"] += 1
    baza.sikl_yakunla(MANBA, sikl, toliq=bool(not faqat))
    return natija


if __name__ == "__main__":
    import sys
    rejim = sys.argv[1] if len(sys.argv) > 1 else "bosh"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    f = sys.argv[3] if len(sys.argv) > 3 else ""
    if rejim == "chuqur":
        print(chuqur(n, f))
    else:
        print(bosh(n, f))
