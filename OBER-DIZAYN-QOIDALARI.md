# OBER — DIZAYN QOIDALARI

Bu fayl har frontend ishidan **oldin** o'qiladi. Claude ham, Codex ham.

Manbasi ikkita: `taste-skill` (github.com/Leonxlnx/taste-skill) dan olingan
g'oyalar, va **bizning o'z o'lchovlarimiz**. Ikkinchisi og'irroq turadi.

Har qoida yonida **nega** va **qaysi o'lchov** yozilgan. Sababi yozilmagan
qoida — bu did emas, taqlid. Sababi eskirса, qoida ham o'zgaradi.

---

## 0. OBER NIMA

**OBER — ish quroli, reklama sahifasi emas.**

Bu farq hamma narsani belgilaydi. Reklama sahifasining vazifasi — taassurot
qoldirish. Ish qurolining vazifasi — **odamni kerakli narsaga eng tez
yetkazish**. Chiroyli, lekin sekin OBER — buzuq OBER.

Bundan kelib chiqadigan asosiy o'lchov:

> **Qidirgan odam birinchi ekranda haqiqiy tovar ko'rishi kerak.**

Sarlavha emas, va'da emas, "biz qanday ishlaymiz" emas. **Tovar.**

`taste-skill` ning ko'p qoidalari lending sahifalar uchun yozilgan va bizga
to'g'ri kelmaydi. Ular haqida 5-bo'limda.

---

## 1. UCHTA SOZLAGICH (1-10)

| Sozlagich | Qiymat | Nega |
|---|---|---|
| Layout tajribasi | **3** | Nostandart joylashuv qidiruvni sekinlashtiradi. Odam bu yerga tomosha qilgani emas, topgani keladi. |
| Harakat (animatsiya) | **2** | Faqat holat o'zgarishini bildirish uchun. Skroll animatsiyasi yo'q. |
| Ma'lumot zichligi | **8** | Bozor sayti. Bo'sh joy — yo'qotilgan e'lon. |

Zichlik 8 bo'lgani uchun `taste-skill` ning "ma'lumot to'kmang, ro'yxatni
qisqartiring" degan qoidalari bizga **teskari** ishlaydi. Bizda uzun ro'yxat —
mahsulotning o'zi.

---

## 2. TEXNOLOGIYA (o'zgartirilmaydi)

- Bitta HTML fayl: `web/index.html`. CSS ham, JS ham ichida.
- **Framework yo'q.** React yo'q, Tailwind yo'q, build bosqichi yo'q.
- Tashqi kutubxona yo'q. **Shrift ham o'z serverimizda** — `web/shrift/`.

**Shrift (2026-08-04 da hal qilindi).** Onest Google Fonts CDN'idan
kelardi: har ochilishda ikkita begona domenga ulanish (ikki DNS, ikki
TLS). Uch sabab bilan ko'chirildi — qoida buzilishi, kechikish, va
Google O'zbekistonda sekinlashsa saytimiz boshqacha ko'rinishi.

Ko'chirishda ikkinchi xato chiqdi: Google'ning CSS'i qanday bo'lsa
shunday olingan edi — 5 qalinlik x 4 alifbo = **20 fayl**. `md5sum`
ko'rsatdiki ulardan atigi **4 tasi noyob**: Onest o'zgaruvchan
(variable) shrift, bitta fayl 400-800 ni qoplaydi. Brauzer uchun esa
har URL alohida fayl — u bir xil 32 KB ni besh marta yuklab olardi.
Endi har alifbo uchun bitta fayl va `font-weight:400 800`.
Lotin uchun: **160 KB -> 32 KB**.

Fayllar ikkilik, loyihada saqlanmaydi. Tiklash:
`bash deploy/shrift-yuklab-ol.sh`.
- Backend Python standart kutubxonasi, `pip install` yo'q.

Nega: bitta odam olib boradi. Har bog'liqlik — kelajakda sinadigan narsa.
Va serverda 2 GB xotira bor, undan yig'uvchi ham foydalanadi.

Yangi kutubxona qo'shishdan oldin savol: **busiz bo'ladimi?** Odatda bo'ladi.

