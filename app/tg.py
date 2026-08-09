"""
OBER — Telegram orqali kirishni tasdiqlash

Telegram faqat akkauntni bog'lash va bir martalik kirish kodini yuborish
uchun ishlatiladi. So'rov, taklif va savdo yozishmalari OBER ichida qoladi.

QOIDA: token faqat `data/bot-token.txt` faylida turadi. Kodda yozilmaydi,
jurnalga chiqarilmaydi.
"""

from __future__ import annotations

import json
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

import baza

API = "https://api.telegram.org/bot{token}/{usul}"
TOKEN_FAYL = "bot-token.txt"

_KUTILAYOTGAN_NARX: dict[str, tuple[int, int, str]] = {}   # chat -> (sorov, sotuvchi, holat)
_OGOHLANTIRILDI: dict[str, bool] = {}
SAVDO_XABARLARI = False


def token() -> str:
    """Tokenni fayldan o'qiydi. Yo'q bo'lsa — bo'sh satr (bot o'chiq)."""
    fayl = baza.DB.with_name(TOKEN_FAYL)
    try:
        return fayl.read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def _sorov(usul: str, _timeout: int = 35, **maydonlar):
    t = token()
    if not t:
        return None
    tana = json.dumps(maydonlar).encode()
    req = urllib.request.Request(
        API.format(token=t, usul=usul), data=tana,
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=_timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        # Tokenni jurnalga CHIQARMAYMIZ — faqat holat kodi.
        # 409 = bitta botga ikkita dastur ulangan. Bu odatda serverning
        # ikki marta ishga tushirilgani. Ekranni to'ldirmasligi uchun
        # bir marta aytamiz va kutamiz (2026-08-01 da shunday bo'lgan).
        if e.code == 409:
            if not _OGOHLANTIRILDI.get("409"):
                _OGOHLANTIRILDI["409"] = True
                print("\n  [tg] DIQQAT: bu botga boshqa dastur ham ulangan.")
                print("       Server ikki marta ishga tushirilgan bo'lishi mumkin.")
                print("       Barcha cmd oynalarini yopib, bittasini oching.\n")
            time.sleep(15)
        else:
            print(f"  [tg] HTTP {e.code} ({usul})")
    except Exception as e:                        # noqa: BLE001
        print(f"  [tg] {type(e).__name__} ({usul})")
    return None


def yubor(chat_id, matn: str, tugmalar=None) -> bool:
    """Xabar yuboradi. Muvaffaqiyatli bo'lsa True qaytaradi.

    2026-08-06: kirish kodini yuborishda JAVOBni tekshirish kerak — aks
    holda foydalanuvchiga "kod yuborildi" deb aytib, kod hech qachon
    bormasa ishonch buziladi. Ilgari bu funksiya hech narsa qaytarmasdi.
    """
    d = {"chat_id": chat_id, "text": matn, "parse_mode": "HTML"}
    if tugmalar:
        d["reply_markup"] = {"inline_keyboard": tugmalar}
    natija = _sorov("sendMessage", **d)
    return bool(natija and natija.get("ok"))


_NOM_KESH = {"nom": None, "vaqt": 0.0}


def bot_nomi() -> str:
    """Bot username. KESHLANADI — aks holda har sahifa ochilishida
    Telegramga so'rov ketadi va sahifa qotib qoladi (2026-08-01)."""
    if _NOM_KESH["nom"] is not None and time.time() - _NOM_KESH["vaqt"] < 3600:
        return _NOM_KESH["nom"]
    d = _sorov("getMe", _timeout=8)
    try:
        nom = d["result"]["username"]
    except Exception:                             # noqa: BLE001
        nom = ""
    _NOM_KESH.update(nom=nom, vaqt=time.time())
    return nom


# ── Kiruvchi xabarlar ────────────────────────────────────────────────────────

def _start(chat_id, kod: str) -> None:
    if not kod:
        yubor(chat_id,
              "Salom! Bu — <b>OBER</b> sotuvchi boti.\n\n"
              "Ulanish uchun OBER sotuvchi kabinetidagi "
              "<b>“Telegramga ulash”</b> tugmasini bosing.")
        return
    s = baza.telegram_ulash(kod, chat_id)
    if not s:
        yubor(chat_id, "Kod eskirgan. OBER’da qaytadan “Telegramga ulash”ni bosing.")
        return
    yubor(chat_id,
          f"✅ Ulandi: <b>{s.get('nom') or 'Sotuvchi'}</b>\n\n"
          "Telegram faqat OBER kirish kodlari uchun ishlatiladi. "
          "So‘rov va savdo yozishmalari OBER ichida qoladi.")


def _javob_yoz(chat_id, sorov_id: int, sotuvchi_id: int,
               holat: str, narx: int | None) -> None:
    baza.javob_yoz(sorov_id, sotuvchi_id, holat, narx, "")
    if holat == "yoq":
        yubor(chat_id, "Rahmat, belgilandi.")
    else:
        yubor(chat_id, f"✅ Taklif yuborildi{f' — {narx:,} so‘m'.replace(',', ' ') if narx else ''}\n"
                       "Xaridor sizga OBER ichida yozishi mumkin.")


def _tugma(chat_id, ma: dict) -> None:
    """callback_data: `j|<sorov>|<holat>`"""
    if not SAVDO_XABARLARI:
        yubor(chat_id, "Taklif va yozishmalar endi faqat OBER ichida ishlaydi.")
        return
    try:
        _, sorov_s, holat = str(ma.get("data") or "").split("|")
        sorov_id = int(sorov_s)
    except ValueError:
        return
    s = baza.sotuvchi_telegramdan(chat_id)
    if not s:
        yubor(chat_id, "Avval OBER’da “Telegramga ulash”ni bosing.")
        return
    if not baza.sorov_ochiqmi(sorov_id):
        yubor(chat_id, "Bu so‘rov yopilgan.")
        return
    if baza.javob_berilganmi(sorov_id, s["id"]):
        yubor(chat_id, "Bu so‘rovga allaqachon javob bergansiz.")
        return

    if holat == "yoq":
        _javob_yoz(chat_id, sorov_id, s["id"], "yoq", None)
        return
    # BOR yoki O'XSHASHI BOR -> narx so'raymiz
    _KUTILAYOTGAN_NARX[str(chat_id)] = (sorov_id, s["id"], holat)
    yubor(chat_id, "Narxini yozing (faqat raqam). Masalan: <code>265000</code>")


def _matn(chat_id, matn: str) -> None:
    if matn.startswith("/start"):
        _start(chat_id, matn[6:].strip())
        return
    if not SAVDO_XABARLARI:
        yubor(chat_id,
              "Bu bot faqat OBER kirish kodlari uchun. "
              "Taklif va yozishmalar OBER ichidagi <b>Chat</b>da.")
        return
    kutilyapti = _KUTILAYOTGAN_NARX.get(str(chat_id))
    if not kutilyapti:
        if matn.startswith("/start"):
            _start(chat_id, matn[6:].strip())
            return
        # CHAT BOTDA EMAS (Aziz, 2026-08-01: "ortiqcha chat botlar kerak
        # emas"). Bot bitta ish qiladi: yangi so'rovni yetkazadi va
        # BOR/YO'Q/narxni oladi. Erkin yozishma — saytda va ilovada,
        # chunki u yerda rasm, joylashuv va onlayn holat bor.
        yubor(chat_id,
              "Javob berish uchun so‘rov ostidagi tugmani bosing.\n"
              "Xaridor bilan yozishish uchun OBER’dagi <b>Chat</b>ni oching.")
        return
    raqam = "".join(ch for ch in matn if ch.isdigit())
    if not raqam:
        yubor(chat_id, "Faqat raqam yozing. Masalan: <code>265000</code>")
        return
    sorov_id, sotuvchi_id, holat = kutilyapti
    _KUTILAYOTGAN_NARX.pop(str(chat_id), None)
    _javob_yoz(chat_id, sorov_id, sotuvchi_id, holat, int(raqam))


# ── Chiquvchi xabarlar ───────────────────────────────────────────────────────

def _sorov_matni(x: dict) -> str:
    qatorlar = [f"🔔 <b>{x['matn']}</b>"]
    ikkinchi = []
    if x.get("tuman"):
        ikkinchi.append(x["tuman"])
    if x.get("byudjet"):
        ikkinchi.append(f"byudjet {int(x['byudjet']):,}".replace(",", " ") + " so‘m")
    if ikkinchi:
        qatorlar.append(" · ".join(ikkinchi))
    return "\n".join(qatorlar)


def kutayotganlarni_yubor() -> int:
    """Yangi so'rovlarni Telegramga uzatadi. Har biriga bir marta."""
    if not SAVDO_XABARLARI:
        return 0
    n = 0
    for x in baza.yuborilmagan_xabarlar():
        tugmalar = [[
            {"text": "BOR", "callback_data": f"j|{x['sorov_id']}|bor"},
            {"text": "YO‘Q", "callback_data": f"j|{x['sorov_id']}|yoq"},
        ], [
            {"text": "O‘XSHASHI BOR",
             "callback_data": f"j|{x['sorov_id']}|oxshash"},
        ]]
        yubor(x["telegram_id"], _sorov_matni(x), tugmalar)
        baza.xabar_belgila(x["yid"])
        n += 1
    return n


# ── Asosiy halqa ─────────────────────────────────────────────────────────────

def halqa() -> None:
    if not token():
        print("  [tg] token yo‘q — bot o‘chiq (data/bot-token.txt)")
        return
    nom = bot_nomi()
    print(f"  [tg] bot ishga tushdi: @{nom}" if nom else "  [tg] bot ishga tushdi")

    ofset = 0
    while True:
        try:
            d = _sorov("getUpdates", offset=ofset, timeout=25)
            for u in (d or {}).get("result", []):
                ofset = u["update_id"] + 1
                if "message" in u:
                    m = u["message"]
                    _matn(m["chat"]["id"], (m.get("text") or "").strip())
                elif "callback_query" in u:
                    q = u["callback_query"]
                    _sorov("answerCallbackQuery", callback_query_id=q["id"])
                    _tugma(q["message"]["chat"]["id"], q)
            kutayotganlarni_yubor()
        except Exception as e:                    # noqa: BLE001
            # 2026-08-04: bu yerda faqat `type(e).__name__` yozilardi.
            # Jurnal 14 soat davomida "OperationalError" deb takrorladi va
            # SABABINI aytmadi — natijada sayt tushganini bilib bo'lmadi.
            # Xato matni HAR DOIM yozilsin: "database is locked" bilan
            # "attempt to write a readonly database" butunlay boshqa dard.
            print(f"  [tg] halqa xatosi: {type(e).__name__}: {e}", flush=True)
            time.sleep(5)


def fonda_boshla() -> None:
    """Serverga ulanib fonda ishlaydi. Token yo'q bo'lsa jim turadi."""
    if not token():
        return
    threading.Thread(target=halqa, daemon=True).start()


if __name__ == "__main__":
    halqa()
