"""
OBER — MAHALLIY SERVER (sinov uchun)

Maqsad: qidiruvni KO'Z BILAN ko'rish. Hisobot yetarli emas — natija
qanday ko'rinishini ko'rmasdan sifatni baholab bo'lmaydi.

Ishga tushirish: KOR-BRAUZERDA.bat
Keyin brauzer o'zi ochiladi: http://127.0.0.1:8800
"""

from __future__ import annotations

import json
import mimetypes
import os

# Python'ning turlar jadvalida `.woff2` yo'q — u `application/octet-stream`
# bo'lib ketardi va brauzer shriftni rad qilardi ("Failed to decode
# downloaded font"). Bir qatorda qo'shib qo'yamiz. (2026-08-04)
mimetypes.add_type("font/woff2", ".woff2")
mimetypes.add_type("font/woff", ".woff")
import base64
import binascii
import threading
import time
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import baza
import ai_vision
import joylar
import xato_xabar
from lugat import byudjet_top, modellarni_top, qismlarni_top
from qidiruv import keshni_tayyorla, qidir
import tahlil
from yonalishlar import belgilar as yonalishlar_belgilar
from yonalishlar import yonalish_nomlari, yonalishlarni_top

# Serverda muhit o'zgaruvchisi bilan boshqariladi, kodni tahrirlash shart
# emas. Uyda hech narsa o'zgarmaydi — standart qiymatlar o'sha-o'sha.
#   OBER_PORT=8800      qaysi portda
#   OBER_HOST=127.0.0.1 kim ulana oladi (serverda 127.0.0.1 qoladi:
#                       tashqariga Caddy chiqaradi, HTTPS bilan)
PORT = int(os.environ.get("OBER_PORT") or 8800)
HOST = os.environ.get("OBER_HOST") or "127.0.0.1"
WEB = Path(__file__).resolve().parent.parent / "web"
UPLOADS = Path(__file__).resolve().parent.parent / "data" / "chat-uploads"
MAX_RASM = 5 * 1024 * 1024


# ── TEZLIK CHEGARASI ─────────────────────────────────────────────────────
# Xotirada, kutubxonasiz. Har IP uchun oynali hisob.
#
# 2026-08-04 — IKKI JIDDIY XATO TUZATILDI.
#
# 1) CHEGARA BUTUN SAYT UCHUN BITTA EDI.
#    IP `self.client_address[0]` dan olinardi. Caddy orqasida esa bu
#    HAR DOIM `127.0.0.1` — ya'ni hamma tashrifchi bitta hisobni
#    bo'lishardi. Amalda: butun OBER soatiga 5 ta sotuvchi va 20 ta
#    so'rov qabul qila olardi. Beshinchi sotuvchidan keyin OLTINCHISIGA
#    "Juda tez-tez" deb yozilardi — u umuman birinchi marta urinayotgan
#    bo'lsa ham. Aziz aynan shunga duch keldi.
#    Endi haqiqiy IP `X-Forwarded-For` dan olinadi.
#
# 2) CHEGARALAR O'ZBEKISTON UCHUN JUDA PAST EDI.
#    Mahalliy mobil operatorlar CGNAT ishlatadi: minglab abonent bitta
#    tashqi IP orqali chiqadi. Soatiga 20 ta so'rov degani — bitta
#    operatorning HAMMA mijozi uchun 20 ta.
#
# 3) URILGANI KO'RINMASDI. Jurnal yozilmagani uchun "haqiqiy odam
#    urilyaptimi yoki bot" degan savolga javob yo'q edi. Endi yoziladi.
_TEZLIK_QULF = threading.Lock()
_TEZLIK: dict[str, list[float]] = {}
_TEZLIK_QOIDA = {
    "/api/sotuvchi/royxat": (10, 3600),     # soatiga 10 ta yangi sotuvchi
    "/api/sotuvchi/kirish": (20, 3600),    # kod so'rash — SMS yuborishdek
    "/api/sotuvchi/tasdiq": (20, 3600),    # kod taxmin qilib bo'lmasin
    "/api/sotuvchi/chiqish": (60, 3600),   # chiqish — sessiyani o'chiradi
    "/api/sotuvchi/profil": (600, 3600),   # profil — o'z egasi, tez-tez yuklanadi
    "/api/sotuvchi/telegram/sinov": (5, 3600),  # egasiga test xabari
    "/api/elon": (20, 3600),               # yangi e'lon — spam e'lonlarga qarshi
    # Rasmli qidiruv pullik vision chaqirig'iga aylanishi mumkin. Kalit
    # qo'yilmaganida tashqi chaqiriq yo'q; yoqilgach anonim suiiste'mol
    # butun limitni yeb qo'ymasligi uchun alohida chegara turadi.
    "/api/ai/rasm-qidiruv": (20, 3600),
    "/api/sorov": (60, 3600),               # soatiga 60 ta so'rov
    "/api/suhbat/xabar": (300, 3600),       # suhbat jonli bo'lsin
}
_TEZLIK_ODATIY = (600, 3600)

# X-Forwarded-For ni FAQAT o'z proksimizdan qabul qilamiz. Aks holda
# istalgan bot o'zi sarlavha yozib chegarani aylanib o'tardi.
_ISHONCHLI_PROKSI = {"127.0.0.1", "::1", "localhost"}

# Kategoriyalar API kesh (2026-08-11). Ikki darajali e'lon soni bitta
# SQL bilan ~0.5 s oladi (300 000+ e'lon guruhlanadi). Baza 45 daqiqada
# yangilanadi — 5 daqiqalik kesh eskirishga yo'l qo'ymaydi, lekin har
# sahifa ochilishida qayta hisoblashni ham kesadi.
_KAT_KESH = {"vaqt": 0.0, "javob": None}


def _haqiqiy_ip(ishlovchi) -> str:
    """Tashrifchining haqiqiy IP manzili.

    Caddy `X-Forwarded-For` ni o'zi qo'yadi. Zanjir bo'lsa
    ("mijoz, proksi1, proksi2") BIRINCHISI mijozniki.
    """
    ulanish = ishlovchi.client_address[0]
    if ulanish in _ISHONCHLI_PROKSI:
        xff = ishlovchi.headers.get("X-Forwarded-For", "")
        if xff:
            return xff.split(",")[0].strip() or ulanish
    return ulanish


def _tezlik_ruxsat(ip: str, yol: str) -> bool:
    chegara, oyna = _TEZLIK_QOIDA.get(yol, _TEZLIK_ODATIY)
    hozir = time.time()
    kalit = f"{ip}|{yol}"
    with _TEZLIK_QULF:
        urinishlar = [t for t in _TEZLIK.get(kalit, ()) if hozir - t < oyna]
        if len(urinishlar) >= chegara:
            _TEZLIK[kalit] = urinishlar
            return False
        urinishlar.append(hozir)
        _TEZLIK[kalit] = urinishlar
        # Xotira cheksiz o'smasin
        if len(_TEZLIK) > 20000:
            for k in [k for k, v in _TEZLIK.items()
                      if not v or hozir - v[-1] > 7200][:10000]:
                _TEZLIK.pop(k, None)
    return True


