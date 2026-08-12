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
        ("grid-template-columns:1fr 1fr 1.2fr 1fr" in tabbar and
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

    print("\n  %d to'g'ri · %d xato  (%d tekshiruv)"
          % (jami - xato, xato, jami))
    return 1 if xato else 0


if __name__ == "__main__":
    sys.exit(main())
