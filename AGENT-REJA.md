# OBER MCP SERVERI — bajarish rejasi

Yozilgan: 2026-08-16. Keyingi seans shu fayldan boshlaydi.

## Nega

2026 ning asosiy o'zgarishi — agentli savdo. OpenAI+Stripe **ACP**
(sentyabr 2025, Etsy va 1 mln+ Shopify sotuvchisida ishlayapti),
Google **UCP** (yanvar 2026, Search AI Mode va Gemini). IBM: 
iste'molchilarning 45%i xarid yo'lining bir qismida AI ishlatadi.

Bugun kimdir ChatGPT'dan "Toshkentdan 3 mln gacha divan top" desa —
javob yo'q. OLX'da agent interfeysi yo'q, Uzum CAPTCHA qo'yadi.
**O'zbekiston bozori AI uchun ko'r nuqta.**

OBERda esa tayyor: 523 000 e'lon, strukturalangan qidiruv,
kategoriya aniqlash, sotuvchiga yo'naltirish.

## Asosiy g'oya — bu yerda hech kimda yo'q narsa bor

ACP ham, UCP ham faqat **mavjud** tovarni sotadi. OBERda boshqasi:

> Agent tovar topmasa, OBER uni sotuvchilardan **so'ray oladi**.

Agent so'raydi -> indeksda yo'q -> talab mos sotuvchilarga boradi ->
sotuvchi narx va rasm bilan javob beradi -> agent egasiga aytadi.

Agentdan boshlanib jonli sotuvchiga boradigan so'rov zanjiri —
qidirib topilmadi. Bu tekshiriladigan da'vo, taxmin emas.

## Qadamlar — shu tartibda

### 1-qadam: `qidir` vositasi (eng arzoni, birinchi)  ✅ BAJARILDI

`app/mcp_server.py` — stdio MCP serveri, **standart kutubxona**.
`app/qidiruv.py:qidir()` ni chaqiradi, HTTP ham kerak emas.

Kirish: `sorov` (matn), ixtiyoriy `viloyat`, `narx_max`, `soni`.
Chiqish: nom, narx (so'm), viloyat, kategoriya, manba havolasi.

DIQQAT — birinchi seansda o'lchangan tuzoq: `qidir()` `dict`
qaytaradi, ichida `natijalar` kaliti bor (`elonlar` emas).

Sinov: `app/mcp_sinov.py` — protokol javoblari va bo'sh natija
holati. `mcp-builder` ko'nikmasi bor, undan foydalanilsin.

### 2-qadam: `sorov_yubor` vositasi — NISHA SHU  ✅ BAJARILDI (2026-08-17)

Agent talab qo'yadi. `baza` da mexanizm tayyor (`sorovlar`,
`_mos_sotuvchilar`, `SOROV_MUDDATI = 24h`).

MUHIM CHEGARA: agent **so'rov qo'yadi**, lekin javobni **odam
o'qiydi**. Agent sotuvchi bilan avtomatik savdolashmasin va
kelishuvni yakunlamasin — OBER to'lov qilmaydi, va odam nomidan
majburiyat olish noto'g'ri. Agent faqat: so'radi, javob keldi, xabar
berdi.

Aloqa uchun `aloqa` maydoni kerak — agent uni **foydalanuvchidan**
olsin, o'zi to'qimasin.

#### Tayyor funksiyalar — qidirib o'tirmang (2026-08-16 da topildi)

    baza.sorov_yoz(matn, tuman, aloqa, ...)   3368-qator  — talab yozadi
    baza._mos_sotuvchilar(c, sorov)           1496-qator  — kimga borishi
    baza.sorov_tokeni(sorov_id)                792-qator  — kuzatish kaliti
    baza.sorov_ochiqmi(sorov_id)              2738-qator  — hali ochiqmi
    baza.sorov_javoblari(sorov_id)            2984-qator  — kelgan javoblar
    baza.sorov_takliflari(sorov_id)           3022-qator  — jamlangan ko'rinish