class Ishlovchi(BaseHTTPRequestHandler):
    def log_message(self, *a):                 # konsolni iflos qilmaymiz
        pass

    def _yubor(self, kod: int, tur: str, tana: bytes,
               headers: dict[str, str] | None = None) -> None:
        self.send_response(kod)
        self.send_header("Content-Type", tur)
        self.send_header("Content-Length", str(len(tana)))
        for nom, qiymat in (headers or {}).items():
            self.send_header(nom, qiymat)
        self.end_headers()
        self.wfile.write(tana)

    def _ulashilgan(self, nom: str, tur: str,
                    qoshimcha: dict[str, str] | None = None) -> None:
        """UMUMIY FAYL — YANGILANSA YANGISI, YANGILANMASA BEPUL.

        2026-08-12 da o'lchov bilan topilgan xato. `ober-ui.css`,
        `tabbar.js` va `i18n.js` `Cache-Control: no-cache` bilan
        berilardi. `no-cache` "ishlatishdan oldin tekshir" degani —
        LEKIN tekshirish uchun brauzerga validator kerak, bizda esa
        na `ETag`, na `Last-Modified` bor edi. Tekshiradigan narsa
        yo'q, shuning uchun Chrome eskisini berardi.

        Ko'rgan holat: deploy tugadi, server yangi CSS ni beryapti,
        `fetch(cache:'reload')` yangisini oldi — lekin SAHIFA hali
        eskisida (57 qoida, eski selektor). Foydalanuvchi uchun bu
        "Aziz tuzatdi, menda o'zgarmadi" degani.

        `ETag` — fayl mtime va hajmidan. O'zgarmasa brauzer
        `If-None-Match` yuboradi va biz 304 qaytaramiz: tana yo'q,
        trafik yo'q. O'zgarsa — yangi ETag, yangi tana.
        """
        fayl = WEB / nom
        st = fayl.stat()
        etag = '"%x-%x"' % (int(st.st_mtime), st.st_size)
        boshliqlar = {"Cache-Control": "no-cache, must-revalidate",
                      "ETag": etag}
        boshliqlar.update(qoshimcha or {})
        if self.headers.get("If-None-Match") == etag:
            self.send_response(304)
            for k, v in boshliqlar.items():
                self.send_header(k, v)
            self.end_headers()
            return
        self._yubor(200, tur, fayl.read_bytes(), boshliqlar)

    def _topilmadi(self) -> None:
        """404 — ORQAGA YO'L BOR.

        Ilgari bu `topilmadi` degan quruq matn edi: oq ekran, qora yozuv,
        hech qanday havola. Odam u yerga tushsa chiqib ketardi. Har
        sahifada qaytish yo'li bo'lishi kerak, xato sahifasida ayniqsa.
        """
        sahifa = """<!DOCTYPE html><html lang="uz"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OBER - sahifa topilmadi</title><link rel="icon" href="/brend/icon.png">
<style>
 body{margin:0;min-height:100svh;display:grid;place-items:center;
  background:#fbfbfa;color:#16181d;padding:24px;
  font-family:"Segoe UI Variable Display","Segoe UI",-apple-system,Roboto,Arial,sans-serif}
 .q{max-width:420px;text-align:center}
 h1{margin:0 0 10px;font-size:22px;letter-spacing:-.02em}
 p{margin:0 0 22px;color:#6b7280;font-size:14px;line-height:1.6}
 a{display:inline-block;min-height:46px;padding:13px 24px;border-radius:10px;
  background:#0b2559;color:#fff;text-decoration:none;font-weight:700;font-size:14px}
</style></head><body><div class="q">
<h1>Bunday sahifa yo&#8217;q</h1>
<p>Havola eskirgan yoki noto&#8217;g&#8217;ri yozilgan bo&#8216;lishi mumkin.
Qidiruvdan boshlang - bozor joyida turibdi.</p>
<a href="/">Bosh sahifaga qaytish</a>
</div></body></html>"""
        self._yubor(404, "text/html; charset=utf-8", sahifa.encode())

    def _oddiy_sahifa(self, nom: str, ichki: str) -> bytes:
        """Oddiy matnli sahifa — maxfiylik/qoidalar kabi. Qaytish havolasi bor."""
        return ("<!DOCTYPE html><html lang=\"uz\"><head>"
                "<meta charset=\"UTF-8\">"
                "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
                "<title>OBER — " + nom + "</title>"
                "<link rel=\"icon\" href=\"/brend/icon.png\">"
                "<style>"
                "body{margin:0;background:#eff2f7;color:#101828;min-width:320px;"
                "font-family:'Segoe UI Variable Display','Segoe UI',Roboto,Arial,sans-serif;"
                "line-height:1.6;font-size:15px}"
                ".q{width:min(100% - 36px,720px);margin:0 auto;padding:48px 0 72px}"
                "h1{font-size:26px;letter-spacing:-.03em;color:#0b2559;margin:0 0 16px}"
                "h2{font-size:17px;color:#0b2559;margin:28px 0 8px}"
                "p,li{color:#475467}"
                "ul{padding-left:20px}"
                "a.ortga{display:inline-block;margin-bottom:28px;color:#0b2559;"
                "font-weight:700;text-decoration:none;border:1px solid #cdd6e4;"
                "padding:10px 16px;border-radius:10px}"
                "a.ortga:hover{background:#eaeff8}"
                "</style></head><body><div class=\"q\">"
                "<a class=\"ortga\" href=\"/\">← Bosh sahifaga</a>"
                + ichki + "</div></body></html>").encode()

    def _sahifa(self, fayl: str) -> None:
        """HTML sahifa — HECH QACHON keshlanmaydi.

        2026-08-02 xato: `/api/qidir` yangi maydonlar qaytara boshladi
        (narx oralig'i o'rniga saralash), lekin brauzerdagi index.html
        eski edi va eski maydonlarni kutardi -> qidiruv "ishlamay qoldi".
        Sabab: sahifa Cache-Control'siz berilardi, brauzer esa uni
        o'zicha keshlab qo'yadi. Endi har ochilishda server tekshiriladi.
        JS/CSS bitta faylning ichida, shuning uchun bu yetarli.

        2026-08-15: `no-cache` YETARLI EMAS ekan. U "ishlatishdan
        oldin tekshir" degani, lekin tekshirish uchun brauzerga
        VALIDATOR kerak — bizda na ETag, na Last-Modified bor edi.
        Tekshiradigan narsa yo'q, shuning uchun brauzer eskisini
        berardi.

        Bugun shu meni bir marta chalg'itdi: sotuvchi sahifasini
        deploy qildim, server yangi faylni beryapti, lekin brauzer
        eskisini ko'rsatib turdi. Men "deploy yetmadi" deb o'yladim.
        Foydalanuvchi uchun bu "Aziz tuzatdi, menda o'zgarmadi".

        `ober-ui.css` va `tabbar.js` uchun bu 2026-08-12 da ETag
        bilan tuzatilgan edi (`_ulashilgan`), lekin HTML sahifalar
        e'tibordan chetda qolgan. Endi ular ham xuddi shunday.
        """
        yol = WEB / fayl
        st = yol.stat()
        etag = '"%x-%x"' % (int(st.st_mtime), st.st_size)
        boshliqlar = {"Cache-Control": "no-cache, must-revalidate",
                      "ETag": etag}
        if self.headers.get("If-None-Match") == etag:
            self.send_response(304)
            for k, v in boshliqlar.items():
                self.send_header(k, v)
            self.end_headers()
            return
        self._yubor(200, "text/html; charset=utf-8",
                    yol.read_bytes(), boshliqlar)

    # ── XATO QAMROVI (2026-08-16) ──────────────────────────────────
    #
    # `do_GET` va `do_POST` ilgari hech narsa bilan o'ralmagandi:
    # istisno chiqsa `BaseHTTPRequestHandler` uni jurnalga yozardi va
    # tamom. Jurnal esa serverda, hech kim o'qimaydi.
    #
    # Endi istisno Sentry'ga boradi — qaysi yo'lda, qaysi qatorda.
    # Muhimi: istisno YUTILMAYDI, qayta ko'tariladi. Aks holda
    # xatolar jimgina yo'qolib, "ishlayapti" degan yolg'on tuyg'u
    # paydo bo'lardi.
    def _qamrab(self, amal, nom: str):
        try:
            return amal()
        except Exception as x:                 # noqa: BLE001
            xato_xabar.xato(x, {"yol": str(self.path)[:200], "usul": nom})
            raise

    def do_GET(self):                          # noqa: N802
        return self._qamrab(self._get_ich, "GET")

    def _get_ich(self):
        u = urlparse(self.path)

        if u.path in ("/", "/index.html"):
            self._sahifa("index.html")
            return

        if u.path in ("/sotuvchi", "/sotuvchi/"):
            self._sahifa("sotuvchi.html")
            return

        if u.path in ("/takliflar", "/takliflar/"):
            self._sahifa("takliflar.html")
            return

        if u.path in ("/kategoriyalar", "/kategoriyalar/"):
            self._sahifa("kategoriyalar.html")
            return

        # Maxfiylik siyosati — Play/App Store talabi (2026-08-14)
        if u.path in ("/privacy", "/privacy/", "/maxfiylik"):
            self._sahifa("privacy.html")
            return

        # OBER'ning o'z e'loni — /elon/{id} (o'z marketplace, 2026-08-06)
        # Sahifa statik, id'ni JS o'qiydi va /api/elon/{id} dan oladi.
        # 404 emas: yopilgan e'lon ham "yopilgan" xabari ko'rsatadi.
        #
        # OG meta'larini SERVER TOMONIDA to'ldiramiz (2026-08-12).
        # Telegram/Facebook kabi skreperlar JavaScript ishlamaydi —
        # ular og:title ni faqat statik HTML'dan o'qiydi. E'lon nomi
        # uchun bazaga murojaat qilamiz; yopilgan e'lon bo'lsa eski
        # (umumiy) meta qoladi, JS "yopilgan" xabarini ko'rsatadi.
        if u.path.startswith("/elon/") and u.path.count("/") == 2:
            html = (WEB / "elon.html").read_bytes()
            try:
                elon_id = int(u.path.rsplit("/", 1)[-1])
            except ValueError:
                elon_id = 0
            if elon_id:
                el = baza.ober_elon_ol(elon_id)
                if el and not el.get("ochirilgan"):
                    joy = ", ".join(x for x in
                                     [el.get("viloyat"), el.get("shahar"),
                                      el.get("tuman")] if x)
                    if el.get("kelishiladi"):
                        narx = "Narxi kelishiladi"
                    elif el.get("narx_som"):
                        try:
                            narx = (f"{int(el['narx_som']):,}"
                                    .replace(",", " ") + " so'm")
                        except (TypeError, ValueError):
                            narx = ""
                    else:
                        narx = ""
                    import html as _html
                    # Sotuvchi kiritgan matn — meta ichida xavfsiz
                    # bo'lishi uchun to'liq escape qilinadi (review
                    # 2026-08-12: faqat qo'shtirnoq yetarli emas,
                    # `&`, `<`, `>` ham kelishi mumkin).
                    nom = _html.escape(el.get("nom") or "E'lon")
                    joy_esc = _html.escape(joy)
                    og_title = nom + " — OBER"
                    og_desc = " · ".join(
                        x for x in [narx, joy_esc, "OBER bozorida"] if x)
                    # Eski satrlar ham .encode() bilan — bytes literal
                    # faqat ASCII qabul qiladi, `—` va `'` esa UTF-8.
                    eski_t = ('<meta property="og:title" content="E\'lon — '
                              'OBER">').encode()
                    eski_d = ('<meta property="og:description" content="OBER '
                              'bozoridagi e\'lon — narx, rasm va sotuvchi '
                              'aloqasi.">').encode()
                    eski_u = ('<meta property="og:url" '
                              'content="https://ober.uz/elon/">').encode()
                    # Google/skreperlar `<title>` ni ham o'qiydi —
                    # og:title bilan birga u ham yangilanadi.
                    eski_title = b'<title>E\'lon \xe2\x80\x94 OBER</title>'
                    # Replace jimgina ishlamay qolmasin: elon.html
                    # o'zgargan bo'lsa (eski serverdagi versiya) —
                    # jurnalga yozamiz, generic meta qoladi.
                    if eski_t not in html:
                        print("  [og] elon.html meta satrlari mos emas",
                              flush=True)
                    html = html.replace(
                        eski_t,
                        ('<meta property="og:title" content="' + og_title
                         + '">').encode())
                    html = html.replace(
                        eski_d,
                        ('<meta property="og:description" content="'
                         + og_desc + '">').encode())
                    html = html.replace(
                        eski_u,
                        ('<meta property="og:url" content="https://ober.uz/elon/'
                         + str(elon_id) + '">').encode())
                    html = html.replace(
                        eski_title,
                        ('<title>' + og_title + '</title>').encode())
            self._yubor(200, "text/html; charset=utf-8", html,
                        {"Cache-Control": "no-cache, must-revalidate"})
            return

        # ── MAXFIYLIK VA QOIDALAR ────────────────────────────────────
        # 2026-08-06 audit: sahifada aloqa va kompaniya ma'lumoti yo'q edi.
        # Minimal, o'zbekcha, server tomonda — Google JavaScript'siz ham
        # o'qiy oladi.
        if u.path in ("/maxfiylik", "/maxfiylik/"):
            self._yubor(200, "text/html; charset=utf-8",
                        self._oddiy_sahifa(
                            "Maxfiylik",
                            "<h1>Maxfiylik</h1>"
                            "<p>OBER ochiq e’lonlarni birlashtiradi va sizning so‘rovlaringizni "
                            "mos sotuvchilarga yuboradi.</p>"
                            "<h2>Qanday ma’lumot saqlanadi?</h2>"
                            "<ul><li>So‘rov matni — faqat mos sotuvchilar ko‘radi.</li>"
                            "<li>Sotuvchi uchun telefon raqami — u kabinet va kirish uchun ishlatiladi.</li>"
                            "<li>Qidiruvlar — sayt sifatini yaxshilash uchun, shaxsiy holda saqlanmaydi.</li>"
                            "<li>Rasmli qidiruvni ishlatsangiz, tanlagan rasmingiz mahsulotni aniqlash uchun "
                            "AI xizmatiga yuboriladi. OBER original rasmni diskka saqlamaydi; brauzer uni "
                            "kichraytiradi va EXIF/geolokatsiya metama’lumotini olib tashlaydi.</li></ul>"
                            "<h2>Nima qilinmaydi?</h2>"
                            "<p>Ma’lumotlar uchinchi shaxsga sotilmaydi va reklama uchun ishlatilmaydi.</p>"))
            return

        # ALOQA — 2026-08-09 da qo'shildi.
        #
        # 6-avgust auditida "aloqa va kompaniya ma'lumoti yo'q" deb
        # yozilgan edi, lekin o'shanda faqat maxfiylik/qoidalar sahifalari
        # qo'shilgan — aloqaning o'zi yo'q qolgan.
        #
        # Nega kerak:
        #   1. Kim turganini ko'rsatmaydigan bozor saytiga ishonilmaydi.
        #   2. Sotuvchi muammo bo'lsa kimga yozishini bilishi kerak.
        #   3. Payme/Click merchant ko'rigida rekvizit va aloqa tekshiriladi.
        #
        # Shaxsiy telefon raqami ATAYLAB yozilmagan: ochiq saytdagi raqam
        # bir necha kunda spam ro'yxatlariga tushadi. Email va bot yetarli;
        # kerak bo'lsa Aziz rasmiy raqam qo'shadi.
        if u.path in ("/aloqa", "/aloqa/"):
            self._yubor(200, "text/html; charset=utf-8",
                        self._oddiy_sahifa(
                            "Aloqa",
                            "<h1>Aloqa</h1>"
                            "<p>Savol, taklif yoki muammo bo‘lsa — yozing. "
                            "Sotuvchilarning xabariga birinchi navbatda javob beramiz.</p>"
                            "<h2>Bog‘lanish</h2>"
                            "<ul>"
                            "<li>Telegram: <a href=\"https://t.me/ober_uz_bot\">@ober_uz_bot</a></li>"
                            "<li>Email: <a href=\"mailto:uznaiza@gmail.com\">uznaiza@gmail.com</a></li>"
                            "</ul>"
                            "<h2>Kompaniya</h2>"
                            "<p>&laquo;NAIZA&raquo; mas’uliyati cheklangan jamiyati<br>"
                            "STIR: 313204884<br>"
                            "O‘zbekiston, Toshkent</p>"
                            "<h2>Sotuvchilar uchun</h2>"
                            "<p>Ro‘yxatdan o‘tish bepul va 30 soniya oladi: "
                            "<a href=\"/sotuvchi\">sotuvchi kabineti</a>. "
                            "Kategoriya tanlash shart emas — nima sotishingizni "
                            "o‘z so‘zingiz bilan yozasiz.</p>"))
            return

        if u.path in ("/qoidalar", "/qoidalar/"):
            self._yubor(200, "text/html; charset=utf-8",
                        self._oddiy_sahifa(
                            "Qoidalar",
                            "<h1>Qoidalar</h1>"
                            "<p>OBER — ochiq bozor qidiruv xizmati. E’lonlar OLX, Telegram "
                            "va boshqa ochiq manbalardan yig‘iladi.</p>"
                            "<h2>Foydalanish</h2>"
                            "<p>E’lon havolasi asl manbaga olib boradi. So‘rov yuborish bilan "
                            "siz mos sotuvchilarga yuborilishiga rozilik berasiz.</p>"
                            "<h2>Xulq-atvor</h2>"
                            "<p>Soxta so‘rov, spam yoki boshqa foydalanuvchini aldash taqiqlanadi. "
                            "Bunday holatda akkaunt bloklanishi mumkin.</p>"))
            return

        # ── NARX SAHIFALARI (SEO o'sish dvigateli) ───────────────────
        # Serverda tayyorlanadi: Google JavaScript'siz o'qishi kerak.
        if u.path == "/robots.txt":
            import seo
            self._yubor(200, "text/plain; charset=utf-8", seo.robots())
            return

        if u.path == "/sitemap.xml":
            import seo
            self._yubor(200, "application/xml; charset=utf-8", seo.sitemap())
            return

        if u.path in ("/narx", "/narx/"):
            import seo
            self._yubor(200, "text/html; charset=utf-8", seo.royxat_sahifasi())
            return

        if u.path.startswith("/narx/"):
            import seo
            slug = u.path[len("/narx/"):].strip("/")
            juft = seo.slugdan(slug)
            if juft:
                sahifa = seo.narx_sahifasi(*juft)
                if sahifa:
                    self._yubor(200, "text/html; charset=utf-8", sahifa)
                    return
            self._yubor(404, "text/html; charset=utf-8",
                        seo.royxat_sahifasi())
            return

        if u.path == "/sw.js":
            self._yubor(200, "application/javascript; charset=utf-8",
                        (WEB / "sw.js").read_bytes(), {
                            "Cache-Control": "no-cache",
                            "Service-Worker-Allowed": "/",
                        })
            return

        # PWA MANIFEST (2026-08-14): Play/App Store tayyorgarligi.
        # Brauzer o'rnatish paneli, Android TWA va iOS bosh ekran
        # ikonasi shu fayl orqali ishlaydi. O'zgarmaydi — uzoq keshlansin.
        if u.path == "/manifest.json":
            self._yubor(200, "application/manifest+json; charset=utf-8",
                        (WEB / "manifest.json").read_bytes(), {
                            "Cache-Control": "public, max-age=86400",
                        })
            return

        if u.path == "/i18n.js":
            self._ulashilgan("i18n.js",
                             "application/javascript; charset=utf-8")
            return

        # DIGITAL ASSET LINKS — TWA to'liq ekran rejimi uchun (2026-08-14).
        # Play Store'ga APK yuklangach, Play Console'dan SHA-256 izi olinadi
        # va `web/.well-known/assetlinks.json` ga yoziladi. Yo'riqnoma:
        # reports/play-market-2026-08-14/TWA-YORIQNOMA.md
        if u.path == "/.well-known/assetlinks.json":
            fayl = (WEB / ".well-known" / "assetlinks.json")
            if fayl.is_file():
                self._yubor(200, "application/json; charset=utf-8",
                            fayl.read_bytes())
            else:
                self._topilmadi()
            return

        # PUSH OCHIQ KALITI — brauzer `applicationServerKey` sifatida
        # ishlatadi. Bu OCHIQ kalit, sir emas: u bilan faqat bizning
        # imzomizni TEKSHIRISH mumkin, yuborish emas.
        if u.path == "/api/push-kalit":
            try:
                import push
                self._yubor(200, "application/json; charset=utf-8",
                            json.dumps({"kalit": push.ochiq_kalit_b64()}).encode(),
                            {"Cache-Control": "public, max-age=3600"})
            except Exception:                     # noqa: BLE001
                # Push sozlanmagan bo'lsa sahifa yiqilmasin — u shunchaki
                # bildirishnomasiz ishlaydi.
                self._yubor(503, "application/json; charset=utf-8",
                            json.dumps({"xato": "push sozlanmagan"}).encode())
            return

        # KUTAYOTGAN TALAB — sotuvchi sahifasi uchun, ochiq.
        # Faqat so'rov matni chiqadi: telefon, ism, token yo'q.
        # Matnni odam qidiruv qatoriga o'zi yozgan.
        if u.path == "/api/talab":
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(baza.kutayotgan_talab(),
                                   ensure_ascii=False).encode(),
                        {"Cache-Control": "public, max-age=60"})
            return

        if u.path == "/push.js":
            self._ulashilgan("push.js",
                             "application/javascript; charset=utf-8")
            return

        if u.path == "/ober-ui.css":
            self._ulashilgan("ober-ui.css", "text/css; charset=utf-8")
            return

        # Pastki tab navigatsiyasi (2026-08-07). Barcha sahifalarga
        # bitta fayl — navigatsiya bir joyda bo'lsin.
        if u.path == "/tabbar.js":
            self._ulashilgan("tabbar.js",
                             "application/javascript; charset=utf-8")
            return

        # KATEGORIYA IKONLARI (2026-08-16). Bitta manba: kategoriyalar
        # sahifasi va bosh sahifadagi bozor bo'limlari to'ri bir xil
        # ikonlarni ko'rsatadi. `tabbar.js` kabi — no-cache + ETag
        # `_ulashilgan` o'zi qo'shadi.
        if u.path == "/kat-ikonlar.js":
            self._ulashilgan("kat-ikonlar.js",
                             "application/javascript; charset=utf-8")
            return

        # FAVICON — BRAUZER UNI HAR DOIM ILDIZDAN SO'RAYDI (2026-08-12).
        #
        # Sahifalarda `<link rel="icon" href="/brend/icon.png">` bor va
        # u to'g'ri ishlaydi. Lekin brauzer baribir `/favicon.ico` ni
        # so'raydi — bu uning eski, o'zgarmas odati. Javob 404 bo'lgani
        # uchun har sahifa ochilishida konsolga xato yozilardi.
        #
        # Tezlikka ta'siri yo'q (server ichida 0.75 ms), lekin konsolda
        # doimiy qizil xato turishi ishning tugallanmaganini bildiradi
        # va haqiqiy xatoni ko'rishga xalaqit beradi.
        #
        # PNG ni `.ico` manzilida berish mumkin — brauzerlar buni
        # qabul qiladi, kengaytma emas, `Content-Type` hal qiladi.
        if u.path == "/favicon.ico":
            fayl = (WEB / "brend" / "icon.png")
            if fayl.is_file():
                self._yubor(200, "image/png", fayl.read_bytes(),
                            {"Cache-Control": "public, max-age=31536000, immutable"})
            else:
                self._topilmadi()
            return

        # Brend va shrift fayllari: faqat o'sha papkalar ichidagi aniq
        # fayllar beriladi. Yo'lni `resolve()` qilish `../` orqali
        # papkadan chiqib ketishni to'xtatadi.
        #
        # 2026-08-04: `/shrift/` qo'shildi. Onest shrifti Google Fonts
        # CDN'idan o'z serverimizga ko'chirildi — sabab
        # `web/shrift/onest.css` boshida.
        if u.path.startswith(("/brend/", "/shrift/")):
            papka = u.path.split("/")[1]
            fayl = (WEB / u.path.lstrip("/")).resolve()
            ildiz = (WEB / papka).resolve()
            if fayl.parent == ildiz and fayl.is_file():
                tur = mimetypes.guess_type(fayl.name)[0] or \
                    "application/octet-stream"
                # Shrift va logotip hech qachon o'zgarmaydi (o'zgarsa nomi
                # ham o'zgaradi). Bir yil keshlansin — har sahifa ochilishida
                # 32 KB qayta yuklanmasin.
                qoshimcha = {"Cache-Control": "public, max-age=31536000, immutable"}
                self._yubor(200, tur, fayl.read_bytes(), qoshimcha)
                return
            self._topilmadi()
            return

        # Chat rasmlari faqat server yaratgan UUID nomi bilan uzatiladi.
        if u.path.startswith("/chat-uploads/"):
            fayl = (UPLOADS / u.path.rsplit("/", 1)[-1]).resolve()
            ildiz = UPLOADS.resolve()
            if fayl.parent == ildiz and fayl.is_file():
                tur = mimetypes.guess_type(fayl.name)[0] or "application/octet-stream"
                self._yubor(200, tur, fayl.read_bytes())
                return
            self._yubor(404, "text/plain; charset=utf-8", "topilmadi".encode())
            return

        # Sotuvchiga tegishli ochiq so'rovlar
        if u.path == "/api/sotuvchi/sorovlar":
            p = parse_qs(u.query)
            sid = _sotuvchi_ident(p)
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(baza.sotuvchi_sorovlari(sid),
                                   ensure_ascii=False).encode())
            return

        # ── PROFIL — kabinetdagi "Profil" bloki (2026-08-08) ──────────────
        # Token/ID orqali ism, nima sotadi, qayerda. Xaridorga OCHIQ EMAS.
        if u.path == "/api/sotuvchi/profil":
            p = parse_qs(u.query)
            sid = _sotuvchi_ident(p)
            if not sid:
                self._yubor(401, "application/json; charset=utf-8",
                            json.dumps({"xato": "Kirish muddati tugagan"},
                                       ensure_ascii=False).encode())
                return
            prof = baza.sotuvchi_profil(sid)
            if not prof:
                self._yubor(404, "application/json; charset=utf-8",
                            json.dumps({"xato": "Profil topilmadi"},
                                       ensure_ascii=False).encode())
                return
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(prof, ensure_ascii=False).encode())
            return

        # ── E'LONLARIM — o'z marketplace'i (2026-08-06) ──────────────────
        # Kabinetdagi "E'lonlarim" ro'yxati. Token bilan (faqat o'ziniki).
        if u.path == "/api/sotuvchi/elonlari":
            p = parse_qs(u.query)
            sid = _sotuvchi_ident(p)
            if not sid:
                self._yubor(401, "application/json; charset=utf-8",
                            json.dumps({"xato": "Kirish muddati tugagan"},
                                       ensure_ascii=False).encode())
                return
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(baza.ober_elonlari(sid),
                                   ensure_ascii=False).encode())
            return

        # Bitta e'lon — /elon/{id} sahifasi uchun OCHIQ (xaridor ko'radi)
        if u.path.startswith("/api/elon/") and u.path.count("/") == 3:
            try:
                elon_id = int(u.path.split("/")[-1])
            except ValueError:
                self._topilmadi()
                return
            el = baza.ober_elon_ol(elon_id)
            if not el:
                self._topilmadi()
                return
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(el, ensure_ascii=False).encode())
            return

        # Sotuvchi yo'nalishidagi TALAB — kabinetga qaytish sababi

        # Sotuvchi yo'nalishidagi TALAB — kabinetga qaytish sababi
        if u.path == "/api/sotuvchi/talab":
            p = parse_qs(u.query)
            sid = _sotuvchi_ident(p)
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(baza.sotuvchi_talabi(sid),
                                   ensure_ascii=False).encode())
            return

        # Xaridor o'z so'roviga kelgan javoblarni ko'radi
        if u.path == "/api/sorov/javoblar":
            p = parse_qs(u.query)
            sid = _xaridor_ident(p)
            if not sid:
                self._yubor(401, "application/json; charset=utf-8",
                            json.dumps({"xato": "So'rov sessiyasi topilmadi"},
                                       ensure_ascii=False).encode())
                return
            # XARIDOR KUTAYOTGAN PAYT — aynan shunda keyingi to'lqin
            # ochilishi kerak. Ilgari to'lqin faqat sotuvchi sahifasi
            # so'raganda ilgarilardi: hech bir sotuvchi ochib turmasa,
            # 3- va 8-daqiqalik to'lqinlar hech qachon ketmasdi.
            # To'lqinni har 4 soniyalik so'rovda emas, dangasa jadval
            # orqali ilgarilatamiz — aks holda yozuv oqimi qidiruvni
            # sekinlashtiradi.
            baza.ochiq_sorovlarni_yurit()
            tarqatish = {"yuborildi": baza.yuborilgan_soni(sid)}
            javoblar = baza.sorov_javoblari(sid)
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps({"javoblar": javoblar,
                                    "yuborildi": tarqatish["yuborildi"]},
                                   ensure_ascii=False).encode())
            return

        if u.path == "/api/sorov/takliflar":
            p = parse_qs(u.query)
            sid = _xaridor_ident(p)
            if not sid:
                self._yubor(401, "application/json; charset=utf-8",
                            json.dumps({"xato": "So'rov sessiyasi topilmadi"},
                                       ensure_ascii=False).encode())
                return
            # Xaridor sahifasi shu manzilni har necha soniyada so'raydi.
            # Shu payt keyingi to'lqinni ham ochamiz — alohida jadval
            # xizmati (cron) kerak bo'lmaydi.
            baza.ochiq_sorovlarni_yurit()
            javob = baza.sorov_takliflari(sid)
            if isinstance(javob, dict):
                javob["yuborildi"] = baza.yuborilgan_soni(sid)
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(javob, ensure_ascii=False).encode())
            return

        # Telegram tashxisi — nima ishlayapti, nima yo'q.
        if u.path == "/api/tg/holat":
            import tg
            h = baza.tg_holat()
            h["token"] = bool(tg.token())
            h["bot"] = tg.bot_nomi() if h["token"] else ""
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(h, ensure_ascii=False).encode())
            return

        # Telegramga ulash havolasi. Token yo'q bo'lsa — o'chiq deb aytadi.
        if u.path == "/api/sotuvchi/telegram":
            p = parse_qs(u.query)
            sid = _sotuvchi_ident(p)
            import tg
            nom = tg.bot_nomi() if tg.token() else ""
            javob = {"yoqilgan": bool(nom), "bot": nom}
            if nom and sid:
                kod = baza.ulash_kodi_ol(sid)
                javob["havola"] = f"https://t.me/{nom}?start={kod}"
                javob["ulangan"] = baza.telegram_ulanganmi(sid)
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(javob, ensure_ascii=False).encode())
            return

        if u.path == "/api/sotuvchi/suhbatlar":
            p = parse_qs(u.query)
            sid = _sotuvchi_ident(p)
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(baza.sotuvchi_suhbatlari(sid),
                                   ensure_ascii=False).encode())
            return

        if u.path == "/api/bildirishnomalar":
            p = parse_qs(u.query)
            rol = (p.get("rol") or ["xaridor"])[0]
            actor = _actor_ident(p, rol)
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(baza.bildirishnomalar_ol(rol, actor),
                                   ensure_ascii=False).encode())
            return

        if u.path == "/api/suhbat":
            p = parse_qs(u.query)
            chat_id = int((p.get("id") or ["0"])[0] or 0)
            rol = (p.get("rol") or ["xaridor"])[0]
            actor = _actor_ident(p, rol)
            natija = baza.suhbat_ol(chat_id, rol, actor)
            if natija is None:
                self._yubor(403, "application/json; charset=utf-8",
                            json.dumps({"xato": "Suhbatga kirish mumkin emas"},
                                       ensure_ascii=False).encode())
                return
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(natija, ensure_ascii=False).encode())
            return

        if u.path == "/api/demo/chat":
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(baza.suhbat_demo_holat(),
                                   ensure_ascii=False).encode())
            return

        if u.path == "/api/qidir":
            p = parse_qs(u.query)
            sorov = (p.get("q") or [""])[0].strip()
            tuman = (p.get("tuman") or [""])[0].strip()
            if not sorov:
                self._yubor(400, "application/json",
                            b'{"xato":"so\'rov bo\'sh"}')
                return
            def _son(nom: str) -> int:
                try:
                    return int((p.get(nom) or ["0"])[0] or 0)
                except ValueError:
                    return 0

            def _bor(nom: str) -> bool:
                return (p.get(nom) or ["0"])[0] in ("1", "true", "ha")

            # "169 ta taklif" deb yozib 60 tasini ko'rsatish halol emas.
            # Sahifa raqami bilan qolgani ham ochiladi.
            sahifa = max(1, _son("sahifa") or 1)
            n = qidir(sorov, tuman, limit=60 * sahifa,
                      tartib=(p.get("tartib") or ["moslik"])[0],
                      narx_dan=_son("narx_dan"), narx_gacha=_son("narx_gacha"),
                      byudjetsiz=_bor("byudjetsiz"),
                      faqat_rasm=_bor("rasm"), faqat_yangi=_bor("yangi"),
                      faqat_dokon=_bor("dokon"))
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(n, ensure_ascii=False).encode())
            # ANALITIKA ALOHIDA OQIMDA.
            # 2026-08-02 o'lchov: "velosiped" 5 816 ms oldi, lekin qidiruvning
            # o'zi atigi 350 ms edi. Qolgani — SQLite yozuv qulfini kutish.
            # Yig'uvchi jarayon bazaga tinmay yozayotganda bu yozuv soniyalab
            # kutadi va ulanishni band qilib turadi. Endi u foydalanuvchini
            # kutdirmaydi.
            threading.Thread(target=baza.qidiruv_yoz,
                             args=(sorov, n, tuman), daemon=True).start()
            return

        # BOSH SAHIFA UCHUN HAQIQIY E'LONLAR.
        # Aziz, 2026-08-02: "prosta turishini qara, AI da qilingani
        # bilinib turibdi, bo'sh va zerikarli". To'g'ri: bazada 126 834 ta
        # real e'lon bor edi va bosh sahifada BITTASI HAM ko'rinmasdi —
        # faqat va'da. Shablonni takrorlash oson, 126 ming o'zbek e'lonini
        # takrorlab bo'lmaydi. Kuchimizni yashirib qo'ygan ekanmiz.
        # Odamlar hozir nima qidirayotgani — bosh sahifadagi chiplar.
        # Sabab `baza.songgi_qidiruvlar` izohida.
        # Markaziy bankning rasmiy dollar kursi. Sabab
        # `baza.dollar_kursi` izohida. Olinmasa 204 — sahifa o'sha
        # satrni umuman chizmaydi.
        if u.path == "/api/kurs":
            k = baza.dollar_kursi()
            if not k:
                self._yubor(204, "application/json; charset=utf-8", b"")
                return
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(k, ensure_ascii=False).encode(),
                        {"Cache-Control": "public, max-age=3600"})
            return

        if u.path == "/api/qidiruvlar":
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(baza.songgi_qidiruvlar(10),
                                   ensure_ascii=False).encode(),
                        {"Cache-Control": "public, max-age=300"})
            return

        if u.path == "/api/yangi":
            p = parse_qs(u.query)
            try:
                n = min(24, max(4, int((p.get("n") or ["12"])[0] or 12)))
            except ValueError:
                n = 12
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(baza.yangi_elonlar(n),
                                   ensure_ascii=False).encode(),
                        {"Cache-Control": "public, max-age=120"})
            return

        if u.path == "/api/holat":
            # JOY RO'YXATI ma'lumotdan emas, joylar.py'dan olinadi.
            # Sabab: OLX aralash yozadi ("Риштан", "Чиланзарский район") va
            # tumanni faqat Toshkentda beradi. Ro'yxatni ma'lumotdan tuzsak
            # u aralash va chala bo'ladi — 2026-07-30 da shunday edi.
            with baza.ulan() as c:
                jami = c.execute(
                    "SELECT COUNT(*) n FROM elonlar WHERE faol=1"
                ).fetchone()["n"]
            # BOT NOMI — sessiyani yo'qotgan xaridor uchun (2026-08-15).
            # U chat bo'limiga kirganda "suhbatlarimni tiklash"
            # havolasini ko'radi; havola shu nomdan quriladi.
            # Bot username ochiq ma'lumot (Telegram'da izlab topiladi),
            # shuning uchun bu yerda berish xavfsiz. Token EMAS.
            try:
                import tg
                bot = tg.bot_nomi() if tg.token() else ""
            except Exception:                     # noqa: BLE001
                bot = ""
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps({"jami": jami,
                                    "daraxt": joylar.daraxt(),
                                    "bot": bot,
                                    "ai_rasm": ai_vision.holat()},
                                   ensure_ascii=False).encode())
            return

        # KATEGORIYALAR — pastki tabning 2-bo'g'ini (2026-08-07).
        # Bozor bo'limlari OLX daraxtidan olinadi; har e'lon uchun emas,
        # bo'limlar ro'yxati uchun. Sahifa `?q=<nom>` bilan qidiruvni
        # ochadi — o'sha yerda xaridor bozorning o'zidan topadi.
        if u.path == "/api/kategoriyalar":
            if not _KAT_KESH["javob"] or time.time() - _KAT_KESH["vaqt"] > 300:
                _KAT_KESH["javob"] = self._kategoriyalar_javob()
                _KAT_KESH["vaqt"] = time.time()
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps(_KAT_KESH["javob"], ensure_ascii=False).encode())
            return

        self._topilmadi()

    def _kategoriyalar_javob(self):
        """Kategoriyalar ikki darajada: yuqori guruh + real e'lon sonlari.

        Avval bu yerda bo'limlar soni (`len(g)`) qaytardi. 2026-08-11 dan
        boshlab `elonlar` DB'dan hisoblanadi va har guruh ichida `pastki`
        (2-daraja) keladi.
        """
        import kategoriyalar
        juftlar = kategoriyalar.royxat()
        guruhlar: dict[str, list[tuple[str, str]]] = {}
        for yol, nom in juftlar:
            guruh = yol.split("/", 1)[0] or "boshqa"
            guruhlar.setdefault(guruh, []).append((yol, nom))
        tartib = ["transport", "nedvizhimost", "elektronika",
                  "dom-i-sad", "detskiy-mir", "moda-i-stil",
                  "uslugi", "rabota", "zhivotnye",
                  "hobbi-otdyh-i-sport", "otdam-darom", "obmen-barter"]
        nomlar = {
            "transport": "Transport",
            "nedvizhimost": "Ko'chmas mulk",
            "elektronika": "Elektr jihozlari",
            "dom-i-sad": "Uy va bog'",
            "detskiy-mir": "Bolalar dunyosi",
            "moda-i-stil": "Moda va stil",
            "uslugi": "Xizmatlar",
            "rabota": "Ish",
            "zhivotnye": "Hayvonlar",
            "hobbi-otdyh-i-sport": "Xobbi va sport",
            "otdam-darom": "Tekinga beraman",
            "obmen-barter": "Ayirboshlash",
        }
        # `data/kategoriyalar.txt` OLX'dan avtomatik qayta yoziladi —
        # yangi ildiz kategoriya paydo bo'lsa, u tartibda bo'lmasa ham
        # sahifadan yo'qolib qolmasin: oxiriga qo'shamiz.
        #
        # IKKI DARAJA (2026-08-11). Kartada endi bo'limlar soni emas,
        # REAL E'LON SONI turadi — u baza'dan olinadi:
        #   `elonlar.kategoriya` to'liq yo'l: "Transport / Yengil
        #   avtomashinalar / Aito". Birinchi segment yuqori guruh,
        #   ikkinchisi 2-daraja. Nomlar `kategoriyalar.txt` bilan
        #   aynan mos (o'lchov: 16599 | Yengil avtomashinalar).
        # Bitta SQL ikkala darajani ham beradi (568 ms, 35 qator).
        baza.init()
        b1_soni: dict[str, int] = {}
        b2_soni: dict[tuple[str, str], int] = {}
        with baza.ulan() as c:
            qatorlar = c.execute("""
                SELECT substr(kategoriya,1,instr(kategoriya,' / ')-1) AS b1,
                       CASE WHEN instr(substr(kategoriya,instr(kategoriya,' / ')+3),' / ')>0
                            THEN substr(substr(kategoriya,instr(kategoriya,' / ')+3),1,
                                 instr(substr(kategoriya,instr(kategoriya,' / ')+3),' / ')-1)
                            ELSE substr(kategoriya,instr(kategoriya,' / ')+3) END AS b2,
                       COUNT(*) n
                FROM elonlar WHERE kategoriya LIKE '% / %'
                GROUP BY b1,b2""").fetchall()
        for r in qatorlar:
            b1, b2, n = r["b1"], (r["b2"] or "").strip(), r["n"]
            b1_soni[b1] = b1_soni.get(b1, 0) + n
            if b2:
                b2_soni[(b1, b2)] = b2_soni.get((b1, b2), 0) + n
        natija = []
        for guruh in tartib + [g for g in guruhlar if g not in tartib]:
            g = guruhlar[guruh]
            nom = nomlar.get(guruh, guruh)
            # 2-daraja: daraxtdan (tartibda), DB'dagi real son bilan.
            # Daraxtda yo'q, lekin DB'da bor bo'limlar ham qo'shiladi.
            pastki: dict[str, dict] = {}
            for yol, toliq in g:
                qism = toliq.split(" / ")
                if len(qism) < 2:
                    continue
                b2 = qism[1].strip()
                if b2 and b2 not in pastki:
                    pastki[b2] = {"nom": b2,
                                  "elonlar": b2_soni.get((nom, b2), 0)}
            for (b1, b2), n in b2_soni.items():
                if b1 == nom and b2 not in pastki:
                    pastki[b2] = {"nom": b2, "elonlar": n}
            natija.append({
                "slug": guruh,
                "nom": nom,
                "elonlar": b1_soni.get(nom, 0),
                "bolimlar": len(g),
                "q": nom,
                "pastki": sorted(pastki.values(),
                                  key=lambda x: x["elonlar"],
                                  reverse=True),
            })
        return natija

    def do_POST(self):                         # noqa: N802
        return self._qamrab(self._post_ich, "POST")

    def _post_ich(self):
        u = urlparse(self.path)

        # ODDIY TEZLIK CHEGARASI.
        # Uyda kerak emas edi — internetda esa birinchi kuniyoq kerak.
        # Himoyasiz POST degani: bir kishi bir soatda 100 000 ta soxta
        # sotuvchi yozib, butun bazani ishlatib bo'lmaydigan qilib
        # qo'yishi mumkin. To'liq autentifikatsiya keyin; hozir hech
        # bo'lmasa oddiy to'siq tursin.
        if not _tezlik_ruxsat(_haqiqiy_ip(self), u.path):
            # JIM QOLMAYDI. Ilgari bu holat hech qayerda yozilmasdi va
            # "haqiqiy odam urilyaptimi yoki bot" degan savolga javob
            # yo'q edi. Chegara noto'g'ri qo'yilgani ham shu sababdan
            # uzoq vaqt sezilmagan.
            print(f"  [tezlik] {_haqiqiy_ip(self)} -> {u.path}", flush=True)
            self._yubor(429, "application/json; charset=utf-8",
                        json.dumps({"xato": "Bir oz shoshildik. "
                                            "Bir daqiqadan keyin qayta "
                                            "yuboring."},
                                   ensure_ascii=False).encode())
            return

        # RASM YOKI RASM+MATN QIDIRUVI.
        # Rasm diskka yozilmaydi. Vision adapter faqat API kaliti server
        # environment'ida bo'lsa tashqi xizmatni chaqiradi; aks holda 503
        # va aniq capability holati qaytadi.
        # PUSH OBUNASI — brauzer o'z endpoint'ini shu yerga yozadi.
        #
        # XAVFSIZLIK — birinchi variantimda zaiflik bor edi: `egasi`
        # ni mijoz o'zi aytardi. Ya'ni birov `{"rol":"sotuvchi",
        # "egasi":104}` yuborib, 104-sotuvchining BARCHA chat
        # bildirishnomalarini o'z telefoniga burib yuborardi.
        #
        # Endi ID mijozdan umuman olinmaydi. Faqat SESSIYA TOKENI
        # qabul qilinadi va u serverda ID ga yechiladi — loyihada
        # allaqachon shu tartib bor (`_actor_ident`, 2026-08-06).
        # Token bo'lmasa obuna yozilmaydi.
        if u.path == "/api/push-obuna":
            try:
                d = self._tana(8 * 1024)
                endpoint = (d.get("endpoint") or "").strip()
                rol = (d.get("rol") or "").strip()
                token = (d.get("token") or "").strip()
                if not endpoint.startswith("https://"):
                    raise ValueError("endpoint noto'g'ri")
                if rol not in ("sotuvchi", "xaridor"):
                    raise ValueError("rol noto'g'ri")

                egasi = _actor_ident({"actor": [token]}, rol)
                if egasi <= 0:
                    self._yubor(401, "application/json; charset=utf-8",
                                json.dumps({"xato": "Sessiya topilmadi"},
                                           ensure_ascii=False).encode())
                    return

                baza.push_obuna_yoz(
                    endpoint, rol, egasi,
                    str(d.get("p256dh") or "")[:200],
                    str(d.get("auth") or "")[:100])
                self._yubor(200, "application/json; charset=utf-8",
                            json.dumps({"ok": True}).encode(),
                            {"Cache-Control": "no-store"})
            except (ValueError, KeyError, TypeError) as e:
                self._yubor(400, "application/json; charset=utf-8",
                            json.dumps({"xato": str(e)},
                                       ensure_ascii=False).encode())
            return

        if u.path == "/api/ai/rasm-qidiruv":
            try:
                d = self._tana(6 * 1024 * 1024)
                natija = ai_vision.tahlil(
                    d.get("rasm_data") or "",
                    (d.get("matn") or "").strip()[:300],
                    "ru" if d.get("til") == "ru" else "uz",
                )
                self._yubor(
                    200,
                    "application/json; charset=utf-8",
                    json.dumps({"ok": True, "tahlil": natija,
                                "qidiruv": natija["qidiruv"]},
                               ensure_ascii=False).encode(),
                    {"Cache-Control": "no-store"},
                )
            except ai_vision.VisionXato as xato:
                self._yubor(
                    xato.http_kod,
                    "application/json; charset=utf-8",
                    json.dumps({"xato": xato.xabar, "kod": xato.kod},
                               ensure_ascii=False).encode(),
                    {"Cache-Control": "no-store"},
                )
            except ValueError:
                self._yubor(
                    413,
                    "application/json; charset=utf-8",
                    json.dumps({"xato": "Rasm 4 MB dan kichik bo‘lishi kerak",
                                "kod": "RASM_KATTA"},
                               ensure_ascii=False).encode(),
                    {"Cache-Control": "no-store"},
                )
            return

        # So'rov qoldirish — qidiruv BOZORGA aylanadigan joy
        if u.path == "/api/sorov":
            uzunlik = int(self.headers.get("Content-Length") or 0)
            try:
                d = json.loads(self.rfile.read(uzunlik) or b"{}")
            except Exception:                  # noqa: BLE001
                self._yubor(400, "application/json", b'{"xato":"noto\'g\'ri"}')
                return

            matn = (d.get("matn") or "").strip()
            # TELEFON SO'RALMAYDI (2026-08-01 qaror).
            # So'rov bir tegishda ketadi; aloqa OBER ichidagi suhbat orqali
            # bo'ladi. Raqam so'rash birinchi marta kirgan odamni to'xtatadi
            # va bizga kerak ham emas — suhbat allaqachon qurilgan.
            aloqa = (d.get("aloqa") or "").strip()
            if not matn:
                self._yubor(400, "application/json; charset=utf-8",
                            json.dumps({"xato": "nima kerakligini yozing"},
                                       ensure_ascii=False).encode())
                return

            byudjet = d.get("byudjet")
            try:
                byudjet = int(str(byudjet).replace(" ", "")) if byudjet else None
            except ValueError:
                byudjet = None
            # BYUDJET MATNNING O'ZIDAN HAM OLINADI.
            # Xaridor alohida maydon to'ldirmaydi, u shunchaki yozadi:
            # "kim 800.000 so'mga beradi?". Sotuvchi uchun bu eng muhim
            # ma'lumot - u javob berishdan oldin narxni biladi.
            if not byudjet:
                byudjet = byudjet_top(matn)

            modellar = sorted(modellarni_top(matn))
            qismlar = sorted(qismlarni_top(matn))
            # YO'NALISH INDEKSDAN ANIQLANADI, lug'atdan emas.
            # `bozor_izi` matnni o'z qidiruvimizga beradi va natijalar
            # qaysi kategoriyada ekanini sanaydi. Sabab `baza.bozor_izi`
            # izohida. Qo'lda yozilgan yo'nalishlar ustiga qo'shiladi —
            # ular banner, xizmat kabi indeksda kam bo'lgan sohalarni
            # qoplaydi.
            yonalishlar = yonalishlar_belgilar(matn)
            sid = baza.sorov_yoz(
                matn, (d.get("tuman") or "").strip(), aloqa, byudjet,
                modellar, qismlar, yonalishlar,
                (d.get("ism") or "").strip()[:40] or None)

            # Birinchi to'lqin darhol ketadi. Qaytadigan son — HAQIQIY son.
            # Ekranda hech qachon "30 ta sotuvchiga yuborildi" deb yozilmaydi
            # agar aslida 15 ta bo'lsa: bitta yolg'on butun ishonchni buzadi.
            tarqatish = baza.tolqin_yubor(sid)

            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps({"ok": True, "id": sid,
                                    "token": baza.sorov_tokeni(sid),
                                    "yuborildi": tarqatish["yuborildi"],
                                    "mos_sotuvchi": tarqatish["mos"],
                                    "holat": ("tarqatildi" if qismlar or yonalishlar
                                              else "aniqlashtirish")},
                                   ensure_ascii=False).encode())
            return

        # Sotuvchi ro'yxatdan o'tadi — 30 soniya, kategoriya daraxti yo'q
        if u.path == "/api/sotuvchi/royxat":
            d = self._tana()
            nom = (d.get("nom") or "").strip()
            nima = (d.get("nima") or "").strip()
            # 2026-08-06: raqam bir xil shaklda saqlansin — kirishda ham
            # xuddi shu normalizatsiya qo'llaniladi.
            aloqa = _telefon_tozala(d.get("aloqa") or "")
            tuman = (d.get("tuman") or "").strip()
            if not nom or not nima or not aloqa or not tuman:
                self._yubor(400, "application/json; charset=utf-8",
                            json.dumps({"xato": "nom, yo'nalish, joy va telefon kerak"},
                                       ensure_ascii=False).encode())
                return
            qismlar = sorted(qismlarni_top(nima))
            modellar = sorted(modellarni_top(nima))
            # Sotuvchi tomonida ham xuddi shu mexanizm — ikkalasi bir
            # xil usulda belgilansagina ular bir-birini topa oladi.
            yonalishlar = yonalishlar_belgilar(nima)

            # SOTUVCHI HECH QACHON RAD ETILMAYDI.
            #
            # 2026-08-04 gacha shu yerda 422 turardi: lug'at tanimasa
            # ro'yxatdan o'tkazmasdi. `yonalishlar.py` da esa BITTA
            # yo'nalish bor edi — banner. Ya'ni OBER amalda faqat
            # avtoehtiyot qism sotuvchi va bannerchini qabul qilardi.
            # Mebelchi, tikuvchi, usta, fotograf, kandolatchi —
            # hammasi eshikdan qaytarilardi.
            #
            # Aziz: "Hali men har xil turdagi sotuvchi va xizmat
            # ko'rsatuvchilarga demak OBER ni tavsiya qila olmas
            # ekanmanda."
            #
            # Aynan shu saboq 2026-08-02 da QIDIRUV tomonida
            # o'rganilgan edi — lug'at shart emas, bonus — lekin
            # sotuvchi halqasiga ko'chirilmagan.
            #
            # Endi lug'at tanimasa ham yozib olamiz: moslik sotuvchining
            # O'Z SO'ZLARI bo'yicha ishlaydi. Tanimaslik bizning
            # kamchiligimiz, sotuvchining aybi emas — buning uchun uni
            # jazolash mumkin emas.
            #
            # Yagona shart: matn mazmunli bo'lsin. Ikkita harf yozib
            # yuborish ro'yxat emas.
            if len(nima) < 3:
                self._yubor(422, "application/json; charset=utf-8",
                            json.dumps({
                                "xato": "Nima sotasiz yoki qanday xizmat ko'rsatasiz — "
                                        "bir-ikki so'z bilan yozing. Masalan: "
                                        "\"mebel yasayman\", \"kir yuvish mashinasi tuzataman\", "
                                        "\"tort pishiraman\"."
                            }, ensure_ascii=False).encode())
                return

            sid = baza.sotuvchi_yoz(nom, nima, qismlar, modellar,
                                    tuman, aloqa, yonalishlar)
            # 2026-08-06: ro'yxatdan o'tish bilan birga sessiya ochiladi —
            # endi kabinet token bilan ishlaydi, ID raqam bilan emas.
            token = baza.sessiya_yarat(sid)
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps({"ok": True, "id": sid, "token": token,
                                    "qismlar": qismlar,
                                    "modellar": modellar,
                                    "yonalishlar": yonalish_nomlari(yonalishlar)},
                                   ensure_ascii=False).encode())
            return

        # Boshqa qurilmadan kabinetga kirish — 1-qadam: kod so'rash.
        # Kod Telegram orqali yuboriladi (SMS xizmati yo'q). Sotuvchi
        # oldin Telegram'ga ulangan bo'lishi shart — ulangan bo'lmasa
        # kodni yuboradigan kanal yo'q va shuni aytamiz.
        #
        # 2026-08-06 kod-review: uch holat uchun bir xil javob beriladi
        # (raqam ro'yxatda yo'q / Telegram ulanmagan / kod yuborilmadi) —
        # qaysi raqamlar ro'yxatda ekanini taxmin qilib bo'lmasin.
        # Ulangan sotuvchi bildirishnoma haqiqatan kelishini o'zi tekshiradi.
        # Sessiya tokeni serverda sotuvchiga yechiladi; Telegram chat ID
        # frontenddan olinmaydi va API javobida oshkor qilinmaydi.
        if u.path == "/api/sotuvchi/telegram/sinov":
            d = self._tana()
            kod, javob = _telegram_sinov((d.get("token") or "").strip())
            self._yubor(kod, "application/json; charset=utf-8",
                        json.dumps(javob, ensure_ascii=False).encode(),
                        {"Cache-Control": "no-store"})
            return

        if u.path == "/api/sotuvchi/kirish":
            d = self._tana()
            aloqa = _telefon_tozala(d.get("aloqa") or "")
            if not aloqa:
                self._yubor(400, "application/json; charset=utf-8",
                            json.dumps({"xato": "telefon raqamini yozing"},
                                       ensure_ascii=False).encode())
                return
            s = baza.sotuvchi_aloqasi(aloqa)
            if not s or not s.get("telegram_id"):
                # RAQAM RO'YXATDAMI YO'QMI — AYTMAYMIZ (enumeration himoyasi)
                self._yubor(200, "application/json; charset=utf-8",
                            json.dumps({"ok": False,
                                        "xato": "kod yuborilmadi. Raqam ro'yxatdan o'tgan "
                                                "va Telegramga ulangan bo'lishi kerak."},
                                       ensure_ascii=False).encode())
                return
            # Bitta raqamga soatiga ko'pi bilan 5 ta kod — boshqa odam
            # kodlarni bekor qilib, egalarini qulflab qo'ymasligi uchun.
            if baza.kirish_kod_soni(aloqa) >= 5:
                self._yubor(429, "application/json; charset=utf-8",
                            json.dumps({"xato": "bu raqamga hozircha ko'p so'rov keldi. "
                                                "Bir soatdan keyin qayta urining."},
                                       ensure_ascii=False).encode())
                return
            import tg
            kod = baza.kirish_kod_yarat(aloqa)
            yuborildi = tg.yubor(s["telegram_id"],
                                 f"🔐 OBER kirish kodi: <b>{kod}</b>\n\n"
                                 f"10 daqiqa amal qiladi. Saytga shu kodni kiriting.",
                                 )
            if not yuborildi:
                baza.kirish_kod_bekor(aloqa)
                self._yubor(502, "application/json; charset=utf-8",
                            json.dumps({"ok": False,
                                        "xato": "kod yuborilmadi. Telegram ishlamayapti — "
                                                "keyinroq qayta urining."},
                                       ensure_ascii=False).encode())
                return
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps({"ok": True}, ensure_ascii=False).encode())
            return

        # Boshqa qurilmadan kabinetga kirish — 2-qadam: kodni tasdiqlash.
        if u.path == "/api/sotuvchi/tasdiq":
            d = self._tana()
            aloqa = _telefon_tozala(d.get("aloqa") or "")
            kod = (d.get("kod") or "").strip()
            sid = baza.kirish_kod_tekshir(aloqa, kod) if aloqa and kod else None
            if not sid:
                self._yubor(401, "application/json; charset=utf-8",
                            json.dumps({"xato": "kod noto'g'ri yoki eskirgan"},
                                       ensure_ascii=False).encode())
                return
            token = baza.sessiya_yarat(sid)
            with baza.ulan() as c:
                s = c.execute("SELECT nom, nima_sotadi FROM sotuvchilar"
                              " WHERE id=?", (sid,)).fetchone()
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps({"ok": True, "id": sid, "token": token,
                                    "nom": s["nom"] if s else ""},
                                   ensure_ascii=False).encode())
            return

        # Chiqish — sessiyani server tomondan bekor qiladi.
        # Avvalgi holat: "Chiqish" tugmasi faqat localStorage'ni tozalardi,
        # sessiya bazada tirik qolardi — token o'g'irlangan bo'lsa kabinet
        # ochiq qolardi. Endi token o'chiriladi va qayta ishlamaydi.
        if u.path == "/api/sotuvchi/chiqish":
            d = self._tana()
            token = (d.get("token") or "").strip()
            baza.sessiya_bekor(token)
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps({"ok": True}, ensure_ascii=False).encode())
            return

        # ── E'LONLARIM — OBER o'z marketplace'i (2026-08-06) ────────────
        # Sotuvchi o'z e'lonini joylashtiradi. Faqat kirgan sotuvchi
        # (token) mumkin. Spamga qarshi: soatiga 20 ta yangi e'lon.
        if u.path == "/api/elon":
            d = self._tana()
            sid = _sotuvchi_ident({"id": [str(d.get("sotuvchi_id") or "")]})
            if not sid:
                self._yubor(401, "application/json; charset=utf-8",
                            json.dumps({"xato": "Kirish muddati tugagan. Qayta kiring."},
                                       ensure_ascii=False).encode())
                return
            nom = (d.get("nom") or "").strip()
            if len(nom) < 3:
                self._yubor(422, "application/json; charset=utf-8",
                            json.dumps({"xato": "Nima sotyotganingizni yozing."},
                                       ensure_ascii=False).encode())
                return
            # Rasm(lar) — chatdagi kabi tekshiriladi va saqlanadi.
            # Eski `/chat-uploads/` yo'llari allaqachon saqlangan — ularni
            # qayta saqlamaymiz, faqat yangi data-URL larni (2026-08-06
            # kod-review: tahrirlashda rasmlar o'chib ketardi).
            try:
                rasmlar = []
                for data in (d.get("rasmlar") or [])[:5]:
                    data = (data or "").strip()
                    if data.startswith("/chat-uploads/") or data.startswith("/elon-rasmlar/"):
                        rasmlar.append(data)
                    else:
                        yol = self._rasm_saqla(data)
                        if yol:
                            rasmlar.append(yol)
            except ValueError as e:
                self._yubor(400, "application/json; charset=utf-8",
                            json.dumps({"xato": str(e)}, ensure_ascii=False).encode())
                return
            narx_xom = d.get("narx") or ""
            elon_id = baza.ober_elon_yoz(sid, {
                "nom": nom,
                "narx_som": narx_xom,
                "kelishiladi": 1 if str(narx_xom).strip() == "" else 0,
                "kategoriya": d.get("kategoriya") or "",
                "viloyat": d.get("viloyat") or "",
                "shahar": d.get("shahar") or "",
                "tuman": d.get("tuman") or "",
                "tavsif": (d.get("tavsif") or "").strip()[:2000],
                "rasm": rasmlar[0] if rasmlar else "",
                "rasmlar_ober": json.dumps(rasmlar, ensure_ascii=False) if rasmlar else "",
            })
            # E'lon joylashtirilishi bilan FTS indeksiga darhol tushadi —
            # qidiruvda chiqishi uchun navbatchi tahlil sikli kutilmaydi.
            # Indeks xatosi e'lon yozilishini buzmasin: navbatchi tahlil
            # keyin yetib oladi (tahlil.py dagi qoida bilan bir xil).
            try:
                tahlil.bitta(elon_id)
            except Exception as e:                # noqa: BLE001
                # 2026-08-15: bu yerda `pass` turardi. Tahlil yiqilsa
                # e'lon indeksga TUSHMAYDI — sotuvchi e'lon joylagan
                # bo'ladi, lekin uni qidiruvda hech kim topolmaydi.
                # Va hech qanday iz qolmasdi: na jurnal, na xabar.
                #
                # E'lonning o'zi saqlangan, shuning uchun javob
                # baribir 200 — lekin endi sabab jurnalda qoladi.
                print(f"  [tahlil] e'lon {elon_id} indekslanmadi: "
                      f"{type(e).__name__}: {e}", flush=True)
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps({"ok": True, "id": elon_id},
                                   ensure_ascii=False).encode())
            return

        # E'lonni tahrirlash / o'chirish — FAQAT egasi
        if u.path.startswith("/api/elon/") and u.path.count("/") == 3:
            qismlar = u.path.split("/")
            try:
                elon_id = int(qismlar[-1])
            except ValueError:
                self._topilmadi()
                return
            d = self._tana()
            sid = _sotuvchi_ident({"id": [str(d.get("sotuvchi_id") or "")]})
            if not sid:
                self._yubor(401, "application/json; charset=utf-8",
                            json.dumps({"xato": "Kirish muddati tugagan. Qayta kiring."},
                                       ensure_ascii=False).encode())
                return
            if d.get("amal") == "ochir":
                if not baza.ober_elon_ochir(sid, elon_id):
                    self._yubor(403, "application/json; charset=utf-8",
                                json.dumps({"xato": "Bu e'lon sizniki emas."},
                                           ensure_ascii=False).encode())
                    return
                self._yubor(200, "application/json; charset=utf-8",
                            json.dumps({"ok": True}, ensure_ascii=False).encode())
                return
            nom = (d.get("nom") or "").strip()
            if len(nom) < 3:
                self._yubor(422, "application/json; charset=utf-8",
                            json.dumps({"xato": "Nima sotyotganingizni yozing."},
                                       ensure_ascii=False).encode())
                return
            try:
                rasmlar = []
                for data in (d.get("rasmlar") or [])[:5]:
                    data = (data or "").strip()
                    if data.startswith("/chat-uploads/") or data.startswith("/elon-rasmlar/"):
                        rasmlar.append(data)
                    else:
                        yol = self._rasm_saqla(data)
                        if yol:
                            rasmlar.append(yol)
            except ValueError as e:
                self._yubor(400, "application/json; charset=utf-8",
                            json.dumps({"xato": str(e)}, ensure_ascii=False).encode())
                return
            narx_xom = d.get("narx") or ""
            ok = baza.ober_elon_yangila(sid, elon_id, {
                "nom": nom,
                "narx_som": narx_xom,
                "kelishiladi": 1 if str(narx_xom).strip() == "" else 0,
                "kategoriya": d.get("kategoriya") or "",
                "viloyat": d.get("viloyat") or "",
                "shahar": d.get("shahar") or "",
                "tuman": d.get("tuman") or "",
                "tavsif": (d.get("tavsif") or "").strip()[:2000],
                "rasm": rasmlar[0] if rasmlar else "",
                "rasmlar_ober": json.dumps(rasmlar, ensure_ascii=False) if rasmlar else "",
            })
            if not ok:
                self._yubor(403, "application/json; charset=utf-8",
                            json.dumps({"xato": "Bu e'lon sizniki emas yoki yopilgan."},
                                       ensure_ascii=False).encode())
                return
            # Tahrirlangach yangi matn bo'yicha indeks yangilanadi.
            try:
                tahlil.bitta(elon_id)
            except Exception as e:                # noqa: BLE001
                # 2026-08-15: bu yerda `pass` turardi. Tahlil yiqilsa
                # e'lon indeksga TUSHMAYDI — sotuvchi e'lon joylagan
                # bo'ladi, lekin uni qidiruvda hech kim topolmaydi.
                # Va hech qanday iz qolmasdi: na jurnal, na xabar.
                #
                # E'lonning o'zi saqlangan, shuning uchun javob
                # baribir 200 — lekin endi sabab jurnalda qoladi.
                print(f"  [tahlil] e'lon {elon_id} indekslanmadi: "
                      f"{type(e).__name__}: {e}", flush=True)
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps({"ok": True, "id": elon_id},
                                   ensure_ascii=False).encode())
            return

        # Bir tegishli javob: chatda yozish (2026-08-07)
        # Ilgari BOR/YO'Q/O'XSHASHI BOR tugmalari + majburiy narx bor edi.
        # Endi sotuvchi chat komposerida yozadi — narx ixtiyoriy, chatda
        # kelishiladi. `holat='bor'` — javob mavjud; `yoq` — yo'q.
        if u.path == "/api/sotuvchi/javob":
            d = self._tana()
            holat = (d.get("holat") or "yoq").strip()
            if holat not in {"bor", "yoq", "oxshash"}:
                self._yubor(400, "application/json; charset=utf-8",
                            json.dumps({"xato": "javob turi noto'g'ri"},
                                       ensure_ascii=False).encode())
                return
            try:
                narx = int(str(d.get("narx") or "").replace(" ", "")) or None
            except ValueError:
                narx = None
            try:
                rasm = self._rasm_saqla(d.get("rasm_data") or "")
            except ValueError as e:
                self._yubor(400, "application/json; charset=utf-8",
                            json.dumps({"xato": str(e)}, ensure_ascii=False).encode())
                return
            sid = _sotuvchi_ident({"id": [str(d.get("sotuvchi_id") or "")]})
            # 2026-08-06: chiqish sessiyani o'chirgach token 0 beradi — yozish
            # ham bloklansin. Aks holda o'chirilgan token bilan javob
            # yozishda davom etish mumkin bo'lardi (sid=0 sifatida).
            if not sid:
                self._yubor(401, "application/json; charset=utf-8",
                            json.dumps({"xato": "Kirish muddati tugagan. Qayta kiring."},
                                       ensure_ascii=False).encode())
                return
            suhbat_id = baza.javob_yoz(
                int(d.get("sorov_id") or 0),
                sid, holat, narx,
                (d.get("izoh") or "").strip()[:1000], rasm)
            if suhbat_id is None:
                self._yubor(409, "application/json; charset=utf-8",
                            json.dumps({"xato": "So'rov sizga yuborilmagan, yopilgan yoki unga javob berilgan."},
                                       ensure_ascii=False).encode())
                return
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps({"ok": True,
                                    "suhbat_id": suhbat_id or None},
                                   ensure_ascii=False).encode())
            return

        if u.path == "/api/taklif/tanlash":
            d = self._tana()
            sorov_id = _actor_ident(
                {"actor": [str(d.get("actor_id") or "")]}, "xaridor")
            if not sorov_id:
                self._yubor(401, "application/json; charset=utf-8",
                            json.dumps({"xato": "So'rov sessiyasi topilmadi"},
                                       ensure_ascii=False).encode())
                return
            suhbat_id = baza.taklif_tanla(
                sorov_id, int(d.get("javob_id") or 0))
            if not suhbat_id:
                self._yubor(404, "application/json; charset=utf-8",
                            json.dumps({"xato": "Taklif topilmadi"},
                                       ensure_ascii=False).encode())
                return
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps({"ok": True, "suhbat_id": suhbat_id},
                                   ensure_ascii=False).encode())
            return

        # KERAKLISI QAYERDAN TOPILDI — xaridor aytadi (2026-08-10).
        # Javob ixtiyoriy. Sabab `baza.natija_yoz` izohida.
        if u.path == "/api/sorov/natija":
            d = self._tana()
            sorov_id = _actor_ident(
                {"actor": [str(d.get("actor_id") or "")]}, "xaridor")
            if not sorov_id:
                self._yubor(401, "application/json; charset=utf-8",
                            json.dumps({"xato": "So'rov sessiyasi topilmadi"},
                                       ensure_ascii=False).encode())
                return
            natija = (d.get("natija") or "").strip()
            if not baza.natija_yoz(sorov_id, natija):
                self._yubor(400, "application/json; charset=utf-8",
                            json.dumps({"xato": "Natija noto'g'ri"},
                                       ensure_ascii=False).encode())
                return
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps({"ok": True}, ensure_ascii=False).encode())
            return

        # Onlayn vaqtni yashirish/ko'rsatish (Telegramdagi kabi tanlov)
        if u.path == "/api/maxfiylik/vaqt":
            d = self._tana()
            rol = (d.get("rol") or "").strip()
            baza.vaqt_yashirish(
                rol,
                _actor_ident({"actor": [str(d.get("actor_id") or "")]}, rol),
                bool(d.get("yashir")))
            self._yubor(200, "application/json", b'{"ok":true}')
            return

        # Xaridor sotuvchining raqamini ochdi — konversiya o'lchovi
        if u.path == "/api/javob/raqam":
            d = self._tana()
            baza.raqam_ochildi(int(d.get("javob_id") or 0))
            self._yubor(200, "application/json", b'{"ok":true}')
            return

        if u.path == "/api/suhbat/xabar":
            d = self._tana()
            matn = (d.get("matn") or "").strip()[:2000]
            try:
                rasm = self._rasm_saqla(d.get("rasm_data") or "")
            except ValueError as e:
                self._yubor(400, "application/json; charset=utf-8",
                            json.dumps({"xato": str(e)}, ensure_ascii=False).encode())
                return
            # JOYLASHUV — "shu yerdaman" deyish uchun. "lat,lon" ko'rinishida
            # saqlanadi; ilovada ham xuddi shu maydon ishlatiladi.
            joy = ""
            try:
                lat = float(d.get("lat"))
                lon = float(d.get("lon"))
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    joy = f"{lat:.6f},{lon:.6f}"
            except (TypeError, ValueError):
                joy = ""
            xabar_id = baza.suhbat_xabar_yoz(
                int(d.get("suhbat_id") or 0), (d.get("rol") or "").strip(),
                _actor_ident({"actor": [str(d.get("actor_id") or "")]},
                             (d.get("rol") or "").strip()),
                matn, rasm, joy)
            if not xabar_id:
                self._yubor(403, "application/json; charset=utf-8",
                            json.dumps({"xato": "Xabar yuborilmadi"},
                                       ensure_ascii=False).encode())
                return
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps({"ok": True, "id": xabar_id, "rasm": rasm},
                                   ensure_ascii=False).encode())
            return

        if u.path == "/api/bildirishnomalar/oqildi":
            d = self._tana()
            soni = baza.bildirishnomalar_oqildi(
                (d.get("rol") or "").strip(),
                _actor_ident({"actor": [str(d.get("actor_id") or "")]},
                             (d.get("rol") or "").strip()))
            self._yubor(200, "application/json; charset=utf-8",
                        json.dumps({"ok": True, "oqildi": soni},
                                   ensure_ascii=False).encode())
            return

        self._yubor(404, "text/plain", b"topilmadi")

    def _tana(self, limit: int | None = None) -> dict:
        uzunlik = int(self.headers.get("Content-Length") or 0)
        if limit is not None and uzunlik > limit:
            raise ValueError("tana juda katta")
        try:
            return json.loads(self.rfile.read(uzunlik) or b"{}")
        except Exception:                      # noqa: BLE001
            return {}

    def _rasm_saqla(self, data_url: str) -> str:
        if not data_url:
            return ""
        if len(data_url) > MAX_RASM * 2:
            raise ValueError("Rasm 5 MB dan kichik bo‘lishi kerak")
        try:
            sarlavha, kod = data_url.split(",", 1)
            mime = sarlavha.split(";", 1)[0].replace("data:", "")
            kengaytma = {"image/jpeg": ".jpg", "image/png": ".png",
                         "image/webp": ".webp"}.get(mime)
            if not kengaytma or ";base64" not in sarlavha:
                raise ValueError
            tana = base64.b64decode(kod, validate=True)
        except (ValueError, binascii.Error):
            raise ValueError("Faqat JPG, PNG yoki WEBP rasm yuboring") from None
        if not tana or len(tana) > MAX_RASM:
            raise ValueError("Rasm 5 MB dan kichik bo‘lishi kerak")
        UPLOADS.mkdir(parents=True, exist_ok=True)
        nom = f"{uuid.uuid4().hex}{kengaytma}"
        (UPLOADS / nom).write_bytes(tana)
        return f"/chat-uploads/{nom}"