---

## 3. LAYOUT INTIZOMI (qattiq qoidalar)

Bularning har biri buzilgan, o'lchangan va tuzatilgan. Takrorlanmasin.

### 3.1 Birinchi ekran

- **Natija sahifasida birinchi karta 700 px dan pastda bo'lmasin** (telefon).
  O'lchov 2026-08-02: birinchi karta 1010 px da edi, ekran 843 px. Ya'ni
  qidirgan odam bitta ham mahsulot ko'rmasdi. Tuzatilgach 583 px.
- **Bosh sahifada hero butun ekranni egallamaydi.** U 100svh edi va ichida
  faqat sarlavha bilan qidiruv qutisi turardi. Qolgan 400 px — bo'sh fon.
- **O'lchash usuli:** `getBoundingClientRect().top + scrollY`. Ko'z bilan
  "yaxshi ko'rinadi" deyish taqiqlanadi.

### 3.2 Yopishqoq elementlar

- Yopishqoq element qo'yishdan oldin **ustidagi yopishqoq elementni
  hisobga ol**. 2026-08-02: saralash paneli `top:0` edi va tepa panel
  (z-index 20) uni butunlay yopib turardi. Ko'rinmasdi ham, bosilmasdi ham.
- Panel balandligi `--panel-h` o'zgaruvchisida. Qo'lda raqam yozilmaydi.
- **Telefonda yopishqoq element eng ko'pi bilan bitta.** Ikkitasi ekranning
  uchdan birini yeydi.
- 2026-08-04 o'lchov (412x674): natija sahifasida **ikkitasi** bor edi —
  tepa panel (sticky, 65 px) va suzuvchi so'rash tugmasi (fixed, 50 px).
  Birgalikda 115 px = ekranning **17% i** doimiy band, ya'ni bitta karta.
  Tepa panel telefonda `position:absolute` qilindi (ro'yxatni ko'rayotganda
  logotip va til kerak emas), suzuvchi tugma qoldi — u OBER'ni oddiy
  e'lonlar ro'yxatidan ajratib turadigan yagona harakat.
  Natija: birinchi karta 484 px dan **427 px** ga ko'tarildi.

### 3.2.1 CSS tartibi — @media har doim ham g'olib emas

`@media` ichida yozilgan qoida avtomatik ustun EMAS. Bir xil
og'irlikdagi (specificity) tanlagichlar orasida **faylda keyingisi**
yutadi.

2026-08-04: `@media (max-width:620px){.results{padding-bottom:88px}}`
599-qatorda, `.results{padding:30px 0 72px}` esa 698-qatorda turardi.
Ikkinchisi birinchisini bekor qilardi — ya'ni telefon uchun yozilgan
tuzatish **hech qachon ishlamagan**, lekin kodda "tuzatilgan" bo'lib
turardi.

Boshqa qoidani bekor qilmoqchi bo'lsang: tanlagich **kamida shunday
og'ir** bo'lsin va **keyinroq** tursin. `body.is-results .topbar` ni
`.topbar` bilan yenga olmaysan.

### 3.3 Animatsiya

- **Layout xossalari animatsiya qilinmaydi:** `min-height`, `padding`,
  `width`, `height`, `top`. Faqat `opacity`, `transform`, `color`, `border`.
- Nega: 2026-08-02 da hero `min-height` va `padding` animatsiyada edi.
  Sekin qurilmada u osilib qolardi va natija ekran ostida qolib ketardi.
- Animatsiya davomiyligi 220 ms dan oshmasin.
- **`max-height` bilan ochish-yopish — eng ko'p uchraydigan buzilish.**
  2026-08-04: `sotuvchi.html` dagi narx qatori `max-height:0 -> 230px`
  va `margin` animatsiyasi bilan ochilardi. Ikki dard: (1) layout
  animatsiyasi, (2) `230px` — taxminiy raqam, matn undan uzun bo'lsa
  kontent **kesilib** qolardi va telefon uchun u yana ham kichik
  (`120px`) qilingan edi.
  To'g'ri yechim: joy `display:none -> grid` bilan **darhol** ochiladi
  (layout bir marta hisoblanadi), kontent esa `opacity` + `transform`
  bilan suriladi. Balandlik chegarasi umuman qo'yilmaydi.

