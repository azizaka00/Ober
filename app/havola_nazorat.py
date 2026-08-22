"""OBER — o'lik havola nazorati (2026-08-16).

MUAMMO
------
E'lon hozir faqat BILVOSITA o'chadi: yig'uvchi uni ketma-ket 3 sikl
ko'rmasa `korilmadi>=3` bo'lib `faol=0` bo'ladi (`baza` 3356-qator).

Bu manba ro'yxatidan tushgan e'lonni tutadi. Lekin ro'yxatda qolib,
sahifasi o'chirilgan e'lonni TUTMAYDI — u faol bo'lib turaveradi va
xaridor bosganda 404 ga tushadi.

Aziz aytdi: bu ishonchni bir zumda yo'q qiladi. Ayniqsa AI agentlar
OBERdan javob ola boshlasa — chirigan havola qaytarsa qaytmaydi.

TAMOYIL: FAQAT ANIQ DALIL O'CHIRADI
-----------------------------------
Nofaollashtirish uchun manba sahifasi ANIQ yo'qligini aytishi kerak:
`404 Not Found` yoki `410 Gone`. Boshqa hech narsa emas.

Ataylab TEGILMAYDIGAN holatlar:
  timeout, ulanish xatosi  -> bizning tarmoq, e'lonning aybi emas
  403, 429                 -> himoya/cheklov, e'lon bor bo'lishi mumkin
  5xx                      -> manba sayti nosoz
  30x                      -> ko'chirilgan, o'chirilmagan

Sabab oddiy: yolg'on o'chirish tuzatib bo'lmaydigan zarar. OLX bir
soat nosoz bo'lsa va biz 5xx ni "o'lik" deb hisoblasak — o'sha soatda
tekshirilgan hamma e'lon yo'qoladi.

IKKI MARTA TASDIQ
-----------------
Bitta 404 ham yetarli emas. Sahifa vaqtincha yo'qolib qaytishi mumkin
(nashr, moderatsiya, keshdan tushish). Shuning uchun sanoq yuritiladi:
ikkinchi 404 dan keyin nofaollashadi. Bir marta 200 qaytsa sanoq
nolga qaytadi.

MANBAGA HURMAT
--------------
So'rovlar sekin: sukut bo'yicha 2 soniyada bitta va bir yugurishda
200 tadan ko'p emas. `HEAD` ishlatiladi — tana yuklanmaydi.
Ba'zi saytlar `HEAD` ni qo'llamaydi (405), o'shanda `GET` bilan
faqat sarlavha o'qiladi va ulanish darhol yopiladi.

CLAUDE.md qoidasi: CAPTCHA yechilmaydi, Cloudflare aylanilmaydi,
`robots` taqiqi buzilmaydi. Bu yerda hech biri qilinmaydi — biz
faqat allaqachon yig'ilgan havolani so'raymiz.

ISHLATISH
---------
    python app/havola_nazorat.py              # 200 ta tekshiradi
    python app/havola_nazorat.py --soni 50
    python app/havola_nazorat.py --quruq      # o'chirmaydi, faqat aytadi
"""

from __future__ import annotations

import argparse
import sys
import time
import urllib.error
import urllib.request

import baza

# Bir yugurishda nechta. Kichik son ataylab: nazorat fon ishi,
# poyga emas. Kuniga bir necha marta yugursa indeks toza qoladi.
SONI = 200

# So'rovlar orasidagi pauza. 2 soniya = soatiga ~1800 so'rov, bu
# OLX uchun sezilmaydigan yuk.
PAUZA = 2.0

# Nechta ketma-ket 404 dan keyin nofaollashtiriladi.
CHEGARA = 2

KUTISH = 12          # soniya, bitta so'rov uchun
AGENT = "OBER-havola-nazorat/1.0 (+https://ober.uz)"

# ANIQ O'LIK deb hisoblanadigan yagona kodlar.
OLIK_KODLAR = (404, 410)


def _ustunlarni_qosh() -> None:
    """`tekshirildi` va `olik_soni` ustunlari (bir martalik)."""
    with baza.ulan() as c:
        bor = {r[1] for r in c.execute("PRAGMA table_info(elonlar)")}
        for nom, tur in (("tekshirildi", "REAL"), ("olik_soni", "INTEGER")):
            if nom not in bor:
                c.execute(f"ALTER TABLE elonlar ADD COLUMN {nom} {tur}")
        c.commit()


