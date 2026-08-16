"""
WEB SINOVI — sahifa brauzerda umuman ishga tushadimi?

NEGA BU FAYL BOR (2026-08-10)
-----------------------------
Aziz: *"yangi e'longa kirsam ham profilga kirsam ham hech narsa
chiqmayapdi"*

Sotuvchi kabineti butunlay bo'sh ochilardi. Sabab bitta belgi edi:
`elonForma()` ichidagi shablon satriga (template literal) HTML izohi
yozilgan va izoh ichida TESKARI APOSTROF bor edi:

    $("#asosiy").innerHTML = `...
      <!-- 2026-08-10: bu yerda `<input placeholder="...">` turardi -->
      ...`;

Birinchi teskari apostrof shablonni YOPADI. Undan keyingi matn JS deb
o'qiladi va butun blok yiqiladi:

    Uncaught SyntaxError: Unexpected identifier 'placeholder'

SyntaxError butun `<script>` blokini ishga tushirmaydi. Sahifa
yuklanadi, CSS chiqadi, lekin HECH NARSA chizilmaydi.

Buni topish qiyin bo'ldi: server 200 qaytarardi, fayllar joyida edi,
API ishlardi. Faqat Caddy jurnalidan ko'rindiki brauzer `/sotuvchi`
ni yuklab, keyin BIRORTA `/api/sotuvchi/*` so'rovi qilmagan.

Bu sinov shu sinfdagi xatolarni fayl darajasida ushlaydi — brauzersiz.

Ishga tushirish:  python3 web_sinov.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parent.parent / "web"


def ichki_skriptlar(matn: str) -> list[tuple[int, str]]:
    """(boshlanish ofseti, kod) — faqat `src` siz `<script>` bloklari."""
    return [(m.start(1), m.group(1)) for m in
            re.finditer(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>",
                        matn, re.S)]


def qator(matn: str, ofset: int) -> int:
    return matn[:ofset].count("\n") + 1


def main() -> int:
    xato = 0
    jami = 0

    for fayl in sorted(WEB.glob("*.html")):
        matn = fayl.read_text(encoding="utf-8")

        # 1. HAR SAHIFADA `[hidden]` QOIDASI BO'LSIN.
        #    Bu xato uch marta takrorlangan (index, takliflar, elon):
        #    qoida bo'lmasa `hidden` atributi ishlamaydi va yashirin
        #    bo'lishi kerak element ekranda qolib ketadi.
        jami += 1
        if not re.search(r"\[hidden\][^{]*\{[^}]*display\s*:\s*none",
                         matn, re.I):
            xato += 1
            print("  XATO %-16s [hidden]{display:none!important} yo'q"
                  % fayl.name)

        for ofset, kod in ichki_skriptlar(matn):
            # 2. TESKARI APOSTROF JUFT BO'LSIN.
            jami += 1
            if kod.count("`") % 2:
                xato += 1
                print("  XATO %-16s teskari apostrof TOQ (%d ta) — "
                      "shablon satri yopilmagan"
                      % (fayl.name, kod.count("`")))

            # 3. JS ICHIDA HTML IZOHI (`<!--`) UMUMAN BO'LMASIN.
            #
            #    Qoida ataylab keng. Avval "faqat shablon satri ichida
            #    bo'lmasin" deb yozilgandi va buning uchun kichik JS
            #    yuruvchi kerak bo'ldi — u ishonchsiz chiqdi: ataylab
            #    buzib sinaganda xatoni KO'RMADI.
            #
            #    JS ichida HTML izohining o'rni yo'q. Tushuntirish
            #    kerak bo'lsa `//` yoki `/* */` bor. Shuning uchun
            #    yuruvchi olib tashlandi va oddiy qoida qoldi —
            #    u yolg'on o'tkazmaydi.
            for m in re.finditer(r"<!--", kod):
                jami += 1
                xato += 1
                print("  XATO %-16s %d-qator: JS ichida HTML izohi "
                      "(<!--). Shablon satriga tushsa va ichida teskari "
                      "apostrof bo'lsa — butun skript yiqiladi. `//` "
                      "ishlating." % (fayl.name, qator(matn, ofset + m.start())))

            # 4. MATN ICHIDA `</script` BO'LMASIN — brauzer blokni
            #    o'sha yerda kesib tashlaydi.
            jami += 1
            if re.search(r"</script", kod, re.I):
                xato += 1
                print("  XATO %-16s skript ichida `</script` matni"
                      % fayl.name)

    # 4d. XOM AMBER CTA RANGI QAYTIB KELMASIN.
    #
    # 2026-08-12 texnik qarz: `linear-gradient(180deg,#ffc24d,#f59e0b)`
    # va `color:#231400` 14+ joyda qo'lda takrorlanardi — bitta tokenga
    # yig'ildi (`--cta-gradient`, `--on-cta`). Qoida: xom qiymat faqat
    # ober-ui.css dagi TOKEN TA'RIFIDA bo'lishi mumkin, sahifalarda —
    # yo'q. Aks holda "rangni o'zgartir" yana bir necha joyda qayta
    # yozishga aylanadi.
    #
    # 90deg/100deg variantlar (tanlangan chip, hero amb, karta chizig'i)
    # ataylab qoldirilgan — bitta joyda, takrorlanmaydi.
    for nom in ("index.html", "takliflar.html", "sotuvchi.html",
                "kategoriyalar.html", "elon.html", "tabbar.js"):
        jami += 1
        matn = (WEB / nom).read_text(encoding="utf-8")
        if ("linear-gradient(180deg,#ffc24d,#f59e0b)" in matn or
                "color:#231400" in matn or
                "color:#ffc24d" in matn or
                "background:#ffc24d" in matn):
            xato += 1
            print("  XATO %-16s xom amber CTA rangi — `var(--cta-gradient)` "
                  "va `var(--on-cta)` ishlating (ober-ui.css da bitta joy)" % nom)

    # 4b. TELEFONDA YOPISHQOQ ELEMENT BITTA.
    #
    # Dizayn qoidasi, `CLAUDE.md` da eng ko'p takrorlangan xatolar
    # ro'yxatida. Sabab o'lchovda: 390x640 ekranda yopishqoq tepa panel
    # (65 px) va pastki tab bar (56 px) birgalikda 121 px — ekranning
    # 19% i doim band, mazmun uchun 519 px qoladi.
    #
    # 2026-08-11 stendida uch sahifada buzilgan edi: /sotuvchi,
    # /kategoriyalar, /takliflar. Pastdagi tab bar yopishqoq qoladi
    # (u navigatsiya), tepa panel esa skroll bilan ketadi.
    for nom in ("sotuvchi.html", "takliflar.html", "kategoriyalar.html"):
        jami += 1
        matn = (WEB / nom).read_text(encoding="utf-8")
        # Mobil media so'rovi ichida `.topbar` yopishqoqligi bekor
        # qilinganmi. Bo'shliqlarga bardoshli qidiramiz.
        bekor = re.search(
            r"@media[^{]*max-width:\s*6[0-9]{2}px[^{]*\{(?:[^{}]|\{[^{}]*\})*?"
            r"\.topbar\s*\{[^}]*position\s*:\s*(?:static|absolute)",
            matn, re.S)
        if not bekor:
            xato += 1
            print("  XATO %-16s telefonda `.topbar` yopishqoqligi "
                  "bekor qilinmagan — tab bar bilan birga ikkita "
                  "yopishqoq element bo'lib qoladi" % nom)

    # 4c. BOSH SAHIFADA SHAFFOF PANEL CHIZIQ QOLDIRMASIN.
    #
    # 2026-08-11, Azizning telefon skrinshoti: hero sarlavhasi ustidan
    # ingichka chiziq o'tib turardi. `index.html` da chegara ataylab
    # `transparent`, lekin `ober-ui.css` (inline stildan KEYIN
    # yuklanadi) barcha sahifalarga `.topbar{border-color;box-shadow}`
    # beradi. Bosh sahifada panel shaffof va rasm ustida suzadi —
    # chegara hech narsani ajratmaydi, faqat rasmni kesib o'tadi.
    #
    # Natijalar sahifasida panel to'q fonli bo'ladi, u yerda chegara
    # KERAK — shuning uchun qoida `:not(.is-results)` bilan.
    jami += 1
    bosh = (WEB / "index.html").read_text(encoding="utf-8")
    if not re.search(r"body:not\(\.is-results\)\s+\.topbar\s*\{"
                     r"[^}]*border-bottom-color\s*:\s*transparent"
                     r"[^}]*box-shadow\s*:\s*none", bosh, re.S):
        xato += 1
        print("  XATO %-16s bosh sahifada shaffof tepa panel chegarasi "
              "va soyasi bekor qilinmagan — hero ustida chiziq "
              "qoladi" % "index.html")

    # 4i. PUSH ZANJIRI UZILMASIN (2026-08-15).
    #
    # Butun push tizimi qurilgan edi — VAPID kaliti, yuborish halqasi,
    # `/api/push-kalit` javob berardi, `enableNotifications:true` ham
    # qo'yilgan edi. Hammasi "tayyor" ko'rinardi.
    #
    # Lekin `push.js` HECH QAYSI sahifaga ulanmagandi va `OBER_PUSH`
    # hech qayerdan chaqirilmasdi. Ya'ni hech kim obuna bo'lmasdi:
    # `push_obunalar` jadvali abadiy bo'sh qolardi va bildirishnoma
    # hech qachon kelmasdi. Xato xabari ham chiqmasdi.
    #
    # Saboq: "komponent bor" != "zanjir ulangan". Oxirgi bo'g'in —
    # foydalanuvchi tomonidagi chaqiruv — eng oson unutiladigani.
    jami += 1
    chat = (WEB / "takliflar.html").read_text(encoding="utf-8")
    yetishmaydi = []
    if 'src="/push.js"' not in chat:
        yetishmaydi.append("push.js ulanmagan")
    if "OBER_PUSH" not in chat:
        yetishmaydi.append("OBER_PUSH chaqirilmagan")
    if "pushTikla" not in chat:
        yetishmaydi.append("obuna tiklanmaydi")
    if yetishmaydi:
        xato += 1
        print("  XATO %-16s push zanjiri uzilgan: %s — hech kim obuna "
              "bo'lmaydi, bildirishnoma kelmaydi"
              % ("takliflar.html", ", ".join(yetishmaydi)))

    # 4h. NAVIGATSIYA IKKI QAVAT BO'LMASIN.
    #
    # 2026-08-12, Azizning ko'zi bilan topilgan: 798px kengligida
    # tepada "Chat" va "Sotish", pastda esa tab barda yana "Chat" —
    # ikkita navigatsiya bir vaqtda.
    #
    # Sabab: topbar havolalari `max-width:600px` da yashirinardi,
    # tab bar esa `min-width:901px` da yo'qolardi. 601-900px oralig'i
    # ikkalasiga ham tegishli emas edi. Kodda "ikkalasi bitta chegara"
    # deb yozilgan edi — yozilgan, lekin tekshirilmagan.
    #
    # Qoida: tab barni yashiradigan `min-width:N` va topbar
    # havolalarini yashiradigan `max-width:M` uchun M = N - 1.
    # Aks holda oraliqda ikkalasi ko'rinadi (yoki ikkalasi yo'qoladi).
    jami += 1
    tb = (WEB / "tabbar.js").read_text(encoding="utf-8")
    # `[^}]*` EMAS: media blok ichida boshqa qoidalar bor, ular `}` bilan
    # tugaydi va sinf to'plami ularni kesib o'tolmaydi. Ochko'z bo'lmagan
    # `.*?` kerak — eng yaqin `.ober-tabbar{display:none}` gacha boradi.
    kiz = re.search(r"min-width:(\d+)px\).*?\.ober-tabbar\{display:none\}", tb, re.S)
    yash = re.search(r"max-width:(\d+)px\)\{\s*\"?,?\s*\"?\s*"
                     r"\.ober-tabbar-joy \.messages-link", tb, re.S)
    if not kiz or not yash:
        xato += 1
        print("  XATO %-16s tab bar / topbar havola chegaralari topilmadi "
              "— naqsh o'zgargan bo'lsa sinovni yangilang" % "tabbar.js")
    elif int(yash.group(1)) != int(kiz.group(1)) - 1:
        xato += 1
        print("  XATO %-16s navigatsiya oralig'i: havolalar %spx da "
              "yashirinadi, tab bar %spx da yo'qoladi — %s-%spx oralig'ida "
              "IKKALASI ko'rinadi" % ("tabbar.js", yash.group(1), kiz.group(1),
                                      int(yash.group(1)) + 1,
                                      int(kiz.group(1)) - 1))

    # 4f. SHISHA QIYMATI XOM YOZILMASIN.
    #
    # 2026-08-12 audit: `backdrop-filter` 78 marta, ichida 5 xil blur
    # va 4 xil saturate — ikkitasi turli birlikda (`1.05` va `140%`).
    # Kategoriyalar tepa paneli 105%, takliflar niki 140% edi.
    # Endi uchta token: --shisha-yupqa / --shisha / --shisha-quyuq.
    #
    # Istisno: modal ostidagi `blur(2px)` parda — u shisha SIRT emas,
    # orqadagi sahifani xiralashtirish. Boshqa maqsad, boshqa qiymat.
    for nom in ("index.html", "takliflar.html", "sotuvchi.html",
                "kategoriyalar.html", "elon.html", "tabbar.js"):
        jami += 1
        matn = (WEB / nom).read_text(encoding="utf-8")
        xom = [q for q in re.findall(r"backdrop-filter:\s*([^;\"']+)", matn)
               if "var(--shisha" not in q and "blur(2px)" not in q]
        if xom:
            xato += 1
            print("  XATO %-16s xom shisha qiymati: %s — `var(--shisha)`, "
                  "`var(--shisha-yupqa)` yoki `var(--shisha-quyuq)` "
                  "ishlating" % (nom, ", ".join(sorted(set(xom))[:3])))

    # 4g. HAR SHISHAGA `-webkit-` JUFTI BO'LSIN.
    #
    # iOS Safari `backdrop-filter` ni prefikssiz TUSHUNMAYDI. Prefiks
    # yo'q bo'lsa telefonda shisha umuman ishlamaydi va element o'z
    # yarim shaffof foni bilan qoladi.
    #
    # 2026-08-12 da uchta joyda yo'q edi, ulardan biri — natija
    # sahifasidagi qidiruv qutisi: to'q hero ustida `rgba(255,255,255,.10)`,
    # ya'ni iPhone'da deyarli ko'rinmas. Saytdagi eng muhim element.
    for nom in ("index.html", "takliflar.html", "sotuvchi.html",
                "kategoriyalar.html", "elon.html", "tabbar.js"):
        jami += 1
        matn = (WEB / nom).read_text(encoding="utf-8")
        oddiy = len(re.findall(r"(?<!-webkit-)backdrop-filter:", matn))
        webkit = len(re.findall(r"-webkit-backdrop-filter:", matn))
        if oddiy != webkit:
            xato += 1
            print("  XATO %-16s backdrop-filter %d ta, -webkit- jufti %d ta "
                  "— iOS Safari'da shisha ishlamaydi" % (nom, oddiy, webkit))

    # 4d. JONLI LENTA QATORIGA O'RAM QO'YILMASIN.
    #
    # 2026-08-12, o'lchov: qator balandligi 1394px, har karta 144x1384 —
    # butun lenta ulkan bo'sh ustunlarga aylangan edi. Jonli saytda.
    #
    # Sabab: ikkinchi nusxa `<span aria-hidden>` ichiga o'ralgan edi.
    # O'ram `.jonli-yol` ning yagona flex bolasi bo'ldi, ichidagi
    # `<a>` lar flex element bo'lmay qoldi (`flex:0 0 170px` o'lik),
    # vertikal taxlandi, o'ram 1384px ga cho'zildi va `stretch` qolgan
    # kartalarni ham tortdi.
    #
    # Qoida: `.jonli-yol` ning bolasi FAQAT karta bo'ladi. Nusxaga
    # belgi kerak bo'lsa — `<a>` ning o'ziga, qo'shimcha qutisiz.
    jami += 1
    if re.search(r"jonli-yol[\"'][^`]{0,80}<span", bosh):
        xato += 1
        print("  XATO %-16s .jonli-yol ichida <span> o'ram — kartalar "
              "flex bo'lmay qoladi va vertikal taxlanadi "
              "(2026-08-12 saboqi)" % "index.html")

    # 4e. LENTA KARTALARI TENG BALANDLIKDA TURSIN.
    #
    # O'lchov: 1 qatorli sarlavha 198px, 2 qatorli 219px. `flex-start`
    # da tublari 21px notekis — gorizontal lentada darrov ko'rinadi.
    # Shuning uchun `stretch` ATAYLAB yozilgan (sukut qiymati bo'lsa
    # ham) — kimdir uni "keraksiz" deb o'chirmasin.
    jami += 1
    if not re.search(r"\.jonli-yol\s*\{[^}]*align-items\s*:\s*stretch", bosh, re.S):
        xato += 1
        print("  XATO %-16s .jonli-yol da `align-items:stretch` yo'q — "
              "karta tublari 21px notekis bo'ladi" % "index.html")

    # 5. SOTISH OQIMI KONTEKSTNI YO'QOTMASIN.
    #
    # 2026-08-11: ro'yxatdan o'tish tugashi bilan Telegram alohida
    # "2-qadam" bo'lib `#asosiy`ni to'liq almashtirardi. Foydalanuvchi
    # o'zini boshqa sahifaga o'tib ketgandek his qilardi. Telegram endi
    # kabinet ichidagi ixtiyoriy karta; e'lon formasi esa Sotish ->
    # E'lonlarim tablari ostida qoladi.
    sotuvchi = (WEB / "sotuvchi.html").read_text(encoding="utf-8")
    sotish_tekshiruvlari = [
        ("telegramQadami" not in sotuvchi,
         "Telegram alohida majburiy sahifaga aylanmasin"),
        (sotuvchi.count("setTimeout(sotishIshiniOch") >= 2,
         "kirish va ro'yxatdan o'tish niyat qilingan Sotish ishiga qaytsin"),
        ('${tabPaneli("elonlar")}' in sotuvchi,
         "e'lon formasi E'lonlarim tabi ostida qolsin"),
        ("Xaridor so‘rovlari" in sotuvchi and
         'aria-label="Sotish bo‘limlari"' in sotuvchi,
         "sotuvchi ichki tablari vazifani aniq aytsin"),
        ('<span class="cabinet-label">Sotish</span>' in sotuvchi and
         '<a class="buyer-link" href="/">Qidirish</a>' in sotuvchi,
         "desktop navigatsiya Qidirish va Sotish nomlarini ishlatsin"),
        (re.search(r"@media\s*\(max-width:560px\).*?\.forma-qator\s*\{\s*grid-template-columns\s*:\s*1fr",
                   sotuvchi, re.S) is not None,
         "telefon e'lon formasida narx va joy siqilib qolmasin"),
        ('p.get("yangi") === "1"' in sotuvchi and
         'sotishManziliniBelgila("elon"' in sotuvchi,
         "to'g'ridan-to'g'ri + E'lon manzili formani ochib, kontekstni saqlasin"),
        ('<div id="tg-quti"></div>' in sotuvchi and
         "telegramQadami" not in sotuvchi,
         "Telegram kabinet ichida qolsin, alohida majburiy qadam bo'lmasin"),
        ('onclick="telegramSinov(this)"' in sotuvchi and
         "Bildirishnomani sinash" in sotuvchi,
         "ulangan sotuvchi Telegram bildirishnomasini o'zi sinay olsin"),
        ('/api/sotuvchi/telegram/sinov' in sotuvchi and
         'body:JSON.stringify({token:MEN})' in sotuvchi,
         "Telegram testi sotuvchi sessiyasi bilan yuborilsin"),
    ]
    for shart, izoh in sotish_tekshiruvlari:
        jami += 1
        if not shart:
            xato += 1
            print("  XATO %-16s %s" % ("sotuvchi.html", izoh))

    # 6. UMUMIY NAVIGATSIYA: + E'LON — TEZKOR AMAL, SOTISH — KABINET.
    # Xaridor bo'lib qidirayotgan foydalanuvchi sotuvchi rejimiga "o'tib"
    # qolmasligi kerak. Besh tab har ikki ekranda bir xil vazifani aytadi.
    tabbar = (WEB / "tabbar.js").read_text(encoding="utf-8")
    tab_tekshiruvlari = [
        ('href="/sotuvchi?yangi=1" data-tab="elon"' in tabbar,
         "mobil markazda + E'lon formasi uchun alohida tezkor amal bo'lsin"),
        ('{yol: "/sotuvchi?yangi=1", nom: "+ E’lon"' in tabbar,
         "desktopda ham + E'lon tezkor amali bo'lsin"),
        # 2026-08-11 (Aziz): sotuvchi tomoniga BITTA eshik.
        # Ilgari "+ E'lon" va "Sotish" ikkalasi ham `/sotuvchi` ga
        # borardi va ro'yxatdan o'tmagan odam uchun ekran harfma-harf
        # bir xil chiqardi — ya'ni har bir yangi kelgan odam uchun
        # navigatsiyaning ikki tugmasi bitta ish qilardi.
        ('data-tab="sotish"' not in tabbar and
         'nom: "Sotish"' not in tabbar,
         "sotuvchi tomoniga ikkinchi takroriy eshik qo'shilmasin"),
        ("grid-template-columns:1fr 1fr 1.12fr 1fr" in tabbar and
         'querySelectorAll(".ober-tab").length !== 4' in tabbar,
         "tab bar to'rt vazifadan iborat bo'lsin va soni himoyalansin"),
        ('window.OBER_TAB_FAOL = faolQil' in tabbar,
         "kabinet ichki bo'limlari faol tabni yangilay olsin"),
        ('qidiruv.get("rol") === "sotuvchi"' in tabbar and
         'window.OBER_BILDIRISH_YANGILA = yangila' in tabbar,
         "bir qurilmadagi buyer/seller unread joriy rol bo'yicha yangilansin"),
    ]
    for shart, izoh in tab_tekshiruvlari:
        jami += 1
        if not shart:
            xato += 1
            print("  XATO %-16s %s" % ("tabbar.js", izoh))

    # 7. LOCAL FONT ASSETS AND CHAT HEADING REGRESSIONS.
    # onest.css local URLlarni ko'rsatib, fayllar bo'lmasa har sahifa
    # ikki marta 404 beradi va qurilmaga qarab tizim shriftiga tushadi.
    for font in (
        "onest-latin.woff2",
        "onest-latin-ext.woff2",
        "onest-cyrillic.woff2",
        "onest-cyrillic-ext.woff2",
    ):
        jami += 1
        font_path = WEB / "shrift" / font
        if not font_path.exists() or font_path.stat().st_size < 1000:
            xato += 1
            print("  XATO %-16s local Onest font fayli yo'q yoki bo'sh" % font)

    chat = (WEB / "takliflar.html").read_text(encoding="utf-8")
    jami += 1
    if ".page-title{display:none}" not in chat or \
            ".top-tools{grid-column:3;" not in chat:
        xato += 1
        print("  XATO %-16s tepa panel va kontekstda Chat sarlavhasi takrorlanadi" %
              "takliflar.html")

    # Jonli lenta ixtiyoriy: yetarli rasmli e'lon bo'lmasa jim yashirinadi.
    # Bu expected empty state console.error bo'lib E2E auditni bulg'amasin.
    jami += 1
    if 'throw new Error("Jonli e\'lonlar yetarli emas")' in bosh:
        xato += 1
        print("  XATO %-16s expected jonli empty state console error beradi" %
              "index.html")

    # 8. 2026-08-13 JONLI MOBIL AUDIT REGRESSIYALARI.
    # Natija bosh sahifadan quyuq rejimga sakramasin, qidiruv ikki qatorga
    # bo'linmasin va suzuvchi reverse-market CTA kartani yopmasin.
    natija_tekshiruvlari = [
        ("NATIJA SAHIFASI QUYUQ" not in bosh and
         "--bg:#f5f7fb" in bosh and
         "NATIJA SAHIFASI — YAGONA OCH TIZIM" in bosh,
         "natija sahifasi bosh sahifa bilan yagona och rang tizimida qolsin"),
        (".search-panel{flex-wrap:nowrap;gap:6px}" in bosh and
         ".search-panel::after{display:none}" in bosh,
         "390px qidiruv kamera va Topish bilan bitta qatorda qolsin"),
        (".tez-sora{display:none!important}" in bosh and
         'suzuvchi = document.createElement("div")' not in bosh,
         "suzuvchi Sotuvchilardan so‘rash CTA kartalarni yopmasin"),
        ("kartalar.splice(" not in bosh and
         '${soraChiziq()}' in bosh,
         "teskari bozor CTA ro‘yxat tepasida bir marta chiqsin"),
        ('id="tartib-select"' in bosh and
         'id="filtr-ochish"' in bosh and
         'id="filtr-qollash"' in bosh,
         "mobil saralash va narx filtri sig‘adigan boshqaruvga ega bo‘lsin"),
    ]
    for shart, izoh in natija_tekshiruvlari:
        jami += 1
        if not shart:
            xato += 1
            print("  XATO %-16s %s" % ("index.html", izoh))


    # 9. 2026-08-13 BRAND VA BIRINCHI EKRAN TARTIBI.
    brand_tekshiruvlari = [
        ('font-family:Georgia' not in bosh and 'Times New Roman' not in bosh,
         "bosh sahifada marketplacega yot serif shrift qolmasin"),
        ('Bir qidiruv.' in bosh and 'Butun bozor.' in bosh,
         "hero agregator vazifasini bir qarashda aytsin"),
        ('id="market-listings"' in bosh and 'id="market-rate"' in bosh and
         '.market-metric strong' in bosh and 'white-space:nowrap' in bosh,
         "e‘lon soni va kurs topbarda bir qatorda ko‘rinsin"),
        ('id="tez"' in bosh and 'class="search-panel"' in bosh and
         bosh.index('id="tez"') < bosh.index('class="search-panel"'),
         "jonli qidiruvlar qidiruv maydonidan oldin tursin"),
        ('id="jonli"' in bosh and 'id="qadamlar"' in bosh and
         bosh.index('id="jonli"') < bosh.index('id="qadamlar"') and
         "O'lchangan, va'da emas" not in bosh and
         'Ishonch <em>dalildan</em>' not in bosh,
         "ikki qatorli real e‘lonlar rasmiy statistika blokidan ustun tursin"),
    ]
    for shart, izoh in brand_tekshiruvlari:
        jami += 1
        if not shart:
            xato += 1
            print("  XATO %-16s %s" % ("index.html", izoh))

    # 10. DIZAYN TIZIMI: XOM QIYMAT YOZILMASIN (2026-08-16).
    #
    # `OBER-DIZAYN-QOIDALARI.md`: burchak radiusi faqat
    # `--r-kichik/orta/katta/pill/belgi` orqali beriladi. Qoida bor
    # edi, lekin uni HECH KIM tekshirmasdi — shuning uchun bugun
    # uchta xom qiymat topildi (index.html'da 10px va 4px, privacy'da
    # 6px). Ular tizim qiymatiga yaqin, lekin teng emas: ya'ni ko'z
    # ilg'amaydigan nomutanosiblik sekin to'planardi.
    #
    # Endi qoida o'zi o'zini qo'riqlaydi. Ruxsat etilgan istisnolar:
    #   `border-radius:0`      — burchakni ataylab o'chirish
    #   `border-radius:50%`    — doira (avatar, nuqta)
    #   `border-radius:999px`  — tabletka (tokeni ham bor, lekin
    #                            eski joylarda xom qolgan)
    xom_radius = re.compile(r"border-radius:\s*(?![0%]|50%|999px)[0-9.]+(px|rem|em)")
    for yol in sorted(WEB.glob("*.html")) + [WEB / "ober-ui.css"]:
        if not yol.exists():
            continue
        jami += 1
        matn = yol.read_text(encoding="utf-8")
        topilgan = [
            "%d-qator" % qator(matn, m.start())
            for m in xom_radius.finditer(matn)
        ]
        if topilgan:
            xato += 1
            print("  XATO %-16s tizimdan tashqari radius: %s"
                  % (yol.name, ", ".join(topilgan[:4])))

    # 11. BOSH SAHIFA CHAP CHEKKASI BIR CHIZIQDA (2026-08-16).
    #
    # 1440 px ekranda o'lchandi:
    #   sarlavha / izoh / tugma / raqamlar -> chap chekka 203 px
    #   qidiruv maydoni va chiplar         -> chap chekka 453 px
    #
    # Sabab: `.search-panel` va `.samples` da `margin-inline:auto`
    # qolgan edi — ular `max-width` bilan cheklangani uchun 1180 px
    # konteynerda markazga tushardi. Ya'ni sahifadagi ENG MUHIM
    # element qolganidan 250 px o'ngda turardi.
    #
    # Telefonda sezilmasdi (u yerda en 100%), shuning uchun uzoq
    # payqalmagan. Aynan shunday xatolar faqat o'lchov bilan
    # topiladi — ko'z 250 px siljishni "shunchaki dizayn" deb
    # qabul qilib yuboradi.
    tekislash = re.compile(
        r"\.(search-panel|samples)\{[^{}]*margin-inline:\s*auto")
    jami += 1
    # IZOHLARNI OLIB TASHLAYMIZ. Birinchi urinishda tashlamagandim va
    # sinov o'z izohimdagi "margin-inline:auto" so'zini xato deb
    # ko'rsatdi — ya'ni sinov KODNI emas, MATNNI o'qiyotgan edi.
    # Izoh o'rniga BIR XIL UZUNLIKDAGI bo'shliq qo'yamiz — shunda
    # qator raqamlari surilmaydi va xato xabari to'g'ri joyni
    # ko'rsatadi.
    bosh_matn = re.sub(
        r"/\*.*?\*/",
        lambda m: re.sub(r"[^\n]", " ", m.group()),
        (WEB / "index.html").read_text(encoding="utf-8"), flags=re.S)
    yomon = [
        "%d-qator" % qator(bosh_matn, m.start())
        for m in tekislash.finditer(bosh_matn)
    ]
    if yomon:
        xato += 1
        print("  XATO %-16s qidiruv bloki markazga tushgan (chap "
              "chekka sarlavhadan farq qiladi): %s"
              % ("index.html", ", ".join(yomon)))

    # 12. YORUG' FONDA OQ MATN BO'LMASIN (2026-08-16).
    #
    # Bugun jonli saytda o'lchandi: natija sahifasidagi saralash
    # tugmalari ("Avval arzoni", "Avval yangisi", "Avval yaqini")
    # matn rangi #e8eef8 — deyarli oq — va foni ham deyarli oq edi.
    # Kontrast ~1.1:1. WCAG AA eng kami 4.5:1. Ya'ni tugmalar
    # BUTUNLAY o'qilmasdi.
    #
    # Sabab: o'sha qoida natija sahifasi TO'Q KO'K bo'lgan paytda
    # yozilgan. Fon yorug'ga o'zgartirilganda qoida qolib ketdi.
    # Bu men qilgan xato va uni ko'z bilan ham payqamagandim —
    # faqat `getComputedStyle` bilan o'lchaganda chiqdi.
    #
    # Tekshiruv: `is-results` uchun yozilgan qoidalarda matn rangi
    # oqqa yaqin (#dde... dan yorug') bo'lmasin. Fon endi yorug'.
    # `(?<![-a-z])` MUHIM: busiz qolip `background-color:#eef2f7` ni
    # ham matn rangi deb o'qidi va toza kodda yolg'on xato berdi.
    # Faqat `color:` ning o'zi kerak — `border-color`, `background-
    # color`, `outline-color` emas.
    oq_matn = re.compile(
        r"body\.is-results[^{}]*\{[^{}]*(?<![-a-z])color:\s*"
        r"(#(?:f[0-9a-f]|e[89a-f])[0-9a-f]{4}\b|rgba?\(\s*2[3-5][0-9])",
        re.I)
    for yol in (WEB / "ober-ui.css", WEB / "index.html"):
        if not yol.exists():
            continue
        jami += 1
        matn = re.sub(r"/\*.*?\*/",
                      lambda m: re.sub(r"[^\n]", " ", m.group()),
                      yol.read_text(encoding="utf-8"), flags=re.S)
        yomon_rang = [
            "%d-qator" % qator(matn, m.start())
            for m in oq_matn.finditer(matn)
        ]
        if yomon_rang:
            xato += 1
            print("  XATO %-16s yorug' natija sahifasida oqqa yaqin "
                  "matn (o'qilmaydi): %s"
                  % (yol.name, ", ".join(yomon_rang[:4])))

    # Layout xossasini animatsiya qilish — kadr tushishining eng
    # keng tarqalgan sababi. `transform`/`opacity` GPU'da, qolgani
    # har kadrda qayta hisoblanadi.
    layout_animatsiya = re.compile(
        r"transition:[^;{}]*?\b(max-height|padding|margin|top|left|"
        r"right|bottom)\b[^;{}]*")
    for yol in sorted(WEB.glob("*.html")) + [WEB / "ober-ui.css"]:
        if not yol.exists():
            continue
        jami += 1
        matn = yol.read_text(encoding="utf-8")
        topilgan = [
            "%d-qator" % qator(matn, m.start())
            for m in layout_animatsiya.finditer(matn)
        ]
        if topilgan:
            xato += 1
            print("  XATO %-16s layout xossasi animatsiyada: %s"
                  % (yol.name, ", ".join(topilgan[:4])))

    for nom, eng_kam in (("logo-ober-20260813.png", 5000), ("icon.png", 5000)):
        jami += 1
        aktiv = WEB / "brend" / nom
        if not aktiv.exists() or aktiv.stat().st_size < eng_kam:
            xato += 1
            print("  XATO %-16s yangi brend PNG aktiv emas" % nom)
    print("\n  %d to'g'ri · %d xato  (%d tekshiruv)"
          % (jami - xato, xato, jami))
    return 1 if xato else 0


if __name__ == "__main__":
    sys.exit(main())
