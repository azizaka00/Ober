---
name: ober-frontend
description: OBER frontend qoidalari — dizayn tizimi, uch qavatli quyuq rejim, amber urg'u tili, web_sinov qoidalari, sinov oqimi. web/ ichida har qanday o'zgarishdan OLDIN o'qiladi.
---

# OBER Frontend — loyiha qoidalari

OBER — ish quroli, reklama sahifasi emas. Sozlagichlar: **Layout 3 · Harakat 2 · Zichlik 8**. Odam bu yerga tomosha qilgani emas, topgani keladi — birinchi ekranda haqiqiy tovar ko'rinsin.

`CLAUDE.md` va `OBER-DIZAYN-QOIDALARI.md` har seans boshida o'qiladi. Bu skill ularning **eng tez buziladigan** qoidalarini va 2026-08-11 redesign'da o'lchangan yangi qarorlarni kodlaydi.

## 1. O'zgarmas texnologiya

- Har sahifa bitta HTML fayl — CSS ham, JS ham ichida. Framework yo'q, build yo'q.
- Backend Python standart kutubxonasi. Yangi bog'liqlikdan oldin: **busiz bo'ladimi?**
- Shrift o'z serverimizda (`web/shrift/`), Google CDN ishlatilmaydi.
- Yangi kutubxona qo'shilmaydi. Agar sinov uchun PNG tahlili kerak bo'lsa — PIL yo'q, sof Python dekoder yoziladi (skrinshotlar RGB, 3 bayt/piksel).

## 2. Dizayn tizimi (tokenlar)

Asosiy tokenlar `web/ober-ui.css` `:root`'ida (barcha sahifaga keladi). Har sahifaning o'z `:root`'ida esa amber oilasi bo'lishi **shart**:

```
--amber:#f5a623   --amber-deep:#e08d00   --amber-line:#f3d9a8   --amber-soft:#fdf3de
```

⚠️ `web/tabbar.js` `var(--amber-deep)` va `var(--amber-soft)` ishlatadi — tabbar **barcha** sahifada yuklanadi. Shuning uchun amber tokenlari 5 sahifaning hammasida bo'lishi kerak (`index`, `kategoriyalar`, `takliflar`, `sotuvchi`, `elon`). 2026-08-11: `elon.html` da `--amber-deep` yo'q edi — buzilgan token. Tekshirish: `grep -c -- '--amber-deep' web/*.html`.

**Rang tili — bitta urg'u:**
- `--navy` — brend rangi. Quyuq rejimda O'ZGARTIRILMAYDI (brend tugma gradienti).
- **Amber = asosiy CTA tili.** Gradient `linear-gradient(180deg,#ffc24d,#f59e0b)`, matn `#231400`. Hover soyasi `--cta-glow` (ober-ui.css da bir joyda, amber).
- **Yashil faqat ma'no tashiganda** — allaqachon tanlangan, yoqilgan. Qizil faqat xato/kesilgan.

