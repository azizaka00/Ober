"""OBER — VAPID imzosi. P-256 ECDSA, sof Python, kutubxonasiz.

NEGA QO'LDA YOZILDI (2026-08-14)
--------------------------------
Web Push serveri o'zini VAPID kaliti bilan tanitadi: `ES256` bilan
imzolangan JWT. `ES256` = ECDSA, P-256 egri chizig'i, SHA-256.

Python standart kutubxonasida elliptik egri chiziq YO'Q. Loyiha
qoidasi esa qat'iy: `pip install` yo'q, backend faqat standart
kutubxona. Ikki yo'ldan biri kerak edi — qoidani buzish yoki
imzolashni o'zimiz yozish. Aziz ikkinchisini tanladi.

XAVF VA U QANDAY YOPILGAN
-------------------------
ECDSA da eng mashhur falokat — `k` (bir martalik tasodifiy son).
Agar `k` ikki xil xabar uchun TAKRORLANSA, maxfiy kalitni oddiy
algebra bilan tiklab bo'ladi. PlayStation 3 shu xatodan sindirilgan.

Shuning uchun bu yerda tasodifiy `k` UMUMAN ishlatilmaydi.
RFC 6979 bo'yicha `k` xabar va maxfiy kalitdan HMAC-SHA256 bilan
DETERMINISTIK hosil qilinadi. Tasodif manbai yo'q — demak uning
buzilishi ham yo'q. Bir xil xabar har doim bir xil imzo beradi.

To'g'riligi taxminga qoldirilmagan: `vapid_sinov.py` RFC 6979
ning A.2.5 bo'limidagi RASMIY test vektorlari bilan solishtiradi.
Ular mos kelmasa sinov yiqiladi.

NIMA QILMAYDI
-------------
Bu modul faqat IMZOLAYDI. Push payloadini shifrlash (ECDH + AES-GCM)
yo'q va kerak ham emas: biz payloadsiz push yuboramiz, matnni
service worker o'zi API'dan oladi. Sabab `push.py` izohida.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time

# ── P-256 (secp256r1 / prime256v1) parametrlari ──────────────────────
# Manba: NIST FIPS 186-4, D.1.2.3
P = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
A = P - 3
B = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
N = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
GX = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
GY = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
G = (GX, GY)

# Cheksizlik nuqtasi (guruh birligi).
CHEKSIZ: tuple[int, int] | None = None


# ── Egri chiziq arifmetikasi ─────────────────────────────────────────
# Affin koordinatalar. Jacobian tezroq, lekin bizga sekundiga bir
# necha imzo kerak, xolos — soddalik muhimroq: sodda kodda xato kam.

def _qosh(p1, p2):
    """Ikki nuqtani qo'shish."""
    if p1 is CHEKSIZ:
        return p2
    if p2 is CHEKSIZ:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        if (y1 + y2) % P == 0:
            return CHEKSIZ          # P + (-P) = cheksizlik
        # Ikkilantirish: qiyalik = (3x^2 + a) / 2y
        qiyalik = (3 * x1 * x1 + A) * pow(2 * y1, P - 2, P) % P
    else:
        qiyalik = (y2 - y1) * pow(x2 - x1, P - 2, P) % P
    x3 = (qiyalik * qiyalik - x1 - x2) % P
    y3 = (qiyalik * (x1 - x3) - y1) % P
    return (x3, y3)


def _kopaytir(k: int, nuqta=G):
    """Skalyar ko'paytirish: k * nuqta.

    Ikkilantir-va-qo'sh usuli. Bu yerda `k` MAXFIY, shuning uchun
    vaqt bo'yicha hujum haqida o'ylash kerak bo'lardi — lekin biz
    serverdamiz, hujumchi imzolash vaqtini o'lchay olmaydi (u
    faqat tayyor JWT ni ko'radi). Shu sabab oddiy variant yetarli.
    """
    k %= N
    natija = CHEKSIZ
    qoshiluvchi = nuqta
    while k:
        if k & 1:
            natija = _qosh(natija, qoshiluvchi)
        qoshiluvchi = _qosh(qoshiluvchi, qoshiluvchi)
        k >>= 1
    return natija


def egrida_mi(nuqta) -> bool:
    """Nuqta haqiqatan egri chiziqda yotadimi: y^2 == x^3 + ax + b."""
    if nuqta is CHEKSIZ:
        return True
    x, y = nuqta
    return (y * y - (x * x * x + A * x + B)) % P == 0


# ── RFC 6979: deterministik k ────────────────────────────────────────

def _bits2int(b: bytes) -> int:
    """Baytlarni butun songa; ortiqcha bitlar o'ngdan tashlanadi."""
    son = int.from_bytes(b, "big")
    ortiqcha = len(b) * 8 - N.bit_length()
    return son >> ortiqcha if ortiqcha > 0 else son


def _int2octets(x: int) -> bytes:
    return x.to_bytes(32, "big")


