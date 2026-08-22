"""OBER — manbalar qorovuli (2026-08-22).

NEGA BU FAYL BOR
----------------
2026-08-22 da o'lchandi: oltita manbadan TO'RTTASI sakkiz kundan
beri hech narsa yig'magan edi, va buni hech kim payqamagan.

    manba      faol e'lon   oxirgi ko'rilgan   24 soatda yangi
    olx           664 522   hozir                       46 173
    telegram        3 003   30 daqiqa                      209
    glotr          12 825   7.8 KUN                          0
    avizinfo          774   8.2 KUN                          0
    avtoelon          132   8.9 KUN                          0
    shahar             78   8.8 KUN                          0

Sabab oddiy edi: `ober-yangilik` faqat `yangilik.py` ni yuritadi
(OLX + Telegram), hamma adapterni topadigan `yigish.py` esa hech
qanday taymerga ulanmagan edi. Ya'ni kod ishlayapti, uni CHAQIRISH
unutilgan.

BU XATONING TURI MUHIM. U hech qayerda XATO BERMAYDI:

  * adapter yiqilmaydi — chunki umuman chaqirilmaydi;
  * `sikl_yakunla` nol natijada HECH NARSANI nofaol qilmaydi
    (bu ataylab shunday — nol natijali sikl butun manbani
    o'chirib yuborishi mumkin edi);
  * saytda e'lonlar turaveradi, faqat ESKIRADI.

Ya'ni yig'ish to'xtaganini faqat SUKUNAT bildiradi. Sukunatni esa
kimdir ataylab kuzatmasa, ko'rinmaydi.

NEGA TARMOQQA CHIQMAYDI
-----------------------
Manbani "tirikmi" deb qayta so'rash mumkin edi, lekin shart emas:
yig'uvchi har e'londa `oxirgi_korildi` ni yozib boradi. Signal
allaqachon bazada. Qorovul faqat o'qiydi — manbaga qo'shimcha
yuk tushmaydi va sekin ham emas.

NEGA SERVERDA, NOUTBUKDA EMAS
-----------------------------
`reports/salomatlik-jurnali.tsv` — qo'lda yuritilgan kunlik
nazorat — 2026-08-18 da to'xtagan. Sababi jurnalning o'zida
yozilgan: "NAVBATCHI.bat ishlamayapti". Noutbukka bog'liq nazorat
noutbuk yopilganda o'ladi, va aynan o'sha kunlar nazoratsiz qoladi.
Shuning uchun bu skript systemd taymeri bilan SERVERDA yuradi.

ISHLATISH
---------
    python3 app/manba_qorovul.py            # tekshiradi, jurnalga yozadi
    python3 app/manba_qorovul.py --jim      # faqat muammo bo'lsa yozadi

Chiqish kodi: muammo bo'lsa 1, toza bo'lsa 0.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import baza

ILDIZ = Path(__file__).resolve().parent.parent
JURNAL = ILDIZ / "reports" / "manba-jurnali.tsv"

# Manba shu muddatdan uzoq jim tursa — muammo.
#
# 36 soat: yig'ish kunlik, ya'ni 24 soat normal oraliq. 36 soat bir
# marta o'tkazib yuborishga joy qoldiradi (server qayta yoqildi,
# manba bir kecha nosoz edi) va ikkinchisida ogohlantiradi.
CHEGARA_SOAT = 36

# Yangi manba qo'shilganda u hali hech narsa yig'magan bo'ladi.
# Birinchi sutkada jim turgani muammo emas.
YANGI_MANBA_IMTIYOZ_SOAT = 24


def holat() -> list[dict]:
    """Har manba bo'yicha: nechta e'lon, oxirgi qachon ko'rilgan."""
    baza.init()
    hozir = time.time()
    with baza.ulan() as c:
        qatorlar = c.execute("""
            SELECT manba,
                   SUM(faol=1)  faol,
                   SUM(faol=0)  nofaol,
                   MAX(oxirgi_korildi) oxirgi,
                   MIN(olindi)  birinchi,
                   SUM(CASE WHEN olindi > ? THEN 1 ELSE 0 END) yangi24
            FROM elonlar
            GROUP BY manba
        """, (hozir - 86400,)).fetchall()

    natija = []
    for r in qatorlar:
        oxirgi = float(r["oxirgi"] or 0)
        birinchi = float(r["birinchi"] or 0)
        natija.append({
            "manba": r["manba"] or "?",
            "faol": int(r["faol"] or 0),
            "nofaol": int(r["nofaol"] or 0),
            "yangi24": int(r["yangi24"] or 0),
            "jim_soat": (hozir - oxirgi) / 3600 if oxirgi else -1.0,
            "yosh_soat": (hozir - birinchi) / 3600 if birinchi else 0.0,
        })
    natija.sort(key=lambda x: -x["faol"])
    return natija


# ADAPTERI YO'Q, LEKIN HAQIQIY MANBA (2026-08-22 da topildi).
#
# Telegram `manbalar/` ichida emas — uni `yangilik.py` to'g'ridan
# yig'adi. Birinchi yugurishda qorovul uni "kutilmagan" deb chetlab
# o'tdi, ya'ni Telegram yig'ishi to'xtasa HECH KIM bilmasdi.
#
# OLX bu ro'yxatda YO'Q va kerak ham emas: `manbalar/olx.py` bor,
# u eski `olx.py` ga yo'naltiradi, shuning uchun adapterlar
# ro'yxatiga o'zi tushadi.
ADAPTERSIZ = {"telegram"}

