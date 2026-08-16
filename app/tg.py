"""
OBER — Telegram orqali kirish va sotuvchi bildirishnomalari

Telegram akkauntni bog'laydi, bir martalik kirish kodini yuboradi va
sotuvchiga yangi so'rov hamda xaridor xabari kelganini bildiradi. Erkin
yozishma OBER chatida davom etadi; to'lov va yetkazib berish OBER orqali
bajarilmaydi.

QOIDA: token faqat `data/bot-token.txt` faylida turadi. Kodda yozilmaydi,
jurnalga chiqarilmaydi.
"""

from __future__ import annotations

import json
import html
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
SAVDO_XABARLARI = True
OBER_CHAT = "https://ober.uz/takliflar?rol=sotuvchi"
BILDIRISH_ORALIGI = 2.0
_FONDA_QULF = threading.Lock()
_FONDA_BOSHLANDI = False


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
        _OXIRGI_KOD.kod = e.code
        return None
    except Exception as e:                        # noqa: BLE001
        print(f"  [tg] {type(e).__name__} ({usul})")
    _OXIRGI_KOD.kod = 0
    return None


# Oxirgi HTTP xato kodi. `yubor` uni o'qib, xato QAYTARIB BO'LMAYDIGANmi
# yoki vaqtinchalikmi ekanini ajratadi.
_OXIRGI_KOD = threading.local()

# QAYTA URINISH FOYDASIZ BO'LGAN KODLAR.
#
# 403 — foydalanuvchi botni bloklagan yoki hech qachon ochmagan.
# 400 — chat topilmadi / noto'g'ri chat_id.
#
# Bularda qayta urinish HECH QACHON yordam bermaydi: chat_id o'zgarmasa
# javob ham o'zgarmaydi.
QAYTARIB_BOLMAYDI = (400, 403)

# Kiruvchi getUpdates va chiquvchi sendMessage alohida threadlarda ishlaydi.
# Oxirgi HTTP kod umumiy global bo'lsa, getUpdates timeouti sendMessage'ning
# 403 kodini bosib ketib, foydasiz xabarni cheksiz qayta yuborishi mumkin.
# threading.local har halqaning natijasini o'zida saqlaydi.


def yubor(chat_id, matn: str, tugmalar=None) -> bool:
    """Xabar yuboradi. Muvaffaqiyatli bo'lsa True qaytaradi.

    2026-08-06: kirish kodini yuborishda JAVOBni tekshirish kerak — aks
    holda foydalanuvchiga "kod yuborildi" deb aytib, kod hech qachon
    bormasa ishonch buziladi. Ilgari bu funksiya hech narsa qaytarmasdi.
    """
    d = {"chat_id": chat_id, "text": matn, "parse_mode": "HTML"}
    if tugmalar:
        d["reply_markup"] = {"inline_keyboard": tugmalar}
    _OXIRGI_KOD.kod = 0
    natija = _sorov("sendMessage", **d)
    return bool(natija and natija.get("ok"))


def qaytarib_bolmaydi() -> bool:
    """Oxirgi yuborish QAYTARIB BO'LMAYDIGAN xato bilan tugadimi.

    NEGA KERAK (2026-08-11, jonli serverda topildi)
    -----------------------------------------------
    Savdo bildirishnomalari birinchi marta yoqilganda jurnal shu bilan
    to'ldi — har 2 soniyada, to'xtovsiz:

        [tg] HTTP 403 (sendMessage)
        [tg] HTTP 403 (sendMessage)

    Qoida shunday edi: xabar yuborilmasa yozuv "yuborildi" deb
    belgilanmaydi va keyingi aylanishda qayta uriniladi. Vaqtinchalik
    xato (timeout, 5xx) uchun bu to'g'ri.

    Lekin 403 vaqtinchalik EMAS — sotuvchi botni bloklagan yoki
    umuman ochmagan. `chat_id` o'zgarmaguncha javob ham o'zgarmaydi.
    Qayta urinish hech qachon yordam bermaydi va Telegram API'da
    bizni cheklab qo'yishi mumkin.

    Bunday holatda xabar "urinib ko'rildi" deb belgilanadi va navbatdan
    chiqadi. Sotuvchining `telegram_id` siga TEGILMAYDI: u OBER
    kabinetida xabarni baribir ko'radi, ulanishni o'zi tiklashi ham
    mumkin. Biz faqat foydasiz urinishni to'xtatamiz.
    """
    return getattr(_OXIRGI_KOD, "kod", 0) in QAYTARIB_BOLMAYDI


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