### 3.3.1 Bir marta tuzatilgan xato boshqa faylga ko'chirilsin

`[hidden]{display:none!important}` qoidasi 2026-08-02 da `index.html`
uchun yozilgan edi. 2026-08-04 o'lchovi `takliflar.html` da xuddi
o'sha xatoni topdi: `aside.notification-panel` da `hidden` bor edi,
lekin `display:grid` uni bekor qilib turardi va blok **ko'rinmay
163 px** joy egallardi.

Ya'ni saboq yozilgan, lekin bitta faylga. Umumiy qoidani tuzatganda
**uchala sahifani ham tekshirish shart**.

### 3.4 Ko'rinish va yashirinish

- `hidden` atributi **har doim ishlashi shart**: `[hidden]{display:none!important}`.
  2026-08-02: `.answer-list{display:grid}` `hidden` ni bekor qilib yuborgan va
  yopiq deb o'ylagan blok 227 px joyni egallab turgan edi.
- Element `display:none` qilinsa, u **umuman chizilmasin** — JS'da ham.
  Ko'rinmaydigan kontent yozish behuda ish. 2026-08-02: namuna so'rovlar
  ikkala holatda ham yashirilgan edi, ya'ni hech qachon chiqmagan.

### 3.4.1 To'liq ekranli qatlam shaffof bo'lmasin

2026-08-04, Aziz telefonda suratga oldi: chat ochilganda **orqadagi
suhbatlar ro'yxati matn ichidan ko'rinib turardi** — "Nexia Usta",
"GM Parts", "Avto Lider" xabar ustiga chiqib, hech narsani o'qib
bo'lmasdi.

Sabab: `.inbox,.chat{background:rgba(255,255,255,.78)}`. Kompyuterda
bu **to'g'ri** — chat ikki ustunli sahifaning bir bo'lagi, ostida
sahifa foni turadi va shaffoflik chuqurlik beradi. Telefonda esa o'sha
element `position:fixed;inset:76px 0 0` bo'lib ro'yxat **ustiga**
chiqadi, ostida esa boshqa MATN qoladi.

Qoida: element telefonda to'liq ekranga aylansa, foni ham
o'zgarishi kerak. Shaffoflik ostida fon bo'lsa go'zal, matn bo'lsa
nosozlik.

### 3.4.2 Panjara ustunlari soni bolalar soniga bog'liq

O'sha suratda "Rasm" va "Joylashuv" tugmalari matn maydonining ustiga
chiqib qolgan, "Yuborish" esa pastda alohida qator bo'lib turardi.

`.compose-row` da **uchta** ustun e'lon qilingan edi
(`auto minmax(0,1fr) auto`), ichida esa **to'rtta** element bor:
Rasm, Joylashuv, matn maydoni, Yuborish. "Joylashuv" keyinroq
qo'shilib, panjara yangilanmagan. Natijada matn maydoni oxirgi tor
ustunga tushdi, "Yuborish" esa yangi qatorga sakradi.

Yangi tugma qo'shsang, `grid-template-columns` ni ham sana. Telefonda
to'rttasi bir qatorga sig'masa — `grid-template-areas` bilan ikki
qator qil, siqib tiqishtirma.

### 3.5 Media so'rovlar

- Desktop qoidasini tuzatgach, **`@media` bloklarini ham tekshir**.
  2026-08-02: hero desktopda tuzatildi, telefonda esa eski `100svh` va
  390 px to'ldirma joyida qoldi. Muammo yarim tuzatilgan bo'lib chiqdi.
- Har ko'p ustunli layout uchun `< 620px` holati **aniq yozilsin**.

---

## 3.6 Shakl va rang tizimi

2026-08-02 audit natijasi: faylda **13 xil burchak radiusi** (2, 4, 8, 11,
12, 13, 14, 16, 18, 22, 24, 99, 999) va o'zgaruvchilar tizimidan tashqarida
25 dan ortiq qo'lda yozilgan rang bor edi. Hech qanday tizim yo'q edi.