def _telefon_tozala(aloqa: str) -> str:
    """Telefon raqamini bir xil shaklga keltiradi: faqat raqamlar.

    2026-08-06: ro'yxatda '+998 90 123 45 67' yozib, kirishda
    '+998901234567' yozsa kod topilmas edi. Ro'yxatga olish ham,
    kirish ham bir xil funksiyadan o'tsin.
    """
    raqam = "".join(ch for ch in (aloqa or "") if ch.isdigit())
    # 8 dan boshlansa O'zbekiston prefiksi qo'shiladi (990901234567)
    if len(raqam) == 9 and raqam.startswith("9"):
        return "998" + raqam
    if len(raqam) == 12 and raqam.startswith("998"):
        return raqam
    return raqam


def _telegram_sinov(token: str) -> tuple[int, dict]:
    """Sotuvchining o'z Telegramiga bitta xavfsiz test xabari yuboradi."""
    sotuvchi_id = baza.sessiya_sotuvchisi(token)
    if not sotuvchi_id:
        return 401, {"ok": False, "xato": "Sotuvchi sessiyasi topilmadi"}

    telegram_id = baza.sotuvchi_telegrami(sotuvchi_id)
    if not telegram_id:
        return 409, {"ok": False,
                     "xato": "Avval Telegramni ulang, keyin qayta sinang"}

    import tg
    matn = ("✅ <b>OBER bildirishnomasi ishlayapti</b>\n\n"
            "Endi yangi so‘rov va xaridor chat xabarlari shu yerga keladi.")
    tugmalar = [[{"text": "Sotish bo‘limini ochish",
                  "url": "https://ober.uz/sotuvchi"}]]
    if tg.yubor(telegram_id, matn, tugmalar):
        return 200, {"ok": True}
    return 502, {"ok": False,
                 "xato": "Test xabar yuborilmadi. Botni ochib /start bosing, "
                         "keyin qayta sinang"}


