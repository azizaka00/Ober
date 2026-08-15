"""OBER — assetlinks.json uchun SHA-256 izlarini so'raydi va yozadi.

`assetlinks_yoz.py` ni interaktiv qobiq bilan o'raydi: izlarni
buyruq satridan emas, savol-javob bilan oladi. Sabab — iz 95 belgi
va uni Play Console'dan nusxa olib buyruq satriga qo'yish noqulay.

Ikki iz nega kerakligi `assetlinks_yoz.py` izohida batafsil.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import assetlinks_yoz  # noqa: E402


def main() -> int:
    print("=" * 60)
    print("  OBER — assetlinks.json yozish")
    print("=" * 60)
    print()
    print("Play Console -> Test and release -> Setup -> App signing")
    print()
    print("1-iz: \"App signing key certificate\" ostidagi SHA-256.")
    print("      Bu GOOGLE'ning kaliti. Play foydalanuvchiga")
    print("      yetkazishdan oldin paketni qayta imzolaydi, ya'ni")
    print("      telefondagi ilovada aynan shu iz turadi.")
    print("      ASOSIYSI shu — ko'pchilik shu yerda adashadi.")
    print()
    iz1 = input("1-iz SHA-256: ").strip()
    if not iz1:
        print("\nXATO: birinchi iz majburiy.")
        return 1

    print()
    print("2-iz: \"Upload key certificate\" ostidagi SHA-256.")
    print("      Bu BIZNING kalitimiz (android.keystore). Lokal")
    print("      qurilgan APK'ni telefonda sinaganda kerak bo'ladi.")
    print("      Bo'sh qoldirsangiz faqat 1-iz yoziladi.")
    print()
    iz2 = input("2-iz SHA-256 (ixtiyoriy): ").strip()

    print()
    sys.argv = ["assetlinks_yoz.py", iz1] + ([iz2] if iz2 else [])
    return assetlinks_yoz.main()


if __name__ == "__main__":
    raise SystemExit(main())
