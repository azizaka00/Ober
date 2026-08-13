# MANBALAR — aniq tekshiruv natijasi
_2026-07-30 · faqat SHAXSAN tekshirilgani yozilgan, taxmin yo'q_
_Yangilandi: 2026-08-11 — butun O'zbekiston bozori qayta auditi_
_Yangilandi: 2026-08-13 — Avtoelon, Asaxiy va Shahar.uz adapterlari_

---

# 2026-08-13 ULANGAN MANBALAR

| Manba | Holat | Qanday yig'iladi |
|---|---|---|
| **OLX.uz** | ✅ ulangan | `yangilik.py` sikl — issiq har 45 daqiqada, to'liq sutkada |
| **Avtoelon.uz** | ✅ **ulangan (2026-08-13)** | `app/manbalar/avtoelon.py` — issiq `bosh(1)`, to'liq `chuqur(3)` |
| **Asaxiy.uz** | ⚠️ **lokal ishlaydi, serverda bloklangan** | `app/manbalar/asaxiy.py` — issiq `bosh(1)`, to'liq `chuqur(3)` |
| **Shahar.uz** | ✅ **ulangan (2026-08-13)** | `app/manbalar/shahar.py` — issiq `bosh(1)`, to'liq `chuqur(3)` |
| **Telegram kanallar** | ✅ ulangan | `telegram_sikli` har siklda |

Avtoelon adapteri: `/avto/` (avtomobillar) va `/zapchasti/` (ehtiyot qismlar)
bo'limlarini yig'adi. Narx `y.e.` (dollar) da — `dollar_kursi()` orqali so'mga
o'tkaziladi. E'lon sahifasidan tavsif, parametrlar va katta rasm olinadi.

**Qidiruvda ko'rinishi:** yangi manba e'lonlari boshqalar bilan bir xil
qidiruvda chiqadi, kartada "Avtoelon" manba belgisi bilan. Sarlavhada
so'rov so'zi bor e'lonlar tepaga chiqadi (2026-08-13 o'lchov: "shazor"
so'rovida avtoelon BYD Chazor e'lonlari 344-o'rindan 42-o'ringa chiqdi).