def _sotuvchi_ident(p) -> int:
    """So'rov parametridan sotuvchi identifikatori.

    2026-08-06: kabinet endi sessiya TOKENI bilan ochiladi (boshqa qurilmada
    ham ishlaydi, ID taxmin qilib bo'lmaydi). Eski qurilmalarda localStorage'da
    ID raqami qolgan bo'lishi mumkin — u ham qabul qilinadi.
    """
    qiymat = (p.get("id") or [""])[0].strip()
    if not qiymat:
        return 0
    if qiymat.isdigit():
        return 0
    return baza.sessiya_sotuvchisi(qiymat) or 0


def _xaridor_ident(p) -> int:
    """Querydagi xaridor sessiya tokenini ichki so'rov IDga yechadi."""
    qiymat = (p.get("id") or p.get("actor") or [""])[0].strip()
    return baza.sorov_id_token(qiymat) or 0


def _actor_ident(p, rol: str) -> int:
    """Chat aktori roliga mos yopiq sessiya tokeni bilan aniqlanadi."""
    qiymat = (p.get("actor") or [""])[0].strip()
    if not qiymat:
        return 0
    if rol == "sotuvchi":
        return _sotuvchi_ident({"id": [qiymat]})
    if rol == "xaridor":
        return baza.sorov_id_token(qiymat) or 0
    return 0


