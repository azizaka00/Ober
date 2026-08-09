# OBER — CODEX UCHUN TOPSHIRIQ HUJJATI

Sana: 2026-07-31 · Yozgan: Claude · Davom ettiruvchi: Codex
Boss: Aziz. Muloqot tili — o'zbekcha. Kod izohlari ham o'zbekcha.

---

## 1. OBER nima

**Teskari bozor** (reverse marketplace) — O'zbekiston uchun.

Oddiy bozorda (OLX, Uzum) xaridor qidiradi va o'zi topadi. OBER'da:

1. Xaridor **nima kerakligini yozadi** ("kobalt fara")
2. Tizim yig'ilgan ochiq e'lonlardan darhol **kontekst** beradi:
   odatiy narx, oraliq, kimda bor
3. Ayni paytda so'rov **shu yo'nalishdagi sotuvchilarga tarqaladi**
4. Sotuvchi **bir tegishda** javob beradi: BOR / YO'Q / O'XSHASHI BOR + narx
5. Xaridor jonli javoblarni ko'radi va o'zi bog'lanadi

Asosiy g'oya: **indeks — kontekst, jonli javob — bugungi haqiqat.**
E'lon eski bo'lishi mumkin, sotuvchining javobi esa har doim rost.

Domen: ober.uz · Instagram: mavjud

---

## 1-A. OBER NIMA EMAS (buni chalkashtirmang)

Bu bo'lim 2026-07-31 da qo'shildi, chunki OBER uchta boshqa mahsulotga
o'xshab ketadi va har safar boshqasiga siljib ketish xavfi bor.

### OBER — OLX emas (agregator emas)

OLX'da odam **o'zi qidiradi va o'zi topadi**. Natija — 40% noto'g'ri
mashina, eski e'lonlar, "bormi yo'qmi" noma'lum.

OBER'da qidiruv **javobning boshi**, oxiri emas. Biz noto'g'ri modelni
kesamiz, odatiy narxni aytamiz va **sotuvchidan tasdiq olamiz**.

Agar biz shunchaki e'lonlarni chiroyliroq ko'rsatsak — biz OLX'ning
yomonroq nusxasimiz. Bizda 9 000 e'lon, ularda 46 000 faqat Toshkentda.
Bu jangda yutib bo'lmaydi va yutish shart emas.

### OBER — Profi.ru / Thumbtack emas (taklif so'rash emas)

U yerda: so'rov yozasan -> **kutasan** -> takliflar keladi.

OBER'da kutish — **yengiladigan muammo**, mahsulotning o'zi emas.
Xaridor "gentra fara" deb yozgan zahoti, hech kimni kutmasdan ko'radi:
143 natija, odatiy narx 450 000, eng arzoni 60 000, kimda bor edi.

So'rov qoldirish — bu **ustiga qo'shimcha**, asos emas. Indeks kontekst
beradi, jonli javob tasdiqlaydi.

Shuning uchun sotuvchi javobiga "tayyor bo'lish vaqti", "yetkazish",
"kafolat" kabi maydonlar qo'shilmaydi. Bu xizmat bozorining shakli.
Bizda savol bitta: **bormi va qancha.**

### OBER — AI suhbatdosh emas

"Menga fara kerak" deb yozib, chat oynasida gaplashadigan mahsulot emas.
Chat sekin, noaniq va har xabar pul turadi. Odam bozorga gaplashgani
emas, **javob olgani** keladi.

### Bir jumlada o'lchov

> Odam OBER'ga kelganda **3 soniyada javob**, **3 daqiqada tasdiq**
> olishi kerak.

Har qanday yangi funksiya shu ikki raqamni yaxshilaydimi yoki
yomonlashtiradimi — shundan baholanadi.

### Xaridor telefon raqami

Raqam so'rov qoldirilganda olinadi, lekin **darhol hamma sotuvchiga
ochilmaydi**. Faqat "BOR" deb javob bergan sotuvchiga ochiladi.
`baza.sotuvchi_sorovlari()` javobida `aloqa` maydoni bo'lmasligi kerak.

