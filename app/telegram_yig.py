"""
OBER — TELEGRAM KANALLARINI YIG'ISH

  python telegram_yig.py                -- ro'yxatdagi hamma kanal, 1 sahifa
  python telegram_yig.py 3              -- har kanaldan 3 sahifa (chuqurroq)
  python telegram_yig.py sinov          -- faqat 2 ta kanal, tekshirish uchun
  python telegram_yig.py kanal roboshopuz   -- bitta kanal

Kanal ro'yxati: `data/telegram-kanallar.txt`

DIQQAT — SIFAT KANAL TANLASHGA BOG'LIQ.
2026-08-02 o'lchov: `roboshopuz` kanalining 18 xabaridan 12 tasida matn,
faqat 6 tasida narx bor edi — ya'ni uchdan biri e'lon. `optomelonuz` esa
umuman tovar sotmaydi, boshqa kanallarni reklama qiladi. Yaxshi kanal —
har xabarda bitta tovar, narxi bilan. Yomon kanal indeksni axlatga
to'ldiradi. Shuning uchun ro'yxatga qo'shishdan oldin kanalni ochib
ko'ring: xabarlarda narx bormi?
"""

from __future__ import annotations

import sys
import time

import baza
import telegram_manba as tg
from tahlil import kesh_belgila
from tahlil import main as tahlil_qil


def yig(kanallar: list[str], sahifalar: int = 1) -> dict:
    baza.init()
    belgi = baza.sikl_boshlash(tg.MANBA)
    jami = {"korildi": 0, "elon": 0, "yangi": 0, "yangilandi": 0,
            "qaytdi": 0, "ozgarmadi": 0, "xato": 0}

    print("=" * 70)
    print(f"  OBER — TELEGRAM: {len(kanallar)} kanal x {sahifalar} sahifa")
    print("=" * 70)
    print()

    boshlandi = time.time()
    for i, nom in enumerate(kanallar, 1):
        h = tg.kanal(nom, sahifalar, belgi)
        for k in jami:
            jami[k] += h.get(k, 0)
        ulush = f"{h['elon']}/{h['korildi']}" if h["korildi"] else "0/0"
        print(f"  {i:3}. @{nom:28} xabar {ulush:9}"
              f" yangi {h['yangi']:4} · yangilandi {h['yangilandi']:4}"
              f" · xato {h['xato']}")
        time.sleep(tg.KUTISH)

    if jami["yangi"] or jami["qaytdi"]:
        try:
            tahlil_qil()
        except Exception as e:                       # noqa: BLE001
            print(f"  [tahlil] xato: {type(e).__name__}: {e}")
    kesh_belgila()

    daqiqa = (time.time() - boshlandi) / 60
    print("\n" + "-" * 70)
    print(f"  {daqiqa:.1f} daqiqa · ko'rilgan xabar {jami['korildi']}"
          f" · e'lon deb topildi {jami['elon']}")
    print(f"  yangi {jami['yangi']} · yangilandi {jami['yangilandi']}"
          f" · o'zgarmadi {jami['ozgarmadi']} · xato {jami['xato']}")
    if jami["korildi"]:
        ulush = jami["elon"] * 100 // jami["korildi"]
        print(f"  E'lon ulushi: {ulush}%"
              + ("  <- past. Kanal ro'yxatini qayta ko'ring." if ulush < 25
                 else ""))
    s = baza.statistika()
    print(f"\n  BAZADA: {s['jami']} e'lon (faol {s['faol']})\n")
    return jami


def main() -> int:
    args = [a.lower() for a in sys.argv[1:]]
    sahifalar = next((int(a) for a in args if a.isdigit()), 1)

    if "kanal" in args:
        i = args.index("kanal")
        nomlar = [a for a in sys.argv[1:][i + 1:] if not a.isdigit()]
        if not nomlar:
            print("  Kanal nomini yozing:  python telegram_yig.py kanal roboshopuz")
            return 1
        yig([n.lstrip("@") for n in nomlar], sahifalar)
        return 0

    kanallar = tg.kanallar_royxati()
    if not kanallar:
        print("\n  Kanal ro'yxati bo'sh.")
        print("  `data/telegram-kanallar.txt` fayliga kanal nomlarini yozing"
              " (har qatorda bittadan).\n")
        return 1
    if "sinov" in args:
        kanallar = kanallar[:2]
    yig(kanallar, sahifalar)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
