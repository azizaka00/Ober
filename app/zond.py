"""
OBER — ZOND (probe)
Maqsad: OLX sahifasining ICHKI tuzilishini aniqlash.

Nega kerak: parser yozish uchun HTML ichida ma'lumot qanday saqlanishini
bilish shart. Zamonaviy saytlar ko'pincha ma'lumotni JSON blok ichida
beradi (__NEXT_DATA__ kabi) — agar shunday bo'lsa, parser ancha sodda
va barqaror bo'ladi.

Ishga tushirish: ZOND.bat (yoki: python zond.py)
Natija: ober/data/zond/ papkasiga saqlanadi.
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent.parent          # ober/
OUT = BASE / "data" / "zond"

# Hurmat bilan: o'zimizni tanitamiz, sekin so'raymiz
UA = "OberBot/0.1 (+https://ober.uz; aloqa: uznaiza@gmail.com)"
KUTISH = 2.0                                            # so'rovlar orasida soniya

SAHIFALAR = {
    # nom: URL
    "olx_kategoriya": "https://www.olx.uz/transport/avtozapchasti-i-aksessuary/avtozapchasti/",
    "olx_qidiruv": "https://www.olx.uz/transport/avtozapchasti-i-aksessuary/q-neksiya-kolodka/",
    "olx_elon": "https://www.olx.uz/d/obyavlenie/perednyaya-tormoznaya-kolodka-dlya-neksiya-ID30KUS.html",
}


def yukla(url: str) -> str:
    req = Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "uz,ru;q=0.9,en;q=0.8",
    })
    with urlopen(req, timeout=30) as r:
        raw = r.read()
    return raw.decode("utf-8", errors="replace")


def json_bloklarini_top(html: str) -> dict:
    """Sahifa ichidagi ma'lumot bloklarini qidiradi."""
    topildi = {}

    # 1) Next.js standarti
    m = re.search(
        r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if m:
        topildi["__NEXT_DATA__"] = m.group(1)

    # 2) window.__ ... = {...}
    for m in re.finditer(r'window\.(__[A-Za-z0-9_]+)\s*=\s*(\{.*?\});', html, re.S):
        nom, matn = m.group(1), m.group(2)
        if len(matn) > 200:                              # arzimas bloklarni tashlaymiz
            topildi[nom] = matn

    # 3) JSON-LD (tuzilgan ma'lumot)
    ld = re.findall(
        r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
    if ld:
        topildi["ld+json"] = "\n---\n".join(ld)

    return topildi


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("=" * 60)
    print("  OBER ZOND — sahifa tuzilishini aniqlash")
    print("=" * 60)

    xulosa = []

    for nom, url in SAHIFALAR.items():
        print(f"\n[{nom}]")
        print(f"  {url}")
        try:
            html = yukla(url)
        except Exception as e:                            # noqa: BLE001
            print(f"  XATO: {type(e).__name__}: {e}")
            xulosa.append((nom, "XATO", str(e)[:80]))
            continue

        # Xom HTML saqlanadi — men keyin o'qib parser yozaman
        p = OUT / f"{nom}.html"
        p.write_text(html, encoding="utf-8")
        print(f"  saqlandi: {p.name}  ({len(html):,} belgi)")

        bloklar = json_bloklarini_top(html)
        if bloklar:
            for bnom, bmatn in bloklar.items():
                fayl = OUT / f"{nom}__{bnom.strip('_')}.json"
                # chiroyli formatga solishga urinamiz (o'qish oson bo'lsin)
                try:
                    fayl.write_text(
                        json.dumps(json.loads(bmatn), ensure_ascii=False, indent=1),
                        encoding="utf-8")
                    holat = "JSON OK"
                except Exception:                          # noqa: BLE001
                    fayl.write_text(bmatn, encoding="utf-8")
                    holat = "xom"
                print(f"    -> {bnom}: {len(bmatn):,} belgi ({holat})")
            xulosa.append((nom, "OK", ", ".join(bloklar.keys())))
        else:
            print("    -> JSON blok topilmadi (HTML'dan o'qish kerak bo'ladi)")
            xulosa.append((nom, "OK", "JSON yo'q"))

        time.sleep(KUTISH)

    print("\n" + "=" * 60)
    print("  XULOSA")
    print("=" * 60)
    for nom, holat, izoh in xulosa:
        print(f"  {nom:20} {holat:6} {izoh}")
    print(f"\n  Fayllar: {OUT}")
    print("  Endi Claude'ga ayting — u shu fayllarni o'qib parser yozadi.\n")


if __name__ == "__main__":
    sys.exit(main())
