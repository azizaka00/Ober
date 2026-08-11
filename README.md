# OBER — [ober.uz](https://ober.uz)

**Siz yozasiz. Bozor javob beradi.**

Bozor agregatori va teskari marketplace. Xaridor kategoriya daraxtini
titkilamaydi — o'z so'zi bilan yozadi:

> *"menga soat kerak bambino 6, kim 800 000 so'mga beradi?"*

OBER uch ish qiladi:

1. **Indeksdan topadi** — ochiq manbalardan yig'ilgan e'lonlar orasidan.
2. **Topilmasa — so'raydi.** Talab mos sotuvchilarga boradi; narx, muddat
   va rasm OBER ichidagi chatda qaytadi.
3. **O'z e'lonini qabul qiladi.** Sotuvchi e'lonini OBERga joylaydi va
   kabinetidan boshqaradi.

Tashqi e'lon asl manba havolasida ochiladi. OBER chatida aloqa va kelishish
mumkin, lekin to'lov, yetkazib berish va oldi-sotdi OBER orqali bajarilmaydi.

---

## Hozir nima ishlaydi

`ober.uz` productionda, 2026-08-03 dan beri uzluksiz.

| | |
|---|---|
| Faol e'lon | **276 715** |
| Hudud | 14 viloyat, tuman darajasigacha |
| Manba | OLX + ochiq Telegram kanallari |
| Yangilanish | issiq kategoriyalar har 45 daqiqada, to'liq qamrov sutkasiga bir marta |
| Qidiruv tezligi | ~88 ms |
| Til | o'zbekcha / ruscha |

**Ishlaydigan imkoniyatlar:**

- Erkin matnli qidiruv — imlo va til aralashsa ham tushunadi
- **Rasm bilan qidirish** — telefonda suratga olasiz, OBER nima ekanini
  aniqlab, indeksdan qidiradi
- Xaridor so'rovini mos sotuvchilarga yo'naltirish
- OBER ichidagi chat: narx, muddat, rasm, joylashuv
- Sotuvchi kabineti — Telegram orqali bir martalik kod bilan kirish
- Sotuvchining o'z e'lonlari (OBER endi faqat agregator emas)
- Bildirishnomalar markazi, brauzer push va sotuvchi uchun Telegram xabari

**Hali reja:** rasmiy API yoki hamkorlik beradigan qo'shimcha manba
adapterlari va deduplikatsiya qatlamini kuchaytirish.

---

## Nega bu ishlaydi

**Tuxum-tovuq muammosi chetlab o'tilgan.** Sotuvchi bazasi noldan
yig'ilmaydi — bozor ma'lumoti ochiq manbalardan indekslanadi, sotuvchilar
esa tayyor talab ustiga keladi.

**Og'riq isbotlangan.** O'zbek e'lonlarida bitta so'z besh xil yoziladi:
`chexol · chehol · chixol · chihol · чехол`. Bir sarlavhada o'zbek lotin,
o'zbek kirill va rus tili aralashadi. Odatiy qidiruv bunda ishlamaydi —
shuning uchun sotuvchilar sarlavhaga barcha variantni tiqishtiradi.
Normalizatsiya qatlami aynan shu muammoni yechadi.

**Google buni yecholmaydi.** Do'kondagi tovar internetda yozilmagan.
Google yozilganni topadi; OBER esa biladigan odamdan so'raydi.

---

## Texnologiya

Ataylab kichik. Bitta odam olib boradi, har bog'liqlik — kelajakda
sinadigan narsa.

- **Backend:** Python **standart kutubxonasi**. `pip install` yo'q.
- **Baza:** SQLite + FTS5, WAL rejimida.
- **Frontend:** har sahifa bitta HTML fayl, CSS va JS ichida.
  Framework yo'q, build bosqichi yo'q.
- **Production:** Hetzner CPX12 (2 GB), Caddy + avtomatik HTTPS,
  systemd xizmatlari, tiriklik qorovuli.

Yangi kutubxona qo'shishdan oldingi savol: *busiz bo'ladimi?*
Odatda bo'ladi.

```
app/      backend — qidiruv, indeks, sotuvchi halqasi, AI adapter
web/      sahifalar (bosh, kategoriyalar, e'lon, chat, sotuvchi)
deploy/   systemd, Caddy, o'rnatish skriptlari
docs/     qarorlar tarixi va tadqiqot
memory/   loyiha holati va saboqlar
```

---

## Ishlash uslubi

Bu loyihada ikkita fayl kodning o'zidan kam ahamiyatli emas:

**[`OBER-DIZAYN-QOIDALARI.md`](OBER-DIZAYN-QOIDALARI.md)** — har frontend
ishidan oldin o'qiladi. Undagi har qoida yonida **o'lchov va sana**
turibdi. Sababsiz qoida yo'q: har biri bir marta buzilgan, o'lchangan va
tuzatilgan narsa.

**[`memory/lessons.md`](memory/lessons.md)** — har xatodan keyin bitta
xulosa. Masalan: reverse proxy orqasida IP manzil noto'g'ri o'qilgani
uchun butun sayt soatiga 5 ta sotuvchi qabul qila olardi — va buni
hech kim sezmasdi, chunki chegara jimgina ishlardi.

Asosiy tamoyil: **"yaxshi ko'rinadi" — dalil emas.** Har layout qarori va
har tezlik da'vosi raqam bilan tasdiqlanadi.

---

## Qat'iy qoidalar

- **"Eng arzon" deb aytilmaydi.** Faqat: *"4 ta taklif: 150 000 – 240 000"*.
  Isbotlab bo'lmaydigan da'vo ishonchni o'ldiradi.
- **Xaridordan pul olinmaydi.** U kamyob tomon.
- **Manba har doim ko'rsatiladi** — kartada OLX yoki Telegram yozuvi turadi.
- **Sotilgan tovar chiqarilmaydi.** Xaridor bosib borsa tovar yo'q bo'lsa,
  bir martada ishonch ketadi.
- Ma'lumot yig'ishda manbalarning qoidalari hurmat qilinadi.

---

## Sirlar

Repoda **hech qanday kalit yo'q** va hech qachon bo'lmaydi.

| Nima | Qayerda |
|---|---|
| AI kaliti | serverda `/etc/ober-ai.env`, `chmod 600` |
| Telegram bot kaliti | serverda `data/bot-token.txt` |
| Baza | serverda, git'ga tushmaydi |

Kalitsiz ham kod ishlaydi: rasm qidiruvi o'chadi, matnli qidiruv
davom etadi.

---

## Kompaniya

**"NAIZA" MChJ** — STIR 313204884. Mahsulot brendi: **OBER**.
