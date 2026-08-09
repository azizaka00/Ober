# OBER — CODEX UCHUN ISH TOPSHIRIG'I

Sana: 2026-07-31 · Buyurtmachi: Aziz
Birga o'qiladi: `CODEX-HANDOFF.md` (mantiq) · `OBER-DIZAYN-BRIF.md` (ko'rinish)

---

## MAQSAD — buni har qadamda esda tuting

O'zbekistonda savdo **parchalanib ketgan**. Bir odam mahsulot qidirsa:
OLX'ni ochadi, keyin BirBir'ni, keyin Uzum'ni, keyin o'nta Telegram
kanalini varaqlaydi. Har birida boshqa narx, boshqa til, boshqa tartib.
Qayerda arzonroq ekanini hech qachon bilmaydi.

**OBER shu bo'shliqni yopadi: hammasini bir joyga yig'adi, tahlil qiladi
va bitta qidiruvda javob beradi.**

O'zbekistonda bunday xizmat yo'q. Bu bizning asosiy qiymatimiz —
"yana bitta e'lonlar sayti" emas, **umumiy qidiruv**.

Bundan kelib chiqadigan uchta texnik talab:

1. **Manba qo'shish arzon bo'lishi kerak.** Har yangi sayt uchun butun
   tizimni qayta yozib bo'lmaydi. Adapter interfeysi kerak.
2. **Takroriy e'lon birlashtirilishi kerak.** Bitta fara OLX'da ham,
   Telegram'da ham turgan bo'lsa, xaridor uni **bir marta** ko'rsin.
   Aks holda "umumiy qidiruv" spamga aylanadi.
3. **Manbalar teng ko'rinsin.** Natijada qaysi manbadan kelgani
   ko'rsatiladi, lekin OLX imtiyozli emas.

---

## QAYSI E'LONLARNI OLAMIZ — tanlash qoidalari

**Hammasini olish qidiruvni yaxshilamaydi, buzadi.** Narxsiz, rasmsiz,
uch oylik va allaqachon sotilgan e'lonlar bazani to'ldirsa, xaridor 500
ta natija ko'radi va yarmi yolg'on bo'ladi. Bu aynan OLX'ning muammosi.

### 1. Majburiy maydonlar — bularsiz olinmaydi

| Maydon | Nega |
|---|---|
| `nom` | busiz qidiruv ishlamaydi |
| `havola` | manbaga qaytish shart (huquqiy va ishonch) |
| `tashqi_id` | takrorni aniqlash uchun |
| `viloyat` yoki `shahar` | joysiz e'lon foydasiz |
| `sana` | eskisini ajratish uchun |

Bittasi yo'q bo'lsa — o'tkazib yuboriladi, xato sifatida sanalmaydi.

### 2. Qimmatli maydonlar — bo'lsa saqlanadi, bo'lmasa e'lon qoladi

