# OBER — loyiha konteksti

Bu fayl har seans boshida o'qiladi.

## OBER nima

OBER — bozor agregatori va teskari marketplace. Xaridor kategoriya
daraxtini titkilamaydi — **o'z so'zi bilan yozadi**: "menga soat kerak
bambino 6, kim 800 000 so'mga beradi?". OBER uch ish qiladi:

1. **Indeksdan qidiradi** — OLX va ochiq Telegram kanallaridan yig'ilgan
   270 mingdan ortiq e'lon, har 45 daqiqada yangilanadi.
2. **Topilmasa — so'raydi.** Talab mos sotuvchilarga boradi, ular OBER
   ichidagi chatda narx, muddat va rasm bilan javob beradi.
3. **O'z e'lonini joylashtiradi.** Sotuvchi OBER indeksiga o'z e'lonini
   qo'shadi va kabinetidan boshqaradi.

Tashqi e'lon kartasi asl manba havolasini ochadi. OBER chatida aloqa va
kelishish mumkin, lekin to'lov, yetkazib berish va oldi-sotdi OBER orqali
bajarilmaydi.

**Bu faqat avtoqism sayti EMAS.** Avtoqism birinchi vertikal edi —
bozor zichligini yaratish uchun tanlangan. Maqsad: har qanday mahsulot,
xizmat va usta.

## Navigatsiya — ISH bo'yicha, sahifa bo'yicha emas

To'rtta tab: **Qidirish · Kategoriyalar · Chat · Sotish**.

Ilgari beshta edi va ikkitasi (`➕ Yangi e'lon`, `Profil`) bir joyga —
`/sotuvchi` ga borardi. Hech narsa sotmaydigan odam "Profil" ni bosib
"Sotuvchi sifatida boshlang" degan ro'yxat shaklini ko'rardi.

Bitta odam ham sotadi, ham sotib oladi. Shuning uchun tab nomi u
QAYERGA borishini emas, NIMA QILISHINI aytadi. Sotuvchi sahifasida
xaridor uchun chiqish yo'li bor ("Qidirish bo'limiga o'ting").

## MAHALLIY SINOV MUHITI — ISH BOSHIDA KO'TARILADI

Jonli saytga deploy qilib sinash **taqiqlanmagan, lekin oxirgi
chora**. Bir deploy ~100 soniya; 2026-08-16 da shu sabab bir kunda
~40 daqiqa kutishga ketdi va bitta xato topilmay qoldi.

    python app/sinov_muhiti.py --ishga     # http://127.0.0.1:8811

Nima qiladi:

- `app/` ni `/tmp/ober-sinov` ga nusxalaydi;
- **`web/` ni NUSXA OLMAYDI — bog'laydi.** HTML/CSS tahriri darhol
  ko'rinadi, serverni qayta yoqish shart emas;
- jonli bazani FAQAT O'QIB, undan e'lonlar namunasini oladi.

**Shaxsiy ma'lumot ko'chirilmaydi.** `sotuvchilar`, `suhbatlar`,
`xabarlar`, `sorovlar`, `javoblar`, `push_obunalar` bo'sh qoladi va
skript buni yozishdan oldin tekshiradi — bo'sh bo'lmasa to'xtaydi.

Javob vaqti ~6 ms.

**Ma'lum cheklov:** namuna `ORDER BY id DESC LIMIT 3000` — ya'ni
faqat eng yangi e'lonlar. Qidiruv sifatini (masalan `divan charm`
-> Charmhoo shinalari) sinash uchun bu YETMAYDI, chunki kerakli
tovar namunaga tushmaydi. Bunday ish uchun `OBER_SINOV_NAMUNA`
ni oshiring yoki `sinov_muhiti.py` dagi tanlovni mavzuga qarab
o'zgartiring.

