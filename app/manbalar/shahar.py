"""Shahar.uz — O'zbekiston ko'chmas mulk e'lonlari taxtasi.

A TUR (sotuvchi beradi) — OBER uchun yangi vertikal: ko'chmas mulk.
2026-08-13 tekshiruv: server (Hetzner) dan ham ochiq (200), Asaxiy'dan
farqli o'laroq blok yo'q. Ro'yxat sahifasi SSR — brauzer kerak emas.

Kategoriyalar:
    /kvartira          — kvartira sotish (asosiy)
    /kvartira-posutochno — sutkalik ijara
    /arenda-domov      — uy ijarasi
    /arenda-kvartir    — kvartira ijarasi
    /dom               — xususiy uy sotish
    /dacha             — dala uyi

Narx DOLLARDA ko'rsatiladi (`115 000 $`) — `baza.dollar_kursi()`
orqali so'mga o'tkaziladi (avtoelon'dagi kabi). Kurs olinmasa
narx_som=None — karta narxsiz chiqadi, qidiruv buzilmaydi.

Karta tuzilishi (2026-08-13 o'lchov, 21 karta/sahifa):
    <a href="/kvartira/prodaja-...-149650">
      <img class="img-thumbnail" src="/img/data/...jpg">
      <div class="box_type"><b>115 000 $</b></div>
      <div class="boxed_mini_details"> xonalar, qavat, maydon </div>
      <small class="optype22 small_title"> Продажа квартира ... </small>
      <div class="property_desc"> 13-08-2026 </div>
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request

import baza

MANBA = "shahar"
NOM = "Shahar.uz"
KUTISH = 1.0            # soniya, so'rovlar orasida (saytni urishmaymiz)
_TAYANCH = "https://shahar.uz"
_SARLAVHA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/126.0 Safari/537.36"}

# (slug, o'zbekcha kategoriya, OBER kategoriyasi)
_BO_LIMLAR = [
    ("kvartira", "kvartira sotish", "Ko'chmas mulk"),
    ("arenda-kvartir", "kvartira ijara", "Ko'chmas mulk"),
    ("kvartira-posutochno", "kvartira sutkalik ijara", "Ko'chmas mulk"),
    ("doma", "xususiy uy sotish", "Ko'chmas mulk"),
    ("arenda-domov", "uy ijara", "Ko'chmas mulk"),
    ("dacha", "dala uyi", "Ko'chmas mulk"),
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

    HTTPError/URLError tutib olinadi — bitta bo'lim yiqilsa qolgan
    bo'limlar davom etadi, xato sanoqqa tushadi.
    """
    soz = urllib.request.Request(_TAYANCH + yol, headers=_SARLAVHA)
    try:
        with urllib.request.urlopen(soz, timeout=20) as r:
            if r.status != 200:
                print(f"  [shahar] {yol} -> HTTP {r.status}")
                return ""
            return r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"  [shahar] {yol} -> HTTP {e.code} ({e.reason})")
        return ""
    except urllib.error.URLError as e:
        print(f"  [shahar] {yol} -> tarmoq xatosi: {e.reason}")
        return ""


def _narx_qiymat(raqam: int | None) -> tuple[int | None, str | None]:
    """Dollar narxni so'mga o'tkazadi.

    `115 000 $` -> narx_asl "115 000 $" + narx_som kursga ko'paytirilgan.
    Kurs olinmasa narx_som=None — karta narxsiz chiqadi, qidiruv
    buzilmaydi (avtoelon'dagi xuddi shu qoida).
    """
    if not raqam:
        return None, None
    narx_asl = f"{raqam:,}".replace(",", " ") + " $"
    kurs = baza.dollar_kursi()
    if not kurs or not kurs.get("kurs"):
        return None, narx_asl
    return raqam * kurs["kurs"], narx_asl


def _kartalar(sahifa: str, bo_lim: str) -> list[tuple[str, str, str]]:
    """Ro'yxat sahifasidagi e'lonlar: (tashqi_id, havola, karta HTML).

    Karta `property_wrapper` div'idan boshlanadi va keyingi
    `property_wrapper`gacha cho'ziladi. ID va havola karta ICHIDAGI
    `<a href="/.../...-{id}">` dan olinadi.

    2026-08-13: bo'lim slug'iga bog'lash XATO edi — URL naqshi bo'limga
    mos kelmaydi (`arenda-kvartir` sahifasida `/kvartira/...` havolalar,
    `arenda-domov` da `/doma/...`). Shahar.uz bo'lim sahifasida ham
    boshqa bo'limlarning e'lonlari chiqishi mumkin.
    """
    boshlar = [m.start() for m in re.finditer(
        r'class="property_wrapper[^"]*"', sahifa)]
    natija: list[tuple[str, str, str]] = []
    for i, bosh in enumerate(boshlar):
        tugash = boshlar[i + 1] if i + 1 < len(boshlar) else bosh + 30000
        blok = sahifa[bosh:tugash]
        m = re.search(r'<a href="(/[^"]+-\d+)"', blok)
        if not m:
            continue
        mm = re.search(r'-(\d+)$', m.group(1))
        if not mm:
            continue
        natija.append((mm.group(1), m.group(1), blok))
    return natija