Server yo'li: `/api/sorov` (server.py 1138-qator).
Tezlik cheklovi allaqachon bor: **soatiga 60 ta** (server.py 89-qator)
— agent uchun yetarli, lekin bir agent butun bazani spamlay olmasin
degan qoida shu yerda tekshiriladi.

`_mos_sotuvchilar` so'rovchining o'zini chetlab o'tadi (telefonning
oxirgi 9 raqami bo'yicha) — Aziz o'ziga o'zi xabar yuborgani uchun
2026-08-15 da qo'shilgan edi.

### BO'SH NATIJA MUAMMOSI — 2-qadam bilan BIR ISH  ✅ YOPILDI (2026-08-17)

2026-08-16 da MCP sinovida o'lchandi: `qidir("zzqqxx yoq narsa")`
-> **10 ta begona e'lon** qaytardi. Sabab ma'lum: indeksda hech
narsa mos kelmasa `fts_erkin` "kamida bitta so'z" bosqichiga
tushadi (`baza.py` dagi izohga qarang).

Odam buni ko'rib "bu men so'raganim emas" deydi va o'zi
filtrlaydi. **Agent esa buni haqiqiy javob deb foydalanuvchiga
uzatadi.** Ya'ni agentli savdo bu xatoni bir necha barobar
jiddiylashtiradi — bu endi bezovtalik emas, yolg'on ma'lumot.

Shuning uchun 2-qadam ikki qismdan iborat:

1. **Ishonch chegarasi.** `qidir` natijasi ishonchsiz bo'lsa (OR
   bosqichidan kelgan, aniq so'z mosligi yo'q), uni "topildi" deb
   qaytarmaslik. `qidiruv.py` da ballash bor — chegara o'sha
   yerdan olinadi, yangi mantiq yozilmaydi.
2. **O'rniga taklif.** Bo'sh natijada agent `sorov_yubor` ni
   chaqira olsin va javob shunday bo'lsin:

       "Bunday tovar indeksda yo'q. So'rovingiz 4 ta mos
        sotuvchiga yuborildi, javob kelsa aytaman."

Bu OBERning butun g'oyasi — faqat endi agent uchun.

#### Nima qilindi (2026-08-17)

`app/mcp_server.py` v0.2.0 — ikki vosita, yozadigani bitta.
`app/mcp_sinov.py` — 62 ta tekshiruv, o'z vaqtinchalik bazasida
(jonli `data/ober.db` ga bir marta ham yozmaydi, yakunda mtime va
hajm solishtiriladi).

ISHONCH CHEGARASI — `qidiruv.py` O'ZGARMADI. Chegara MCP qatlamida
turadi, ya'ni sayt bir xil ishlaydi va 523 000 e'lonli jonli
qidiruvga regressiya xavfi yo'q. Yangi ballash yozilmadi —
`qidiruv._yakunla` qo'ygan `_ishonchli` bayrog'i va yuqoridagi
`sozlar` ro'yxati o'qiladi. Ikki shart:

  1. `sozlar` bo'sh bo'lmasin;
  2. kamida bitta natijada `_ishonchli=True` bo'lsin.

1-shart nega kerak — o'lchandi: `qidir("zzz vvv yyy")` 1404 natija
qaytaradi, chunki "vvv" lug'atda `volkswagen` ga bog'langan. Model
yo'lida `_ishonchli` standart qiymati True, ya'ni u YOLG'ONDAN
ishonchli ko'rinadi. `sozlar` bo'shligi buni ushlaydi.

O'LCHOV (jonli indeks, 500 000+ e'lon):

    12 ta yolg'on so'rov  -> 12 tasi rad etildi, 0 ta xato qabul
    24 ta haqiqiy so'rov  -> 21 tasi qabul qilindi