Bu ko'zga tashlanmaydi, lekin sayt **saranjom emasdek** tuyulishining
asosiy sababi aynan shu.

2026-08-04 qayta tekshiruv: `index.html` va `sotuvchi.html` tozalangan
edi, lekin **`takliflar.html` e'tibordan chetda qolgan**. U yerda hali
`5px`, `6px`, `17px`, `28px` degan tasodifiy qiymatlar turardi (chat
pufagi, sahifa varag'ining tepasi, tutqich). Hammasi tizimga o'tkazildi.
Chat pufagining o'tkir burchagi uchun beshinchi **nomlangan** qiymat
qo'shildi: `--r-quyruq:5px`. Nomlangan — demak tasodifiy emas.

**Burchak — to'rtta qiymat, boshqasi yo'q:**

| O'zgaruvchi | Qiymat | Qayerda |
|---|---|---|
| `--r-kichik` | 10px | input, kichik tugma, belgi |
| `--r-orta` | 14px | karta, panel |
| `--r-katta` | 20px | katta panel, qidiruv qutisi |
| `--r-pill` | 999px | chip, yumaloq tugma |

Yangi qiymat qo'shilmaydi. `border-radius:16px` yozish taqiqlanadi.

**Rang — bitta urg'u.** Asosiy rang `--navy`. Yashil, sariq va qizil
faqat **ma'no tashiganda** (do'kon, yangi, xato). Bezak uchun yangi rang
qo'shilmaydi. 2026-08-02 da men Telegram belgisi uchun beshinchi ko'k
(`#1f6fa8`) qo'shgan edim — o'z qoidamni o'zim buzdim, qaytarildi.

**Bosilganda javob.** Har bosiladigan element `:active` da 1 px pastga
tushadi. Telefonda hover yo'q — bosish yagona javob. Faylda atigi 2 ta
`:active` bor edi, ya'ni tugmalar bosilganda o'lik turardi.

## 4. KONTENT ZICHLIGI

### 4.1 Isbot va'dadan ustun

Bosh sahifada **haqiqiy e'lon ko'rinishi shart**. Rasmi, narxi, joyi,
sanasi bilan.

Nega: shablonni takrorlash oson, 127 ming o'zbek e'lonini takrorlab
bo'lmaydi. Bu bizning yagona nusxalab bo'lmaydigan aktivimiz.

Aziz, 2026-08-02: *"prosta turishini qara, AI da qilingani bilinib turibdi,
bo'sh va zerikarli"*. Sabab bitta edi: sahifada bitta ham real tovar yo'q edi.

**Lekin real tovar qo'yish yetarli emas — u ISHONARLI bo'lishi kerak.**

2026-08-04, Aziz bosh sahifani telefonda suratga oldi. Lentada:

| Karta | Muammo |
|---|---|
| katta qizil X rasmi, "Kozoynaklar likvidatsiyasi" | ikki marta ketma-ket |
| sariq barmoq emojisi, "Тошкентда ким бор?" — 2 560 000 so'm | e'lon emas, kanaldagi savol |
| "ISHGA TAKLIF QILAMIZ" — 11 400 000 so'm | ish e'loni, raqam esa MAOSH |
| "Logistika Dispatcher kerak" — 312 180 973 so'm | telefon raqami narx bo'lib olingan |

Vitrina o'zining eng yomon tomonini ko'rsatib turardi. Uchta qoida
chiqdi:

1. **Maosh — narx emas.** Ish e'loni indeksda qoladi (OBER "mahsulot,
   xizmat va ishlarni" topadi), lekin narxsiz. Aks holda "arzonidan"
   saralaganda ish e'loni divan bilan aralashadi.
2. **Savol — e'lon emas.** Sarlavhasi `?` bilan tugagan post kanaldagi
   oddiy suhbat, uning ichidagi raqam narx emas.
3. **Vitrinada nusxa bo'lmasin.** Bir e'lon kanalga qayta-qayta
   tashlanadi; lenta o'zini takrorlab ko'rsatsa, "bozor kichkina"
   degan taassurot qoladi.

