"""
OBER — YANGILIK SIKLI (ma'lumot eskirmasligi uchun)

MUAMMO (Aziz, 2026-08-02: "OLX ga yangi e'lon joylansa bizda ko'rinadimi?"):
`hammasi.py` bir marta yuradi va to'xtaydi. Tugagan kategoriya x viloyat
juftligi `tugadi=1` deb belgilanadi va keyingi yurishda BUTUNLAY o'tkazib
yuboriladi. Ya'ni bugun tugagan kategoriyaga ertaga 200 ta e'lon joylansa,
biz ularni hech qachon ko'rmaymiz. Teskarisi ham yomon: sotilgan e'lon
bizda qolib ketadi va xaridor bosganda OLX'da sahifa topilmaydi.

YECHIM — arzon sikl.
OLX standart holatda eng yangisini birinchi ko'rsatadi. Demak bugun
joylangan hamma narsa 1-sahifada turadi. Butun kategoriyani qayta yurish
shart emas — 1-2 sahifa yetadi. Bu to'liq yig'ishdan ~25 barobar arzon.

IKKI TEZLIK (hammasini bir xil chastotada yurgizib bo'lmaydi:
10 000+ juftlik x 1 sahifa ~ 3 soat):
  issiq   — talab yuqori bo'lgan kategoriyalar, tez-tez
  sovuq   — qolgani, sutkasiga bir marta

SOTILGANLARNI O'CHIRISH:
Bu tezkor sikl faqat eng yangi 1-2 sahifani ko'radi, shuning uchun unda
ko'rinmagan eski e'lonni sotilgan deb belgilamaydi. Nofaollik faqat barcha
sahifalarni ko'rgan haqiqiy to'liq crawl yoki alohida havola tekshiruvi
bilan aniqlanishi kerak.

ISHLATISH:
  python yangilik.py             -- bir marta: issiq kategoriyalar
  python yangilik.py hammasi     -- bir marta: barcha kategoriyalar
  python yangilik.py kuzat       -- to'xtamay yuradi (issiq 45 daq, to'liq 24 soat)
  python yangilik.py hammasi 2   -- har juftlikdan 2 sahifa
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import baza
import olx
from kategoriyalar import royxat
from tahlil import kesh_belgila
from tahlil import main as tahlil_qil

# ── ISSIQ KATEGORIYALAR ──────────────────────────────────────────────────
# Talab yuqori va aylanma tez bo'lgan yo'nalishlar. Yo'l BOSHI bo'yicha
# solishtiriladi — "doma" kabi qisqa bo'lakni matn ichidan qidirish
# kutilmagan kategoriyalarni ham tortib kelardi.
#
# `legkovye-avtomobili` ATAYLAB YO'Q: OLX uni 60 ta markaga bo'lgan,
# ya'ni 60 x 14 = 840 juftlik. Yolg'iz o'zi issiq siklni ikki barobar
# uzaytirardi. Mashinaning o'zi sutkalik to'liq siklda yangilanadi;
# OBER'ning o'zagi — ehtiyot qism.
#
# Bu ro'yxat taxmin. `qidiruvlar` jadvali to'lgach uni haqiqiy talabdan
# qayta hisoblash kerak — odamlar nimani ko'p qidirsa, o'sha issiq.
ISSIQ = (
    "transport/avtozapchasti-i-aksessuary/",
    "transport/shiny-diski",
    "elektronika/telefony/",
    "elektronika/kompyutery/",
    "elektronika/bytovaya",
    "nedvizhimost/kvartiry/",
    "nedvizhimost/doma/",
    "dom-i-sad/mebel/",
)

# Sikllar orasidagi tanaffus (soniya)
ISSIQ_ORALIQ = 45 * 60
TOLIQ_ORALIQ = 24 * 60 * 60
TOLIQ_BELGI = Path(__file__).resolve().parent.parent / "data" / "toliq-oxirgi.txt"


def issiqmi(yol: str) -> bool:
    return yol.startswith(ISSIQ)


def bitta(yol: str, nom: str, viloyat_bolagi: str, viloyat_nomi: str,
          sahifalar: int, sikl: str) -> dict:
    """Bitta juftlikning BIRINCHI sahifalari.

    `yigish_holati` ga TEGMAYDI. To'liq yig'ish o'z holatini yuritadi;
    yangilik sikli esa har safar boshidan o'qiydi — maqsadi ham shu.
    """
    url = f"https://www.olx.uz/oz/{yol}/{viloyat_bolagi}/"
    hisob = {"korildi": 0, "yangi": 0, "yangilandi": 0, "ozgarmadi": 0,
             "qaytdi": 0, "xato": 0}

    for n in range(1, sahifalar + 1):
        manzil = url if n == 1 else f"{url}?page={n}"
        try:
            sahifa = olx.yukla(manzil)
        except Exception:                            # noqa: BLE001
            hisob["xato"] += 1
            break
        elonlar = olx.holatdan_oqi(sahifa, viloyat_nomi)
        if not elonlar:
            break
        for e in elonlar:
            e["kategoriya"] = nom
            hisob["korildi"] += 1
            try:
                hisob[baza.saqla(e, sikl)] += 1
            except Exception:                        # noqa: BLE001
                hisob["xato"] += 1
        time.sleep(olx.KUTISH)
    return hisob


def sikl(faqat_issiq: bool = True, sahifalar: int = 1,
         cheklov: int = 0) -> dict:
    """Bitta to'liq o'tish. `cheklov` — sinov uchun juftliklar soni."""
    baza.init()
    kategoriyalar = [(y, n) for y, n in royxat()
                     if not faqat_issiq or issiqmi(y)]
    viloyatlar = [(b, nom) for b, nom, _ in olx.VILOYATLAR]
    # Bu yangilovchi har kategoriya/viloyatning faqat 1-2 eng yangi
    # sahifasini ko'radi. Shu sabab bu yerda `oxirgi_sikl` yozilmaydi:
    # eski, lekin hali faol e'lon birinchi sahifada ko'rinmagani uchungina
    # "sotilgan" deb belgilanishi mumkin emas. Haqiqiy to'liq crawl
    # (`hammasi.py`) o'z sikl belgisini alohida yuritadi.
    belgi = ""

    juftlar = [(y, nm, b, v) for y, nm in kategoriyalar
               for b, v in viloyatlar]
    if cheklov:
        juftlar = juftlar[:cheklov]
    jami_juft = len(juftlar)
    turi = "SINOV" if cheklov else ("ISSIQ" if faqat_issiq else "TO'LIQ")
    print(f"\n  [{turi}] {len(kategoriyalar)} kategoriya x"
          f" {len(viloyatlar)} viloyat = {jami_juft} juftlik,"
          f" har biridan {sahifalar} sahifa")

    boshlandi = time.time()
    jami = {"korildi": 0, "yangi": 0, "yangilandi": 0, "qaytdi": 0, "xato": 0}
    tahlilsiz = 0
    for n, (yol, nom, bolak, viloyat) in enumerate(juftlar, 1):
        h = bitta(yol, nom, bolak, viloyat, sahifalar, belgi)
        for k in jami:
            jami[k] += h.get(k, 0)
        tahlilsiz += h["yangi"] + h["qaytdi"]
        if h["yangi"] or h["xato"] or cheklov:
            print(f"      {nom[:30]:30} {viloyat:20}"
                  f" ko'rildi {h['korildi']:4} · yangi {h['yangi']:4}"
                  f" · xato {h['xato']}   [{n}/{jami_juft}]")
        # ORALIQ TAHLIL. Tahlil faqat sikl oxirida chaqirilardi — to'liq
        # sikl 7 soat ketadi, ya'ni yig'ilgan e'lon yarim kun qidiruvda
        # ko'rinmasdi. Endi har 500 tadan keyin indeksga tushadi.
        if tahlilsiz >= 500:
            try:
                tahlil_qil()
            except Exception as e:                   # noqa: BLE001
                print(f"  [tahlil] xato: {type(e).__name__}: {e}")
            tahlilsiz = 0

    # Bu tezkor yangilovchi nofaollashtirmaydi: "to'liq" bu yerda barcha
    # kategoriyalar qamrovi, barcha e'lon sahifalari emas. Birinchi sahifada
    # yo'q e'lon sotilgan degani emas.
    yakun = {"toliq": False}

    # YANGI E'LON DARHOL QIDIRILSIN.
    # Tahlilsiz e'lon indeksga tushmaydi, ya'ni yig'ilgani bilan hech kim
    # topolmaydi — bu butun siklni ma'nosiz qilardi.
    if tahlilsiz:
        try:
            tahlil_qil()
        except Exception as e:                       # noqa: BLE001
            print(f"  [tahlil] xato: {type(e).__name__}: {e}")
    kesh_belgila()

    daqiqa = (time.time() - boshlandi) / 60
    print(f"\n  [{turi}] {daqiqa:.0f} daqiqa · ko'rildi {jami['korildi']}"
          f" · yangi {jami['yangi']} · yangilandi {jami['yangilandi']}"
          f" · qaytdi {jami['qaytdi']} · xato {jami['xato']}")
    if yakun.get("toliq"):
        print(f"           topilmadi {yakun['otkazildi']}"
              f" · sotilgan deb belgilandi {yakun['nofaol_qilindi']}")
    return jami


def telegram_sikli() -> dict:
    """Telegram kanallarining yangi xabarlari.

    2026-08-02: adapter yozildi va sinovdan o'tdi, lekin hech qayerda
    CHAQIRILMASDI - ya'ni Telegram faqat qo'lda yig'ilardi. Yig'uvchi
    sikl esa OBER'ning "hech kim tugma bosmasin" va'dasining o'zagi.
    Endi u ham issiq sikl bilan birga yuradi.

    Kanallar kam (bittadan bir necha o'ntagacha) va har biridan 1 sahifa
    olinadi, shuning uchun bu OLX siklidan bir necha daqiqa uzoq emas.
    """
    try:
        import telegram_manba as tg
        import telegram_yig
    except Exception as e:                           # noqa: BLE001
        print(f"  [telegram] modul yuklanmadi: {type(e).__name__}: {e}")
        return {}
    kanallar = tg.kanallar_royxati()
    if not kanallar:
        return {}                                    # ro'yxat bo'sh - jim
    try:
        return telegram_yig.yig(kanallar, sahifalar=1)
    except Exception as e:                           # noqa: BLE001
        # Telegram yiqilsa OLX sikli davom etsin.
        print(f"  [telegram] xato: {type(e).__name__}: {e}")
        return {}


def yigish_sikli(toliq: bool = False) -> dict:
    """`app/manbalar/` dagi barcha adapterlar (avtoelon va keyingilar).

    2026-08-13: avtoelon.uz adapteri yozildi, lekin issiq sikl uni
    chaqirmaydigan bo'lsa — avvalgidek qo'lda yig'iladi, ya'ni hech
    kim yig'maydi. Telegram uchun shu xato 2026-08-02 da qilingan edi
    (adapter bor, chaqiriq yo'q).

    `toliq=False` — `bosh(1)`: 1-2 sahifa, tez (har 45 daqiqada).
    `toliq=True`  — `chuqur(...)`: ko'p sahifa + e'lon tavsiflari
    (sutkada bir marta, to'liq qamrov). Har bir adapter o'z
    `CHUQUR_SAHIFA`sini e'lon qiladi (avtoelon 10, qolganlari 3) —
    `yigish_sikli` uni ishlatadi. Har bir adapter xatosi alohida
    hisoblanadi va boshqa adapterlarni to'xtatmaydi.
    """
    try:
        import yigish
    except Exception as e:                           # noqa: BLE001
        print(f"  [yigish] modul yuklanmadi: {type(e).__name__}: {e}")
        return {}
    # `yigish.main` oxirida `tahlil.main()` chaqiradi — bu sikl uni
    # allaqachon boshqaradi (tahlilsiz >= 500 da va oxirida). Tahlil
    # idempotent, lekin har 45 daqiqada ikki marta ishlash ortiqcha.
    # Shuning uchun adapterlarni to'g'ridan-to'g'ri chaqiramiz.
    #
    # OLX bu yerda ATAYLAB YO'Q: u yuqoridagi `sikl()` orqali yig'iladi.
    # Ikkalasi ham yursa OLX har 45 daqiqada ikki marta o'qiladi.
    jami = {}
    for kalit, adapter in yigish.adapterlar().items():
        if kalit == "olx":
            continue
        try:
            if toliq:
                # Adapter o'z chuqurligini e'lon qiladi (CHUQUR_SAHIFA);
                # e'lon qilmaganlar uchun 3 — eski me'yor.
                chuqur = getattr(adapter, "CHUQUR_SAHIFA", 3)
                natija = adapter.chuqur(chuqur)
            else:
                natija = adapter.bosh(1)
            jami[adapter.NOM] = natija
        except Exception as e:                       # noqa: BLE001
            print(f"  [yigish:{kalit}] xato: {type(e).__name__}: {e}")
            jami[adapter.NOM] = {"xato": 1}
    return jami


def kuzat(sahifalar: int = 1) -> None:
    """To'xtamay yuradi: issiq har 45 daqiqada, to'liq sutkada bir marta."""
    print("=" * 66)
    print("  OBER — YANGILIK SIKLI (to'xtatish: Ctrl+C)")
    print("=" * 66)
    print(f"\n  Issiq kategoriyalar: har {ISSIQ_ORALIQ // 60} daqiqada")
    print(f"  Barchasi:            har {TOLIQ_ORALIQ // 3600} soatda")
    print("  Telegram kanallari:  har siklda")
    oxirgi_toliq = 0.0
    while True:
        boshlandi = time.time()
        try:
            toliq_vaqti = time.time() - oxirgi_toliq >= TOLIQ_ORALIQ
            if toliq_vaqti:
                sikl(faqat_issiq=False, sahifalar=sahifalar)
                oxirgi_toliq = time.time()
            else:
                sikl(faqat_issiq=True, sahifalar=sahifalar)
            telegram_sikli()
            # Manba adapterlari: issiq siklda tez (1-2 sahifa), to'liq
            # siklda chuqur (ko'p sahifa + tavsiflar).
            yigish_sikli(toliq=toliq_vaqti)
        except KeyboardInterrupt:
            print("\n  To'xtatildi.")
            return
        except Exception as e:                       # noqa: BLE001
            # Sikl HECH QACHON o'lmasin. Bitta xato tufayli tunda
            # yangilanish to'xtab qolsa, ertalab ma'lumot eskirgan bo'ladi.
            print(f"  [xato] {type(e).__name__}: {e} — 5 daqiqada qayta")
            time.sleep(300)
            continue
        # Sikl o'zi 45 daqiqadan uzoq ketsa kutmaymiz — darhol keyingisi.
        # Aks holda "45 daqiqada bir marta" va'dasi jimgina buzilardi.
        kutish = max(0.0, ISSIQ_ORALIQ - (time.time() - boshlandi))
        if kutish:
            keyingi = time.time() + kutish
            print("  Keyingisi: "
                  f"{time.strftime('%H:%M', time.localtime(keyingi))}\n")
        try:
            time.sleep(kutish)
        except KeyboardInterrupt:
            print("\n  To'xtatildi.")
            return


def _toliq_belgi_oqi() -> float:
    """Oxirgi muvaffaqiyatli to'liq sikl vaqtini qaytaradi."""
    try:
        return float(TOLIQ_BELGI.read_text(encoding="ascii").strip())
    except (OSError, ValueError):
        return 0.0


def _toliq_belgi_yoz(vaqt: float | None = None) -> None:
    """To'liq sikl vaqtini atomar yozadi."""
    TOLIQ_BELGI.parent.mkdir(parents=True, exist_ok=True)
    vaqtinchalik = TOLIQ_BELGI.with_suffix(".tmp")
    vaqtinchalik.write_text(str(vaqt or time.time()), encoding="ascii")
    vaqtinchalik.replace(TOLIQ_BELGI)


def issiq_kuzat(sahifalar: int = 1) -> None:
    """Issiq kategoriyalar va Telegramni mustaqil yangilaydi."""
    print("=" * 66)
    print("  OBER — ISSIQ YANGILIK (to'xtatish: Ctrl+C)")
    print("=" * 66)
    print(f"\n  Issiq kategoriyalar: har {ISSIQ_ORALIQ // 60} daqiqada")
    print("  Telegram kanallari:  har siklda")
    while True:
        boshlandi = time.time()
        try:
            sikl(faqat_issiq=True, sahifalar=sahifalar)
            telegram_sikli()
        except KeyboardInterrupt:
            print("\n  To'xtatildi.")
            return
        except Exception as e:                       # noqa: BLE001
            print(f"  [xato] {type(e).__name__}: {e} — 5 daqiqada qayta")
            time.sleep(300)
            continue
        kutish = max(0.0, ISSIQ_ORALIQ - (time.time() - boshlandi))
        if kutish:
            keyingi = time.time() + kutish
            print("  Keyingi issiq sikl: "
                  f"{time.strftime('%H:%M', time.localtime(keyingi))}\n")
        try:
            time.sleep(kutish)
        except KeyboardInterrupt:
            print("\n  To'xtatildi.")
            return


def toliq_kuzat(sahifalar: int = 1) -> None:
    """Sutkalik to'liq siklni issiq sikldan mustaqil yuritadi."""
    print("=" * 66)
    print("  OBER — TO'LIQ YANGILIK (to'xtatish: Ctrl+C)")
    print("=" * 66)
    while True:
        oxirgi = _toliq_belgi_oqi()
        kutish = max(0.0, TOLIQ_ORALIQ - (time.time() - oxirgi)) if oxirgi else 0.0
        if kutish:
            keyingi = time.time() + kutish
            print("  Keyingi to'liq sikl: "
                  f"{time.strftime('%Y-%m-%d %H:%M', time.localtime(keyingi))}")
            try:
                time.sleep(kutish)
            except KeyboardInterrupt:
                print("\n  To'xtatildi.")
                return
        try:
            sikl(faqat_issiq=False, sahifalar=sahifalar)
            _toliq_belgi_yoz()
        except KeyboardInterrupt:
            print("\n  To'xtatildi.")
            return
        except Exception as e:                       # noqa: BLE001
            print(f"  [xato] {type(e).__name__}: {e} — 5 daqiqada qayta")
            time.sleep(300)


def main() -> int:
    args = [a.lower() for a in sys.argv[1:]]
    sahifalar = next((int(a) for a in args if a.isdigit()), 1)
    if "issiq-kuzat" in args:
        issiq_kuzat(sahifalar)
        return 0
    if "toliq-kuzat" in args:
        toliq_kuzat(sahifalar)
        return 0
    if "kuzat" in args:
        kuzat(sahifalar)
        return 0
    if "sinov" in args:
        sikl(faqat_issiq=True, sahifalar=sahifalar, cheklov=3)
        return 0
    sikl(faqat_issiq="hammasi" not in args, sahifalar=sahifalar)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