Rad etilgan 3 ta "haqiqiy" so'rov qo'lda tekshirildi, uchalasi ham
TO'G'RI rad etilgan va uchalasi ham `sorov_yubor` uchun tug'ilgan:

    "usta santexnik"              indeksda santexnik yo'q
    "divan charm"                 divan bor, charm divan yo'q
    "2 xonali kvartira chilonzor" yagona natija 4 xonali

Ya'ni chegara natijani kesmaydi — uni OBERning nishasiga buradi.

JAVOB SHAKLI. `holat` to'rt qiymat oladi: `topildi`,
`aniq_moslik_yoq`, `narx_boyicha_yoq`, `topilmadi`. Oxirgi uchtasida
`elonlar` ATAYLAB bo'sh va `keyingi_qadam: sorov_yubor` turadi.
`soralgani_emas` — yaqin e'lonlarning faqat NOMI, narxsiz va
HAVOLASIZ: havolasiz e'lonni taklif sifatida uzatib bo'lmaydi,
lekin agent aniq gapira oladi ("OBER'da divan bor, charm divan
yo'q"). Yonida `ogohlantirish` maydoni.

NARX YOLG'ON GAPIRMAYDI. `narx_max` berilib natija bo'sh chiqsa,
qidiruv narxsiz qayta yuriladi va agentga HAQIQIY eng arzon narx
aytiladi ("«divan» bor, lekin 1000 so'mgacha emas — eng arzoni
54 000 so'm"). Aks holda "bunday tovar yo'q" degan javob yolg'on
bo'lardi.

`sorov_yubor` — chegaralar:

  * `aloqa` MAJBURIY va tekshiriladi (9+ raqam, bir xil raqamlar
    rad etiladi). Xato javobida agentga aniq aytiladi: raqamni
    FOYDALANUVCHIDAN so'ra, o'zing to'qima.
  * Tezlik: soatiga 10, daqiqasiga 3. Sayt tomonidagi 60/soat
    chegara HTTP qatlamida (`server.py`) va MCP `baza` ni
    to'g'ridan chaqirgani uchun u yerda ISHLAMAYDI — shuning uchun
    qaytadan qo'yildi, qattiqroq qilib.
  * Nusxa: aynan bir xil `matn`+`aloqa` 1 soat ichida qayta
    yozilmaydi (agent qayta urinsa sotuvchiga ikki marta xabar
    bormasin). Nusxa tekshiruvi tezlik chegarasidan OLDIN —
    qayta urinish chegarani yemasin.
  * Javobda sotuvchi telefoni yo'q. Xaridorga
    `https://ober.uz/takliflar?kalit=<token>` beriladi.
  * Vosita matnida ham, javob izohida ham yozilgan: agent
    savdolashmaydi, narx kelishmaydi, buyurtmani yakunlamaydi.

SINOVDA MUTATSIYA BILAN TEKSHIRILDI: ishonch chegarasi kodda
o'chirilsa 62 tadan 12 ta sinov qulaydi. Ya'ni sinov haqiqatan shu
xatti-harakatni qo'riqlaydi, shunchaki yashil bo'lib turmaydi.

`sorov_yubor` `kalit` qaytaradi — `javoblar` shu bilan ishlaydi.
Raqamli `sorov_id` emas: u ketma-ket va taxmin qilinadi.

### 3-qadam: `javoblar` vositasi  ✅ BAJARILDI (2026-08-17)

So'rov holati: nechta sotuvchiga bordi, nechtasi javob berdi,
narxlar qanday.

#### Nima qilindi (2026-08-17)

Zanjir yopildi: agent so'radi -> sotuvchi javob berdi -> agent
odamga aytdi. Endi `sorov_yubor` javobi "javob keladi" deb ayta
oladi, chunki uni tekshiradigan vosita bor.

KIRISH FAQAT KALIT BILAN. Raqamli `sorov_id` qabul qilinmaydi —
u ketma-ket, ya'ni taxmin qilib begona odamning takliflarini
ochib bo'lardi. Sayt ham shunday (`server._xaridor_ident` faqat
tokenni yechadi). Agent ko'pincha butun havolani qaytaradi,
shuning uchun `kalit=` undan ajratib olinadi — behuda ishqalanish
bo'lmasin.

`bor` va `oxshash` AGENT TILIGA O'GIRILADI (`aynan` / `oxshash`)
va vosita tavsifida ularni aralashtirmaslik alohida yozilgan.
Aks holda yolg'on ma'lumot muammosi qaytadi — faqat endi
indeksdan emas, jonli sotuvchidan kelgani.

MAYDONLAR ATAYLAB TANLAB OLINADI, `**t` yozilmaydi.
`baza.sorov_takliflari` ichki maydonlarni ham qaytaradi
(`sotuvchi_id`, `suhbat_id`, `javob_id`) — kelajakda ustun
qo'shilsa u o'zi javobga sizib chiqmasin. Telefon raqami ikkala
tomonda ham yo'q (sinov buni matn ichidan qidirib tekshiradi).

TO'LQIN — FAQAT O'Z SO'ROVI. Sayt xaridor sahifasi umumiy
`baza.ochiq_sorovlarni_yurit()` ni chaqiradi (BARCHA ochiq
so'rovlarga tegadi). MCP'da ataylab `baza.tolqin_yubor(sid)` —
o'qish vositasi begona talablarga ta'sir qilmasligi kerak.
Bu YANGI talab yaratmaydi: tarqatishga ruxsat `sorov_yubor` da
berilgan, bu esa o'sha tarqatishning jadval bo'yicha keyingi
qadami (`TOLQIN_JADVALI` va `CHEGARA_ODATIY` bilan chegaralangan,
ya'ni sikl bilan ham oshirib bo'lmaydi).

Sotuvchiga JAVOB YOZADIGAN vosita yo'q va qo'shilmaydi —
sinovning 11-bo'limi buni qo'riqlaydi. Tanlash va savdolashish
odamning ishi.

MUTATSIYA SINOVI — 9 ta buzilish, 9 tasi ham ushlandi:

    ishonch chegarasi o'chirilsa      12 sinov quladi
    nusxa qo'riqchisi o'chirilsa       3
    aloqa majburiyligi o'chirilsa      3
    tezlik chegarasi o'chirilsa        2
    umumiy to'lqinga o'tilsa           2
    narx qayta yurishi o'chirilsa      2
    raqamli ID ga ruxsat berilsa       1
    ichki maydonlar ochilsa (`**t`)    1
    `bor`/`oxshash` o'girilmasa        1

Ikkitasi birinchi urinishda O'TIB KETGAN edi va sinov shu sabab
tuzatildi — sabab pastda, `memory/lessons.md` da.

### 4-qadam: strukturalangan feed (keyinroq)

`schema.org/Product` yoki UCP shakli — Google va boshqa agentlar
o'zi topadi. Bu SEO ishi, MCP dan alohida.

## Qoidalar — buzilmasin

- **Standart kutubxona.** MCP protokoli JSON-RPC over stdio,
  kutubxona shart emas.
- **Yozadigan vosita faqat bitta** (`sorov_yubor`) va u ham hech
  narsa o'chirmaydi, hech kimga pul o'tkazmaydi.
- **Tezlik cheklovi.** Bitta agent butun sotuvchi bazasini
  spamlamasin. `sorovlar` jadvalida allaqachon cheklov bor —
  tekshirilsin va kerak bo'lsa kuchaytirilsin.
- Sinovlar avval **mahalliy muhitda** (`app/sinov_muhiti.py`),
  jonli saytda emas.

## Boshlash

1, 2 va 3-qadam tugadi. Keyingi ish — 4-qadam
(strukturalangan feed) yoki MCP ni haqiqiy agentda sinash.

    python app/mcp_sinov.py            # 87 ta tekshiruv
    python app/sinov_muhiti.py --ishga # sayt uchun
