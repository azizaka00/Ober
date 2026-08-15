"""OBER — push bildirishnomalarini yuboruvchi halqa.

`tg.py` dagi `bildirish_halqa` bilan bir xil tuzilma va bir xil
sabab: yuborish alohida oqimda ketadi, chunki bitta sekin tarmoq
so'rovi butun navbatni to'xtatmasligi kerak.

TELEGRAMDAN MUSTAQIL
--------------------
`xabarlar.push_yuborildi` — `tg_yuborildi` dan ALOHIDA ustun.
Foydalanuvchi ikkalasiga ham obuna bo'lishi mumkin va ikkalasini
ham olishi kerak. Bitta bayroqni bo'lishganda biri ikkinchisini
"yuborilgan" deb o'tkazib yuborardi.

KIMGA KETADI
------------
Xabar `rol='xaridor'` bo'lsa — sotuvchiga.
Xabar `rol='sotuvchi'` bo'lsa — xaridorga.
Ya'ni xabarni YOZGAN odamga o'zining xabari qaytmaydi.
"""
from __future__ import annotations

import time

import baza
import push

ORALIQ = 3.0

# Ketma-ket shuncha xatodan keyin obuna o'chiriladi. O'lik obuna
# har aylanishda 10 soniya kutishga sabab bo'lib, butun navbatni
# sekinlashtiradi.
XATO_CHEGARASI = 5


def _kimga(xabar: dict) -> tuple[str, int] | None:
    """Xabar kimga borishi kerak: (rol, egasi)."""
    egalar = baza.push_suhbat_egasi(xabar["suhbat_id"])
    if not egalar:
        return None
    if xabar["rol"] == "xaridor":
        return "sotuvchi", egalar["sotuvchi_id"]
    if xabar["rol"] == "sotuvchi":
        return "xaridor", egalar["sorov_id"]
    return None


def sikl() -> int:
    """Bir aylanish. Yuborilgan bildirishnomalar sonini qaytaradi."""
    xabarlar = baza.push_yuborilmagan()
    if not xabarlar:
        return 0

    yuborildi = 0
    for x in xabarlar:
        manzil = _kimga(x)
        if not manzil:
            # Suhbat o'chirilgan — bu xabarni boshqa urinmaymiz.
            baza.push_belgila(x["id"])
            continue

        rol, egasi = manzil
        obunalar = baza.push_obunalar(rol, egasi)

        # Obuna yo'q — bu XATO EMAS. Odam push'ga ruxsat bermagan
        # bo'lishi mumkin (Telegram baribir ishlaydi). Belgilaymiz,
        # aks holda bu xabar navbatda abadiy qolib, har aylanishda
        # qayta ko'rib chiqilardi.
        if not obunalar:
            baza.push_belgila(x["id"])
            continue

        for endpoint in obunalar:
            ok, kod, izoh = push.yubor(endpoint)
            if ok:
                yuborildi += 1
                continue
            if push.olib_tashlash_kerakmi(kod):
                baza.push_obuna_ochir(endpoint)
                print(f"  [push] obuna o'chirildi ({kod}): "
                      f"{endpoint[:48]}...", flush=True)
                continue
            n = baza.push_xato_qayd(endpoint)
            print(f"  [push] xato {kod} ({n}-marta): {izoh[:80]}", flush=True)
            if n >= XATO_CHEGARASI:
                baza.push_obuna_ochir(endpoint)
                print("  [push] ketma-ket xato — obuna o'chirildi",
                      flush=True)

        baza.push_belgila(x["id"])
    return yuborildi


def halqa() -> None:
    print("  [push] bildirishnoma halqasi ishga tushdi", flush=True)
    while True:
        try:
            sikl()
        except Exception as e:                    # noqa: BLE001
            print(f"  [push] halqa xatosi: {type(e).__name__}: {e}",
                  flush=True)
        time.sleep(ORALIQ)
