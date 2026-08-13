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

## Ochiq muammolar (2026-08-10)

1. Dizayn tizimida tizimdan tashqari radius qiymatlari (`elon.html`
   va `sotuvchi.html` da), `elon.html` da `[hidden]` qoidasi yo'q.
2. Telefon ko'rinishi to'liq sinalmagan.
3. `nexia kolodka` 205 tadan 20 taga tushdi — aniqlik oshdi, lekin
   haqiqiy tovar ham kesilgan bo'lishi mumkin. O'lchash kerak.
4. **Xaridor qidiruvi 4+ so'zda ~200 ms.** `fts_erkin` "hamma so'z"
   bosqichlaridan o'tolmay butun indeks bo'yicha OR qidiruviga
   tushadi (1 so'z 1 ms, 3 so'z 8 ms, 4+ so'z ~200 ms). `bozor_izi`
   bu bosqichni endi so'ramaydi, lekin `qidir()` hali so'raydi.
5. **Yetim yozuvlar:** 47 ta `yuborishlar`, 24 ta `suhbatlar`, 3 ta
   `javoblar` o'chirilgan sotuvchilarga tegishli. Hech kimga
   ko'rinmaydi, lekin sanoqlarni chalg'itishi mumkin. Tozalash
   kerak — `sotuvchilar` o'chganda bog'liq yozuvlar ham o'chsin
   (FOREIGN KEY ... ON DELETE CASCADE yoki qo'lda).
6. **`gilam sotaman` degan sotuvchi `kat:Xizmatlar` yorlig'ini
   oladi.** Indeksda gilam YUVISH xizmati e'lonlari gilamning
   o'zidan ko'p (85%). Moslik baribir ishlaydi — so'z ustma-ustligi
   orqali — lekin yorliq noto'g'ri. Sotuvchi matni odatda qisqa
   (2-3 so'z) va tuzatadigan boshqa signal yo'q. Indeks o'sgach
   o'zi to'g'rilanadi.

**Yopilgan:** OBER o'z e'lonlarida kategoriya bo'sh edi — endi
`baza.taxminiy_kategoriya()` uni indeksdan aniqlaydi, sotuvchidan
so'ramaydi (12 ta haqiqiy e'lon matnida 12/12).

## Til

Aziz bilan muloqot — o'zbekcha, aniq va qisqa.
Interfeys — o'zbekcha, ruscha tarjima `web/i18n.js` orqali.
Raqamlar bo'shliq bilan: `127 360 so'm`. `toLocaleString` ishlatilmaydi.