**Brauzer yo'q.** Qumtepada Chromium o'rnatib bo'lmadi (tarmoq
ruxsati yo'q). Ya'ni bu muhit serverni, API'ni, qidiruvni va
ballashni tekshiradi — LEKIN ko'rinishni emas. Vizual tekshiruv
hamon jonli saytda va Azizning brauzerida bo'ladi.

## FRONTEND ISHIDAN OLDIN — MAJBURIY

`web_sinov.py` har sahifani tekshiradi. Uchta qoida, uchalasi ham
bir marta buzilgan:

- **JS ichida HTML izohi (`<!--`) bo'lmaydi.** 2026-08-10: shablon
  satri ichidagi izohda teskari apostrof bor edi — u shablonni yopdi
  va butun kabinet bo'sh ochildi. Izoh kerak bo'lsa `//` bilan,
  funksiyadan tashqarida.
- **`[hidden]{display:none!important}` har sahifada.**
- **Teskari apostrof juft bo'lsin.**


`web/` ichida biror narsa o'zgartirishdan oldin
**`OBER-DIZAYN-QOIDALARI.md` ni to'liq o'qi.**

Undagi har qoida yonida o'lchov va sana turibdi. Sababsiz qoida yo'q —
har biri bir marta buzilgan, o'lchangan va tuzatilgan narsa.

Eng ko'p takrorlangan xatolar:
- `[hidden]{display:none!important}` — har sahifada bo'lishi shart.
  Bu xato uch marta takrorlangan (index, takliflar, elon).
- Burchak radiusi faqat `--r-kichik/orta/katta/pill`. Xom `12px` yozilmaydi.
- Layout xossalari (`max-height`, `padding`, `width`) animatsiya qilinmaydi.
- Telefonda yopishqoq element **bitta**.
- `@media` ichidagi qoida avtomatik ustun emas — faylda keyingisi yutadi.

## Texnologiya — o'zgartirilmaydi

- Frontend: bitta HTML fayl, CSS va JS ichida. Framework yo'q, build yo'q.
- Backend: Python **standart kutubxonasi**. `pip install` yo'q.
- Baza: SQLite + FTS5, WAL rejimida.
- Yangi bog'liqlik qo'shishdan oldin: **busiz bo'ladimi?** Odatda bo'ladi.

## Production

- Sayt: https://ober.uz — Hetzner (77.42.123.90), Caddy + HTTPS
- Xizmatlar: `ober-server`, `ober-yangilik` (issiq sikl),
  `ober-toliq` (sutkalik qamrov), `ober-qorovul.timer` (tiriklik nazorati)
- **Serverga ulanish:** `NAVBATCHI.bat` ni oching. U `data/buyruq.txt` ni
  kutadi, serverda bajaradi, natijani `data/javob.txt` ga yozadi.
  Kod yuklash uchun buyruq fayliga bitta so'z: `yuklash`

## Sirlar — git'ga hech qachon tushmaydi

`.gitignore` himoya qiladi, lekin bilib turish kerak:

| Fayl | Nima |
|---|---|
| `data/bot-token.txt` | Telegram bot kaliti |
| `tmp/*token*` | jonli sotuvchi sessiya tokenlari |
| `data/ober.db` | baza — foydalanuvchi ma'lumotlari bilan |

AI kaliti loyihada **umuman yo'q** — u serverda `/etc/ober-ai.env`
(chmod 600). Kalitsiz ham kod ishlaydi, rasm tashqariga yuborilmaydi.

## Ishlash uslubi

- **O'lchov majburiy.** "Yaxshi ko'rinadi" — dalil emas. Har layout
  qarori raqam bilan tasdiqlanadi.
- **Sekinlikning sababi ko'pincha kodda emas, muhitda.** Avval o'lch,
  keyin optimallashtir.
- **Umumiy tamoyilni tuzatganda, u yana qayerda buzilganini qidir.**
  Bitta faylni tuzatib "tugadi" deyish — saboqni yarim o'rganish.