`narx_som` · `rasm` · `qism_turi` · `tuman` · `biznes` · `tavsif` ·
`telefon` (Telegram'da bor, OLX'da yo'q)

**Narx eng qimmati.** OBER'ning asosiy qiymati — "odatiy narx 450 000".
Narxsiz e'lon bu hisobga kirmaydi, lekin "kimda bor" ro'yxatida qoladi.
Saralashda narxi borlar tepada (`+5 ball`, hozir ham shunday).

### 3. Kesiladiganlar

- **Narx ishonchsiz** — `5 000` dan past yoki `2 000 000 000` dan yuqori.
  Sotuvchilar `999999999` yozadi, u o'rtacha narxni buzadi.
  (`olx.py` da bor, yangi adapterlarda ham bo'lsin)
- **90 kundan eski** — ko'rsatilmaydi. **O'chirilmaydi**: narx tarixi
  bizning boyligimiz, u tahlil uchun qoladi. Faqat `faol = 0`.
- **Narx ham, rasm ham yo'q** — bunday e'lon xaridorga hech narsa
  bermaydi
- **Spam** — bir sotuvchi bir xil sarlavhani 10 marta qo'ygan bo'lsa,
  bittasi qoladi
- **Bizning yo'nalishimizga tegishli emas** — 4-bo'limga qarang

### 4. YO'QOLGAN E'LONNI BELGILASH — hozir yo'q, kerak

**Bu ishonch masalasi.** Sotilgan mahsulotni ko'rsatish xaridorni
bir marta aldash va butunlay yo'qotish demak.

- [ ] `elonlar` jadvaliga `faol` (0/1) va `korilmadi` (necha marta
      yig'ishda uchramadi) maydonlari
- [ ] E'lon ketma-ket 3 marta yig'ishda uchramasa -> `faol = 0`
- [ ] Qidiruv faqat `faol = 1` larni chiqaradi
- [ ] Ma'lumot o'chirilmaydi — narx tarixi qoladi

### 5. Qaysi kategoriyalar

Aziz qarori (2026-07-31): **avval chuqurlik, keyin kenglik.**

**1-bosqich — avto (hozirgi yo'nalish):**
- `avtozapchasti` — hozir shu yig'ilmoqda
- `shiny-diski` — g'ildirak va disklar
- `avtoaksessuary` — aksessuarlar
- `avtozvuk`, `avtoelektronika`

Bular bitta lug'at bilan ishlaydi (`lugat.py` da mashina modellari
allaqachon bor) — ya'ni deyarli bepul kengayish.

**2-bosqichgacha kutadi:** uy-joy, telefon, mebel, kiyim, ish.
**Sabab:** har kategoriyaga o'z lug'ati kerak. Uy uchun xona soni,
qavat, tuman; telefon uchun model, xotira, holat. Lug'atsiz ma'lumot
foydasiz — qidiruv tushunmaydi.

**Hech qachon olinmaydi:** qurol, dori-darmon, kattalar uchun, hujjat
va shaxsiy ma'lumot sotuvi.

### 6. Telegram uchun boshqacha qoida

Telegram'da kategoriya yo'q — xabarlar aralash keladi. Shuning uchun
**lug'at filtr vazifasini bajaradi**: xabarda mashina modeli yoki qism
nomi topilmasa, u savdo e'loni emas deb hisoblanadi va olinmaydi.

Qo'shimcha kesish belgilari: 3 so'zdan qisqa xabar, faqat rasm,
"kanalga obuna bo'ling" kabi reklama, takroriy yuborilgan xabar.

### 7. Huquqiy va axloqiy chegara

- **Har e'londa manbaga havola bo'lishi shart.** Biz ko'rsatamiz,
  o'zimizniki qilib olmaymiz. Bu qoida buzilmaydi.
- Rasmlar manba serveridan ko'rsatiladi, o'zimizga ko'chirilmaydi
- **Yopiq telefon raqami olinmaydi.** OLX'da raqam bosilganda
  ochiladi — biz uni olmaymiz. Telegram'da raqam matnda ochiq turadi —
  uni olish mumkin.
- So'rovlar orasida kutish (`KUTISH`), o'zimizni tanitish (`UA`)
- Manba "olmang" desa — to'xtatamiz. Janjal qilmaymiz, chunki
  uzoq muddatda bizga sotuvchilarning o'zi kerak, ko'chirma emas.

---

## QARORLAR — 2026-08-01 (Aziz tasdiqlagan)

Bu bo'lim oldingi bo'limlardan USTUN. Ziddiyat bo'lsa shu yerdagisi to'g'ri.

### 1. Bitta qidiruv, ketma-ket ikkinchi qadam

Ikkita qidiruv qutisi YONMA-YON qo'yilmaydi. Odam hech narsa ko'rmasdan
turib tanlashi kerak bo'ladi va hozir sotuvchi kam bo'lgani uchun "jonli"
tomonni tanlagan birinchi mijoz bo'sh ekran ko'radi.

To'g'ri tuzilish — **ketma ket**:

1. Bitta qidiruv maydoni. Odam yozadi -> butun bozor darhol chiqadi
   (indeks: e'lon soni, odatiy narx, eng arzoni).
2. Natijadan KEYIN, aniq va katta:
   *"Bugun aniq kerakmi? Hozir kimda borligini sotuvchilardan so'raymiz."*
   **[ Sotuvchilardan so'rash ]** — bir tegish, shakl yo'q, telefon yo'q.

Bilgan foydalanuvchi uchun ikkinchi darajali to'g'ri havola bo'lsin
(`Sotuvchilardan so'rash →`), lekin bosh sahifani egallamasin.

Nomlar mexanizmni emas, NATIJANI aytsin:
`Bozor narxini ko'rish` · `Sotuvchilardan so'rash`.

### 2. To'lqinli yuborish — VAQT bo'yicha, takror bo'yicha EMAS

"Odam 5 marta qidirsa" degan tetik ishlatilmaydi: qayta qidiruv ko'pincha
tasodifiy (sahifa yangilandi, imlo tuzatildi), sabrli odam esa bir marta
qidirib kutadi va unga ikkinchi to'lqin hech qachon bormaydi.

```
0-daqiqa   -> eng mos sotuvchilar (1-to'lqin)
3-daqiqa   -> javob yo'q bo'lsa keyingi to'lqin
8-daqiqa   -> yana bir to'lqin, hudud kengroq
20-daqiqa  -> so'rov yopiladi
```

Javob kelishi to'lqinni to'xtatadi.

### 3. Sotuvchi soni — HAQIQIY SON KO'RSATILADI

- Chegara: bir so'rov uchun eng ko'pi bilan **30** sotuvchi.
- **BOSHLANG'ICH REJIM (hozir):** kategoriyada sotuvchi kam. Shu sababli
  so'rov mos keladigan **hamma** sotuvchiga boradi, **50 tagacha**.
  Sabab qamrov emas — har sotuvchi OBER qanday ishlashini KO'RISHI kerak.
  So'rov kelmasa u tizimni tushunmaydi va tashlab ketadi.
- **O'chirish sharti:** kategoriyada 50 dan ortiq sotuvchi bo'lgach, eng
  mos 30 taga o'tiladi (moslik, javob tezligi, hudud bo'yicha).
- **Ekranda hech qachon yolg'on son yozilmaydi.** 15 ta bo'lsa
  "15 ta sotuvchiga yuborildi". "30 ta" deb yozish taqiqlanadi.
- Yo'nalish umuman mos kelmasa yuborilmaydi. Banner sotuvchisiga fara
  so'rovi bormaydi — bu o'qitish emas, bezovta qilish.

### 4. Jonli qatlam KO'RINISHI shart

Eng muhim talab. Agar sahifada shunchaki e'lonlar ro'yxati chiqsa, biz
OLX'ning nusxasimiz va foydalanuvchi farqni sezmaydi.

Natija chiqqan zahoti, e'lonlar TEPASIDA:

> **15 ta sotuvchiga yuborildi** · javob kutilmoqda
> Chilonzor, Sergeli, Yunusobod · odatda 4 daqiqada javob keladi

Javob kelganda o'sha joyda paydo bo'ladi:

> **BOR — 180 000 so'm** · Chilonzor · hozirgina

Ikki qatlam vizual jihatdan aniq farqlansin:
- E'lon kartasi — kulrang, `3 kun oldin · OLX`
- Javob kartasi — navy, `hozir · sotuvchidan`

Bu farq ko'rinmasa, jonli qatlam yo'q bilan barobar.

### 5. Bildirishnoma

**Brauzer bildirishnomasini avtomatik yoqib BO'LMAYDI.** Bu bizning
tanlovimiz emas: Chrome, Safari va Firefox aniq rozilik talab qiladi va u
foydalanuvchi harakati paytida so'ralishi kerak. Sahifa ochilishida
so'rasak, ko'pchilik rad etadi va Chrome saytni belgilab qo'yadi — kanal
butunlay yo'qoladi.

To'g'ri payt — so'rov yuborilgandan KEYIN:

> ✓ 15 ta sotuvchiga yuborildi
> Javob kelganda xabar beraylikmi? **[Ha, xabar bering]**

Cheklov: iPhone'da web-push faqat sayt bosh ekranga o'rnatilgan bo'lsa
ishlaydi.

**TELEGRAM BOT QILINMAYDI** — Aziz qarori, 2026-08-01. Bu bildirishnoma
kanallarini web-push, sahifadagi jonli yangilanish va eslab qolingan
so'rov bilan cheklaydi. Rejaga qo'shmang.

**DIQQAT — farqni chalkashtirmang:** Telegram BOT (bildirishnoma) scope'da
YO'Q. Telegram ADAPTERI (kanallardan e'lon yig'ish) esa qoladi va u eng
muhim manba bo'lib qolaveradi — Bosqich 3.

### 6. OLX bilan cheklanmaymiz

Tasdiqlandi. Tartib: Telegram kanallari -> BirBir -> Uzum -> Exzap.
Uzum boshqa maqsadda: undagi narx ETALON ("yangi 450 000, ishlatilgani
150 000").

Takroriy e'lonni birlashtirish (Bosqich 4) — "umumiy qidiruv" shusiz
yo'q. Eng kuchli argumentimiz shundan chiqadi:
*"Telegram'da 50 000 arzonroq".*

---

## BOSQICH 0 — hozirgi holatni tugatish (1 kun)

Yangi ish boshlashdan oldin mavjudi tekshirilsin.

- [ ] `KOR-BRAUZERDA.bat` -> qidiruv tekshirilsin: rasm chiqayaptimi,
      joy nomlari toza-mi, tezlik qanday
- [ ] To'liq halqa bosib ko'rilsin: qidiruv -> so'rov -> sotuvchi
      javobi -> xaridor javobni ko'radi
- [ ] `baza.sotuvchi_sorovlari()` dan `aloqa` maydoni **olib
      tashlansin** — hozir xaridor raqami barcha sotuvchiga ketmoqda
- [ ] Bir sotuvchiga kuniga keladigan so'rov soni cheklansin (spam)
- [ ] `faol` va `korilmadi` maydonlari qo'shilsin (yuqoridagi 4-qoida) —
      yo'qolgan e'lonni belgilash. Bu ishonch uchun eng muhim tuzatish.

**Qabul:** 9 139 e'londa qidiruv 500ms dan tez, halqa uziliksiz ishlaydi.

---

## BOSQICH 1 — SERVERGA CHIQISH (eng muhim, 2-3 kun)

Hozir hamma narsa Azizning noutbukida `.bat` orqali. Bu mahsulot emas.

- [ ] Railway yoki arzon VPS'ga ko'chirish
- [ ] SQLite saqlanadigan doimiy disk (yoki Postgres'ga o'tish qarori)
- [ ] Jadval (scheduler) — ikki aylanma:

| Aylanma | Nima | Qanchada |
|---|---|---|
| Bosh | Har manbaning 1-sahifasi | har 5 daqiqada |
| Chuqur | 60 sahifagacha | kechasi 1 marta |

- [ ] `ober.uz` domeni ulanadi, HTTPS
- [ ] Oddiy sog'liq sahifasi: oxirgi yig'ish qachon bo'lgan, nechta
      e'lon, nechta xato

**Qabul:** Aziz hech narsa bosmasdan, OLX'ga 5 daqiqa oldin qo'yilgan
e'lon `ober.uz` da chiqadi.

---

## BOSQICH 2 — ADAPTER INTERFEYSI (2 kun)

Hozir `olx.py` alohida yozilgan. Yangi manba qo'shish uchun umumiy
shakl kerak.

Har adapter shu ko'rinishda bo'lsin:

```python
# app/manbalar/<nom>.py
MANBA = "olx"            # baza uchun kalit
NOM = "OLX"              # odamga ko'rsatiladigan nom
KUTISH = 2.5             # so'rovlar orasidagi pauza

def bosh(cheklov: int = 1) -> list[dict]:
    """Eng yangi e'lonlar (bosh aylanma uchun)."""

def chuqur(sahifalar: int = 60) -> list[dict]:
    """To'liq yig'ish (kechasi)."""
```

Qaytariladigan lug'at maydonlari `CODEX-HANDOFF.md` 4-bo'limdagi
`elonlar` jadvaliga mos bo'lsin.

- [ ] `olx.py` shu shaklga keltirilsin (mantiq o'zgarmasin)
- [ ] `app/yigish.py` — barcha adapterlarni topib yurituvchi
- [ ] Bir adapter yiqilsa boshqalari ishlashda davom etsin
- [ ] Har manba uchun statistika: nechta olindi, nechta xato

**Qabul:** yangi manba qo'shish = bitta fayl yozish, boshqa hech joyga
tegmasdan.

---

## BOSQICH 3 — TELEGRAM ADAPTERI (3-4 kun, eng katta qamrov)

O'zbekistonda savdoning katta qismi Telegram kanallarida. Va u yerda
**telefon raqamlar ochiq** — OLX'da yo'q narsa.

- [ ] `t.me/s/<kanal>` orqali o'qish (login kerak emas, tekshirilgan)
- [ ] Kanallar ro'yxati fayl sifatida (`data/kanallar.txt`), oson
      to'ldiriladigan
- [ ] Xabar matnidan ajratish: mahsulot nomi, narx, telefon, joy, rasm
- [ ] Telefon raqami `telefon` maydoniga yozilsin
- [ ] Savdoga aloqasi yo'q xabarlar filtrlansin (reklama, e'lon emas)

**Diqqat:** Telegram matni tartibsiz — "Fara gentra 250mn kelishamiz
+998901234567 Chilonzor". Lug'at (`lugat.py`) shu yerda eng kerak.

**Qabul:** kamida 20 ta kanal o'qiladi, telefon raqami bor e'lonlar
ulushi 50% dan yuqori.

---

## BOSQICH 4 — TAKRORIY E'LONLARNI BIRLASHTIRISH (2-3 kun)

**"Umumiy qidiruv" shu ishsiz ishlamaydi.** Bitta mahsulot uch manbada
turgan bo'lsa, xaridor uni bir marta ko'rishi kerak.

Belgilar (kuchidan tartib bilan):

1. **Telefon raqami bir xil + narx yaqin** -> aniq bitta
2. **Rasm bir xil** (o'lcham + oddiy heshdan boshlang, murakkab
   algoritm keyin)
3. **Sarlavha juda o'xshash + narx bir xil + joy bir xil**

- [ ] `elonlar` jadvaliga `guruh_id` maydoni
- [ ] Birlashtirish yig'ishdan keyin ishlaydigan alohida bosqich
- [ ] Qidiruvda guruh bir marta chiqadi, ichida "3 manbada bor"
- [ ] Kartada manbalar nishoni: `OLX` `Telegram` `BirBir`
- [ ] **Eng arzon narx guruhning narxi bo'ladi**, va farq ko'rsatiladi:
      "Telegram'da 50 000 arzonroq" — bu xaridor uchun sof foyda va
      bizning eng kuchli argumentimiz

**Qabul:** bir mahsulot uch manbada bo'lsa, natijada bitta karta
chiqadi va uchala manba ko'rinadi.

---

## BOSQICH 5 — BOSHQA MANBALAR (har biri 1-2 kun)

Tartib bilan: **BirBir** -> **Uzum** -> **Exzap** -> qolganlari.

- [ ] Har birida avval `PRERENDERED_STATE` yoki shunga o'xshash JSON
      blokini qidiring (`CODEX-HANDOFF.md` 5-bo'lim). Ko'p O'zbek sayti
      Next.js'da — usul takrorlanadi.
- [ ] HTML parser faqat oxirgi chora

**Uzum haqida eslatma:** u do'kon, e'lon sayti emas. Undagi narx
**etalon narx** sifatida qimmat: "yangi 450 000, ishlatilgani 150 000".
Bu "bu narx normalmi?" savoliga javob beradi.

---

## BOSQICH 6 — FRONTEND (parallel ishlanishi mumkin)

`OBER-DIZAYN-BRIF.md` bo'yicha to'liq qayta qurish.

Qo'shimcha talablar — **umumiy qidiruv** g'oyasi ko'rinishi uchun:

- [ ] Kartada manba nishoni
- [ ] "3 manbada bor · Telegram'da 50 000 arzonroq" qatori
- [ ] Narx blokida manbalar bo'yicha taqqoslash
- [ ] Bosh sahifada ishonch qatori: "OLX, Telegram, BirBir va Uzum'dan
      N ta e'lon bir joyda"

---

## BOSQICH 7 — SOTUVCHIGA XABAR (2 kun)

Hozir sotuvchi sahifani ochib turishi kerak. Bu ishlamaydi.

- [ ] Telegram bot: sotuvchi `/start` bosadi, `sotuvchilar` jadvaliga
      `telegram_id` yoziladi
- [ ] So'rov kelganda bot xabar yuboradi, tugmalar: BOR / YO'Q /
      O'XSHASHI BOR
- [ ] Narx botda so'raladi
- [ ] Xaridorga "3 ta taklif keldi" xabari (Telegram yoki SMS)

**Qabul:** sotuvchi saytni ochmasdan, faqat Telegram orqali javob bera
oladi.

---

## QILINMAYDIGAN ISHLAR

Bular ataylab tashqarida — so'ralsa `CODEX-HANDOFF.md` 1-A ga qarang:

- Chat oynasi / AI suhbatdosh
- Sotuvchi javobiga qo'shimcha maydonlar (yetkazish, kafolat, tayyor
  bo'lish vaqti) — javob bir tegish bo'lib qolsin
- To'lov o'tkazish, bitimni ichkariga olish
- Ro'yxatdan o'tishni majburlash
- Har qidiruvda AI chaqirish (`CODEX-HANDOFF.md` 12-A, AI jadvali)

---

## TARTIB VA VAQT

```
0. Hozirgini tugatish       1 kun
1. Serverga chiqish         2-3 kun   <- eng muhim
2. Adapter interfeysi       2 kun
3. Telegram adapteri        3-4 kun   <- eng katta qamrov
4. Takrorini birlashtirish  2-3 kun   <- "umumiy qidiruv" shusiz yo'q
5. BirBir, Uzum             2-4 kun
7. Sotuvchiga xabar         2 kun

6. Frontend — parallel, istalgan paytda
```

Har bosqich tugagach Azizga ko'rsating va **o'lchov raqamini** ayting:
nechta e'lon, nechta manba, qidiruv necha millisekund, nechta takror
birlashtirildi.

Raqamsiz "tayyor" degan xabar qabul qilinmaydi.
