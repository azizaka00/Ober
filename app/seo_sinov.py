"""SEO narx sahifalarini tekshiradi va namuna faylga yozadi."""

from __future__ import annotations

import time

import baza
import seo


def main() -> None:
    baza.init()
    print("=" * 62)
    print("  OBER — narx sahifalari")
    print("=" * 62)

    t = time.time()
    k = seo.kombinatsiyalar()
    print(f"\n  Sahifa yasashga arziydigan yo'nalish: {len(k)} ta")
    print(f"  Hisoblash: {(time.time() - t):.1f} soniya\n")

    if not k:
        print("  Ma'lumot yetarli emas. Avval yig'ish kerak.\n")
        return

    print(f"  {'YO`NALISH':<28} {'E`LON':>6}   MANZIL")
    print("  " + "-" * 58)
    for x in k[:15]:
        print(f"  {x['model'] + ' ' + x['qism']:<28} {x['soni']:>6}"
              f"   /narx/{x['slug']}")

    # Namuna sahifa — brauzerda ochib ko'rish uchun
    t = time.time()
    sahifa = seo.narx_sahifasi(k[0]["model"], k[0]["qism"])
    ms = (time.time() - t) * 1000
    if not sahifa:
        print("\n  XATO: namuna sahifa yasalmadi\n")
        return

    fayl = baza.DB.with_name("namuna-narx-sahifa.html")
    fayl.write_bytes(sahifa)

    xarita = seo.sitemap()
    print(f"\n  Namuna sahifa: {len(sahifa):,} bayt, {ms:.0f} ms")
    print(f"  Sitemap: {xarita.count(b'<url>')} manzil")
    print(f"\n  Ko'rish uchun:")
    print(f"    {fayl}")
    print(f"    http://127.0.0.1:8800/narx")
    print(f"    http://127.0.0.1:8800/narx/{k[0]['slug']}")
    print(f"    http://127.0.0.1:8800/sitemap.xml\n")


if __name__ == "__main__":
    main()
