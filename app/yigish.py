"""OBER — barcha ma’lumot manbalari uchun umumiy yig‘ish runneri."""

from __future__ import annotations

import importlib
import pkgutil
import sys

import manbalar


def adapterlar() -> dict[str, object]:
    """`app/manbalar/` ichidagi adapterlarni avtomatik topadi."""
    topildi: dict[str, object] = {}
    for modul in pkgutil.iter_modules(manbalar.__path__):
        if modul.name.startswith("_"):
            continue
        a = importlib.import_module(f"manbalar.{modul.name}")
        for nom in ("MANBA", "NOM", "bosh", "chuqur"):
            if not hasattr(a, nom):
                raise RuntimeError(f"{modul.name} adapterida `{nom}` yo‘q")
        topildi[str(a.MANBA)] = a
    return topildi


def main(rejim: str = "bosh", sahifalar: int = 1,
         faqat_manba: str = "", joy: str = "") -> int:
    mavjud = adapterlar()
    if faqat_manba:
        if faqat_manba not in mavjud:
            print(f"Noma’lum manba: {faqat_manba}. Mavjud: {', '.join(mavjud)}")
            return 2
        mavjud = {faqat_manba: mavjud[faqat_manba]}

    print("=" * 62)
    print(f"  OBER — {rejim.upper()} YIG‘ISH · {len(mavjud)} manba")
    print("=" * 62)

    jami_xato = 0
    for kalit, adapter in mavjud.items():
        print(f"\n  MANBA: {adapter.NOM} ({kalit})")
        try:
            if rejim in ("bosh", "sinov"):
                natija = adapter.bosh(sahifalar, joy)
            elif rejim == "chuqur":
                natija = adapter.chuqur(sahifalar, joy)
            else:
                print("Rejim `bosh`, `sinov` yoki `chuqur` bo‘lishi kerak.")
                return 2
        except Exception as xato:  # bitta adapter boshqalarini to‘xtatmasin
            print(f"  ADAPTER XATOSI: {type(xato).__name__}: {xato}")
            jami_xato += 1
            continue
        jami_xato += int(natija.get("xato", 0))

    print("\n" + "-" * 62)
    print(f"  YAKUN — adapter/page xatolari: {jami_xato}")

    # TAHLIL HAR DOIM YURITILADI — xato bo'lsa ham.
    # Ilgari `if not jami_xato` sharti bor edi. 2026-08-01 da shu tufayli
    # 11 500 e'londan 8 470 tasi qidiruvda ko'rinmay qolgan edi: bitta
    # vaqtinchalik tarmoq xatosi butun siklning teglarini to'sib qo'yadi,
    # tegsiz e'lon esa qidiruvga umuman kirmaydi.
    # Tahlil idempotent va arzon — uni xatoga bog'lash noto'g'ri edi.
    if rejim != "sinov":
        import tahlil
        tahlil.main()
    return 1 if jami_xato else 0


if __name__ == "__main__":
    rejim = sys.argv[1].lower() if len(sys.argv) > 1 else "bosh"
    sahifalar = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    manba = sys.argv[3].lower() if len(sys.argv) > 3 else ""
    joy = sys.argv[4] if len(sys.argv) > 4 else ""
    raise SystemExit(main(rejim, sahifalar, manba, joy))