def _port_bandmi() -> bool:
    """8800 allaqachon band bo'lsa — eski server ishlab turibdi."""
    import socket
    s = socket.socket()
    s.settimeout(1)
    try:
        s.connect(("127.0.0.1", PORT))
        return True
    except OSError:
        return False
    finally:
        s.close()


class Server(ThreadingHTTPServer):
    """ThreadingHTTPServer, lekin kutish navbati kattaroq.

    2026-08-04, sayt 14 soat 502 berib turdi. Caddy jurnali:
    "dial tcp 127.0.0.1:8800: i/o timeout" — ya'ni TCP ULANIB ham
    bo'lmadi, HTTP xatosi emas. `ss -tln` sababini ko'rsatdi:

        LISTEN 6  5  127.0.0.1:8800

    Chapdagi 6 — navbatda kutayotgan ulanish, o'ngdagi 5 — chegara.
    Navbat to'lgach yadro yangi ulanishni javobsiz tashlaydi.
    `request_queue_size` standarti 5 — bu 1990-yillardan qolgan qiymat.
    Bitta sahifa ochilishi HTML + rasmlar uchun bir nechta ulanish
    oladi, demak 5 ta odam bir vaqtda kirsa yetmaydi.
    """

    request_queue_size = 128
    daemon_threads = True


