"""OBER — xatolarni Sentry'ga yuborish (2026-08-16).

NEGA KERAK
----------
Bugungacha jonli saytdagi xatoni faqat Aziz aytganda bilardik.
2026-08-16 da uchta xato shunday topildi: saralash tugmalari
o'qilmasdi, lenta yolg'on va'da berardi, kurs "—" bo'lib qolardi.
Uchalasini ham odam ko'rib aytdi, kod emas.

Endi xato o'zi xabar beradi: qaysi so'rovda, qaysi qatorda, necha
marta.

NEGA KUTUBXONA YO'Q
-------------------
`sentry-sdk` `pip install` talab qiladi. CLAUDE.md qoidasi: Python
standart kutubxonasi, yangi bog'liqlik yo'q. Sentry esa oddiy HTTP
qabul qiladi — "envelope" formati hujjatlashtirilgan va barqaror.
Bu fayl atigi shuni yuboradi.

KALIT KODDA EMAS
----------------
DSN muhit o'zgaruvchisidan olinadi: `OBER_SENTRY_DSN`. Serverda
`/etc/ober-sentry.env` (chmod 600) da turadi, xuddi AI kaliti kabi.
Git'ga hech qachon tushmaydi.

DSN yo'q bo'lsa modul JIM ishlaydi — hech narsa yubormaydi, xato
ham bermaydi. Ya'ni mahalliy ishlash va sinovlar o'zgarmaydi.

XATO XABAR YUBORISH SAYTNI BUZMASLIGI SHART
-------------------------------------------
Bu yerdagi HAR bir amal `try` ichida. Sentry o'chgan bo'lsa, tarmoq
yo'q bo'lsa, format o'zgargan bo'lsa — OBER hech narsa sezmasligi
kerak. Xato haqida xabar berish jarayoni o'zi xato bo'lib saytni
yiqitsa, bu kulgili va halokatli bo'lardi.
"""

from __future__ import annotations

import json
import os
import socket
import sys
import threading
import time
import traceback
import urllib.parse
import urllib.request
import uuid

_DSN = os.environ.get("OBER_SENTRY_DSN") or ""
_MUHIT = os.environ.get("OBER_MUHIT") or "production"

# Bir xil xato takrorlanganda har safar yubormaymiz — Sentry ham,
# tarmoq ham bezovta bo'lmasin. Kalit: fayl+qator+tur.
_OXIRGI: dict[str, float] = {}
_TAKROR_ORALIQ = 300.0          # bir xil xato 5 daqiqada bir marta
_QULF = threading.Lock()


def _manzil() -> tuple[str, str] | None:
    """DSN'dan (envelope URL, ochiq kalit) chiqaradi.

    DSN ko'rinishi:  https://<ochiq_kalit>@<host>/<loyiha_id>
    """
    if not _DSN:
        return None
    try:
        u = urllib.parse.urlparse(_DSN)
        loyiha = u.path.strip("/")
        if not (u.hostname and u.username and loyiha):
            return None
        port = f":{u.port}" if u.port else ""
        return (f"{u.scheme}://{u.hostname}{port}/api/{loyiha}/envelope/",
                u.username)
    except Exception:                                # noqa: BLE001
        return None


def yoqilganmi() -> bool:
    return _manzil() is not None


# ── MIJOZ UZILISHI XATO EMAS (2026-08-17) ────────────────────────────
#
# Sentry'dan kelgan birinchi haqiqiy xabar shu bo'ldi:
#
#     NAIZA-API-4 — ConnectionResetError: [Errno 104]
#     Connection reset by peer
#
# Jurnalda manbasi ko'rindi:
#
#     Exception occurred during processing of request
#     from ('127.0.0.1', 34656)
#
# `127.0.0.1` — bu Caddy, ya'ni KIRUVCHI ulanish. Mijoz javob
# yozilayotgan payt uzilgan: odam tabni yopdi, boshqa sahifaga o'tdi
# yoki telefon tarmog'i tushdi. Vebda bu KUNDALIK hodisa, serverning
# nosozligi emas.
#
# `ThreadingHTTPServer` har so'rovni alohida ipda bajaradi, `ornat()`
# esa `threading.excepthook` qo'yadi — natijada har uzilish Sentry'ga
# "new issue" bo'lib ketardi. API'lar 2-4 soniya javob berayotgan
# paytda (o'lchov 2026-08-17) bunday uzilish ko'p bo'ladi va Sentry
# shovqinga to'ladi. Shovqin ichida haqiqiy xato ko'rinmay qoladi —
# ya'ni nazorat vositasi o'zini o'zi ko'r qiladi.
#
# CHEGARA ANIQ: faqat KIRUVCHI ulanish jim qilinadi. Tashqariga
# chiqqan ulanish uzilsa (OLX yig'ish, Telegram yuborish) — bu
# HAQIQIY muammo va Sentry'ga boradi. Ikkalasi bir xil turdagi
# istisno, farqi izda: kiruvchisi `socketserver`/`http.server`
# ichida tugaydi.
_UZILISH = (ConnectionResetError, BrokenPipeError, ConnectionAbortedError)
_KIRUVCHI_FAYLLAR = ("socketserver.py", "http/server.py", "http\\server.py")