def _kontakt_sora(chat_id) -> bool:
    """Raqamni ulashish tugmasini chiqaradi.

    `yubor()` faqat `inline_keyboard` ni biladi, kontakt so'rash esa
    `reply_keyboard` + `request_contact` talab qiladi — Telegram'da
    bu ikki xil markup. Shuning uchun alohida funksiya.

    `one_time_keyboard`: tugma bir marta bosilgach yo'qoladi, chat
    tozaligicha qoladi.
    """
    natija = _sorov("sendMessage",
                    chat_id=chat_id,
                    text="Raqamingizni ulashing — so‘rovlaringizni topaman.",
                    reply_markup={
                        "keyboard": [[{"text": "📱 Raqamni ulashish",
                                       "request_contact": True}]],
                        "resize_keyboard": True,
                        "one_time_keyboard": True,
                    })
    return bool(natija and natija.get("ok"))


def _start(chat_id, kod: str) -> None:
    if not kod:
        yubor(chat_id,
              "Salom! Bu — <b>OBER</b> boti.\n\n"
              "<b>Sotuvchi bo‘lsangiz:</b> OBER kabinetidagi "
              "“Telegramga ulash” tugmasini bosing.\n\n"
              "<b>Xaridor bo‘lsangiz:</b> telefoningizni almashtirgan "
              "yoki brauzerni tozalagan bo‘lsangiz — pastdagi tugma "
              "bilan raqamingizni ulashing, so‘rovlaringizni "
              "qaytarib beraman.")
        _kontakt_sora(chat_id)
        return
    s = baza.telegram_ulash(kod, chat_id)
    if not s:
        yubor(chat_id, "Kod eskirgan. OBER’da qaytadan “Telegramga ulash”ni bosing.")
        return
    nom = html.escape(str(s.get("nom") or "Sotuvchi"))
    yubor(chat_id,
          f"✅ Ulandi: <b>{nom}</b>\n\n"
          "Yangi mos so‘rov va xaridor xabari shu yerga keladi. "
          "Batafsil yozishma OBER chatida davom etadi.")