# ── _lugat_qorovuli OLIB TASHLANDI (2026-08-10) ──────────────────────
#
# Bu oqim har 6 soatda `soz_kategoriya.qur()` ni chaqirib, HAR SO'Z
# uchun bitta kategoriya beradigan jadval quriardi. Endi uni hech kim
# ishlatmaydi — o'rniga `baza.bozor_izi` keldi.
#
# Farqi: eski jadval so'zni YOLG'IZ ko'rardi ("oyna" -> "Uy va bog'"),
# yangisi butun matnni indeksdan o'tkazadi va so'zlarni BIRGALIKDA
# ko'radi ("lacetti + oyna" -> Transport).
#
# `soz_kategoriya.py` fayli qoldirildi: u boshqa maqsadda (bozor
# tahlili) foydali bo'lishi mumkin va hech narsani buzmaydi. Faqat
# avtomatik qayta qurish to'xtatildi — bu har 6 soatda 300 000
# e'lonni bekorga o'qish edi.

# ── KESHNI ISITIB TURISH (2026-08-17) ────────────────────────────────
#
# MUAMMO — o'lchangan, taxmin emas. Aziz "sayt juda sekin" dedi va
# raqamlar shuni ko'rsatdi:
#
#   server yuki 0.07 (bo'sh)        sahifaning o'zi 679 ms (tez)
#   /api/yangi?n=14   3 KB -> 3835 ms
#   /api/kategoriyalar 2 KB -> 3029 ms
#   /api/qidiruvlar   0 KB -> 1673 ms
#
# Serverda o'sha funksiyalarni to'g'ridan chaqirsak: 1906 / 0 / 0 ms.
# Birinchi chaqiruv soniyalar, keyingi ikkitasi NOL — ya'ni ish emas,
# SOVUQ KESH.
#
# `yangi_elonlar` da 2 daqiqalik kesh, kategoriyalarda 5 daqiqalik
# kesh bor. Ular YUK bo'lganda foyda beradi: kimdir sovuq narxni
# to'laydi, qolgan yuzlab odam issiqdan oladi. OBERda esa hali yuk
# yo'q — tashrifchilar bir-biridan daqiqalar uzoq keladi, ya'ni
# DEYARLI HAR TASHRIFCHI sovuq keshga tushadi va 3 soniya kutadi.
#
# Bu eng yoqimsiz turdagi muammo: trafik kelsa o'zi yo'qoladi, lekin
# aynan o'sha trafikni qochiradi.
#
# Yechim: keshni ODAM emas, SERVER isitadi. 90 soniya — ikkala
# TTL'dan (120 s va 300 s) qisqa, ya'ni haqiqiy odam har doim
# issiqqa tushadi.
#
# NEGA HTTP ORQALI, funksiyani to'g'ridan chaqirib emas: kesh ikki
# joyda (`baza._YANGI_KESH` va `server._KAT_KESH`), va biri
# ishlovchi metodining ichida. O'z manzilimizga so'rov yuborish
# ularning HAMMASINI, foydalanuvchi yuradigan aynan yo'l bilan
# isitadi — kelajakda yangi kesh qo'shilsa ham o'zi qamraladi.
ISITISH_ORALIQ = 90
ISITILADIGAN = ("/api/yangi?n=14", "/api/kategoriyalar", "/api/qidiruvlar")