def holat_kodi(havola: str) -> int | None:
    """HTTP holat kodi. Tarmoq xatosida `None` — bu "bilmadim".

    `None` va kod farqi muhim: `None` hech qachon o'chirishga olib
    kelmaydi.
    """
    for usul in ("HEAD", "GET"):
        soz = urllib.request.Request(havola, method=usul,
                                     headers={"User-Agent": AGENT})
        try:
            with urllib.request.urlopen(soz, timeout=KUTISH) as j:
                return j.status
        except urllib.error.HTTPError as x:
            # 405 = HEAD qo'llanmaydi. GET bilan qayta urinamiz.
            if x.code == 405 and usul == "HEAD":
                continue
            return x.code
        except Exception:                            # noqa: BLE001
            # Timeout, DNS, SSL, ulanish uzilishi — "bilmadim".
            return None
    return None


def nomzodlar(soni: int) -> list:
    """Eng uzoq vaqt tekshirilmagan faol e'lonlar."""
    with baza.ulan() as c:
        return c.execute(
            "SELECT id, havola, olik_soni FROM elonlar"
            " WHERE faol=1 AND havola IS NOT NULL AND havola<>''"
            " ORDER BY COALESCE(tekshirildi, 0) ASC, id ASC"
            " LIMIT ?", (soni,)).fetchall()


def main() -> int:
    p = argparse.ArgumentParser(description="O'lik havola nazorati")
    p.add_argument("--soni", type=int, default=SONI)
    p.add_argument("--pauza", type=float, default=PAUZA)
    p.add_argument("--quruq", action="store_true",
                   help="o'chirmaydi, faqat hisobot beradi")
    a = p.parse_args()

    baza.init()
    _ustunlarni_qosh()

    ro = nomzodlar(a.soni)
    if not ro:
        print("  tekshiriladigan e'lon yo'q")
        return 0

    print(f"\n  O'lik havola nazorati — {len(ro)} ta e'lon"
          f"{' (QURUQ)' if a.quruq else ''}\n")

    hisob = {"tirik": 0, "olik": 0, "nomalum": 0, "ochirildi": 0}
    hozir = time.time()

    for i, r in enumerate(ro):
        if i:
            time.sleep(a.pauza)
        kod = holat_kodi(r["havola"])

        if kod is None:
            # Bilmadik. HECH NARSA o'zgartirmaymiz — `tekshirildi` ham
            # yangilanmaydi, shunda keyingi yugurishda yana urinamiz.
            hisob["nomalum"] += 1
            continue

        if kod in OLIK_KODLAR:
            son = (r["olik_soni"] or 0) + 1
            hisob["olik"] += 1
            ochirilsin = son >= CHEGARA
            if ochirilsin:
                hisob["ochirildi"] += 1
                print(f"    o'lik ({kod}) x{son} -> nofaol: {r['havola'][:66]}")
            if not a.quruq:
                with baza.ulan() as c:
                    if ochirilsin:
                        c.execute(
                            "UPDATE elonlar SET faol=0, olik_soni=?,"
                            " tekshirildi=? WHERE id=?",
                            (son, hozir, r["id"]))
                    else:
                        c.execute(
                            "UPDATE elonlar SET olik_soni=?, tekshirildi=?"
                            " WHERE id=?", (son, hozir, r["id"]))
                    c.commit()
            continue

        # Har qanday boshqa kod (200, 30x, 403, 5xx) — tirik deb
        # hisoblaymiz va sanoqni NOLGA QAYTARAMIZ. Vaqtincha 404
        # bo'lgan e'lon qaytsa, u yig'ilgan sanoq bilan qolmasin.
        hisob["tirik"] += 1
        if not a.quruq:
            with baza.ulan() as c:
                c.execute("UPDATE elonlar SET olik_soni=0, tekshirildi=?"
                          " WHERE id=?", (hozir, r["id"]))
                c.commit()

    print(f"\n  tirik {hisob['tirik']} · o'lik javob {hisob['olik']}"
          f" · nofaollashdi {hisob['ochirildi']}"
          f" · noma'lum {hisob['nomalum']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