# MA'LUM CHEKLOV — TUZATILADIGAN XATO EMAS (2026-08-22 da o'lchandi).
#
# Bu manbalar adapteri to'g'ri, lekin manba tomonidan cheklangan.
# Ular har kuni "NOSOZ" bo'lib turishi kerak EMAS: doim qizil turgan
# tekshiruv odamni qizilga ko'niktiradi va o'shanda haqiqiy nosozlik
# ham e'tiborsiz qoladi.
#
# Shu bilan birga ular YASHIRILMAYDI ham — pastda alohida ro'yxatda
# ko'rinadi, sababi bilan. Unutilgan cheklov ham yomon: bir yildan
# keyin "nega asaxiy yo'q?" degan savolga javob qolmaydi.
#
# Cheklov yo'qolsa (manba ochilsa) qatorni shu yerdan o'chirish
# kifoya — qorovul yana kuzata boshlaydi.
MA_LUM_CHEKLOV = {
    "asaxiy": "asaxiy.uz so'rovni rad etadi — HTTP 403. Adapter "
              "buni o'zi aniqlaydi (`_Bloklandi`). Server IP'si "
              "sababli bo'lishi mumkin; boshqa IP'dan sinalmagan.",
}


def kutilgan_manbalar() -> set[str]:
    """Qaysi manbalar ishlashi KERAK.

    Ro'yxat qo'lda yozilmaydi — `yigish.adapterlar()` o'zi topadi.
    Sabab: yangi adapter qo'shilganda uni qorovul ro'yxatiga ham
    yozishni unutish oson, va o'shanda qorovul aynan yangi manbani
    ko'rmay qoladi.
    """
    try:
        import yigish
        return set(yigish.adapterlar()) | ADAPTERSIZ
    except Exception:                                # noqa: BLE001
        return set(ADAPTERSIZ)


def muammolar(h: list[dict], kutilgan: set[str]) -> list[str]:
    """Ogohlantirishga arziydigan holatlar."""
    xabar = []
    korilgan = {x["manba"] for x in h}

    for x in h:
        if x["manba"] not in kutilgan:
            continue                    # `ober` — o'z e'lonlarimiz, yig'ilmaydi
        if x["manba"] in MA_LUM_CHEKLOV:
            continue                    # ma'lum cheklov — pastda alohida
        if x["jim_soat"] < 0:
            xabar.append(f"{x['manba']}: hech qachon ko'rilmagan")
            continue
        # Yangi manbaga birinchi sutkada tegilmaydi.
        if x["yosh_soat"] < YANGI_MANBA_IMTIYOZ_SOAT:
            continue
        if x["jim_soat"] > CHEGARA_SOAT:
            xabar.append(
                f"{x['manba']}: {x['jim_soat']:.0f} soat jim "
                f"({x['faol']} e'lon eskirmoqda)")

    # ADAPTERI BOR, LEKIN BAZADA UMUMAN YO'Q — hech qachon ishlamagan.
    for m in sorted(kutilgan - korilgan - set(MA_LUM_CHEKLOV)):
        xabar.append(f"{m}: adapter bor, lekin bazada bitta ham e'lon yo'q")

    return xabar


def _jurnalga(h: list[dict], xato: list[str]) -> None:
    JURNAL.parent.mkdir(parents=True, exist_ok=True)
    yangi = not JURNAL.exists()
    with JURNAL.open("a", encoding="utf-8") as f:
        if yangi:
            f.write("sana\tmanba\tfaol\tjim_soat\tyangi24\tholat\n")
        kun = time.strftime("%Y-%m-%d")
        nosoz = {x.split(":")[0] for x in xato}
        for x in h:
            f.write("%s\t%s\t%d\t%.1f\t%d\t%s\n" % (
                kun, x["manba"], x["faol"], x["jim_soat"], x["yangi24"],
                "NOSOZ" if x["manba"] in nosoz else "ok"))


def main() -> int:
    jim = "--jim" in sys.argv
    h = holat()
    kutilgan = kutilgan_manbalar()
    xato = muammolar(h, kutilgan)

    try:
        _jurnalga(h, xato)
    except OSError as x:                             # noqa: BLE001
        print(f"  [qorovul] jurnalga yozilmadi: {x}")

    if xato:
        # SENTRY'GA — chunki bu jimgina xato va uni hech kim
        # so'ramaydi. `xato_xabar` DSN bo'lmasa jim ishlaydi.
        try:
            import xato_xabar
            xato_xabar.xato(
                RuntimeError("Manba yig'ishni to'xtatdi: "
                             + "; ".join(xato)),
                {"manbalar": [x["manba"] for x in h],
                 "chegara_soat": CHEGARA_SOAT})
        except Exception:                            # noqa: BLE001
            pass

    if not jim or xato:
        print("=" * 58)
        print("  OBER — manbalar qorovuli")
        print("=" * 58)
        print("  %-11s %8s %8s %10s %9s" % (
            "manba", "faol", "nofaol", "jim(soat)", "24s_yangi"))
        print("  " + "-" * 50)
        for x in h:
            belgi = "  " if x["manba"] in kutilgan else " ·"
            print("%s%-11s %8d %8d %10.1f %9d" % (
                belgi, x["manba"], x["faol"], x["nofaol"],
                x["jim_soat"], x["yangi24"]))
        print()
        if xato:
            print(f"  MUAMMO — {len(xato)} ta:")
            for x in xato:
                print(f"    ! {x}")
        else:
            print(f"  Hammasi joyida (chegara {CHEGARA_SOAT} soat).")
        if MA_LUM_CHEKLOV:
            print()
            print("  MA'LUM CHEKLOV (ogohlantirilmaydi, lekin unutilmasin):")
            for m, sabab in sorted(MA_LUM_CHEKLOV.items()):
                print(f"    · {m}: {sabab}")
        print()
    return 1 if xato else 0


if __name__ == "__main__":
    raise SystemExit(main())