def _keshni_isit(oraliq: int = ISITISH_ORALIQ) -> None:
    """Sovuq keshni odamdan oldin server o'zi isitadi."""
    import urllib.error
    import urllib.request
    # Server hali `serve_forever` ga yetmagan bo'lishi mumkin.
    time.sleep(3)
    while True:
        for yol in ISITILADIGAN:
            try:
                soz = urllib.request.Request(
                    f"http://127.0.0.1:{PORT}{yol}",
                    headers={"User-Agent": "ober-isitgich"})
                urllib.request.urlopen(soz, timeout=30).read()
            except (urllib.error.URLError, OSError, ValueError):
                # Isitish HECH QACHON saytni buzmasin. Server
                # ko'tarilmagan yoki so'rov sekin bo'lsa — keyingi
                # aylanada qayta urinamiz, jimgina.
                pass
        time.sleep(oraliq)


def _wal_qorovuli(oraliq: int = 600) -> None:
    """WAL faylni vaqti-vaqti bilan qisqartiradi.

    2026-08-04: `ober.db-wal` 154 MB gacha shishgan edi (bazaning o'zi
    445 MB). SQLite odatda uni o'zi tozalaydi (`wal_autocheckpoint`,
    ~4 MB), lekin tozalash faqat WAL'ni O'QIYOTGAN hech kim qolmaganda
    bajariladi. Bizda yig'uvchi doim yozadi, qidiruv doim o'qiydi —
    "bo'sh lahza" hech qachon kelmaydi va WAL cheksiz o'sadi.

    Katta WAL = har o'qish ko'proq sahifa aylanadi = qidiruv sekinlashadi.

    TRUNCATE band bo'lsa shunchaki muvaffaqiyatsiz qaytadi (0 emas) —
    hech narsani buzmaydi, keyingi safar qayta urinadi.
    """
    while True:
        time.sleep(oraliq)
        try:
            with baza.ulan() as c:
                c.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        except Exception as e:                        # noqa: BLE001
            print(f"  [wal] {type(e).__name__}: {e}", flush=True)


