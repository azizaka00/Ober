"""OBER — VAPID kriptografiyasi sinovi.

NEGA BU FAYL ENG MUHIMI
-----------------------
`vapid.py` dagi ECDSA qo'lda yozilgan. Qo'lda yozilgan
kriptografiyaning xavfi shundaki, XATO JIMGINA O'TADI: kod
ishlaydi, imzo hosil bo'ladi, hech qanday istisno chiqmaydi —
lekin imzo noto'g'ri yoki, undan yomoni, maxfiy kalitni oshkor
qiladi. "Ishladi" degan his bu yerda dalil emas.

Shuning uchun bu yerda o'z natijamizni o'zimiz bilan
solishtirmaymiz. RFC 6979 ning A.2.5 bo'limidagi RASMIY test
vektorlari ishlatiladi — ular IETF hujjatida bosilgan va butun
dunyodagi amalga oshiruvlar shu bilan tekshiriladi.

Agar bizning `k`, `r` yoki `s` ulardan bittasiga ham mos
kelmasa — amalga oshiruv noto'g'ri, tamom.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import vapid  # noqa: E402

# ── RFC 6979, A.2.5: ECDSA, 256 bit (Prime Field), P-256, SHA-256 ────
MAXFIY = 0xC9AFA9D845BA75166B5C215767B1D6934E50C3DB36E89B127B8A622B120F6721
OCHIQ_X = 0x60FED4BA255A9D31C961EB74C6356D68C049B8923B61FA6CE669622E60F29FB6
OCHIQ_Y = 0x7903FE1008B8BC99A41AE9E95628BC64F2F1B20C2D7E9F5177A3C294D4462299

VEKTORLAR = [
    # (xabar, kutilgan k, kutilgan r, kutilgan s)
    (b"sample",
     0xA6E3C57DD01ABE90086538398355DD4C3B17AA873382B0F24D6129493D8AAD60,
     0xEFD48B2AACB6A8FD1140DD9CD45E81D69D2C877B56AAF991C34D0EA84EAF3716,
     0xF7CB1C942D657C41D436C7A1B6E29F65F3E900DBB9AFF4064DC4AB2F843ACDA8),
    (b"test",
     0xD16B6AE827F17175E040871A1C7EC3500192C4C92677336EC2537ACAEE0008E0,
     0xF1ABB023518351CD71D881567B1EA663ED3EFCF6C5132B354F28D3B0B7D38367,
     0x019F4113742A2B14BD25926B49C649155F267E60D3814B4C0CC84250E46F0083),
]


def main() -> int:
    xato = 0
    jami = 0

    def tekshiruv(nom: str, shart: bool, izoh: str = "") -> None:
        nonlocal xato, jami
        jami += 1
        if shart:
            print(f"  OK   {nom}")
        else:
            xato += 1
            print(f"  XATO {nom}" + (f" — {izoh}" if izoh else ""))

    print("VAPID / P-256 ECDSA SINOVI")
    print("=" * 58)
    print("Manba: RFC 6979, A.2.5 (rasmiy test vektorlari)")
    print()

    # 1. Egri chiziq parametrlari o'zaro mos
    print("1. Egri chiziq")
    tekshiruv("G egri chiziqda yotadi", vapid.egrida_mi(vapid.G))
    tekshiruv("N * G = cheksizlik", vapid._kopaytir(vapid.N) is None,
              "guruh tartibi noto'g'ri")

    # 2. Ochiq kalit maxfiydan to'g'ri hosil bo'ladi
    print("\n2. Kalit hosil qilish")
    ochiq = vapid._kopaytir(MAXFIY)
    tekshiruv("ochiq kalit X mos", ochiq[0] == OCHIQ_X,
              f"olindi {ochiq[0]:x}")
    tekshiruv("ochiq kalit Y mos", ochiq[1] == OCHIQ_Y,
              f"olindi {ochiq[1]:x}")
    tekshiruv("ochiq kalit egri chiziqda", vapid.egrida_mi(ochiq))

    # 3. Deterministik k — RFC vektorlari bilan
    print("\n3. RFC 6979 deterministik k")
    import hashlib
    for xabar, kutilgan_k, _, _ in VEKTORLAR:
        xesh = hashlib.sha256(xabar).digest()
        olingan = vapid._deterministik_k(MAXFIY, xesh)
        tekshiruv(f"k({xabar.decode()})", olingan == kutilgan_k,
                  f"olindi {olingan:x}")

    # 4. Imzo — RFC vektorlari bilan
    print("\n4. RFC 6979 imzo (r, s)")
    for xabar, _, kutilgan_r, kutilgan_s in VEKTORLAR:
        imzo = vapid.imzola(MAXFIY, xabar)
        r = int.from_bytes(imzo[:32], "big")
        s = int.from_bytes(imzo[32:], "big")
        tekshiruv(f"r({xabar.decode()})", r == kutilgan_r, f"olindi {r:x}")
        tekshiruv(f"s({xabar.decode()})", s == kutilgan_s, f"olindi {s:x}")

    # 5. Determinizm: bir xil kirish — bir xil imzo.
    #    Bu tasodifiy k ISHLATILMAYOTGANINING dalili.
    print("\n5. Determinizm (tasodifiy k yo'qligining dalili)")
    a = vapid.imzola(MAXFIY, b"ober")
    b = vapid.imzola(MAXFIY, b"ober")
    tekshiruv("bir xil xabar — bir xil imzo", a == b,
              "k tasodifiy bo'lib qolgan — XAVFLI")
    tekshiruv("boshqa xabar — boshqa imzo",
              vapid.imzola(MAXFIY, b"ober2") != a)

    # 6. Tekshirish funksiyasi
    print("\n6. Imzoni tekshirish")
    tekshiruv("o'z imzosini qabul qiladi",
              vapid.tekshir(ochiq, b"ober", a))
    tekshiruv("buzilgan xabarni rad etadi",
              not vapid.tekshir(ochiq, b"obeR", a))
    buzuq = bytearray(a)
    buzuq[0] ^= 0x01
    tekshiruv("buzilgan imzoni rad etadi",
              not vapid.tekshir(ochiq, b"ober", bytes(buzuq)))
    tekshiruv("noto'g'ri uzunlikdagi imzoni rad etadi",
              not vapid.tekshir(ochiq, b"ober", a[:63]))

    # 7. Kodlash
    print("\n7. base64url va nuqta formati")
    tekshiruv("b64 to'ldiruvchisiz", "=" not in vapid.b64(b"abcde"))
    tekshiruv("b64 aylanma", vapid.b64_ochish(vapid.b64(b"\x00\xff\x10")) == b"\x00\xff\x10")
    xb = vapid.ochiq_bayt(ochiq)
    tekshiruv("ochiq kalit 65 bayt", len(xb) == 65, f"olindi {len(xb)}")
    tekshiruv("siqilmagan belgisi 0x04", xb[0] == 0x04)

    # 8. Yangi kalit juftligi izchilmi
    print("\n8. Yangi kalit yaratish")
    m2, o2 = vapid.kalit_yarat()
    tekshiruv("yangi ochiq kalit egri chiziqda", vapid.egrida_mi(o2))
    tekshiruv("yangi kalit bilan imzo tekshiriladi",
              vapid.tekshir(o2, b"sinov", vapid.imzola(m2, b"sinov")))
    tekshiruv("maxfiy kalit diapazonda", 1 <= m2 < vapid.N)

    # 9. JWT tuzilmasi
    print("\n9. VAPID JWT")
    token = vapid.jwt_yasa(MAXFIY, "https://fcm.googleapis.com",
                           "mailto:nematovazizbek7@gmail.com")
    qismlar = token.split(".")
    tekshiruv("uch qismdan iborat", len(qismlar) == 3, f"olindi {len(qismlar)}")
    import json
    sarlavha = json.loads(vapid.b64_ochish(qismlar[0]))
    tana = json.loads(vapid.b64_ochish(qismlar[1]))
    tekshiruv("alg = ES256", sarlavha.get("alg") == "ES256")
    tekshiruv("aud origin (to'liq endpoint EMAS)",
              tana.get("aud") == "https://fcm.googleapis.com")
    tekshiruv("sub bor", str(tana.get("sub", "")).startswith("mailto:"))
    import time
    muddat = tana.get("exp", 0) - int(time.time())
    tekshiruv("exp 24 soatdan kam", 0 < muddat <= 24 * 3600,
              f"{muddat} soniya")
    tekshiruv("JWT imzosi to'g'ri",
              vapid.tekshir(ochiq, qismlar[0].encode() + b"." + qismlar[1].encode(),
                            vapid.b64_ochish(qismlar[2])))

    print()
    print("-" * 58)
    if xato:
        print(f"NATIJA: {jami - xato} to'g'ri · {xato} xato  ({jami} tadan)")
        print()
        print("DIQQAT: kriptografiya xato. Push YOQILMASIN —")
        print("noto'g'ri imzo eng yaxshi holatda ishlamaydi, eng")
        print("yomonida maxfiy kalitni oshkor qiladi.")
        return 1
    print(f"NATIJA: {jami} to'g'ri · 0 xato  ({jami} tadan)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
