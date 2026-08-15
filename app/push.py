"""OBER — Web Push yuboruvchi. Standart kutubxona, kutubxonasiz.

QANDAY ISHLAYDI
---------------
Brauzer push xizmatiga (Chrome uchun FCM, Firefox uchun Mozilla)
obuna bo'ladi va bizga `endpoint` manzilini beradi. Biz o'sha
manzilga POST yuboramiz, xizmat esa xabarni telefonga yetkazadi.

Server o'zini VAPID kaliti bilan tanitadi — `vapid.py` dagi
qo'lda yozilgan ECDSA imzo. Aks holda xizmat 401 qaytaradi.

NEGA PAYLOADSIZ (bu asosiy qaror)
---------------------------------
Web Push payloadini shifrlash mumkin, lekin u ECDH + HKDF +
AES-128-GCM talab qiladi. Python standart kutubxonasida ECDH ham,
AES ham YO'Q. Ya'ni shifrlashni ham qo'lda yozish kerak bo'lardi —
imzolashdan ancha murakkab va xato qilish osonroq joy.

Yechim: BO'SH push yuboramiz. Brauzer service worker'ni
uyg'otadi, SW esa `/api/bildirishnomalar` ga o'zi murojaat qilib
matnni oladi. Natija foydalanuvchi uchun bir xil — telefon
jiringlaydi va xabar ko'rinadi.

Qo'shimcha yutuq: xabar matni push xizmati (ya'ni Google)
serveridan UMUMAN o'tmaydi. Shifrlangan payload ham o'qilmaydi,
lekin bo'lmagan narsa umuman xavf tug'dirmaydi.

Yagona shart: SW `push` hodisasida albatta bildirishnoma
ko'rsatishi kerak (`userVisibleOnly`). Aks holda brauzer obunani
bekor qiladi. `sw.js` shuni bajaradi.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import vapid

ILDIZ = Path(__file__).resolve().parent.parent
KALIT_FAYL = ILDIZ / "data" / "vapid.json"

# VAPID `sub` — push xizmati muammo bo'lsa shu manzilga yozadi.
ALOQA = "mailto:nematovazizbek7@gmail.com"

# JWT ni har yuborishda qayta imzolash isrof: bitta imzo ~40 ms
# (sof Python). Bir xil audience uchun u 12 soat yaroqli, shuning
# uchun keshlaymiz. 100 ta obunaga 100 ta imzo emas, 1-2 ta imzo.
_jwt_kesh: dict[str, tuple[str, float]] = {}


def kalit_ol() -> tuple[int, tuple[int, int]]:
    """VAPID kalitini o'qiydi, bo'lmasa BIR MARTA yaratadi.

    Kalit o'zgarsa barcha obunalar kuchini yo'qotadi — shuning
    uchun u faylda saqlanadi va qayta yaratilmaydi.
    """
    if KALIT_FAYL.is_file():
        m = json.loads(KALIT_FAYL.read_text(encoding="utf-8"))
        maxfiy = int(m["maxfiy"], 16)
        return maxfiy, (int(m["x"], 16), int(m["y"], 16))

    maxfiy, ochiq = vapid.kalit_yarat()
    KALIT_FAYL.parent.mkdir(parents=True, exist_ok=True)
    KALIT_FAYL.write_text(json.dumps({
        "maxfiy": f"{maxfiy:064x}",
        "x": f"{ochiq[0]:064x}",
        "y": f"{ochiq[1]:064x}",
        "yaratildi": int(time.time()),
        "izoh": "VAPID kaliti. YO'QOTMANG - o'zgarsa barcha obunalar uziladi.",
    }, indent=2), encoding="utf-8")
    try:
        KALIT_FAYL.chmod(0o600)
    except OSError:
        pass          # Windows'da chmod ishlamaydi, muammo emas
    return maxfiy, ochiq


def ochiq_kalit_b64() -> str:
    """Brauzerga beriladigan `applicationServerKey`."""
    _, ochiq = kalit_ol()
    return vapid.b64(vapid.ochiq_bayt(ochiq))


def _audience(endpoint: str) -> str:
    """Endpoint'dan ORIGIN ajratiladi.

    Ko'p uchraydigan xato: `aud` ga to'liq endpoint yoziladi va
    xizmat 401 beradi. RFC 8292 origin talab qiladi.
    """
    q = urllib.parse.urlsplit(endpoint)
    return f"{q.scheme}://{q.netloc}"


def _jwt(endpoint: str) -> str:
    aud = _audience(endpoint)
    kesh = _jwt_kesh.get(aud)
    # Muddat tugashiga 1 soat qolganda yangilaymiz.
    if kesh and kesh[1] - time.time() > 3600:
        return kesh[0]
    maxfiy, _ = kalit_ol()
    token = vapid.jwt_yasa(maxfiy, aud, ALOQA, muddat_soat=12)
    _jwt_kesh[aud] = (token, time.time() + 12 * 3600)
    return token


def yubor(endpoint: str, ttl: int = 86400) -> tuple[bool, int, str]:
    """Bitta obunaga bo'sh push yuboradi.

    Qaytaradi: (muvaffaqiyat, http_kodi, izoh)

    Kodlar:
      201  — qabul qilindi
      404  — obuna yo'q
      410  — obuna bekor qilingan (foydalanuvchi ruxsatni oldi)
      429  — juda ko'p so'rov
    404 va 410 da obunani BAZADAN O'CHIRISH kerak: u boshqa hech
    qachon ishlamaydi va har yuborishda behuda urinish bo'ladi.
    """
    _, ochiq = kalit_ol()
    sorov = urllib.request.Request(
        endpoint, data=b"", method="POST",
        headers={
            "TTL": str(ttl),
            "Content-Length": "0",
            "Authorization": (f"vapid t={_jwt(endpoint)}, "
                              f"k={vapid.b64(vapid.ochiq_bayt(ochiq))}"),
        })
    try:
        with urllib.request.urlopen(sorov, timeout=10) as javob:
            return True, javob.status, "ok"
    except urllib.error.HTTPError as e:
        tana = ""
        try:
            tana = e.read().decode("utf-8", "replace")[:200]
        except Exception:
            pass
        return False, e.code, tana or e.reason
    except urllib.error.URLError as e:
        return False, 0, f"tarmoq: {e.reason}"
    except OSError as e:
        return False, 0, f"tarmoq: {e}"


def olib_tashlash_kerakmi(kod: int) -> bool:
    """404/410 — obuna butunlay o'lgan, bazadan o'chiriladi."""
    return kod in (404, 410)
