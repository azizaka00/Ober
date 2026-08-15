"""OBER — Digital Asset Links faylini yozadi.

NEGA KERAK (2026-08-14)
-----------------------
TWA (Trusted Web Activity) — bu Chrome'ning ilova ichida ishlashi.
Chrome har ochilishda `https://ober.uz/.well-known/assetlinks.json`
ni so'raydi va u yerda O'ZINI IMZOLAGAN kalitning SHA-256 izini
qidiradi.

Iz mos kelsa — to'liq ekran, manzil satri yo'q, ilovaga o'xshaydi.
Iz mos kelmasa — tepada brauzer manzil satri chiqadi va ilova
oddiy veb-saytga aylanadi. Xato xabari YO'Q, shunchaki ishlamaydi.

ENG KO'P UCHRAYDIGAN XATO
-------------------------
Play App Signing yoqilganda IKKI XIL kalit bo'ladi:

  1. Upload key   — bizdagi `android.keystore`. Biz shu bilan
                    imzolab Play'ga yuklaymiz.
  2. App signing key — Google'niki. Play foydalanuvchiga
                    yetkazishdan oldin paketni QAYTA imzolaydi.

Foydalanuvchining telefonidagi ilovada Google'ning izi turadi.
Shuning uchun assetlinks'ga `App signing key` izi kerak — lekin
ko'pchilik upload key izini yozadi va nima uchun ishlamayotganini
tushunmaydi.

Yechim: IKKALASINI ham yozamiz. Ro'yxat bo'lgani uchun mumkin.
Shunda Play'dan o'rnatilgan ilova ham, lokal qurilgan APK ham
ishlaydi.

Play Console'da qayerdan olinadi:
    Test and release -> Setup -> App signing
      "App signing key certificate"  -> SHA-256   (asosiysi)
      "Upload key certificate"       -> SHA-256   (ikkinchisi)

Ishlatish:
    python app/assetlinks_yoz.py AA:BB:.. [CC:DD:..]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ILDIZ = Path(__file__).resolve().parent.parent
CHIQISH = ILDIZ / "web" / ".well-known" / "assetlinks.json"
PAKET = "uz.ober.app"

# 32 bayt = 32 juft o'n oltilik raqam, ikki nuqta bilan ajratilgan.
QOLIP = re.compile(r"^(?:[0-9A-F]{2}:){31}[0-9A-F]{2}$")


def tozala(xom: str) -> str:
    """Play Console'dan nusxa olinganda bo'shliq va kichik harf tushadi."""
    return xom.strip().replace(" ", "").replace("\n", "").upper()


def main() -> int:
    izlar_xom = sys.argv[1:]
    if not izlar_xom:
        print(__doc__)
        print("XATO: kamida bitta SHA-256 izi kerak.")
        return 1

    izlar: list[str] = []
    for xom in izlar_xom:
        iz = tozala(xom)
        if not QOLIP.match(iz):
            print(f"XATO: iz formati noto'g'ri:\n  {iz}")
            print("\nKutilgan ko'rinish — 32 juft, ikki nuqta bilan:")
            print("  AB:CD:EF:01:23:45:...:89  (jami 95 belgi)")
            print(f"Sizda {len(iz)} belgi bor.")
            return 1
        if iz in izlar:
            print(f"OGOHLANTIRISH: iz takrorlandi, bittasi olindi:\n  {iz}")
            continue
        izlar.append(iz)

    tana = [{
        "relation": ["delegate_permission/common.handle_all_urls"],
        "target": {
            "namespace": "android_app",
            "package_name": PAKET,
            "sha256_cert_fingerprints": izlar,
        },
    }]

    CHIQISH.parent.mkdir(parents=True, exist_ok=True)
    CHIQISH.write_text(json.dumps(tana, indent=2) + "\n", encoding="utf-8")

    print(f"Yozildi: {CHIQISH}")
    print(f"Paket:   {PAKET}")
    for i, iz in enumerate(izlar, 1):
        print(f"Iz {i}:    {iz}")
    if len(izlar) == 1:
        print()
        print("DIQQAT: faqat BITTA iz yozildi.")
        print("Play App Signing yoqilgan bo'lsa ikkitasi kerak:")
        print("  - App signing key certificate  (Google'niki, asosiysi)")
        print("  - Upload key certificate       (bizniki)")
        print("Aks holda Play'dan o'rnatilgan ilovada manzil satri qoladi.")
    print()
    print("KEYINGI QADAM:")
    print("  1. NAVBATCHI.bat oching, `data/buyruq.txt` ga: yuklash")
    print("  2. Tekshiring:  https://ober.uz/.well-known/assetlinks.json")
    print("  3. Google tekshirgichi:")
    print("     https://developers.google.com/digital-asset-links/tools/generator")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