def _mijoz_uzildimi(xat: BaseException, iz) -> bool:
    if not isinstance(xat, _UZILISH):
        return False
    return any(str(k.filename).endswith(_KIRUVCHI_FAYLLAR) for k in iz[-6:])


def _yubor_ipda(url: str, kalit: str, tana: bytes) -> None:
    soz = urllib.request.Request(url, data=tana, method="POST", headers={
        "Content-Type": "application/x-sentry-envelope",
        "X-Sentry-Auth": (
            "Sentry sentry_version=7, sentry_client=ober/1.0, "
            f"sentry_key={kalit}"),
    })
    try:
        urllib.request.urlopen(soz, timeout=6).read()
    except Exception:                                # noqa: BLE001
        # Jim. Xato xabar berish xatosi jurnalni ifloslantirmasin.
        pass


def xato(xat: BaseException, qoshimcha: dict | None = None) -> None:
    """Istisnoni Sentry'ga yuboradi. Hech qachon o'zi xato bermaydi."""
    try:
        manzil = _manzil()
        if not manzil:
            return
        url, kalit = manzil

        iz = traceback.extract_tb(xat.__traceback__)
        if _mijoz_uzildimi(xat, iz):
            return
        oxirgi = iz[-1] if iz else None
        belgi = (f"{type(xat).__name__}:"
                 f"{oxirgi.filename if oxirgi else '?'}:"
                 f"{oxirgi.lineno if oxirgi else 0}")

        hozir = time.time()
        with _QULF:
            if hozir - _OXIRGI.get(belgi, 0.0) < _TAKROR_ORALIQ:
                return
            _OXIRGI[belgi] = hozir
            if len(_OXIRGI) > 500:               # xotira o'smasin
                _OXIRGI.clear()

        hodisa = {
            "event_id": uuid.uuid4().hex,
            "timestamp": hozir,
            "platform": "python",
            "level": "error",
            "logger": "ober",
            "server_name": socket.gethostname(),
            "environment": _MUHIT,
            "exception": {"values": [{
                "type": type(xat).__name__,
                "value": str(xat)[:400],
                "stacktrace": {"frames": [{
                    "filename": k.filename,
                    "function": k.name,
                    "lineno": k.lineno,
                    "context_line": k.line,
                } for k in iz[-25:]]},
            }]},
            "extra": qoshimcha or {},
        }

        sarlavha = json.dumps({"event_id": hodisa["event_id"]})
        tana_j = json.dumps(hodisa, ensure_ascii=False)
        element = json.dumps({"type": "event",
                              "length": len(tana_j.encode("utf-8"))})
        tana = f"{sarlavha}\n{element}\n{tana_j}\n".encode("utf-8")

        # Fon ipida — so'rov javobini kutdirmaydi.
        threading.Thread(target=_yubor_ipda, args=(url, kalit, tana),
                         daemon=True).start()
    except Exception:                                # noqa: BLE001
        pass


def ornat() -> None:
    """Tutilmagan istisnolarni ham qamrab oladi."""
    if not yoqilganmi():
        return
    asl = sys.excepthook

    def qarmoq(tur, qiymat, iz):
        xato(qiymat, {"manba": "excepthook"})
        asl(tur, qiymat, iz)

    sys.excepthook = qarmoq

    try:                                             # ip ichidagi xatolar
        asl_ip = threading.excepthook

        def ip_qarmoq(a):
            if a.exc_value is not None:
                xato(a.exc_value, {"manba": "thread",
                                   "ip": getattr(a.thread, "name", "?")})
            asl_ip(a)

        threading.excepthook = ip_qarmoq
    except Exception:                                # noqa: BLE001
        pass
