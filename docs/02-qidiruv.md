# 02 — QIDIRUV: qanday qurildi va nima o'rganildi
_2026-07-30_

## Muammo (o'lchangan, taxmin emas)

OLX'da `neksiya kolodka` so'rovi → 10 natija, shundan **4 tasi boshqa mashina**
(Трекер, Малибу, Эквинокс). Narx 95 000 – 490 000, izohsiz.

Sotuvchilar bitta so'zni 4 xil imloda yozadi ("chexol chehol chixol chihol") —
chunki qidiruv ishlamaydi va ular buni qoplashga urinadi.

## Yechim: uch qatlam

### 1. Normallashtirish (`lugat.normalla`)
Kirill → lotin, apostroflar olib tashlanadi, va o'zbek yozuvidagi
tebranishlar bir shaklga keltiriladi: `q→k`, `w→v`, `y→i`, `j→z`, `c→s`,
takroriy harf qisqartiriladi.

Natija: `нексия` va `neksiya` — bir xil. `Qoblt` va `kobalt` — bir xil.

### 2. Lug'at (`lugat.MODELLAR`, `lugat.QISMLAR`)
~70 mashina brendi, ~60 qism turi, har biri variantlari bilan.
**Bu loyihaning eng qimmatli qismi** — kod nusxalanadi, lug'at esa vaqt
va ma'lumot bilan yig'iladi.

### 3. Xato yozilishlarni tanish (`lugat._masofa`)
Tahrir masofasi (Levenshtein), foizli o'xshashlik EMAS.

**Nega foiz ishlamadi:**
```
koblt  -> kobalt   1 harf tushgan      = imlo xatosi  (kerak)
gelivi -> geli     2 harf qo'shilgan   = boshqa so'z  (kerak emas)
```
Ikkalasi ham ~0.80 o'xshashlik beradi — ajratib bo'lmaydi.
Tahrir masofasi aniq ajratadi: 1 va 2.

**Ruxsat:** 8 harfgacha 1 ta farq, 9+ harfda 2 ta.
**Qisqa yozuvlar (≤4 harf) taxminiy taqqoslanmaydi** — `geli` (geely)
`gelvi` (gel akkumulyator) dan atigi 1 farqda, xavfli.

### 4. Qo'shimchalar (`lugat.ozak`)
O'zbekcha qo'shimchalar cheksiz: `fara→farasi`, `eshik→eshiklar`,
`zapchast→zapchastlari`. Har shaklni yozish o'rniga qo'shimcha tanib
o'zagi taqqoslanadi. Undosh yumshashi ham: `eshigi→eshik`.

## Qidiruv mantiqi (`qidiruv.qidir`)

1. **Qism turi MAJBURIY** — so'rovda ko'rsatilgan bo'lsa, mos kelmagan e'lon
   tashlanadi. (Xato edi: model mos kelsa yetarli deb hisoblardim, natijada
   `neksiya kolodka` so'roviga Neksiyaning *tumanka*si va *katushka*si chiqardi.)
2. **Model mos kelmasa — kesiladi.** Modeli ko'rsatilmagan umumiy e'lon qoladi,
   lekin pastroqda. **Bu OLX'dagi asosiy muammoni yechadi.**
3. Qo'shimcha ball: tuman yaqinligi · narxi borligi · do'kon · rasm · yangilik

## Natija (1607 e'lon ustida)

| So'rov | Kesildi | Holat |
|---|---|---|
| `kobalt fara` | 68 | 5 tasi ham to'g'ri ✅ |
| `матиз бампер` | 66 | begona model qolmadi ✅ |
| `spark rul` | 24 | tepadagi 3 tasi to'g'ri ✅ |
| `akumlyator` + Sergeli | — | 5 tasi ham Sergelida ✅ |
| `neksiya kolodka` | 28 | 15 natija (avval 2 edi) |

`neksiya kolodka` va `нексия колодка` — **aynan bir xil natija.**

Lug'at sinovi: **21 holatdan 21 tasi** (`lugat_sinov.py`).

## Lug'atni to'ldirish — qo'lda emas, ma'lumotdan

`nomalum.py` e'lonlarda tez uchraydigan, lekin lug'atга tushmagan so'zlarni
topadi. Ya'ni lug'at **taxmin bilan emas, haqiqiy ehtiyoj bo'yicha** to'ladi.

Shu yo'l bilan topilgan qismlar: `galofka`(lampa) · `suport` · `oblisovka` ·
`richag` · `kabina` · `bagaj` · `kuzov` · `most` · `injektor` · `zaslonka` ·
`katalizator` · `trambler` · `spidometr` · `ftulka` · `podushka` va h.k.

Noma'lum so'zlar: 1636 → 1536 → 1428 (eng yuqori chastota 80 → 25 → 20).

**To'xtash mezoni:** qolgan so'zlar 1607 e'londa 5-7 martadan uchraydi (0.4%) —
natijaga ta'sir qilmaydi. Ma'lumot ko'paygach ro'yxat o'zi aniqlashadi.

## Saboq

**Lug'atda so'z bo'lmasa, taxminiy moslashtiruv eng yaqin NOTO'G'RI narsani
ilib oladi.** (`galofka` → `kalodka` deb tanilgan edi.)
Ya'ni qamrov aniqlikni belgilaydi — taxminiy topishni bo'shatish emas.

Ko'rilgan variant har doim lug'atга yoziladi; taxminiy topish faqat
**ko'rilmagan** xatolar uchun.
