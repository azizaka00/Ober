"""`havola_nazorat` sinovi — tarmoqsiz, soxta HTTP javoblari bilan.

ENG MUHIM SINOV: YOLG'ON O'CHIRISH BO'LMASIN.

O'lik havolani o'tkazib yuborish — kichik zarar (keyingi yugurishda
tutiladi). Tirik e'lonni o'chirish — tuzatib bo'lmaydigan zarar.
Shuning uchun sinovlarning ko'pi aynan shuni tekshiradi: timeout,
403, 429, 5xx va 30x da e'lon HECH QACHON o'chmasligi kerak.
"""

from __future__ import annotations

import sys
import time

import baza
import havola_nazorat as hn

jami = 0
xato = 0


def tekshir(shart: bool, izoh: str) -> None:
    global jami, xato
    jami += 1
    if not shart:
        xato += 1
        print(f"  XATO  {izoh}")


def elon_qoy(havola: str, olik_soni=None) -> int:
    """Sinov uchun e'lon yaratadi va id qaytaradi."""
    with baza.ulan() as c:
        # `tashqi_id` NOT NULL — har sinov e'loniga noyob qiymat.
        c.execute(
            "INSERT INTO elonlar(manba, tashqi_id, nom, havola, faol,"
            " olik_soni) VALUES('sinov',?,'sinov e''loni',?,1,?)",
            (f"sinov-{time.time_ns()}", havola, olik_soni))
        c.commit()
        return c.execute("SELECT last_insert_rowid() i").fetchone()["i"]


def holat(elon_id: int) -> dict:
    with baza.ulan() as c:
        r = c.execute("SELECT faol, olik_soni, tekshirildi FROM elonlar"
                      " WHERE id=?", (elon_id,)).fetchone()
        return dict(r) if r else {}


def bitta(elon_id: int) -> list:
    """Aynan shu e'lonni qaytaradi.

    DIQQAT: asl `nomzodlar()` ni filtrlash ISHLAMAYDI. U
    `tekshirildi ASC, id ASC` bo'yicha saralaydi, ya'ni yangi
    qo'shilgan sinov e'loni (eng katta id) 126 ming yozuvning
    oxirida qoladi va ro'yxatga tushmaydi. Birinchi urinishda
    shu sabab "tekshiriladigan e'lon yo'q" chiqdi.
    """
    with baza.ulan() as c:
        return c.execute("SELECT id, havola, olik_soni FROM elonlar"
                         " WHERE id=?", (elon_id,)).fetchall()


def yugur(elon_id: int, kod, quruq=False) -> None:
    """Nazoratni bitta e'lon uchun soxta kod bilan yugurtiradi."""
    asl_kod, asl_nomzod, asl_argv = hn.holat_kodi, hn.nomzodlar, sys.argv
    hn.holat_kodi = lambda h: kod
    hn.nomzodlar = lambda n: bitta(elon_id)
    sys.argv = ["havola_nazorat", "--pauza", "0"] + (
        ["--quruq"] if quruq else [])
    try:
        hn.main()
    finally:
        hn.holat_kodi, hn.nomzodlar, sys.argv = asl_kod, asl_nomzod, asl_argv


def main() -> int:
    baza.init()
    hn._ustunlarni_qosh()
    print("\n  O'LIK HAVOLA NAZORATI SINOVI\n" + "-" * 52)

    # ── 1. TIRIK E'LON O'CHMAYDI ───────────────────────────────────
    for kod, nom in ((200, "200 OK"), (301, "301 ko'chirilgan"),
                     (302, "302 vaqtincha"), (403, "403 taqiq"),
                     (429, "429 ko'p so'rov"), (500, "500 server xatosi"),
                     (503, "503 band")):
        e = elon_qoy(f"https://sinov.uz/{kod}")
        yugur(e, kod)
        h = holat(e)
        tekshir(h.get("faol") == 1, f"{nom}: e'lon faol qolishi kerak")
        tekshir((h.get("olik_soni") or 0) == 0,
                f"{nom}: sanoq nolda qolishi kerak")

    # ── 2. TARMOQ XATOSI HECH NARSAGA TEGMAYDI ─────────────────────
    e = elon_qoy("https://sinov.uz/timeout")
    yugur(e, None)
    h = holat(e)
    tekshir(h.get("faol") == 1, "timeout: e'lon faol qolishi kerak")
    tekshir(h.get("tekshirildi") is None,
            "timeout: `tekshirildi` yangilanmasin — keyin qayta urinilsin")

    # ── 3. BITTA 404 O'CHIRMAYDI ───────────────────────────────────
    e = elon_qoy("https://sinov.uz/404-bir")
    yugur(e, 404)
    h = holat(e)
    tekshir(h.get("faol") == 1, "birinchi 404: hali o'chmasin")
    tekshir(h.get("olik_soni") == 1, "birinchi 404: sanoq 1 bo'lsin")

    # ── 4. IKKINCHI 404 O'CHIRADI ──────────────────────────────────
    yugur(e, 404)
    h = holat(e)
    tekshir(h.get("faol") == 0, "ikkinchi 404: nofaollashsin")
    tekshir(h.get("olik_soni") == 2, "ikkinchi 404: sanoq 2 bo'lsin")

    # ── 5. 410 HAM O'LIK HISOBLANADI ───────────────────────────────
    e = elon_qoy("https://sinov.uz/410", olik_soni=1)
    yugur(e, 410)
    tekshir(holat(e).get("faol") == 0, "410 (Gone): nofaollashsin")

    # ── 6. QAYTGAN E'LON SANOQNI NOLGA QAYTARADI ───────────────────
    # Sahifa vaqtincha yo'qolib qaytishi mumkin. Yig'ilgan sanoq
    # qolib ketsa, keyingi bitta 404 uni darhol o'chirardi.
    e = elon_qoy("https://sinov.uz/qaytdi", olik_soni=1)
    yugur(e, 200)
    tekshir(holat(e).get("olik_soni") == 0,
            "200 qaytgach sanoq nolga tushsin")
    yugur(e, 404)
    tekshir(holat(e).get("faol") == 1,
            "nolga tushgach bitta 404 o'chirmasin")

    # ── 7. QURUQ REJIM BAZAGA YOZMAYDI ─────────────────────────────
    e = elon_qoy("https://sinov.uz/quruq", olik_soni=1)
    yugur(e, 404, quruq=True)
    h = holat(e)
    tekshir(h.get("faol") == 1, "quruq rejim: e'lon o'chmasin")
    tekshir(h.get("olik_soni") == 1, "quruq rejim: sanoq o'zgarmasin")

    # ── 8. FAQAT 404 VA 410 O'LIK RO'YXATIDA ───────────────────────
    tekshir(hn.OLIK_KODLAR == (404, 410),
            "o'lik kodlar ro'yxati kengaymasin — 403/5xx qo'shilmasin")

    # Tozalash
    with baza.ulan() as c:
        c.execute("DELETE FROM elonlar WHERE manba='sinov'")
        c.commit()

    print("-" * 52)
    print(f"  NATIJA: {jami - xato} to'g'ri · {xato} xato  ({jami} tadan)\n")
    return 1 if xato else 0


if __name__ == "__main__":
    raise SystemExit(main())
