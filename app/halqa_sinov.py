"""
OBER — TO'LIQ HALQA SINOVI

Brauzersiz, boshdan oxirigacha:
  xaridor qidiradi -> topilmaydi -> so'rov qoldiradi ->
  sotuvchi ro'yxatdan o'tadi -> so'rovni KO'RADI -> bir tegishda javob beradi ->
  xaridor javobni KO'RADI

Har qadamda tekshiriladi. Bitta bo'g'in uzilsa — darhol ko'rinadi.
Sinov ma'lumoti oxirida o'chiriladi (haqiqiy bazaga aralashmaydi).
"""

from __future__ import annotations

import sys

import baza
from lugat import modellarni_top, normalla, qismlarni_top
from qidiruv import qidir
from yonalishlar import yonalishlarni_top

OK, XATO = 0, 0


def tek(shart: bool, matn: str, izoh: str = "") -> None:
    global OK, XATO
    if shart:
        OK += 1
        print(f"  [OK  ] {matn}")
    else:
        XATO += 1
        print(f"  [XATO] {matn}" + (f"  -> {izoh}" if izoh else ""))


def main() -> None:
    baza.init()
    print("=" * 64)
    print("  OBER — TO'LIQ HALQA SINOVI")
    print("=" * 64)

    # ── 1. Xaridor qidiradi
    print("\n  1. XARIDOR QIDIRADI")
    n = qidir("neksiya kolodka", "")
    tek(isinstance(n.get("jami"), int), "qidiruv ishlaydi")
    tek("nexia" in n["tushunildi"]["modellar"], "model tanildi (nexia)",
        str(n["tushunildi"]))
    tek("kolodka" in n["tushunildi"]["qismlar"], "qism tanildi (kolodka)",
        str(n["tushunildi"]))

    # ── 2. Qidiruv yozib borilyaptimi
    print("\n  2. QIDIRUV YOZILADI")
    with baza.ulan() as c:
        oldin = c.execute("SELECT COUNT(*) n FROM qidiruvlar").fetchone()["n"]
    baza.qidiruv_yoz("sinov-qidiruv", n, "Сергелийский район")
    with baza.ulan() as c:
        keyin = c.execute("SELECT COUNT(*) n FROM qidiruvlar").fetchone()["n"]
    tek(keyin == oldin + 1, "qidiruv bazaga yozildi")

    # ── 3. So'rov qoldiradi
    print("\n  3. XARIDOR SO'ROV QOLDIRADI")
    matn = "Neksiya 3 ga old tormoz kolodka kerak"
    sorov_id = baza.sorov_yoz(
        matn, "Сергелийский район", "+998901112233", 200000,
        sorted(modellarni_top(matn)), sorted(qismlarni_top(matn)))
    tek(bool(sorov_id), "so'rov yaratildi", f"id={sorov_id}")
    with baza.ulan() as c:
        s = c.execute("SELECT * FROM sorovlar WHERE id=?", (sorov_id,)).fetchone()
    tek(s["holat"] == "yangi", "holati 'yangi'")
    tek("kolodka" in (s["qismlar"] or ""), "so'rovda qism aniqlangan",
        s["qismlar"] or "(bo'sh)")
    tek(s["byudjet"] == 200000, "byudjet saqlandi")

    # ── 4. Sotuvchi ro'yxatdan o'tadi
    print("\n  4. SOTUVCHI RO'YXATDAN O'TADI")
    nima = "tormoz kolodka, disk, support"
    q_s = sorted(qismlarni_top(nima))
    sotuvchi_id = baza.sotuvchi_yoz("Sinov Avto", nima, q_s,
                                    sorted(modellarni_top(nima)),
                                    "Сергелийский район", "+998907778899")
    tek(bool(sotuvchi_id), "sotuvchi yaratildi")
    tek("kolodka" in q_s, "sotuvchi yo'nalishi tushunildi", str(q_s))

    # ── 5. Sotuvchi so'rovni KO'RADIMI (eng muhim bog'lanish)
    print("\n  5. SOTUVCHI SO'ROVNI KO'RADI")
    ruyxat = baza.sotuvchi_sorovlari(sotuvchi_id)
    idlar = [r["id"] for r in ruyxat]
    tek(sorov_id in idlar, "so'rov sotuvchiga yetib bordi",
        f"ko'rgani: {idlar}")
    if sorov_id in idlar:
        r = next(x for x in ruyxat if x["id"] == sorov_id)
        tek(r["yaqin"] is True, "bir xil tuman 'yaqin' deb belgilandi")
        tek("aloqa" not in r, "xaridor telefoni sotuvchiga ochilmadi")

    # ── 6. Begona yo'nalishdagi sotuvchiga BORMASLIGI kerak
    print("\n  6. BEGONA SOTUVCHIGA BORMAYDI (spam himoyasi)")
    begona_nima = "akkumulyator, akumlyator"
    begona_id = baza.sotuvchi_yoz("Akum Sinov", begona_nima,
                                  sorted(qismlarni_top(begona_nima)), [],
                                  "Сергелийский район", "+998900000000")
    begona_ruyxat = [r["id"] for r in baza.sotuvchi_sorovlari(begona_id)]
    tek(sorov_id not in begona_ruyxat,
        "kolodka so'rovi akkumulyator sotuvchisiga BORMADI",
        f"ko'rgani: {begona_ruyxat}")

    # ── 6-A. UNIVERSAL BANNER PILOTI VA XAVFSIZ ROUTING
    print("\n  6-A. BANNER PILOTI VA XAVFSIZ ROUTING")
    banner_matn = "25 kv banner kerak, 5 ga 5 metr"
    banner_qidiruv = qidir(banner_matn, "")
    banner_begona = [e for e in banner_qidiruv["natijalar"]
                     if "baner" not in normalla(e.get("nom") or "")]
    tek(not banner_begona, "banner so'roviga begona e'lon chiqmaydi")
    tek(bool(banner_qidiruv["tushunildi"]["yonalishlar"]),
        "banner yo'nalishi tanildi")
    banner_y = sorted(yonalishlarni_top(banner_matn))
    banner_sorov = baza.sorov_yoz(
        banner_matn, "Toshkent shahri", "+998901234567", 300000,
        [], [], banner_y)
    banner_sotuvchi = baza.sotuvchi_yoz(
        "Print Sinov", "banner va tashqi reklama", [], [],
        "Toshkent shahri", "+998909999999", banner_y)
    banner_idlar = [r["id"] for r in baza.sotuvchi_sorovlari(banner_sotuvchi)]
    tek(banner_sorov in banner_idlar,
        "banner so'rovi faqat banner sotuvchisiga yetdi")
    avto_idlar = [r["id"] for r in baza.sotuvchi_sorovlari(sotuvchi_id)]
    tek(banner_sorov not in avto_idlar,
        "banner so'rovi avto sotuvchisiga BORMADI")

    noma_matn = "menga bir narsa kerak"
    noma_sorov = baza.sorov_yoz(
        noma_matn, "", "+998900001111", None, [], [], [])
    tek(noma_sorov not in [r["id"] for r in baza.sotuvchi_sorovlari(banner_sotuvchi)],
        "aniqlanmagan so'rov sotuvchiga tarqalmadi")

    # ── 7. Bir tegishda javob
    print("\n  7. SOTUVCHI JAVOB BERADI")
    baza.javob_yoz(sorov_id, sotuvchi_id, "bor", 150000, "")
    with baza.ulan() as c:
        s2 = c.execute("SELECT holat FROM sorovlar WHERE id=?",
                       (sorov_id,)).fetchone()
    tek(s2["holat"] == "javob_bor", "so'rov holati yangilandi")

    ikkinchi_id = baza.sotuvchi_yoz(
        "Ikkinchi Avto", nima, q_s, sorted(modellarni_top(nima)),
        "Toshkent shahri", "+998901010101")
    tek(sorov_id not in [r["id"] for r in baza.sotuvchi_sorovlari(ikkinchi_id)],
        "javob kelgach yangi sotuvchiga ortiqcha yuborilmaydi")

    # ── 8. Javob bergan so'rov qayta ko'rsatilmasin
    qayta = [r["id"] for r in baza.sotuvchi_sorovlari(sotuvchi_id)]
    tek(sorov_id not in qayta, "javob berilgan so'rov ro'yxatdan chiqdi")

    # ── 9. Xaridor javobni KO'RADIMI (halqa yopiladi)
    print("\n  8. XARIDOR JAVOBNI KO'RADI")
    javoblar = baza.sorov_javoblari(sorov_id)
    tek(len(javoblar) == 1, "javob xaridorga yetib bordi",
        f"{len(javoblar)} ta")
    if javoblar:
        j = javoblar[0]
        tek(j["narx"] == 150000, "narx to'g'ri")
        tek("aloqa" not in j, "sotuvchi telefoni xaridorga ochilmadi")
        tek(j["nom"] == "Sinov Avto", "sotuvchi nomi ko'rinadi")

    # ── Tozalash
    # Sotuvchilar avval o'chiriladi — `sotuvchi_ochir` ularning
    # suhbatlari, xabarlari, javoblari va yuborishlarini ham oladi.
    # Keyin qolgan javoblar so'rov bo'yicha, so'ng so'rovlarning o'zi.
    for sid in (sotuvchi_id, begona_id, banner_sotuvchi, ikkinchi_id):
        baza.sotuvchi_ochir(sid)
    with baza.ulan() as c:
        c.execute("DELETE FROM javoblar WHERE sorov_id=?", (sorov_id,))
        c.execute("DELETE FROM sorovlar WHERE id IN (?,?,?)",
                  (sorov_id, banner_sorov, noma_sorov))
        c.execute("DELETE FROM qidiruvlar WHERE sorov='sinov-qidiruv'")

    print("\n" + "-" * 64)
    print(f"  NATIJA: {OK} to'g'ri · {XATO} xato")
    print("  (sinov ma'lumoti o'chirildi)\n")
    return 1 if XATO else 0


if __name__ == "__main__":
    sys.exit(main())