**Burchak — to'rtta qiymat, boshqasi yo'q:** `--r-kichik:10px` (input/tugma) · `--r-orta:14px` (karta) · `--r-katta:20px` (panel/qidiruv) · `--r-pill:999px` (chip). Xom `16px`, `12px` yozish taqiqlanadi. Kichik dekorativ belgilar uchun `--r-belgi:5px` (nomlangan, `--r-quyruq` sabog'i bilan bir xil).

## 3. Quyuq rejim — UCH QAVAT (2026-08-11, eng muhim)

`web/index.html` CSS'i uch qavatli:

1. **Asosiy (yorug')** — tokenlar o'z holida.
2. **`body:not(.is-results)`** — bosh sahifa quyuq (kechki bozor, A varianti).
3. **`body.is-results`** — natija sahifasi quyuq: token qayta belgilash (hammasi avtomatik quyuqlashadi) + qattiq ranglar alohida.

Qoidalar:
- Yangi komponent qo'shilsa — **uchala qavatda ham** tekshiriladi.
- Qavatda token o'zgartirish afzal; qattiq rang faqat token yetmaganida.
- Quyuq qoidalar `</style>` oldida turishi shart — teng og'irlikda **faylda keyingisi yutadi**.
- `body:not(.is-results)` boshqa sahifalarga ham tegadi (ular ham `is-results` emas!). Umumiy qoida yozayotganda buni hisobga ol — kod review bir marta shu sabab xato tutgan (tabbar boshqa sahifalarda ham quyuq bo'lib qolgan edi).
- Quyuqda yashil ma'no ranglari yorug'lashadi: `#0f7a4a` → `#5fd3a3` kabi, aks holda ko'rinmaydi.
- Quyuqda `--navy-soft` kabi "soft" fonlar shaffof oq (`rgba(255,255,255,.1)`-oilasi) bilan almashadi.

## 4. Amber urg'u qo'llash

| Element | Holat |
|---|---|
| Asosiy CTA (Topish, Yuborish, Kirish, Saqlash, Yangi e'lon) | amber gradient |
| `+ E'lon` tab (tabbar.js), "Sotish" pill | amber gradient |
| Faol tab (`.ober-tab.faol`) | `--amber-deep` matn + `--amber-soft` fon |
| Tanlangan saralash chip (`.tartib-btn.tanlangan`) | amber gradient, matn `#231400` |
| Karta hover urg'usi (`.kat-karta`) | tepa chiziq amber gradient, hover fon amber-soft |
| Breadcrumb urg'u, qidiruv fokus halqasi | amber |
| O'qilmagan nishon (`.ober-top-nishon`) | `--amber-deep` |

Yashil holatlar saqlanadi — ular ma'no tashiydi ("allaqachon tanlangan", "yoqilgan"). Amber urg'uni yashilga almashtirmaslik.

## 5. web_sinov.py qoidalari (buzilgan → brauzer butunlay yiqilishi mumkin)

Har `web/` o'zgarishidan keyin `cd app && python web_sinov.py` ishga tushiriladi:

1. **`[hidden]{display:none!important}` har sahifada bo'lishi shart** — xato uch marta takrorlangan.
2. **JS ichida `<!--` izohi UMUMAN bo'lmaydi.** Shablon satriga tushsa va ichida teskari apostrof bo'lsa — butun skript yiqiladi, sahifa bo'sh ochiladi. Izoh kerak bo'lsa `//` yoki `/* */`.
3. **Teskari apostrof juft bo'lsin** — toq bo'lsa template literal yopilmagan.
4. Skript ichida `</script` matni bo'lmasin.
5. **Telefonda yopishqoq element bitta** — `sotuvchi/takliflar/kategoriyalar` da `.topbar` `max-width:6xx` media'da `position:static/absolute` bo'lishi shart (tabbar yopishqoq qoladi).
6. `index.html`: `body:not(.is-results) .topbar` chegarasi `transparent` + `box-shadow:none` (shaffof panel hero ustida chiziq qoldirmasin).
7. **Xom amber CTA rangi sahifalarda bo'lmaydi** — faqat `ober-ui.css` dagi token ta'rifida: `var(--cta-gradient)`, `var(--on-cta)`, `var(--amber-yorqin)` ishlatiladi. 90deg/100deg maxsus gradientlar (tanlangan chip, hero amb) ataylab qoldirilgan — takrorlanmasa.

## 6. Sinov oqimi (har o'zgarishdan keyin, majburiy)

1. `cd app && python web_sinov.py` → **0 xato** bo'lishi shart.
2. `python i18n_sinov.py` → 0 xato.
3. Ruscha tarjima: yangi o'zbekcha qator qo'shilsa `web/i18n.js` dagi ruscha qolip ham yangilanadi (dinamik qoliplar bir xil qurilishda — `«...»` almashuvi regex bilan emas, qolip bilan).
4. **Skrinshot** (Chrome headless, `--virtual-time-budget=9000`): 1280×1400 (desktop) + 390×1800 (mobil). Manzil `reports/redesign-dsrupt-2026-08-11/`.
5. **Piksel tahlili**: amber va quyuqlik ulushini o'lcha (sof Python PNG dekoder). Amber 0% chiqsa — urg'u ekranda yo'q, sababini top.
6. **Real DOM computed-style**: kichik test sahifa qurib, asosiy komponentlarning hisoblangan ranglarini isbotla (piksel — rangni, DOM — qoida ishlaganini ko'rsatadi).
7. Vaqtinchalik fayllarni o'chir, `web/_*.html` qoldirmaslik.

## 7. Tez buziladigan dizayn qoidalari

- **Kicker/eyebrow taqiqlanadi** (AI belgisi). Sarlavha + izoh + kontent o'rniga — faqat kontent.
- **Layout xossalari animatsiya qilinmaydi**: `width/height/padding/top/min-height`. Faqat `opacity/transform/color/border`. Davomiylik ≤ 220 ms.
- **`max-height` bilan ochish-yopish taqiqlanadi** (kontent kesiladi). `display:none → grid` darhol + `opacity/transform` surish.
- **`@media` avtomatik g'olib emas** — teng og'irlikda faylda keyingisi yutadi. Bekor qilmoqchi bo'lsang: kamida shunday og'ir va keyinroq.
- **Telefonda yopishqoq element eng ko'pi bilan bitta.**
- **Grid ustunlari soni = bolalar soni.** Yangi tugma qo'shsang `grid-template-columns` ni ham sana.
- **Soxta ma'lumot yo'q.** Demo kerak bo'lsa — bazadan haqiqiy e'lon. `"Aziz Nematov"`, `99.9%` yozilmaydi.
- **Raqamlar bo'shliq bilan**: `127 360 so'm`. `toLocaleString` ishlatilmaydi — `formatInt()`.
- **Sanalar o'zbekcha nisbiy**: Bugun / Kecha / 2 kun oldin / 23 iyul. Xom sana chiqarilmaydi.
- **Manba har doim ko'rsatiladi** (OLX / Telegram) — yolg'on manba ishonchni buzadi.
- **To'rt holat**: yuklanmoqda (skelet) / bor / yo'q (nima qilish kerakligi aytiladi) / xato (odamga tushunarli + konsolga sabab).

## 8. Fayl xaritasi

| Fayl | Nima | Umumiymi? |
|---|---|---|
| `web/index.html` | Bosh + natija sahifasi — eng katta, uch qavatli quyuq | — |
| `web/kategoriyalar.html` | Ikki darajali daraxt, breadcrumb | — |
| `web/takliflar.html` | Chat / inbox | — |
| `web/sotuvchi.html` | Sotuvchi kabineti (kirish, e'lon, Telegram kartasi) | — |
| `web/elon.html` | E'lon kartasi | — |
| `web/ober-ui.css` | **Tokenlar, `--cta-glow`, `.empty-misol/.empty-tozalash`** — har o'zgarish barcha sahifaga ta'sir qiladi | ✅ |
| `web/tabbar.js` | 4 tab, amber faol, `+ E'lon` — barcha sahifaga ta'sir qiladi | ✅ |
| `web/i18n.js` | Ruscha tarjima | ✅ |

Umumiy faylni o'zgartirgach — **barcha 5 sahifani** tekshir (qoida bir faylda tuzatilib, boshqasida buzilgan qolmasin).

## 9. O'lchov madaniyati

- **"Yaxshi ko'rinadi" — dalil emas.** Har layout qarori raqam bilan tasdiqlanadi.
- **Sekinlikning sababi ko'pincha muhitda** (SQLite qulfi, Caddy, DNS) — avval o'lcha, keyin optimallashtir.
- Brauzer fon rejimidagi tabda `loading="lazy"` rasmlar yuklanmaydi — test artefakti, xato emas.
- Har ishdan keyin `memory/lessons.md` ga bitta xulosa yoziladi.