Asaxiy adapteri: B tur (do'kon) — tayanch narx. 16 bo'lim yig'iladi
(elektronika, maishiy texnika, avto, mebel...). Narx so'mda, `biznes=1`
(do'kon) belgilanadi. O'lchov (2026-08-13): "samsung a57" so'rovida
Asaxiy tovari OLX e'lonlari bilan aralash, 4-o'rinda chiqdi (ball 122).

**MUHIM — serverda bloklangan (2026-08-13 o'lchov):** Asaxiy Hetzner
server IP'sini (77.42.123.90) butunlay bloklagan — IPv4 ham, IPv6 ham
403 qaytaradi (saytning o'z retro-403 sahifasi, Cloudflare emas). Lokal
(uy IP) dan 200 — adapter to'g'ri ishlaydi. Shu sabab adapter birinchi
403'da darhol to'xtaydi (`_Bloklandi`) — 16 bo'limni urib saytni
bosmaydi. Serverda asaxiy e'lonlari yig'ilmaydi: qidiruvda faqat lokal
yig'ilgan 369 ta e'lon bor. Yechim: hamkorlik yoki o'zbek IP'si.
CLAUDE.md qoidasi: blok aylanib o'tilmaydi.

Shahar.uz adapteri: A tur (sotuvchi beradi) — **ko'chmas mulk vertikali**.
6 bo'lim: kvartira sotish/ijara, sutkalik, uy sotish/ijara, dacha.
Narx DOLLARDA (`115 000 $`) — `baza.dollar_kursi()` orqali so'mga
(avtoelon'dagi kabi). Serverdan ochiq (200) — Asaxiy'dan farqli.
O'lchov (2026-08-13): 120 karta/sikl, "kvartira" so'rovida 36 ta shahar
e'loni chiqadi (OLX bilan aralash, 701-o'rin — OLX yangiroq va do'kon
bo'lgani uchun yuqorida; adolatli raqobat).

---

# 2026-08-11 QAYTA AUDIT — O'ZBEKISTONDAGI BARCHA BOZORLAR

Har bir sayt **shu kuni bevosita tekshirildi** (curl, HTTP holat, robots.txt,
sahifa kontenti, API prob). Xulosa:

## A tur — E'lonlar taxtasi (SOTUVCHI beradi) ← asosiy manbamiz

| Sayt | Holat 2026-08-11 | API | Izoh |
|---|---|---|---|
| **OLX.uz** | ✅ **ochiq, ishlaydi** | yo'q (HTML) | allaqachon ulangan, 30 000+ avtoqism |
| **Telegram ochiq kanallar** | ✅ **ishlaydi** | yo'q (`t.me/s/`) | allaqachon ulangan |
| **Avtoelon.uz** | ✅ **OCHIQ — yangi imkoniyat!** | yo'q (HTML) | SSR, real e'lon + narx (20–50 mln so'm namunalari), shahar bo'yicha |
| **BirBir.uz** | ❌ **403 Cloudflare** (30.07 da ochiq edi) | yo'q | himoya qo'shilgan — tekshiruvda `403 Forbidden` |
| **Glotr.uz** | ✅ jonli, eski va kichik | yo'q (HTML) | "первый торговый центр в интернете", qidiruv robots'da yopiq |
| **Avizinfo.uz** | ⚠️ **portal** — har shaharga alohida subdomen | yo'q | `tashkent.avizinfo.uz`, `andijan.avizinfo.uz`... e'lon tuzilishi chuqur tekshirilmagan |
| **Torg.uz** | ❌ **DNS javob yo'q** | — | OLX'ga birlashib ketgan (eski nom) |
| **Doska.uz** | ❌ **DNS javob yo'q** | — | o'lik |

## B tur — Onlayn do'kon / marketplace (sotuvchi BERMAYDI, faqat NARX)

| Sayt | Holat 2026-08-11 | API | Izoh |
|---|---|---|---|
| **Uzum Market** | ⚠️ **robots ALLOW qiladi, lekin CAPTCHA** | seller API — ro'yxatdan o'tgan sotuvchilar uchun (yopiq) | `robots.txt` **rasman** `/category/`, `/product/`, `?skuId=`, `?filters=` ni ochgan — lekin sayt "Siz robot emasmisiz?" sahifasini qaytaradi. Hamkorlik uchun asos bor |
| **Olcha.uz** | ⚠️ HTTP 200 + SSR bosh sahifa, **tovarlar JS-render** | yo'q (yopiq ichki) | kategoriya sahifasida `product-card` faqat CSS izi — tovar nomi/narx curl'da yo'q (brauzersiz olinmaydi) |
| **Asaxiy.uz** | ✅ **OCHIQ, SSR** | yo'q | tovar sahifasida 28 ta `product-name` + real narx — B tur uchun **eng oson manba** |
| **Mediapark.uz** | ⚠️ SSR bor, lekin **robots `/ru/` ni taqiqlaydi** | yo'q | `Content-Signal: ai-train=no` — hurmat qilamiz |
| **Texnomart.uz** | ⚠️ SSR HTML (175KB), **tovarlar JS-render** | yo'q | 30.07 da 403 edi — endi ochilgan, lekin curl'ga tovar yo'q |
| **Wildberries.uz** | ⚠️ 301 → `www.wildberries.uz`, SPA | yo'q ochiq | rus platformasi, mahalliy tovar ochiq emas |
| **Alif Shop** | ⚠️ SPA | yo'q | `/catalog` curl'ga title ham bermaydi — to'liq JS |
| **Kivano.uz · 99mart.uz · Elko.uz · Sello · Astra.uz** | ❌ **DNS javob yo'q** | — | o'lik yoki boshqa domen ostida (kivano.kz kabi) |

## Ko'chmas mulk (vertikal uchun)

| Sayt | Holat | Izoh |
|---|---|---|
| **Uybor.uz** | ✅ 200 | birlamchi ko'chmas mulk platformasi |
| **Shahar.uz** | ✅ 200 | regional e'lonlar |
| **Uysot.uz** | ⚠️ 429 | tezlik chegarasi — ochiq lekin ehtiyot talab |
| **Woody.uz** | ✅ 200 | mebel bozori (3 tilda katalog) |

## B2B (ulgurji — keyinroq)

| Sayt | Holat | Izoh |
|---|---|---|
| **Prom.uz** | ❌ 403 | Cloudflare |
| **B2B-Savdo.uz** | ⚠️ 200 → `www` ga redirect | keyingi bosqich |

---

## NIMA O'ZGARDI (30.07 dan 11.08 gacha)

1. **Avtoelon.uz — eng katta topilma.** Ochiq server-rendered avto e'lonlar
   taxtasi: real e'lonlar, narxlar, shahar filtrlari. OLX'dan keyingi eng
   kuchli A tur manbai. **Keyingi qadam: adapter yozish.**
2. **Asaxiy.uz ochildi.** 30.07 da Cloudflare 403 edi — endi tovarlar SSR
   holatda ochiq. B tur (tayanch narx) uchun eng oson manba.
3. **BirBir.uz yopildi.** 30.07 da ochiq edi — endi 403. Cloudflare qo'shgan.
4. **Uzum robots.txt ni ochdi** (product/category rasman ruxsat), lekin
   amalda CAPTCHA — himoya yo'qolmagan. **Bu hamkorlik suhbatiga asos.**
5. Olcha, Texnomart, Mediapark 403'dan qutuldi, lekin tovarlari JS-render —
   brauzersiz olinmaydi.

## HIMOYA QOIDALARI (o'zgarmaydi)

1. Faqat **ochiq ko'rinadigan** ma'lumot olinadi — himoya buzilmaydi
2. **Manba doim ko'rsatiladi** + havola qaytariladi
3. Har e'lon yonida **"o'chirish"** tugmasi — so'ralsa darhol olib tashlanadi
4. Yig'ilgan raqamlarga **so'ralmagan xabar yuborilmaydi**
5. Sekin va hurmat bilan yig'iladi — manba yuklanmaydi
6. **robots.txt ni hurmat qilamiz** — Mediapark (ru/ yopiq), Texnomart kabi
   taqiqlangan bo'limlardan yig'ilmaydi

---

# 2026-07-30 ASOSIY TEKSHIRUV (batafsil)

## 1. OLX.uz ✅ eng kuchli manba

**Tekshirildi:** kategoriya sahifasi, qidiruv sahifasi, e'lon sahifasi.

### Hajm
- Avtozapchasti: **30 859** e'lon
- Aksessuarlar: 26 383 · Avtozvuk: 5 247 · GPS: 2 303
- Toshkent viloyati (butun kategoriya): **46 966**
- Viloyatlar: Samarqand 4 156 · Buxoro 3 215 · Farg'ona 2 282 · Xorazm 1 587 ·
  Qashqadaryo 1 460 · Navoiy 1 088 · Andijon 909 · Qoraqalpog'iston 811 ·
  Namangan 665 · Jizzax 645 · Surxondaryo 645 · Sirdaryo 485

### Ro'yxat sahifasidan olinadi
nomi · narxi (so'm) · "Договорная" bayrog'i · holati (Yangi/B.u.) ·
**tuman** (Sergeli, Chilonzor...) · sana va vaqt · havola

### E'lon sahifasidan qo'shimcha olinadi
- **Telefon** — sotuvchi nomi sifatida OCHIQ turadi (masalan `998903565358`).
  Alohida telefon maydoni esa yopiq (`xxx xxx xxx` + "показать").
  Ya'ni raqam ochiq matnda bor, himoyani buzish shart emas.
- **"Бизнес" belgisi** — do'konmi yoki shaxsmi
- **Qism turi** — "Вид запчасти: Тормозная система" (OLX o'zi tasniflagan)
- **Holati** — Новый / Б/у
- **To'liq tavsif** — mahsulot kodi bilan (masalan PD02)
- **Rasmlar** — bir nechta, to'liq o'lchamda
- **Sotuvchi profili** → `/list/user/<ID>/` — **o'sha sotuvchining BARCHA e'lonlari**
- **Sotuvchi yoshi** — "OLX'da 2018-yil martdan" (ishonch belgisi)
- E'lon ID (44509358)

### URL tuzilishi
```
/transport/avtozapchasti-i-aksessuary/q-<so'rov>/     qidiruv
/transport/.../?page=N                                sahifalash (25 gacha)
/transport/.../<viloyat>/                             hudud
/d/obyavlenie/<slug>-ID<kod>.html                     e'lon
/list/user/<ID>/                                      sotuvchi
```

### Qidiruv sifati — bizning imkoniyatimiz
"neksiya kolodka" so'rovi → **10 natija**, shundan **4 tasi boshqa mashina**
(Трекер, Малибу, Эквинокс). Narx 95 000 – 490 000 (5 barobar farq, izohsiz).
**OLX qidiruvi yomon — biz aynan shuni tuzatamiz.**

---

## 2. Telegram ochiq kanallar ✅ ochiq telefon

**Tekshirildi:** `t.me/s/avtoelon` (3.15K obunachi), `t.me/s/zapchast_uz`.

### Ishlaydi
`t.me/s/<kanal>` orqali postlar to'liq o'qiladi — ro'yxatdan o'tish kerak emas.

### Olinadi
mahsulot nomi · texnik xususiyatlari · narx · **telefon (post matnida OCHIQ)** ·
rasm · sana/vaqt · ko'rishlar soni · post havolasi

Namuna:
> 🚗 #Kia Sonet · 📍 #Toshkent · 2025 · 1.5 benzin · 27 000 km
> 💸 17 100 $ · 📱 +998774815500

### Qo'shimcha imkoniyatlar
- Kanal ichida qidiruv: `?q=<so'rov>` (hashtag bo'yicha ham)
- Tarix: `?before=<post_id>` — eski postlarga kirish
- Post ID ketma-ket → hammasini yig'ish mumkin

### Ishlamaydi
Yopiq **guruhlar** (kanal emas) — tashqaridan ko'rinmaydi.
Sinov: @avto_zapchast_111 (188 a'zo) — postlar chiqmadi.

**Xulosa:** yirik ochiq kanallar ishlaydi, mayda do'kon guruhlari yo'q.

---

## 3. BirBir.uz — 30.07 da ochiq edi, 11.08 da 403

**30.07 da tekshirildi:** Toshkent ehtiyot qismlar kategoriyasi.

### Olinardi
nomi · narx (**so'm YOKI y.e. — aralash!**) · "Narx kelishiladi" ·
shahar · sana/vaqt · rasm · havola

### Ikkita foydali narsa
- **Tayyor kategoriya daraxti — 15 bo'lim:** Ehtiyot qismlar · Ta'mirlash uchun ·
  Shina/disk/g'ildirak · Audio-video · Avtoaksessuarlar · Tyuning · Yukxona/farkop ·
  Asboblar · Tirkamalar · Uskunalar · Yog'lar va kimyo · O'g'irlikka qarshi ·
  GPS · Mototsikl qismlari · Boshqa
- **Sotuvchi turi belgilangan:** "Do'kon" · "PRO" · "Yetkazib berish"

### Kamchilik
Joylashuv faqat **shahar** darajasida (OLX'da tuman bor).
Telefon ro'yxat sahifasida yo'q (e'lon sahifasida bo'lishi mumkin — tekshirilmagan).

### 11.08 da
`403 Forbidden` — Cloudflare himoyasi qo'shilgan. Qayta tekshiriladi yoki
hamkorlik orqali.

---

## 4. Exzap.uz ✅ standart nom + tayanch narx

**Tekshirildi:** bosh sahifa.

Bu **do'kon**, bozor emas — bitta sotuvchi. Sotuvchi manbai sifatida foydasiz.

### Qiymati boshqa joyda
- **To'g'ri, standart mahsulot nomlari** — tartibsiz e'lonlarni tozalash uchun lug'at
- **Tayanch narx** (masalan: Antifriz SHELL G12+ 200kg — 7 575 000 so'm)
- Muddatli to'lov narxi · mavjudlik ("Ertaga") · rasm · mahsulot sahifasi
- **VIN bo'yicha qidiruv bor** — kelajakda bizga ham g'oya

---

# UCHTA HAL QILINISHI KERAK BO'LGAN MUAMMO

**1. Aralash valyuta.** so'm, y.e., $ — bir formatga keltirish kerak.
OLX'da ba'zi narx dollardan avtomatik o'girilgan (119 611 = $10, kurs ~11 961).

**2. Bir tovar — turli nom.** Sotuvchilar imloni takrorlaydi:
"chexol chehol chixol chihol", "Акумлятор / Akumlyator". Lotin, kirill, rus aralash.
Birlashtirish kerak — **AI ishi.**

**3. Takroriy spam.** Bitta tovar 7 marta, narxi ozgina farq bilan
(1 100 421 / 1 112 382 / 1 124 343...). Filtrlash kerak.

---

# KEYINGI QADAM (ustuvorlik bo'yicha)

1. ~~**Avtoelon.uz adapteri**~~ — **✅ 2026-08-13 ulandi** (`app/manbalar/avtoelon.py`).
   Issiq sikl `bosh(1)`, to'liq sikl `chuqur(3)`. Avto vertikal uchun
   OLX'ni to'ldiradi.
1a. ~~**Shahar.uz adapteri**~~ — **✅ 2026-08-13 ulandi**
   (`app/manbalar/shahar.py`). Ko'chmas mulk vertikali, 6 bo'lim,
   narx dollar→so'm. **✅ To'liq sikl `CHUQUR_SAHIFA=10`** (avtoelon
   bilan bir xil) — ~200 e'lon/bo'lim.
2. ~~**Asaxiy.uz adapteri**~~ — **✅ 2026-08-13 yozildi** (`app/manbalar/asaxiy.py`),
   lekin **serverda bloklangan** (Hetzner IP 403 — yuqoriga qarang).
   Lokal ishlaydi, serverda yig'ilmaydi. Hamkorlik yoki o'zbek IP'si kerak.
   Birinchi 403'da `_Bloklandi` bilan to'xtaydi — sayt urilmaydi.
3. **Uzum bilan hamkorlik suhbati** — robots endi rasman ruxsat beradi,
   CAPTCHA to'siq. Rasmiy API/kelishuv — eng yirik bozor.
4. ~~**Asaxiy qamrovini kengaytirish**~~ — **to'xtatildi**: serverda
   bloklangan, chuqurlikni oshirishning ma'nosi yo'q. Agar blok olinsa
   — avtoelon'dagi kabi `CHUQUR_SAHIFA` beriladi.
