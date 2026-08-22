"""`xato_xabar` sinovi — tarmoqsiz, Sentry'ga hech narsa yubormaydi.

ENG MUHIM SINOV: SHOVQIN O'TMASIN, HAQIQIY XATO O'TSIN.

2026-08-17 da Sentry'dan kelgan birinchi xabar mijoz uzilishi edi
(`ConnectionResetError`, `127.0.0.1` dan — ya'ni Caddy). Bu vebda
kundalik hodisa: odam tabni yopadi, sahifadan chiqadi, telefon
tarmog'i tushadi. Uni "new issue" qilib yuborish Sentry'ni shovqinga
to'ldiradi va haqiqiy xato ko'rinmay qoladi.

Lekin AYNAN SHU turdagi istisno tashqariga chiqqan ulanishda
(OLX yig'ish, Telegram yuborish) HAQIQIY muammo. Shuning uchun
sinovning yarmi "jim qilinsin", yarmi "jim qilinmasin" ni tekshiradi.

ISHLATISH
---------
    python app/xato_sinov.py
"""

from __future__ import annotations

import os
import traceback

# DSN bo'lmasa modul jim ishlaydi — sinov hech qachon tashqariga
# so'rov yubormasin.
os.environ.pop("OBER_SENTRY_DSN", None)

import xato_xabar as xx                                 # noqa: E402

jami = 0
xato = 0


def tekshir(shart: bool, izoh: str) -> None:
    global jami, xato
    jami += 1
    if not shart:
        xato += 1
        print(f"  XATO  {izoh}")


def iz(*fayllar: str):
    """Soxta traceback izi — faqat fayl nomlari muhim."""
    return [traceback.FrameSummary(f, 1, "f") for f in fayllar]


def main() -> int:
    print("\n  XATO XABAR SINOVI\n" + "-" * 52)

    # ── 1. KIRUVCHI ULANISH — JIM QILINADI ─────────────────────────
    for fayl in ("/usr/lib/python3.10/socketserver.py",
                 "/usr/lib/python3.10/http/server.py",
                 "C:\\Python310\\Lib\\http\\server.py"):
        tekshir(
            xx._mijoz_uzildimi(ConnectionResetError(104, "reset"),
                               iz("app/server.py", fayl)),
            f"kiruvchi uzilish jim qilinsin ({fayl})")

    tekshir(xx._mijoz_uzildimi(BrokenPipeError(32, "broken"),
                               iz("/usr/lib/python3.10/socketserver.py")),
            "BrokenPipeError ham mijoz uzilishi")
    tekshir(xx._mijoz_uzildimi(ConnectionAbortedError(103, "abort"),
                               iz("/usr/lib/python3.10/socketserver.py")),
            "ConnectionAbortedError ham mijoz uzilishi")

    # ── 2. CHIQUVCHI ULANISH — JIM QILINMAYDI ──────────────────────
    #
    # Bu eng muhim yarim. OLX yig'ish yoki Telegram yuborish paytida
    # ulanish uzilsa — bu haqiqiy muammo va ko'rinishi SHART.
    tekshir(not xx._mijoz_uzildimi(
        ConnectionResetError(104, "reset"),
        iz("app/olx.py", "/usr/lib/python3.10/urllib/request.py")),
        "OLX yig'ishdagi uzilish JIM QILINMASIN")
    tekshir(not xx._mijoz_uzildimi(
        ConnectionResetError(104, "reset"),
        iz("app/tg.py", "/usr/lib/python3.10/http/client.py")),
        "Telegram yuborishdagi uzilish JIM QILINMASIN")

    # ── 3. BOSHQA ISTISNOLAR UMUMAN TEGILMAYDI ─────────────────────
    for x in (ValueError("x"), KeyError("k"), TimeoutError("t"),
              OSError(5, "I/O")):
        tekshir(not xx._mijoz_uzildimi(
            x, iz("/usr/lib/python3.10/socketserver.py")),
            f"{type(x).__name__} jim qilinmasin — u mijoz uzilishi emas")

    # ── 4. IZ BO'SH BO'LSA — JIM QILINMAYDI ────────────────────────
    #
    # Dalil yo'q bo'lsa xatoni yashirish noto'g'ri: bilmaslik
    # "muammo yo'q" degani emas.
    tekshir(not xx._mijoz_uzildimi(ConnectionResetError(104, "reset"), []),
            "izsiz uzilish jim qilinmasin — dalil yo'q")

    # ── 5. IZNING FAQAT OXIRI QARALADI ─────────────────────────────
    #
    # `socketserver` chuqurda, oxirida esa bizning kod bo'lsa —
    # bu chiqib ketgan xato, mijoz uzilishi emas.
    uzun = iz("/usr/lib/python3.10/socketserver.py", "app/server.py",
              "app/baza.py", "app/qidiruv.py", "app/lugat.py",
              "app/joylar.py", "app/tahlil.py")
    tekshir(not xx._mijoz_uzildimi(ConnectionResetError(104, "r"), uzun),
            "iz chuqurida socketserver bo'lsa ham, oxiri bizniki bo'lsa —"
            " jim qilinmasin")

    # ── 6. DSN YO'Q — MODUL JIM VA XATO BERMAYDI ───────────────────
    tekshir(xx.yoqilganmi() is False, "DSN yo'q — o'chiq")
    try:
        xx.xato(ConnectionResetError(104, "reset"), {"sinov": 1})
        xx.xato(ValueError("haqiqiy xato"), {"sinov": 2})
        xx.ornat()
        tinch = True
    except Exception:                                    # noqa: BLE001
        tinch = False
    tekshir(tinch, "DSN yo'qda ham hech narsa yiqilmasin")

    print("-" * 52)
    print(f"  NATIJA: {jami - xato} to'g'ri · {xato} xato  ({jami} tadan)\n")
    return 1 if xato else 0


if __name__ == "__main__":
    raise SystemExit(main())