def _kontakt(chat_id, kontakt: dict) -> None:
    """Xaridor kontaktini ulashdi — so'rovlarini topib qaytaramiz.

    NEGA SHU YO'L TANLANDI (2026-08-15)
    -----------------------------------
    Xaridorda hisob yo'q va u faqat brauzerdagi kalit bilan tanalardi.
    Brauzer tozalansa suhbat butunlay yo'qolardi.

    Uch yo'l ko'rib chiqildi:
      SMS      — pul va tashqi provayder kerak, loyihada yo'q.
      Parol    — xaridorni ro'yxatdan o'tishga majburlash. OBER'ning
                 butun ma'nosi "ro'yxatsiz so'ra" edi, buzardi.
      Telegram — bot ALLAQACHON bor, raqam `sorovlar.aloqa` da
                 ALLAQACHON saqlanadi. Yangi hech narsa kerak emas.

    Telegram kontakt tugmasi raqamni O'ZI beradi — odam qo'lda
    yozmaydi, xato qilmaydi. Va bu raqam Telegram tomonidan
    tasdiqlangan, ya'ni birov begona raqamni kiritolmaydi.
    """
    raqam = str(kontakt.get("phone_number") or "")
    # Telegram raqamni "+998901234567" yoki "998901234567" beradi.
    # Bazada qanday saqlanganini bilmaymiz, shuning uchun oxirgi
    # 9 raqam bo'yicha solishtiramiz — O'zbekiston uchun yetarli.
    oxirgi9 = "".join(ch for ch in raqam if ch.isdigit())[-9:]
    if len(oxirgi9) < 9:
        yubor(chat_id, "Raqam tanilmadi. Qaytadan urinib ko'ring.")
        return

    topildi = []
    for shakl in (f"+998{oxirgi9}", f"998{oxirgi9}", oxirgi9, f"+{oxirgi9}"):
        topildi = baza.xaridor_sorovlari(shakl)
        if topildi:
            break

    if not topildi:
        yubor(chat_id,
              "Bu raqam bo‘yicha <b>ochiq so‘rov topilmadi</b>.\n\n"
              "So‘rov yopilgan bo‘lishi yoki boshqa raqam bilan "
              "yuborilgan bo‘lishi mumkin. "
              "Yangi so‘rov yuborish: https://ober.uz")
        return

    qatorlar = ["🔎 <b>Sizning so‘rovlaringiz</b>\n"]
    for s in topildi:
        matn = html.escape(str(s.get("matn") or "")[:60])
        javob = s.get("javob") or 0
        holat = f"{javob} ta javob" if javob else "javob kutilmoqda"
        qatorlar.append(
            f"• <b>{matn}</b> — {holat}\n"
            f"  https://ober.uz/takliflar?rol=xaridor&kalit={s['token']}")
    qatorlar.append("\nHavolani bosing — suhbat o‘sha telefonda ochiladi.")
    yubor(chat_id, "\n".join(qatorlar))


def _javob_yoz(chat_id, sorov_id: int, sotuvchi_id: int,
               holat: str, narx: int | None) -> None:
    natija = baza.javob_yoz(sorov_id, sotuvchi_id, holat, narx, "")
    if natija is None:
        yubor(chat_id,
              "Javob yuborilmadi. So‘rov yopilgan, avval javob berilgan "
              "yoki sizga biriktirilmagan bo‘lishi mumkin.")
        return
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
    qatorlar = [f"🔔 <b>{html.escape(str(x['matn']))}</b>"]
    ikkinchi = []
    if x.get("tuman"):
        ikkinchi.append(html.escape(str(x["tuman"])))
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
        if yubor(x["telegram_id"], _sorov_matni(x), tugmalar):
            baza.xabar_belgila(x["yid"])
            n += 1
        elif qaytarib_bolmaydi():
            # Manzil o'lik — qayta urinish foydasiz. Navbatdan
            # chiqaramiz, sabab `qaytarib_bolmaydi` izohida.
            baza.xabar_belgila(x["yid"])
            print(f"  [tg] {x['telegram_id']} javob bermadi — "
                  f"navbatdan chiqarildi (so'rov {x['sorov_id']})")
    return n


def _chat_matni(x: dict) -> str:
    """Xaridor xabarini HTML xavfsiz, qisqa bildirishnomaga aylantiradi."""
    qatorlar = ["💬 <b>Xaridordan yangi xabar</b>",
                f"So‘rov: {html.escape(str(x.get('sorov_matni') or ''))}"]
    matn = (x.get("matn") or "").strip()
    if matn:
        qatorlar.append(html.escape(matn))
    ilovalar = []
    if x.get("rasm"):
        ilovalar.append("rasm")
    if x.get("joy"):
        ilovalar.append("joylashuv")
    if ilovalar:
        qatorlar.append("Ilova: " + ", ".join(ilovalar))
    return "\n".join(qatorlar)