- Har ishdan keyin `memory/lessons.md` ga bitta xulosa.

## COMMITDAN OLDIN — AVTOMAT TEKSHIRUV

`hooks/pre-commit` har commitda `app/bat_sinov.py` ni yugurtiradi
(`git config core.hooksPath hooks` orqali yoqilgan). U `.bat`
fayllaridagi blok qavs xatolarini qo'riqlaydi — 2026-08-13 da
NAVBATCHI.bat shunday xatodan oyna ochilib darhol yopilgan edi.
Hook xato topsa commit bloklanadi. `bat_sinov.py` ni tuzatib,
qayta commit qilinadi.

## Qidiruv qanday ishlaydi — ASOSIY QOIDA

**Indeksning o'zi lug'at.** 300 000 dan ortiq e'lon bor va har
birining kategoriyasi ma'lum. Qo'lda lug'at yozish SHART EMAS.

`baza.bozor_izi(matn)` — matnni o'z qidiruvimizdan o'tkazadi va
natijalar qaysi kategoriyada ekanini sanaydi. Sotuvchi va xaridor
shu usulda belgilanadi, keyin kesishma olinadi.

**Yorliqni faqat `yonalishlar.belgilar(matn)` orqali oling.** U
qo'lda yozilgan yo'nalishlarni `bozor_izi` bilan qo'shadi VA avto
qoidasini butun to'plamga qo'llaydi. Ilgari server o'zi
`tozalangan(...) | bozor_izi(...)` deb yozardi — tozalash `|` dan
oldin bo'lgani uchun tuzatilgan xato qaytib kelgan edi (2026-08-10).

Ishonch ikki xil o'lchanadi, dalil turiga qarab:

- So'zlar **birga** 20 tadan ko'p e'londa uchrasa — o'sha namunaning
  ulushi olinadi. Namuna kichrayganda talab oshadi (5-19 ta uchun
  80%, 1-4 ta uchun 95%): kam natijada faqat to'liq kelishuv dalil.
- Birga kam uchrasa — har so'z **alohida** so'raladi va ovozi ikki
  narsaga ko'paytiriladi: **aniqlik** (natijalari bir kategoriyada
  jamlanganmi) va **noyoblik** (indeksda kam uchraydimi). `uzuk`
  95% bir kategoriyada — kuchli; `oltin` 43/18/14 tarqoq — kuchsiz;
  `3x4` butun indeksda 28 marta — juda kuchli.

Yana ikki qoida:

- **Umumiy so'z hisobga olinmaydi.** Indeksning 5% idan ko'proq
  e'lonida uchragan so'z (`yangi` 32%, `holati` 56%, `sotiladi` 12%)
  kategoriya haqida hech narsa aytmaydi. Ro'yxat QO'LDA yozilmaydi —
  indeksning o'zi ko'rsatadi, ya'ni yangi manba qo'shilsa o'zi
  yangilanadi.
- **`faqat_birga=True`.** `bozor_izi` `fts_erkin` ning "kamida bitta
  so'z" bosqichini so'ramaydi. U bosqich qidiruv uchun kerak, bu
  yerda esa yolg'on javob beradi: so'zlar birga uchramaganda ham
  "birga shunday" degan xulosaga asos bo'lib qolardi.

`moslik_sinov.py` (48 ta holat) shuni qo'riqlaydi.

Qo'lda yozilgan lug'atlar faqat ikki tor ish uchun qoldi:

- `lugat.py` — **avto model va qismlari.** "Nexia kolodka" so'ralganda
  Range Rover kolodkasi chiqmasligi uchun. Bu faqat avtoda muammo:
  "divan" so'ralsa divan chiqadi, model ajratish kerak emas.
  `relevans_sinov.py` (13 test) shuni qo'riqlaydi.
- `yonalishlar.py` — indeksda kam bo'lgan sohalar (banner, xizmat).