def main() -> None:
    # Xato xabari — DSN bo'lmasa jim qoladi, hech narsa o'zgarmaydi.
    xato_xabar.ornat()
    if xato_xabar.yoqilganmi():
        print("  Xato xabari: Sentry yoqilgan", flush=True)

    # IKKI MARTA ISHGA TUSHIRISHNI OLDINI OLAMIZ.
    # 2026-08-01: eski server portni ushlab turgan, yangisi ko'tarilmagan.
    # Natijada sayt ESKI kod bilan ishlayotgani bilinmay qoldi (yangi
    # manzillar "topilmadi" qaytardi), Telegram boti esa 409 xatosini
    # takrorlab turdi. Endi bu holat darhol va aniq aytiladi.
    if _port_bandmi():
        print("=" * 60)
        print("  DIQQAT — OBER ALLAQACHON ISHLAB TURIBDI")
        print("=" * 60)
        print(f"\n  {PORT}-port band. Ya'ni boshqa cmd oynasida server bor.")
        print("  Yangi kod ishlashi uchun ESKISINI YOPING:")
        print("    1. Barcha cmd oynalarini yoping (Ctrl+C yoki X)")
        print("    2. KOR-BRAUZERDA.bat ni QAYTA bosing\n")
        return

    baza.init()

    # YETIM YOZUVLAR — o'chirilgan sotuvchilarga tegishli qoldiqlar.
    # Har startda tozalanadi (CLAUDE.md #5): yuborishlar, suhbatlar,
    # xabarlar, javoblar, push obunalari. Yangi yetim bo'lmasa hech
    # narsa o'chmaydi; xato bo'lsa server baribir ko'tariladi.
    try:
        tozalangan = baza.yetimlarni_tozala()
        jami = sum(tozalangan.values())
        if jami:
            print(f"  Yetim yozuvlar tozalandi: {tozalangan}")
    except Exception as e:                        # noqa: BLE001
        print(f"  Yetim tozalash o'tkazib yuborildi: {type(e).__name__}")

    def _indeksni_tekshir() -> None:
        """INDEKS BO'SH QOLIB KETMASIN.

        Tahlil qilingan e'lon bor, indeks esa bo'sh bo'lsa — qidiruv hech
        narsa topmaydi. Bu jimgina sodir bo'ladigan nosozlik, shuning uchun
        server o'zi tekshiradi va tuzatadi. Tahlildan KEYIN chaqiriladi:
        aks holda hali tahlil qilinmagan e'lonlar hisobga olinmay,
        indeks behuda qayta qurilardi.
        """
        if not baza.FTS_BOR:
            return
        try:
            with baza.ulan() as c:
                tayyor = c.execute(
                    "SELECT COUNT(*) n FROM elonlar"
                    " WHERE faol=1 AND tan_qismlar IS NOT NULL").fetchone()["n"]
                indeksda = c.execute(
                    "SELECT COUNT(*) n FROM elonlar_fts").fetchone()["n"]
            if tayyor and indeksda < tayyor * 0.9:
                print(f"\n  Qidiruv indeksi to'liq emas ({indeksda}/{tayyor})"
                      f" — qayta quriladi...")
                import fts_qur
                fts_qur.main()
        except Exception as e:                        # noqa: BLE001
            print(f"  [indeks] xato: {type(e).__name__}: {e}")

    # TAHLIL QILINMAGAN E'LON QOLMASIN.
    # 2026-07-31: baza 1 607 dan 8 527 ga o'sgach qidiruv qotib qoldi.
    # Sabab: tahlil qilinmagan e'lon har so'rovda qaytadan tahlil qilinadi
    # (imlo, lug'at, qo'shimchalar) — 8 500 ta uchun bu daqiqalar demak.
    # Endi server ko'tarilishida o'zi tekshiradi va tugatadi.
    # 2026-08-01, o'lchandi: bazada 11 500 e'lon bor edi, qidiruv esa
    # atigi 3 030 tasini ko'rardi. 8 470 e'lon — 74% — KO'RINMAS edi,
    # chunki tahlil qilinmagan e'lon `qidiruv._elonlar()` filtridan
    # o'tmaydi (`tan_qismlar IS NOT NULL`).
    #
    # Sabab: tahlil "kesh belgisi fayli yo'q bo'lsa" shartiga bog'langan
    # edi va yig'ish xatosi bo'lganda `yigish.py` uni butunlay o'tkazib
    # yuborardi. Ekranda "oxirgi tayyor kesh ishlaydi" deb yozilardi —
    # ya'ni nosozlik NORMAL holat kabi ko'rinardi va hech kim sezmasdi.
    #
    # Endi shart yo'q: tahlil qilinmagan e'lon qolsa, HAR DOIM tugatiladi.
    # Tahlil idempotent — qiladigan ish bo'lmasa darhol qaytadi.
    with baza.ulan() as c:
        qoldi = c.execute("SELECT COUNT(*) n FROM elonlar"
                          " WHERE faol=1 AND tan_qismlar IS NULL").fetchone()["n"]
    if qoldi:
        # TAHLIL SAYTNI KUTDIRMAYDI.
        # 2026-08-02, serverda o'lchandi: 31 250 ta tahlil qilinmagan e'lon
        # bor edi va server portni OCHMASDAN oldin hammasini tahlil qildi.
        # 1 yadroli mashinada bu 15-30 daqiqa — ya'ni har qayta ishga
        # tushirishda sayt yarim soatga o'chib turardi. Foydalanuvchi uchun
        # bu "sayt ishlamayapti" degani.
        #
        # Endi tahlil fonda ketadi. Sayt darhol ochiladi; tahlil qilinmagan
        # e'lonlar bir necha daqiqa ichida qidiruvga qo'shilib boradi.
        print(f"\n  {qoldi} ta e'lon tahlil qilinmagan — FONDA tahlil "
              f"qilinmoqda. Sayt darhol ishlaydi, e'lonlar asta qo'shiladi.")

        def _fonda_tahlil():
            try:
                import tahlil
                tahlil.main()
                print("  [tahlil] tugadi — hamma e'lon qidiruvda")
            except Exception as e:                    # noqa: BLE001
                print(f"  [tahlil] xato: {type(e).__name__}: {e}")
            _indeksni_tekshir()

        threading.Thread(target=_fonda_tahlil, daemon=True).start()
    else:
        _indeksni_tekshir()

    kesh_soni = keshni_tayyorla()

    with baza.ulan() as c:
        jami = c.execute(
            "SELECT COUNT(*) n FROM elonlar WHERE faol=1"
        ).fetchone()["n"]

    manzil = f"http://127.0.0.1:{PORT}"
    print("=" * 60)
    print("  OBER — sinov serveri")
    print("=" * 60)
    print(f"\n  Bazada {jami} e'lon")
    print(f"  Qidiruv keshida {kesh_soni} tayyor e'lon")
    print(f"  Manzil: {manzil}")
    print("\n  Brauzer o'zi ochiladi. To'xtatish: Ctrl+C\n")

    # Serverda brauzer yo'q — o'zi ochilmasin (systemd OBER_NO_BROWSER=1 beradi)
    if os.environ.get("OBER_NO_BROWSER") != "1":
        try:
            webbrowser.open(manzil)
        except Exception:                      # noqa: BLE001
            pass

    # Telegram akkauntni bog'laydi, kirish kodini yuboradi va sotuvchiga
    # yangi mos so'rov hamda xaridor chat xabarini bildiradi.
    try:
        import tg
        if tg.token():
            tg.fonda_boshla()
            print("  Telegram kirish va bildirishnomalar: yoqilgan")
        else:
            print("  Telegram kirish va bildirishnomalar: o'chiq "
                  "(data/bot-token.txt yo'q)")
    except Exception as e:                        # noqa: BLE001
        print(f"  Telegram boti ishga tushmadi: {type(e).__name__}")

    # WEB PUSH — telefon jiringlashi uchun (2026-08-14).
    # Telegramdan MUSTAQIL: biri o'chiq bo'lsa ikkinchisi ishlaydi.
    # Kalit yo'q bo'lsa bu yerda BIR MARTA yaratiladi va
    # `data/vapid.json` ga saqlanadi (git'ga tushmaydi).
    try:
        import push
        import push_halqa
        push.kalit_ol()          # yo'q bo'lsa yaratadi
        threading.Thread(target=push_halqa.halqa, daemon=True).start()
        print("  Web Push bildirishnomalari: yoqilgan")
    except Exception as e:                        # noqa: BLE001
        # Push ishlamasa sayt baribir ishlashi kerak — bu qo'shimcha
        # kanal, asosiy funksiya emas.
        print(f"  Web Push ishga tushmadi: {type(e).__name__}: {e}")

    threading.Thread(target=_wal_qorovuli, daemon=True).start()
    threading.Thread(target=_keshni_isit, daemon=True).start()

    # ThreadingHTTPServer: bitta sekin so'rov butun saytni to'xtatib
    # qo'ymasligi uchun. Oddiy HTTPServer navbat bilan ishlaydi va
    # sinov paytida sahifa butunlay qotib qolgan edi.
    #
    # request_queue_size: standarti 5. 2026-08-04 da sayt tushganda
    # `ss -tln` "LISTEN 6 5" ko'rsatdi — navbat TO'LGAN edi va Caddy
    # TCP ulana olmay 502 berdi. 5 juda kichik: bitta sahifa ochilishi
    # HTML + rasmlar uchun bir nechta ulanish oladi.
    Server((HOST, PORT), Ishlovchi).serve_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n  To'xtatildi.\n")