def _bits2octets(b: bytes) -> bytes:
    z1 = _bits2int(b)
    z2 = z1 - N
    return _int2octets(z2 if z2 >= 0 else z1)


def _deterministik_k(maxfiy: int, xesh: bytes) -> int:
    """RFC 6979, 3.2-bo'lim. HMAC-SHA256 asosida."""
    h1 = xesh
    v = b"\x01" * 32
    k = b"\x00" * 32
    x = _int2octets(maxfiy)
    o = _bits2octets(h1)

    k = hmac.new(k, v + b"\x00" + x + o, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    k = hmac.new(k, v + b"\x01" + x + o, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()

    while True:
        v = hmac.new(k, v, hashlib.sha256).digest()
        nomzod = _bits2int(v)
        if 1 <= nomzod < N:
            return nomzod
        # Nomzod diapazondan chiqdi — RFC bo'yicha qayta hosil qilamiz.
        k = hmac.new(k, v + b"\x00", hashlib.sha256).digest()
        v = hmac.new(k, v, hashlib.sha256).digest()


# ── Imzolash ─────────────────────────────────────────────────────────

def imzola(maxfiy: int, xabar: bytes) -> bytes:
    """ECDSA imzo, 64 bayt: r (32) || s (32) — JOSE formati."""
    xesh = hashlib.sha256(xabar).digest()
    e = _bits2int(xesh)
    while True:
        k = _deterministik_k(maxfiy, xesh)
        nuqta = _kopaytir(k)
        if nuqta is CHEKSIZ:
            continue
        r = nuqta[0] % N
        if r == 0:
            continue
        s = pow(k, N - 2, N) * (e + r * maxfiy) % N
        if s == 0:
            continue
        return r.to_bytes(32, "big") + s.to_bytes(32, "big")


def tekshir(ochiq: tuple[int, int], xabar: bytes, imzo: bytes) -> bool:
    """Imzoni tekshirish. Faqat o'z-o'zini sinash uchun."""
    if len(imzo) != 64:
        return False
    r = int.from_bytes(imzo[:32], "big")
    s = int.from_bytes(imzo[32:], "big")
    if not (1 <= r < N and 1 <= s < N):
        return False
    e = _bits2int(hashlib.sha256(xabar).digest())
    w = pow(s, N - 2, N)
    nuqta = _qosh(_kopaytir(e * w % N), _kopaytir(r * w % N, ochiq))
    if nuqta is CHEKSIZ:
        return False
    return nuqta[0] % N == r


# ── Kalit ────────────────────────────────────────────────────────────

def b64(xom: bytes) -> str:
    """base64url, to'ldiruvchisiz — JWT va VAPID shuni talab qiladi."""
    return base64.urlsafe_b64encode(xom).rstrip(b"=").decode("ascii")


def b64_ochish(matn: str) -> bytes:
    return base64.urlsafe_b64decode(matn + "=" * (-len(matn) % 4))


def kalit_yarat() -> tuple[int, tuple[int, int]]:
    """Yangi VAPID kalit juftligi.

    `secrets` — operatsion tizimning kriptografik tasodif manbai.
    Kalit BIR MARTA yaratiladi va saqlanadi; o'zgarsa barcha
    mavjud obunalar kuchini yo'qotadi.
    """
    import secrets
    maxfiy = secrets.randbelow(N - 1) + 1
    return maxfiy, _kopaytir(maxfiy)


def ochiq_bayt(ochiq: tuple[int, int]) -> bytes:
    """Siqilmagan nuqta: 0x04 || X(32) || Y(32) — 65 bayt.

    `applicationServerKey` brauzerga aynan shu ko'rinishda beriladi.
    """
    return b"\x04" + ochiq[0].to_bytes(32, "big") + ochiq[1].to_bytes(32, "big")


# ── VAPID JWT ────────────────────────────────────────────────────────

def jwt_yasa(maxfiy: int, audience: str, aloqa: str,
             muddat_soat: int = 12) -> str:
    """VAPID uchun `ES256` JWT.

    `audience` — push xizmatining ORIGIN'i (masalan
    `https://fcm.googleapis.com`), to'liq endpoint emas. Ko'p
    uchraydigan xato shu: to'liq endpoint yozilsa xizmat 401 beradi.

    Muddat 24 soatdan oshmasligi kerak (RFC 8292). 12 soat olamiz —
    soat farqi bo'lsa ham xavfsiz oraliq qoladi.
    """
    sarlavha = {"typ": "JWT", "alg": "ES256"}
    tana = {
        "aud": audience,
        "exp": int(time.time()) + muddat_soat * 3600,
        "sub": aloqa,
    }
    qism = (b64(json.dumps(sarlavha, separators=(",", ":")).encode()) + "."
            + b64(json.dumps(tana, separators=(",", ":")).encode()))
    imzo = imzola(maxfiy, qism.encode("ascii"))
    return qism + "." + b64(imzo)