**Lug'atni kengaytirmang.** Yangi mahsulot turi chiqsa, u indeksga
tushadi va `bozor_izi` uni o'zi taniydi. Kod o'zgarmaydi.

**Normallashgach to'xtash so'ziga aylangan ibora tashlanadi.**
`normalla("kiyim")` -> `"kim"`, qolip esa so'z boshi bo'yicha
qidiradi — natijada "kimda bor" degan har bir so'rov tikuvchiga
borardi (2026-08-10). `yonalishlar._TASHLANGAN` nimalar tashlanganini
ko'rsatadi.

## Manbalar — 2026-08-11 da qayta audit qilingan

| Sayt | Holat |
|---|---|
| OLX | ✅ ochiq, ishlaydi |
| Telegram (ochiq kanal) | ✅ ishlaydi |
| **avtoelon.uz** | ✅ **ochiq SSR — yangi A tur manbai (adapter yozish kerak)** |
| **asaxiy.uz** | ✅ **ochiq SSR — B tur tayanch narx uchun eng oson** |
| uzum.uz | robots **rasman** product/category ni ochgan, lekin CAPTCHA — hamkorlik suhbatiga asos |
| olcha.uz · texnomart.uz | SSR bor, lekin tovarlari JS-render (brauzersiz olinmaydi) |
| mediapark.uz | SSR bor, lekin robots `/ru/` ni taqiqlaydi — hurmat qilinadi |
| birbir.uz | 403 (30.07 da ochiq edi — himoya qo'shilgan) |
| prom.uz | 403 |

To'liq ro'yxat: `docs/01-manbalar.md` (2026-08-11 audit bo'limi).

CAPTCHA yechilmaydi, Cloudflare aylanilmaydi, robots taqiqini buzilmaydi.
Yangi manba qo'shish — kod ishi emas, **hamkorlik ishi**: rasmiy API yoki
kelishuv. Lekin ochiq SSR manbalar (avtoelon, asaxiy) oddiy HTTP adapter
talab qiladi.

## Ochiq muammolar (2026-08-16 holatiga yangilandi)

1. ~~Dizayn tizimida tizimdan tashqari radius qiymatlari~~ —
   **✅ yopiq.** `grep 'border-radius:[0-9]+px' web/*.html` — 0 natija
   (elon, sotuvchi toza), `[hidden]{display:none!important}` har
   sahifada bor. `web_sinov.py` (103 tekshiruv) ikkalasini qo'riqlaydi.
2. **Telefon ko'rinishi — iframe o'lchovi bilan yopildi (2026-08-16).**
   18 ta 390px skrinshot bor va qo'shimcha tizimli o'lchov: har
   sahifa 390px iframe'da — **yopishqoq element bitta** (elon'da
   topbar sticky edi — tuzatildi, `61cea1b`) va **horizontal
   overflow yo'q** (6/6 sahifa). Qoldiq: haqiqiy qurilmada jonli
   sinov — reja `reports/qurilma-sinov-2026-08-16/REJA.md` da
   (TWA APK + xaridor/sotuvchi oqimi + push + offline + safe-area).
3. ~~`nexia kolodka` 205 tadan 20 taga tushdi~~ — **✅ 2026-08-16 o'lchandi:**
   haqiqiy tovar kesilmagan. Butun indeksda "neksia + kolodka" birga
   atigi 2 ta e'lon bor (ikkalasi ham natijada), 178 kesilgani —
   boshqa modellar (matiz, cobalt). TOP-5 Nexia kolodkalari, umumiy
   kolodkalar pastda — to'g'ri ishlaydi.
4. ~~**Xaridor qidiruvi 4+ so'zda ~200 ms.**~~ — **✅ 2026-08-16 yopildi.**
   Uchta aybdor topildi va tuzatildi: (a) AND bosqichlariga umumiy
   so'zlar kirardi (`pro`, `yangi` → 7 157 ms) — endi `fts_erkin`
   va `fts_nomzodlar` ularni filtri; (b) OR bosqichida `ORDER BY
   rank` butun moslar to'plamini bm25 bilan baholardi (458–1167 ms)
   — endi OR faqat nomzod yig'adi, natija Python'da ballanadi;
   (c) `elonlar_idlardan` da `faol=1 AND id IN` SQLite'ni ix_faol_manba
   indeksiga tashlardi (4000 id uchun 20 129 ms) — `id IN` birinchi
   bo'ldi. Natija: 4+ so'zli so'rovlar ~120–200 ms, model so'rovlari
   ham (neksiya kolodka 339→101 ms, kobalt fara 695→201 ms).
5. ~~**Yetim yozuvlar**~~ — **✅ 2026-08-16 yopildi.**
   `baza.sotuvchi_ochir()` sotuvchini VA bog'liq yozuvlarni bir
   tranzaksiyada o'chiradi (xabarlar → suhbatlar → javoblar →
   yuborishlar → push_obunalar → sotuvchilar). `baza.yetimlarni_tozala()`
   eski yetimlarni har server startida tozalaydi. Test skriptlari ham
   endi `sotuvchi_ochir` ni ishlatadi — yangi yetim paydo bo'lmaydi.
   DIQQAT: `javoblar.sotuvchi` TEXT — eski nomli yozuvlarga tegmaydi,
   faqat raqamli ID lar solishtiriladi.