### 4.1.1 Yangilik xilma-xillikni bermaydi

O'sha tuzatishdan keyin lentada 12 ta karta chiqdi — **12 tasi ham
kompyuter**. Sabab: yig'uvchi kategoriyalarni birma-bir aylanadi,
shuning uchun "eng yangi" e'lonlar deyarli har doim bitta
kategoriyadan bo'ladi.

O'lchov: eng yangi 96, 240, 480, 1 200 va hatto **3 000** e'lonning
hammasi bitta yuqori kategoriyadan chiqdi. Ya'ni ro'yxatni
kengaytirish yordam bermaydi — **so'rovni** o'zgartirish kerak edi.

"Butun bozor bitta qidiruvda" degan va'dani 12 ta kompyuter
isbotlamaydi. 12 xil narsa isbotlaydi. Endi so'rov har kategoriyadan
eng yangi 3 tasini oladi (`ROW_NUMBER() OVER (PARTITION BY ...)`) va
`rn` bo'yicha saralab aralashtiradi. Natija: 12 karta, **11 xil
kategoriya**. Narxi 0.45 s, kesh 120 s.

### 4.2 Sarlavha emas, ma'lumot

- **Bo'lim ustidagi kichkina katta harfli yorliq (kicker/eyebrow) —
  taqiqlanadi.** Har AI qurgan saytda bor. Bo'limning joylashuvining o'zi
  uni tasniflaydi.
- Sarlavha + izoh + kontent o'rniga, imkon bo'lsa **faqat kontent**.
  2026-08-02: "ANIQ QIDIRUV / So'rovni tushundik / Mos kelmaydigan qismlar
  kesildi" degan uch qator olib tashlandi. Ostidagi chiplar (`Mashina: cobalt`,
  `687 ta boshqa mashina chiqarildi`) ayni shu ma'noni beradi. 179 px -> 56 px.

### 4.3 Qo'shishdan oldin olib tashla

Bugungi har yaxshilanish **olib tashlash** orqali bo'ldi: narx gistogrammasi,
o'rtacha narx, sarlavhalar, filtr chiplari, fon rasmi.

Yangi element qo'shmoqchi bo'lsang, avval savol: **qaysi biri o'rniga?**

### 4.4 Aniq raqam

"Butun bozor" degan va'dani hamma yozadi. **127 360** degan sonni yozib
bo'lmaydi. Imkon bo'lgan joyda aniq, o'zgarib turadigan raqam ishlat.

---

## 5. "TELLS" — AI QILGANINI FOSH QILADIGAN BELGILAR

### 5.1 Bizga tegishlilari (taqiqlanadi)

- **Eyebrow / kicker** sarlavha ustida. Eng ko'p uchraydigani.
- **AI generatsiya qilgan fon rasmi.** Yuvilgan rang, "ideal ko'cha",
  detalsiz. 2026-08-02 da olib tashlandi. Agar rasm kerak bo'lsa —
  haqiqiy e'lon rasmi yoki haqiqiy fotosurat.
- **Div'lardan yasalgan soxta interfeys** ("mana bizning mahsulot" deb
  chizilgan soxta ekran). Bizda haqiqiy kartalar bor, ularni ishlat.
- **Soxta ma'lumot.** "Aziz Nematov", "+998 90 123 45 67", `99.9%`.
  Demo kerak bo'lsa — bazadan haqiqiy e'lon ol.
- **Bo'sh so'zlar:** "zamonaviy", "innovatsion", "eng yaxshi", "qulay".
  Ular hech narsa aytmaydi. Raqam yoki fakt yoz.
- **Hamma narsa markazda.** Sarlavha markazda, matn markazda, tugma
  markazda — bu standart holat, ya'ni "hech kim o'ylamagan" degani.
- **Har qatorda vergul o'rniga nuqta (`·`) ishlatish.** Bir qatorda
  ko'pi bilan bitta.

### 5.2 Bizga TEGISHLI EMAS (muhim)

`taste-skill` inglizcha lending sahifalar uchun yozilgan. Quyidagi
qoidalarini **ko'chirmaymiz**:

