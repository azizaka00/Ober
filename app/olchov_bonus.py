"""YANGI MANBA BONUSI — KENG O'LCHOV (2026-08-14)

Ishlatish: serverda `cd /home/ober/ober/app && python3 olchov_bonus.py`
(lokal bazada yangi manba e'lonlari yo'q — natija bo'sh chiqadi).

Nima tekshiradi:
1. Har so'rovda yangi manba (avtoelon/shahar/glotr/avizinfo) e'lonlari
   TOP-60 ga kirmadimi — bonus ishlayaptimi.
2. Bonus olgan e'lonning nomida so'rov so'zi bormi — noto'g'ri moslik
   tepaga chiqmayaptimi (bonus faqat ishonchli e'longa beriladi).
3. Manbalar taqsimoti adolatlimi — OLX bonus tufayli siqib
   chiqarilmayaptimi.

O'lchov natijasi (2026-08-14, production):
    zaryadnoe       -> glotr 1-o'rin (4 ta), hammasi ishonchli
    planshet        -> glotr 1-o'rin (2 ta)
    noutbuk         -> glotr 1-o'rin, avizinfo 22-o'rin
    kvartira sotish -> shahar 11 ta (25-o'ringacha)
    dom prodaja     -> shahar 7 ta (4-o'rin)
    lacetti         -> avtoelon 1-o'rin, glotr 3-o'rin
    telefon/mebel/karavot -> bonus olgan 0 ta — to'g'ri:
        Glotr'da "karavot" e'lonlari umuman yo'q; "mebel" e'lonlari
        nomida "mebel" so'zi yo'q (ofis texnikasi) — ishonchsiz;
        "telefon" da OLX 862 ta — raqobat adolatli.
"""
import sys
sys.path.insert(0, ".")
import qidiruv

SO_ROVLAR = [
    "zaryadnoe", "planshet", "noutbuk", "matras", "velosiped",
    "lacetti", "kvartira sotish", "dom prodaja", "dveri toyota",
    "korolla", "dvigatel", "telefon", "mebel", "karavot",
]

YANGI = ("avtoelon", "shahar", "glotr", "avizinfo")


def main() -> None:
    for s in SO_ROVLAR:
        r = qidiruv.qidir(s, limit=60)
        e = r.get("elonlar") or r.get("natijalar") or []
        bonus = [x for x in e if x.get("manba") in YANGI]
        print(f"--- {s!r}: bonus olgan {len(bonus)} ta ---")
        for x in bonus[:4]:
            nom = (x.get("nom") or "")[:55]
            print(f"   [{x.get('manba')}] ball={x.get('ball')} "
                  f"ishonchli={x.get('_ishonchli')} | {nom}")


if __name__ == "__main__":
    main()