6. ~~**`gilam sotaman` degan sotuvchi `kat:Xizmatlar` yorlig'ini
   oladi.**~~ — **✅ 2026-08-16 yopildi.** Indeks o'sishi (519k) va
   yolg'iz so'z yo'lidagi NISBAT qoidasi: `gilam` endi faqat
   `kat:Uy va bog'` (avval 85% Xizmatlar). Production'da o'lchandi:
   gilam → Uy va bog' 77% + Xizmatlar 20% → NISBAT (0.75) Xizmatlar
   ni tashladi. 8 so'z sinovida faqat `gilam` va `oltin` o'zgardi,
   `karavot` ikkalasini saqladi (0.76). Ko'p so'zli "gilam yuvish
   xizmati" Xizmatlar yorlig'ini o'zida saqlaydi — to'g'ri.
7. ~~**OR bosqichi begona so'zni olib keladi** ("divan charm" →
   Charmhoo shina tepada).~~ — **✅ 2026-08-16 yopildi.** Aniq so'z
   endi 10 ball, prefiks kengaytmasi 2.5 ball (`qidiruv` erkin
   ballash). "divan charm" production'da: divanlar birinchi,
   Charmhoo pastga tushdi. `moslik_sinov` 5-bo'limi (erkin qidiruv,
   deterministik nomzodlar) buni qo'riqlaydi.

**2026-08-16 qo'shimchasi — qidiruv tartibi xavfi:** OR bosqichi
`ORDER BY rank` dan `rowid DESC` ga o'tdi (tezlik). Tartibsiz `LIMIT`
FTS'ni eski e'lonlardan o'qirdi — keng so'rovlarda yangi e'lonlar
nomzodga kirmasdi. `rowid DESC` yangilarni beradi (4 ms). Saboq:
tartib o'zgarishi natijani ham o'zgartiradi — `moslik_sinov` endi
buni qo'riqlaydi.

**Yopilgan:** OBER o'z e'lonlarida kategoriya bo'sh edi — endi
`baza.taxminiy_kategoriya()` uni indeksdan aniqlaydi, sotuvchidan
so'ramaydi (12 ta haqiqiy e'lon matnida 12/12).

## Til

Aziz bilan muloqot — o'zbekcha, aniq va qisqa.
Interfeys — o'zbekcha, ruscha tarjima `web/i18n.js` orqali.
Raqamlar bo'shliq bilan: `127 360 so'm`. `toLocaleString` ishlatilmaydi.