- **Uzun tire (`—`) taqiqi.** Inglizchada u AI belgisi. **O'zbekchada
  bu oddiy tinish belgisi**: "Bu — muhim". Uni olib tashlash matnni
  buzadi. Bizda ruxsat.
- **"Ma'lumot to'kmang, ro'yxatni qisqartiring".** Bizda uzun ro'yxat —
  mahsulot. 60 ta karta ko'rsatish to'g'ri.
- **Bento grid, logotip devori, mijoz izohlari, GSAP skroll animatsiyalari.**
  Bular reklama sahifasining mebeli. OBER'ga qo'shilsa, u yomonlashadi.
- **Qorong'i rejim "majburiy"** degan qoida. Bizda ustuvorligi past.
- **Tailwind sinflari bo'yicha o'lchamlar** (`text-7xl`, `pt-24`).
  Bizda Tailwind yo'q.

---

## 6. TIL VA RAQAM

- Interfeys tili — **o'zbekcha**. Ruscha tarjima `i18n.js` orqali.
- **Raqamlar bo'shliq bilan ajratiladi:** `127 360`, `550 000 so'm`.
  `toLocaleString("uz-UZ")` **ishlatilmaydi** — u vergul qo'yadi
  (`127,360`) va inglizcha ko'rinadi. `formatInt()` ishlat.
- **Sanalar o'zbekcha va nisbiy:** "Bugun", "Kecha", "2 kun oldin",
  "23 iyul". Manbadan kelgan "2026-07-31" yoki "Сегодня в 06:41" —
  to'g'ridan-to'g'ri chiqarilmaydi.
- Pul birligi har doim yozilsin: `550 000 so'm`, `550 000` emas.

---

## 7. HOLATLAR (har biri majburiy)

Har ma'lumot yuklaydigan blok uchun **to'rtta holat** yozilsin:

1. **Yuklanmoqda** — skelet. Bo'sh ekran emas.
2. **Bor** — asosiy holat.
3. **Yo'q** — nima qilish kerakligi aytilsin. "Hech narsa topilmadi" —
   yetarli emas. "Boshqacha yozib ko'ring yoki sotuvchilardan so'rang."
4. **Xato** — odamga tushunarli jumla, va **konsolga haqiqiy sabab**.
   2026-08-02: `catch` xatoni yutib yuborgan edi va nima buzilganini
   topish uzoq davom etdi.

---

## 8. O'LCHOV MAJBURIYATI

Bu bo'lim eng muhimi.

- **"Yaxshi ko'rinadi" — dalil emas.** Har layout qarori raqam bilan
  tasdiqlanadi: element qayerda, balandligi qancha, ekranga sig'adimi.
- **Tezlik taxmin qilinmaydi.** 2026-08-02: qidiruv 7 875 ms edi va men
  kodni optimallashtirmoqchi bo'ldim. O'lchov qo'yganimda ma'lum bo'ldiki
  qidiruvning o'zi 350 ms, qolgan 7.5 soniya — SQLite qulfini kutish.
  Serverga chiqargach o'sha kod 160 ms da ishladi.
- **Brauzerda tekshirishning cheklovi bor.** Fon rejimidagi tabda
  animatsiya to'xtaydi va `loading="lazy"` rasmlar yuklanmaydi. Bu
  xato emas, test artefakti. Chalkashmaslik uchun bilib turish kerak.

---

## 9. YETKAZISHDAN OLDINGI TEKSHIRUV

Har frontend o'zgarishidan keyin, **aytishdan oldin**:

- [ ] Konsolda xato yo'q
- [ ] Telefon kengligida (390 px) tekshirildi, desktopda ham
- [ ] Natija sahifasida birinchi karta 700 px dan yuqorida
- [ ] Yangi eyebrow/kicker qo'shilmadi
- [ ] Raqamlar bo'shliq bilan, sanalar o'zbekcha
- [ ] Yangi yopishqoq element boshqasini yopmayapti
- [ ] Layout xossalari animatsiyada emas
- [ ] To'rtta holat (yuklanmoqda / bor / yo'q / xato) yozilgan
- [ ] `@media` bloklari ham tuzatildi
- [ ] Yangi tashqi bog'liqlik qo'shilmadi