### Hozirgi qamrov
Faqat **avtoehtiyot qismlar** (OLX `avtozapchasti`), 13 viloyat.
Aziz qarori (2026-07-31): avval **chuqurlik** (shu bozorni to'ldirish),
keyin kenglik (yangi kategoriyalar). Sabab: teskari bozor faqat zichlik
bo'lganda ishlaydi — bitta yo'nalishda ko'p sotuvchi kerak.

---

## 2. Texnik cheklovlar (buzmang)

- **Faqat Python standart kutubxonasi.** `pip install` yo'q. urllib, re,
  sqlite3, json, http.server. Sabab: Azizning kompyuterida sandbox
  ishlamaydi (BIOS'da virtualizatsiya o'chiq, 8GB RAM).
- **Har ish `.bat` fayl orqali yuritiladi** — Aziz ularni bosadi.
- **Bir faylli frontend** — `web/index.html` va `web/sotuvchi.html`
  ichida CSS va JS ham bor. Build yo'q, npm yo'q.
- **Manbaga hurmat**: so'rovlar orasida kutish (`KUTISH = 2.5`),
  o'zimizni tanitish (`UA`), faqat ochiq ko'rinadigan ma'lumot.

---

## 3. Fayllar

```
ober/
  app/
    baza.py       SQLite: jadvallar, saqlash, migratsiya
    lugat.py      Mashina modellari + qism turlari lug'ati (ENG QIMMAT BOYLIK)
    joylar.py     O'zbekiston geografiyasi, ruscha -> o'zbekcha
    olx.py        OLX yig'uvchi
    olx_detal.py  E'lon sahifasi (ENDI DEYARLI KERAK EMAS — 5-bo'limga qarang)
    tahlil.py     E'lonlarni oldindan tahlil qilish (tezlik uchun)
    qidiruv.py    Qidiruv va saralash
    server.py     Mahalliy HTTP server, port 8800
  web/
    index.html    Xaridor sahifasi
    sotuvchi.html Sotuvchi kabineti
  docs/           01-manbalar, 02-qidiruv, 03-tuzilma
  data/ober.db    SQLite bazasi
  *.bat           Ishga tushirish fayllari
```

### Muhim `.bat` fayllar
- `KATTA-YIGISH.bat` — kod tekshiruvi -> 1 sahifalik sinov -> 25 sahifa
  yig'ish -> tahlil. Asosiy ish fayli.
- `KOR-BRAUZERDA.bat` — serverni ko'taradi, brauzer ochiladi
- `KOR.bat` — hisobot chiqaradi (`data/hisobot.txt`)
- `SINOV.bat`, `HALQA-SINOV.bat`, `TALAB.bat` — sinovlar

---

## 4. Baza tuzilishi

**`elonlar`** — yig'ilgan e'lonlar
`manba, tashqi_id, nom, narx_som, narx_asl, valyuta, kelishiladi, holat,
viloyat, shahar, tuman, sana, havola, rasm, telefon, biznes, qism_turi,
tavsif, sotuvchi_id, sotuvchi_nomi, tan_modellar, tan_qismlar, olindi`

- `tashqi_id` — OLX havolasidagi `-ID<kod>.html` dan
- `tan_modellar` / `tan_qismlar` — **oldindan hisoblangan** teglar.
  `NULL` bo'lsa qidiruv har safar qaytadan tahlil qiladi va sekinlashadi.
- Migratsiya `baza.init()` ichida: `PRAGMA table_info` + `ALTER TABLE`

**Boshqa jadvallar:** `narx_tarix`, `qidiruvlar` (har qidiruv yoziladi —
bu butun biznesning urug'i, talab ma'lumoti), `sorovlar`, `javoblar`,
`sotuvchilar`

---

## 5. ENG MUHIM TOPILMA — PRERENDERED_STATE

OLX ro'yxat sahifasining **xom HTML'i ichida** to'liq JSON holat bor:

```python
_HOLAT_RE = re.compile(r'PRERENDERED_STATE__\s*=\s*("(?:[^"\\]|\\.)*")')
holat = json.loads(json.loads(m.group(1)))
elonlar = holat["listing"]["listing"]["ads"]
```

Har e'londa: `title, description, url, photos, isBusiness, createdTime,
lastRefreshTime, price{regularPrice{value,currencyCode,negotiable}},
location{cityName,districtName,regionName}, params[{key,name,value}],
user{id,name,sellerType}, contact{name,phone}`

`params` ichida `key:"part_type"` -> `"Кузовные детали"` (qism turi!)
va `key:"state"` -> `"Б/у"` / `"Новый"`.

**O'lchandi (2-sahifa, 52 e'lon): rasm 51/52, shahar 52/52, tuman 38/52.**
Eski HTML karta parseri: rasm 12%, tuman 8%.

### Bundan kelib chiqadigan xulosalar
1. `olx_detal.py` (har e'lon uchun alohida so'rov, 3 soniya) **endi kerak
   emas** — hamma narsa ro'yxat sahifasida.
2. `ld+json` bloki ham bor, lekin **faqat 1-sahifada** — foydasi kam.
3. **Telefon raqami YO'Q.** `contact.phone` faqat `true/false`.
   Bu tekshirilgan va tasdiqlangan. Telefon uchun Telegram kanallari
   yagona yo'l (hali qurilmagan).

### Ehtiyot bo'ling
`photos` maydoni **uch xil ko'rinishda** keladi: matn, matnlar ro'yxati,
obyektlar ro'yxati. Bitta shakl butun yig'ishni to'xtatgan edi. Shuning
uchun `_lugat()` yordamchisi va har e'lon uchun `try/except` qo'yilgan.
**Bu himoyani olib tashlamang.**

---

## 6. Qidiruv mantiqi (`qidiruv.py`)

OLX muammosi o'lchangan: "neksiya kolodka" -> 10 natija, 4 tasi boshqa
mashina. Biz shuni tuzatamiz:

```
1. Qism turi MAJBURIY (so'rovda ko'rsatilgan bo'lsa)
     mos kelsa +50 · lug'atda yo'q lekin matnda bor +20 · aks holda KESAMIZ
2. Model mos kelmasa KESAMIZ  (asosiy farqimiz)
     mos +40 · boshqa mashina -> chiqarib tashlanadi · modeli yo'q +5
3. Qolgan so'zlar: har biri +4
4. Yaqinlik (joy) +25 · narxi bor +5 · do'kon +4 · rasm +3 · yangilik +0..10
```

Narx oraliqda **chetdagi 10% olib tashlanadi** — "60 000 – 2 761 472"
kabi oraliq odamga hech narsa aytmaydi.

### Tezlik
- `tan_qismlar`/`tan_modellar` oldindan hisoblanadi (`tahlil.py`)
- E'lonlar **xotirada keshlanadi**, baza fayli o'zgargandagina qayta o'qiladi
- `normalla()` faqat kerak bo'lganda chaqiriladi
- Server `ThreadingHTTPServer` — bitta sekin so'rov saytni to'xtatmaydi
- Server ko'tarilishida tahlil qilinmagan e'lon qolsa **o'zi tugatadi**

O'lchov: 8 527 e'londa ~1 soniya edi, kesh qo'shilgach tezroq bo'lishi
kerak (hali o'lchanmagan). **30 000 e'londa qayta o'lchang** — agar 1
soniyadan oshsa, SQL darajasida oldindan filtrlash kerak.

---

## 7. Lug'at (`lugat.py`) — eng qimmat boylik

O'zbek foydalanuvchisi qanday yozsa ham tushunish kerak: kirill/lotin
aralash, imlo xatolari, qo'shimchalar.

- `normalla()` — kirill -> lotin, `q->k, w->v, y->i, j->z, c->s`
- `ozak()` — qo'shimchani olib tashlash (`-lari, -lar, -si, -i`) +
  undosh yumshashi (`g->k, b->p, d->t`)
- Fuzzy: **tahrir masofasi** (Levenshtein), foiz emas.
  `_ruxsat(n)`: 8 harfgacha 1 xato, undan uzunga 2 xato.
  **4 harfdan qisqa yozuvlar aniq mos kelishi shart** — aks holda
  "geely" va "gelvi" chalkashadi.

Bu yerda 4 marta xato qilingan va tuzatilgan. **Lug'atni o'zgartirsangiz
`SINOV.bat` ni yuriting** va `python tahlil.py qayta` bilan teglarni
qayta hisoblang.

---

## 8. Joylar (`joylar.py`)

Aziz shikoyati: "krilcha bo'lib ketibdi, ruscha aralash".

Yechim: joy ro'yxati **ma'lumotdan emas, `joylar.py` faylidan** tuziladi.
14 viloyat + Toshkent shahri, ~180 shahar/tuman, har biriga ruscha
variantlari. `Риштан -> Rishton, Farg'ona`.

- `tani(shahar, tuman, viloyat) -> (viloyat, joy)` — toza nom
- `daraxt()` — tanlov uchun ro'yxat (`/api/holat` shuni qaytaradi)
- `moslikmi(tanlangan, viloyat, joy)` — mos keladimi
- **Diqqat:** `moslikmi` viloyatni `_kalit()` bilan solishtirmaydi, chunki
  u " shahri"/" viloyati" qo'shimchasini olib tashlaydi va "Toshkent
  shahri" bilan "Toshkent viloyati" bir xil bo'lib qoladi.

UI: **ikki bosqichli tanlov** — avval viloyat (14 ta), keyin shahar.
Bitta ro'yxatda 180 ta joy bo'lsa hech kim o'zinikini topolmaydi.

Joy — **"men qayerdaman" EMAS, "qayerdan qidiryapman"**. Jizzaxda turib
Surxondaryodan qidirish mumkin. Va u **filtr emas, saralash** — tanlangan
joydagilar tepada chiqadi, qolganlari yo'qolmaydi.

---

## 9. API

```
GET  /                        xaridor sahifasi
GET  /sotuvchi                sotuvchi kabineti
GET  /api/qidir?q=&tuman=     qidiruv
GET  /api/holat               e'lon soni + joylar daraxti
GET  /api/sotuvchi/sorovlar?id=   sotuvchiga tegishli ochiq so'rovlar
GET  /api/sorov/javoblar?id=      xaridor o'z so'roviga kelgan javoblar
POST /api/sorov               {matn, aloqa, byudjet, tuman}
POST /api/sotuvchi/royxat     {nima, aloqa, tuman}
POST /api/sotuvchi/javob      {sorov_id, sotuvchi_id, holat, narx, izoh}
```

Qidiruv javobida `joy_nom` — ko'rsatish uchun toza nom. `shahar`/`tuman`
xom ruscha, ularni odamga ko'rsatmang.

---

## 10. Frontend qoidalari

- Sotuvchi ro'yxatdan o'tishi — **ikki savol, 30 soniya**. Kategoriya
  daraxti yo'q, o'z so'zi bilan yozadi, tizim tushunadi va nima
  tushunganini ko'rsatadi.
- Javob — **bir tegish**: BOR / YO'Q / O'XSHASHI BOR. Matn yozish kerak
  bo'lsa sotuvchi uchinchi kuni tashlab ketadi. "BOR" bosilsa faqat narx
  so'raladi.
- Xaridor so'rovi `localStorage`da saqlanadi — sahifani yopib qaytsa
  javoblari yo'qolmaydi (bu xato bir marta yuz bergan).
- Sotuvchi javob bergach ro'yxat **qayta chiziladi** — aks holda tepadagi
  "1 ta ochiq so'rov" yozuvi qolib, sahifa bo'm-bo'sh ko'rinadi.
- Ranglar: `--asos:#0f5c4a` (yashil), `--fon:#fbfbfa`. Minimalistik.

---

## 11. HOZIRGI HOLAT

Baza: **8 527 e'lon** (eski parser bilan yig'ilgan)
- rasm ~63%, tuman ~57%, ISO sana 0% (ya'ni yangi parser hali ishlamagan)

Yangi parser (`holatdan_oqi`) yozilgan va xatosi tuzatilgan, lekin
**hali to'liq yuritilmagan**. Aziz `KATTA-YIGISH.bat` ni bosishi kerak.

### Darhol qilinadigan ish
1. `KATTA-YIGISH.bat` yuritilsin
2. Ekranda `52 e'lon (holat) · rasm 51 · tuman 38` chiqishi kerak.
   Agar `(karta)` desa — holat bloki topilmagan, `_HOLAT_RE` ni tekshiring.
3. `KOR-BRAUZERDA.bat`, keyin ko'z bilan tekshirish:
   - rasmlar chiqayaptimi
   - joy nomlari toza-mi
   - qidiruv tezmi
   - to'liq halqa: so'rov -> sotuvchi javobi -> xaridor ko'radi

---

## 12. KEYINGI QADAMLAR (tartib bilan)

**P0 — SERVERGA CHIQISH (eng katta o'zgarish, 12-A bo'limga qarang)**
- Hozir hammasi Azizning noutbukida `.bat` orqali. Bu prototip.
- Railway yoki arzon VPS + jadval (scheduler)
- Ikki xil aylanma: bosh sahifa har 5 daqiqada, chuqur yangilash kechasi

**P0 — chuqurlik**
- Sahifa sonini oshirish (25 -> 60+). Toshkentda 46 966 e'lon bor,
  biz 1 250 tasini olayapmiz.
- 30 000 e'londa qidiruv tezligini qayta o'lchash

**P1 — halqani kuchaytirish**
- Sotuvchiga xabar berish (PWA push yoki Telegram bot).
  Hozir sotuvchi sahifani ochib turishi kerak — bu ishlamaydi.
- Sotuvchi javob berish tezligi va sifati bo'yicha reyting
- So'rov yopilishi (2 soat) — hozir bor, lekin xaridorga ko'rinmaydi

**P2 — ishonch**
- Uzum/Olcha'dan mos narx: "bu narx normalmi?"
- Takroriy e'lon va spam aniqlash
- Sotuvchi tarixi: nechta javob bergan, nechtasi to'g'ri chiqqan

**P3 — kenglik**
- Telegram kanallari adapteri (`t.me/s/<kanal>` — login kerak emas,
  telefon raqamlar ochiq)
- BirBir, Exzap adapterlari
- Yangi kategoriya (uy-joy yoki telefon). **Har kategoriyaga o'z lug'ati
  kerak** — uy uchun xona/qavat/tuman, telefon uchun model/xotira/holat.
  Lug'atsiz ma'lumot foydasiz.

---

## 12-A. ME'MORIY QARORLAR — Azizning savollari (2026-07-31)

Aziz uchta asosli savol berdi. Javoblar shu yerda yozilgan, chunki ular
keyingi bosqichning butun yo'nalishini belgilaydi.

### Savol 1: "5 daqiqa oldin qo'yilgan e'lon chiqadimi?"

**Hozircha yo'q.** Ma'lumot `.bat` bosilganda yig'iladi va keyin qotib
turadi. Bu prototip holati, mahsulot emas.

**Yechim — ikki xil aylanma.** OLX yangi e'lonni har doim 1-sahifaga
qo'yadi. Demak butun bazani qayta o'qish shart emas:

| Aylanma | Nima o'qiladi | Qanchada | Yuk |
|---|---|---|---|
| Bosh | Har viloyatning 1-sahifasi | har 5 daqiqada | 13 so'rov, ~35 soniya |
| Chuqur | 60 sahifagacha | kechasi 1 marta | ~20-30 daqiqa |

Natija: yangi e'lon eng ko'pi bilan **5 daqiqada** bazada bo'ladi.

Chuqur aylanma faqat qamrov uchun emas — narx o'zgarishini yozish va
o'chirilgan e'lonlarni belgilash uchun ham kerak.

**Shart:** bu doimiy ishlaydigan serverda turishi kerak. Shuning uchun
"serverga chiqish" P0 ga ko'tarildi.

**Muhim eslatma:** OBER tuzilishi aynan shu eskirishga qarshi qurilgan.
Indeks — kontekst (odatiy narx, kimda bor edi). Jonli sotuvchi javobi —
bugungi haqiqat. Indeks 5 daqiqa orqada qolsa falokat emas. Bu OLX'da
yo'q ustunlik, uni yo'qotmang.

### Savol 2: "Nega ichiga kuchli AI qidiruvchi qo'ymaymiz?"

**AI ma'lumot muammosini hal qilmaydi.** LLM'da OLX bazasi yo'q — u ham
borib o'qishi kerak, faqat sekinroq va qimmatroq. Qidiruvni o'ylab topib
bo'lmaydi.

**Tartib: lug'at oldinda, AI zaxirada.**

- Lug'at (`lugat.py`) — bepul, bir zumda, ~90% so'rovni qoplaydi
- AI — faqat lug'at yiqilgan so'rovlarda zaxira sifatida

Teskarisi qilinsa har qidiruv pul turadi va sekinlashadi.

**AI haqiqatan foydali joylar:**
1. "Bu narx normalmi?" — 9 000+ e'lon ustida tahlil
2. Tavsifdan ma'no chiqarish ("bittasi singan", "yaxshi holatda")
3. Lug'at tanimagan yangi so'z va jargonni tushunish

**Lug'at o'sishining arzon yo'li:** har qidiruv `qidiruvlar` jadvaliga
yoziladi. Ya'ni lug'at qaysi so'rovda yiqilgani aniq ma'lum
(`natija_soni = 0` bo'lganlar). Har hafta o'shalarni ko'rib lug'atga
qo'shish kerak. Bu AI'dan arzon va aniqroq, chunki haqiqiy foydalanuvchi
so'zlariga o'rganadi. **Buni muntazam ishga aylantiring.**

### AI QAYERGA QO'YILADI — aniq ro'yxat

Umumiy qoida: **AI issiq yo'lda turmaydi.** Ya'ni har qidiruvda
chaqirilmaydi. U so'rovlarning 10% idan kamida ishlasin, aks holda
har qidiruv pul turadi va sekinlashadi.

| # | Joy | Qachon ishlaydi | Nima beradi |
|---|---|---|---|
| 1 | So'rovni tushunish | **faqat** `lugat.py` yiqilganda (`natija_soni = 0`) | yangi so'z, jargon, g'alati imlo |
| 2 | Narx maslahati | natija ko'rsatilgandan keyin, fon rejimida | "bu narx odatdan 40% yuqori" |
| 3 | Tavsifdan ma'no | yig'ish paytida, bir marta | "bittasi singan", "yangi emas" -> teg |
| 4 | Sotuvchi ro'yxati | ro'yxatdan o'tishda, bir marta | "nima sotasiz" erkin matnini kategoriyaga solish |
| 5 | Javoblar xulosasi | 3+ javob kelganda | "eng arzoni 150 ming, eng tezi Chilonzorda" |
| 6 | Lug'at o'sishi | haftada bir marta, ofline | yiqilgan so'rovlardan yangi so'z taklif qilish |

**Eng qimmatlisi — 1 va 6.** Ular birga ishlaydi: AI yiqilgan so'rovni
tushunadi (foydalanuvchi javob oladi), va o'sha tushunish **lug'atga
yoziladi** — keyingi safar AI kerak bo'lmaydi. Ya'ni AI'ga sarflangan
pul bir marta to'lanadi va bilim bizda qoladi.

**AI QO'YILMAYDIGAN joylar:**

- Qidiruvning o'zi — indeks va lug'at bu ishni bepul va tezroq qiladi
- Chat oynasi — 1-A bo'limga qarang
- Sotuvchi javobini yozish — javob bir tegish bo'lishi kerak
- Narxni o'ylab topish — narx faqat sotuvchidan keladi

**Texnik shart:** AI chaqiruvi hech qachon xaridorni kutdirmasin.
Natija avval ko'rsatiladi, AI xulosasi keyin qo'shiladi (progressive
enhancement). AI ishlamay qolsa sayt oddiy ishlashda davom etadi.

### Savol 3: "Boshqa saytlarni ham bittalab qilamizmi?"

Ha, har manbaga alohida adapter kerak — universal scraper yo'q. Lekin:

1. **Adapter kichkina** — ma'lumot qayerdaligini topgandan keyin ~150
   qator. OLX'da bir kun ketdi, chunki qidirish kerak edi.
2. **Ko'p O'zbek sayti Next.js'da** — ya'ni `PRERENDERED_STATE` usuli
   qayta ishlaydi. Yangi manbada **birinchi navbatda shuni tekshiring.**
3. **Telegram — bitta manba emas, butun qatlam.** `t.me/s/<kanal>` login
   talab qilmaydi, bitta adapter minglab kanalni o'qiydi, va u yerda
   **telefon raqamlar ochiq turadi** (OLX'da yo'q). Qamrov bo'yicha
   OLX'dan kuchliroq bo'lishi mumkin. **P3 emas, P1 ga ko'tarishga
   arziydi.**

### Eng muhim strategik nuqta

**Yig'ish mahsulot emas — u boshlang'ich yoqilg'i.**

Har ro'yxatdan o'tgan sotuvchi — bu biz yig'ishimiz shart bo'lmagan tirik
manba. 1 000 faol sotuvchi bo'lganda OLX'dan ko'chirish ahamiyatini
yo'qotadi.

Lekin bugun yig'ish kerak, chunki **bo'sh sayt bilan hech kim kelmaydi**.
Xaridor "kobalt fara" deb yozganda darhol 143 natija va odatiy narxni
ko'rishi shart. Ishonch shundan tug'iladi, keyin so'rov qoldiradi, keyin
halqa aylanadi.

Shuning uchun o'lchov: **e'lon soni emas, faol sotuvchi soni va javob
berish tezligi.** Yig'ish o'sib, sotuvchi o'smasa — noto'g'ri yo'nalish.

---

## 13. SABOQLAR (takrorlamang)

1. **"Test qildim" degani API 200 qaytardi degani emas.** To'liq halqani
   o'zim bosib ko'rgandagina uchta jiddiy kamchilik chiqdi — hammasi
   "to'g'ri ishlayotgan" kod edi, lekin odam uchun natija yo'q edi.
2. **Bir sahifadagi natijani butun manbaga umumlashtirmang.** Men
   `ld+json` ni 1-sahifada ko'rib "hal bo'ldi" dedim — u faqat o'sha
   sahifada bor ekan. Aziz ekran rasmini tashlab ko'rsatdi.
3. **Yig'ish oldidan bir sahifalik sinov.** 20 daqiqalik ish bitta
   `AttributeError` tufayli behuda ketgan edi.
4. **Bo'sh qiymat bilan ustidan yozmang.** E'lon qayta yig'ilganda
   avval to'plangan rasm/tuman o'chib ketardi.
5. **Ma'lumotdan ro'yxat tuzmang.** Joy ro'yxati ma'lumotdan tuzilgani
   uchun aralash va chala edi. Ro'yxat lug'atdan tuzilishi kerak.
6. **Server qayta ishga tushirilmasa kod o'zgarmaydi.** Python
   `http.server` hot-reload qilmaydi. Bir necha marta shu tufayli
   "xato" deb o'ylandi.

---

## 14. NAIZA (boshqa loyiha, hali tugallanmagan)

Azizning tomonidagi ishlar:
- Brevo API kaliti (SMTP Railway'da bloklangan, HTTP API yo'li qurilgan)
- `CREDITS_FREE_VERIFIED_ONLY=1`
- naiza.uz DNS, `PUBLIC_BASE_URL`
- Click merchant hujjatlari

Bu OBER'ga aloqasi yo'q, lekin bitta ish papkasida turadi.