def kutayotgan_chatlarni_yubor() -> int:
    """Xaridorning yangi chat xabarini sotuvchiga bir marta bildiradi.

    VAQTINCHALIK xato qaytsa yozuv belgilanmaydi: keyingi aylanishda
    qayta uriniladi (tarmoq uzildi, Telegram band). QAYTARIB
    BO'LMAYDIGAN xatoda esa belgilanadi — sabab `qaytarib_bolmaydi`
    izohida. Shu qoida yangi so'rov bildirishnomasiga ham tegishli.
    """
    if not SAVDO_XABARLARI:
        return 0
    n = 0
    tugmalar = [[{"text": "OBER chatini ochish", "url": OBER_CHAT}]]
    for x in baza.tg_kutayotgan_chat():
        if yubor(x["telegram_id"], _chat_matni(x), tugmalar):
            baza.tg_chat_belgila(x["id"])
            n += 1
        elif qaytarib_bolmaydi():
            baza.tg_chat_belgila(x["id"])
            print(f"  [tg] {x['telegram_id']} javob bermadi — "
                  f"chat xabari navbatdan chiqarildi ({x['id']})")
    return n


# ── Asosiy halqalar ──────────────────────────────────────────────────────────

def bildirish_sikli() -> int:
    """Navbatdagi barcha chiquvchi xabarlarni bir marta yuborishga urinadi."""
    return kutayotganlarni_yubor() + kutayotgan_chatlarni_yubor()


def bildirish_halqa() -> None:
    """Chiquvchi xabarlarni kiruvchi Telegram long-pollidan mustaqil yuboradi.

    `getUpdates` odatda 25 soniyagacha kutadi yoki tarmoq xatosida undan ham
    kech qaytadi. Bildirishnomani o‘sha so‘rov ortida qoldirish sotuvchiga
    xabar kelishini tasodifiy sekinlashtirardi. Alohida halqa navbatni har ikki
    soniyada tekshiradi; yuborish muvaffaqiyatsiz bo‘lsa DB belgilanmaydi va
    keyingi aylanishda xavfsiz qayta uriniladi.
    """
    while True:
        try:
            bildirish_sikli()
        except Exception as e:                    # noqa: BLE001
            print(f"  [tg] bildirish xatosi: {type(e).__name__}: {e}",
                  flush=True)
        time.sleep(BILDIRISH_ORALIGI)

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
                    # KONTAKT ULASHISH — xaridor suhbatlarini tiklaydi.
                    # Telegram "Raqamni yuborish" tugmasi `contact`
                    # yuboradi, matn emas. Shuning uchun matndan OLDIN
                    # tekshiriladi.
                    if m.get("contact"):
                        _kontakt(m["chat"]["id"], m["contact"])
                    else:
                        _matn(m["chat"]["id"], (m.get("text") or "").strip())
                elif "callback_query" in u:
                    q = u["callback_query"]
                    _sorov("answerCallbackQuery", callback_query_id=q["id"])
                    _tugma(q["message"]["chat"]["id"], q)
        except Exception as e:                    # noqa: BLE001
            # 2026-08-04: bu yerda faqat `type(e).__name__` yozilardi.
            # Jurnal 14 soat davomida "OperationalError" deb takrorladi va
            # SABABINI aytmadi — natijada sayt tushganini bilib bo'lmadi.
            # Xato matni HAR DOIM yozilsin: "database is locked" bilan
            # "attempt to write a readonly database" butunlay boshqa dard.
            print(f"  [tg] halqa xatosi: {type(e).__name__}: {e}", flush=True)
            time.sleep(5)


def fonda_boshla() -> None:
    """Serverda kiruvchi bot va chiquvchi bildirish halqalarini bir marta yoqadi."""
    global _FONDA_BOSHLANDI
    if not token():
        return
    with _FONDA_QULF:
        if _FONDA_BOSHLANDI:
            return
        _FONDA_BOSHLANDI = True
        threading.Thread(target=halqa, daemon=True,
                         name="ober-telegram-kiruvchi").start()
        threading.Thread(target=bildirish_halqa, daemon=True,
                         name="ober-telegram-bildirish").start()


if __name__ == "__main__":
    threading.Thread(target=bildirish_halqa, daemon=True,
                     name="ober-telegram-bildirish").start()
    halqa()