---

## 10. QAROR JURNALI

Qaytarib olinmaydigan qarorlar. Sababi bilan.

**2026-08-02 — Narx agregatlari olib tashlandi.** O'rtacha narx, oraliq,
gistogramma. Sabab: OLX narxlarini odamlar o'z bilganicha yozadi
(10 000 so'mlik "fara", 170 mln so'mlik "fara"). Ular ustidan hisoblangan
har qanday o'rtacha yolg'on chiqadi va uni cheksiz tuzatib yurishga to'g'ri
keladi. O'rniga: hammasini ko'rsatamiz, saralash va filtr xaridorda.
Aziz: *"Hechqanday jadval, narx oralig'i kerak emas."*

**2026-08-02 — Lug'at shart emas, bonus.** Qidiruv lug'at model yoki qism
tanimasa bo'sh qaytarardi. Natijada 101 mingdan ortiq e'londan faqat
avtoqism ko'rinardi. Endi tanimasa — indeksdagi matn bo'yicha ishlaydi.

**2026-08-04 — O'sha saboq SOTUVCHI tomonida ham.** Yuqoridagi qoida
qidiruvga qo'llanilgan, lekin jonli sotuvchi halqasiga ko'chirilmagan
ekan. Ikki joyda to'siq qolgan edi:

1. `server.py` — lug'at tanimasa sotuvchini **422 bilan qaytarardi**.
   `yonalishlar.py` da esa BITTA yo'nalish bor edi (banner). Ya'ni OBER
   amalda faqat avtoehtiyot qism sotuvchi va bannerchini qabul qilardi.
   Mebelchi, tikuvchi, usta, fotograf, kandolatchi, repetitor,
   zargar — hammasi eshikdan qaytarilardi.
2. `baza._mos_sotuvchilar` — so'rov tanilmasa `return []` qilardi.
   Pastda "lug'at tanimagani uchun zaxira yo'l" degan kod turardi,
   lekin u faqat so'rov ALLAQACHON tanilgan bo'lsa ishga tushardi —
   eng kerak bo'lgan holatda esa hech qachon.

Aziz, 2026-08-04: *"Hali men har xil turdagi sotuvchi va xizmat
ko'rsatuvchilarga demak OBER ni tavsiya qila olmas ekanmanda."*

Endi:
- Hech kim rad etilmaydi. Yagona shart — matn 3 harfdan uzun bo'lsin.
- Lug'at 1 dan **20** yo'nalishga kengaytirildi (mebel, kiyim, qurilish,
  maishiy ta'mir, avto xizmat, IT, telefon, go'zallik, tashish, tadbir,
  ta'lim, ko'chmas mulk, hujjat, sog'liq, hayvonlar, bog'dorchilik,
  sport, bolalar, oziq-ovqat, banner).
- Tanimasa — odamning **o'z so'zlari** bo'yicha ishlaydi.

Sinov: *"uzuk yasatmoqchiman zargarga"* — lug'at na "uzuk"ni, na
"zargar"ni biladi, lekin so'rov zargarga yetdi.

**Umumiy qoida:** *tanimaslik bizning kamchiligimiz, foydalanuvchining
aybi emas. Buning uchun uni eshikdan qaytarish mumkin emas.*

**2026-08-02 — Manba har doim ko'rsatiladi.** Karta pastida OLX yoki
Telegram. Xaridor qayerdan kelganini bilishi kerak. Yolg'on manba
ko'rsatish ishonchni buzadi.

**2026-08-02 — "So'rash" tugmasi uch joyda, jimgina.** Ilgari u ro'yxat
oxirida, 10 072 px da turardi va hech kim yetib bormasdi. Endi: natija
boshida bir qator, 12-kartadan keyin karta, telefonda pastda suzuvchi
tugma. Hammasi bir xil ko'k tugma, qisqa jumla, bezaksiz.
Aziz: *"kamroq yozuv, bachkana bo'lmagan holatda"*.

---

Bu fayl tugallangan emas. Yangi qoida **faqat real muammodan keyin**
qo'shiladi, kitobdan ko'chirib emas.
