"""
OBER — BARCHA KATEGORIYALARNI YIG'ISH (bitta tugma)

Har kategoriya x har viloyat bo'yicha yuradi. Bitta ham qolib
ketmasligi uchun holat bazaga yoziladi: to'xtatib, keyin DAVOM
ETTIRISH mumkin. Qayta yuritilganda tugagan juftlar o'tkazib
yuboriladi.

  python hammasi.py              -- davom ettiradi
  python hammasi.py 30           -- har juftlik uchun 30 sahifagacha
  python hammasi.py 30 nedvizh   -- faqat mos kategoriyalar
  python hammasi.py boshdan      -- holatni tozalab, noldan

CHEKLOV (o'lchangan): OLX bitta so'rovga ~25-30 sahifa beradi.
Shuning uchun "hammasi" degani — har kategoriya x viloyat kesimida
OLX ko'rsatadigan hammasi. Shu sababli ro'yxat subkategoriyalarga
bo'lingan: qamrov shundan bir necha barobar oshadi.
"""

from __future__ import annotations

import sys
import time

import baza
import olx
from kategoriyalar import royxat


def bitta(yol: str, nom: str, viloyat_bolagi: str, viloyat_nomi: str,
          sahifalar: int) -> dict:
    """Bitta kategoriya x viloyat. Qolgan sahifadan davom etadi."""
    holat = baza.yigish_holati_ol(yol, viloyat_nomi)
    if holat["tugadi"]:
        return {"otkazildi": True, "yangi": 0}

    boshlang = int(holat["sahifa"] or 0) + 1
    if boshlang > sahifalar:
        # Bu chuqurlikda tugagan, lekin BUTUNLAY tugagan emas.
        # `tugadi` qo'yilmaydi: keyinroq chuqurroq yurgizilsa davom etsin.
        return {"otkazildi": True, "yangi": 0}

    # `/oz/` — O'ZBEKCHA sahifa.
    # 2026-08-02, Aziz ko'rsatdi: kategoriya ro'yxatini o'zbekcha
    # sahifadan olgandik, lekin e'lonlarni RUSCHA sahifadan yig'ardik.
    # Natijada OLX bergan tavsiflar ruscha kelardi: "Кузовные детали",
    # "2 комнаты". Endi ikkalasi ham o'zbekcha.
    url = f"https://www.olx.uz/oz/{yol}/{viloyat_bolagi}/"
    hisob = {"korildi": 0, "yangi": 0, "yangilandi": 0, "ozgarmadi": 0,
             "xato": 0}
    oxirgi = holat["sahifa"] or 0
    tugadi = False

    for n in range(boshlang, sahifalar + 1):
        manzil = url if n == 1 else f"{url}?page={n}"
        try:
            sahifa = olx.yukla(manzil)
        except Exception as e:                      # noqa: BLE001
            print(f"        [{n}] xato: {type(e).__name__}")
            hisob["xato"] += 1
            break                                    # keyingi safar davom etadi

        elonlar = olx.holatdan_oqi(sahifa, viloyat_nomi)
        if not elonlar:
            tugadi = True                            # sahifalar tugadi
            break

        # ATAMA LUG'ATI — faqat BIRINCHI sahifada, faqat BIRINCHI viloyatda.
        # Shu bitta qo'shimcha so'rov evaziga qidiruv ikki tilda ishlaydi.
        # Hamma sahifani ikki tilda o'qish vaqtni ikki barobar oshirardi.
        if n == 1 and holat["sahifa"] == 0:
            try:
                ru = olx.yukla(url.replace("/oz/", "/", 1))
                olx.time.sleep(0.5)
                baza.atama_yoz(olx.atamalarni_juftla(sahifa, ru))
            except Exception:                        # noqa: BLE001
                pass                                 # atama lug'ati ixtiyoriy

        for e in elonlar:
            e["kategoriya"] = nom
            hisob["korildi"] += 1
            try:
                hisob[baza.saqla(e)] += 1
            except Exception as ex:                  # noqa: BLE001
                print(f"        saqlash xatosi: {ex}")
                hisob["xato"] += 1

        oxirgi = n
        baza.yigish_holati_yoz(yol, viloyat_nomi, n, False, len(elonlar))
        time.sleep(olx.KUTISH)

    # `tugadi` FAQAT sahifalar haqiqatan tugaganda qo'yiladi (bo'sh sahifa).
    # Chuqurlik chegarasiga yetgani "tugadi" degani EMAS — aks holda avval
    # 3 sahifadan yurgizib, keyin 25 ga chiqmoqchi bo'lsak, tizim hammasini
    # "allaqachon tugagan" deb o'tkazib yuborardi.
    baza.yigish_holati_yoz(yol, viloyat_nomi, oxirgi, tugadi, 0)
    return {"otkazildi": False, **hisob}


def main(sahifalar: int = 25, faqat: str = "") -> int:
    baza.init()
    kategoriyalar = royxat(faqat)
    viloyatlar = [(b, nom) for b, nom, _ in olx.VILOYATLAR]

    jami_juft = len(kategoriyalar) * len(viloyatlar)
    print("=" * 66)
    print("  OBER — BARCHA KATEGORIYALARNI YIG'ISH")
    print("=" * 66)
    print(f"\n  {len(kategoriyalar)} kategoriya x {len(viloyatlar)} viloyat"
          f" = {jami_juft} juftlik")
    print(f"  Har juftlik uchun {sahifalar} sahifagacha")
    print("\n  To'xtatish: Ctrl+C. Keyin shu faylni qayta bosing —")
    print("  qolgan joydan davom etadi, boshidan boshlamaydi.\n")

    boshlandi = time.time()
    jami = {"yangi": 0, "yangilandi": 0, "korildi": 0, "xato": 0}
    otkazildi = 0
    n = 0

    try:
        for yol, nom in kategoriyalar:
            print(f"\n  ── {nom}")
            for bolak, viloyat in viloyatlar:
                n += 1
                h = bitta(yol, nom, bolak, viloyat, sahifalar)
                if h["otkazildi"]:
                    otkazildi += 1
                    continue
                for k in jami:
                    jami[k] += h.get(k, 0)
                print(f"      {viloyat:22} yangi {h['yangi']:5}"
                      f" · yangilandi {h['yangilandi']:5}"
                      f"   [{n}/{jami_juft}]")
    except KeyboardInterrupt:
        print("\n\n  To'xtatildi. Holat saqlandi — qayta bosganda davom etadi.")

    daqiqa = (time.time() - boshlandi) / 60
    hisobot = baza.yigish_hisoboti()
    s = baza.statistika()

    print("\n" + "-" * 66)
    print(f"  Vaqt: {daqiqa:.0f} daqiqa · o'tkazilgan (tugagan) {otkazildi}")
    print(f"  Bu safar: yangi {jami['yangi']} · yangilandi {jami['yangilandi']}"
          f" · xato {jami['xato']}")
    print(f"  Juftliklar: {hisobot['tugagan']}/{hisobot['juftlar']} tugagan")
    print(f"\n  BAZADA: {s['jami']} e'lon (faol {s['faol']})")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0].lower() == "boshdan":
        baza.init()
        baza.yigishni_boshdan()
        print("  Holat tozalandi — noldan yig'iladi.\n")
        args = args[1:]
    sahifalar = int(args[0]) if args and args[0].isdigit() else 25
    faqat = args[1] if len(args) > 1 else ""
    raise SystemExit(main(sahifalar, faqat))