def _ro_kat(sahifa: str, bo_lim: str, kategoriya: str) -> list[dict]:
    """Ro'yxat sahifasidagi e'lonlarni dict'ga aylantiradi."""
    natija: list[dict] = []
    for tashqi_id, havola_yol, blok in _kartalar(sahifa, bo_lim):
        # NOM — `small_title` blokidan (masalan "Продажа квартира ...")
        nom = ""
        ms = re.search(r'optype22 small_title">(.*?)</small>', blok, re.S)
        if ms:
            nom = _sozla(ms.group(1))
        if not nom:
            continue
        # Joylashuv ajratish: "Продажа квартира Ташкент, Яккасарай Бобур"
        # -> shahar="Ташкент" (verguldan OLDINGI so'z — har doim shahar)
        shahar = ""
        mj = re.search(r"([А-ЯЁа-яё]+)\s*,", nom)
        if mj:
            shahar = mj.group(1)
        # Kategoriya ALOHIDA maydonda beriladi (`kategoriya` ustuni) —
        # sarlavhaga prefiks qo'shish XATO: "Ko'chmas mulk — " sarlavhani
        # uzaytirib, qidiruv ballini pasaytirardi (qisqa sarlavha bonusi
        # va so'z pozitsiyasi; 2026-08-13 o'lchov: shahar e'lonlari 783-o'rin).

        # NARX — `<b>115 000 $</b>` (box_type bloki)
        narx_som, narx_asl = None, None
        mn = re.search(r"<b>\s*([\d\s.]+)\s*\$?\s*</b>", blok)
        if mn:
            raqam_txt = re.sub(r"\s", "", mn.group(1))
            try:
                raqam = int(float(raqam_txt))
            except ValueError:
                raqam = 0
            if raqam:
                narx_som, narx_asl = _narx_qiymat(raqam)

        # TAVSIF — xonalar, qavat, maydon (boxed_mini_details)
        xususiyatlar: dict[str, str] = {}
        md = re.search(r'class="boxed_mini_details[^"]*">(.*?)</div>',
                       blok, re.S)
        if md:
            for tm in re.finditer(
                    r"<strong>([^<]+)</strong><span[^>]*></span>\s*([^<]+)",
                    md.group(1)):
                kalit = _sozla(tm.group(1))
                qiymat = tm.group(2).strip()
                if kalit and qiymat:
                    xususiyatlar[kalit] = qiymat

        # SANA — `glyphicon-calendar` dan keyin
        sana = ""
        dm = re.search(r"glyphicon-calendar\"></i>\s*([\d\-\.]+)", blok)
        if dm:
            sana = dm.group(1).strip()[:10]

        # RASM — `img-thumbnail` src (to'liq URL)
        rasm = ""
        mr = re.search(r'<img[^>]*src="(/img/[^"]+)"', blok)
        if mr:
            rasm = _TAYANCH + mr.group(1)

        e = {
            "manba": MANBA, "tashqi_id": tashqi_id, "nom": nom,
            "narx_som": narx_som, "narx_asl": narx_asl,
            "shahar": shahar, "sana": sana,
            "havola": f"{_TAYANCH}{havola_yol}",
            "rasm": rasm,
            "kategoriya": kategoriya,
        }
        if xususiyatlar:
            e["xususiyatlar"] = json.dumps(xususiyatlar,
                                           ensure_ascii=False)
        natija.append(e)
    return natija


def _tavsif_ol(havola: str) -> dict:
    """E'lon sahifasidan tavsif va katta rasmni oladi."""
    natija: dict = {}
    # Havoladan yo'l olish: /kvartira/prodaja-...-149650
    m = re.search(r"https://shahar\.uz(/[^\s]+)", havola)
    if not m:
        return natija
    yol = m.group(1)
    sahifa = _sahifa_ol(yol)
    if not sahifa:
        return natija
    md = re.search(r'<meta name="description" content="([^"]+)"', sahifa)
    if md:
        natija["tavsif"] = md.group(1).replace("&quot;", '"')[:2000]
    mr = re.search(r'<meta property="og:image" content="([^"]+)"', sahifa)
    if mr:
        natija["rasm"] = mr.group(1)
    return natija


def bosh(cheklov: int = 1, faqat: str = "") -> dict:
    """Tez yig'ish: har bo'limdan birinchi sahifa.

    E'lonlarni yangilaydi, hech narsani nofaol qilmaydi.
    """
    sikl = baza.sikl_boshlash(MANBA)
    natija = {"yangi": 0, "yangilandi": 0, "ozgarmadi": 0, "xato": 0}
    for slug, _, kategoriya in _BO_LIMLAR:
        if faqat and faqat not in slug:
            continue
        html = _sahifa_ol(f"/{slug}")
        if not html:
            natija["xato"] += 1
            continue
        for e in _ro_kat(html, slug, kategoriya):
            holat = baza.saqla(e, sikl)
            natija[holat] = natija.get(holat, 0) + 1
        time.sleep(KUTISH)
    return natija


def chuqur(sahifalar: int = 3, faqat: str = "") -> dict:
    """To'liq yig'ish: ko'p sahifa + e'lon tavsiflari.

    `sahifalar` — har bo'limdan nechta sahifa. E'lon tavsifi alohida
    sahifadan olinadi (baza mavjud ma'lumotni saqlab qoladi).
    """
    sikl = baza.sikl_boshlash(MANBA)
    natija = {"yangi": 0, "yangilandi": 0, "ozgarmadi": 0, "xato": 0}
    for slug, _, kategoriya in _BO_LIMLAR:
        if faqat and faqat not in slug:
            continue
        for sahifa in range(1, max(1, sahifalar) + 1):
            manzil = f"/{slug}?page={sahifa}" if sahifa > 1 else f"/{slug}"
            html = _sahifa_ol(manzil)
            if not html:
                natija["xato"] += 1
                continue
            for e in _ro_kat(html, slug, kategoriya):
                e.update(_tavsif_ol(e.get("havola") or ""))
                holat = baza.saqla(e, sikl)
                natija[holat] = natija.get(holat, 0) + 1
                time.sleep(KUTISH)
            time.sleep(KUTISH)
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
