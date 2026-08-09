# OBER — DIZAYN BRIFI (Codex uchun)

Sana: 2026-07-31 · Buyurtmachi: Aziz
Bu hujjat `CODEX-HANDOFF.md` bilan **birga** o'qiladi. U yerda mahsulot
mantiqi, bu yerda ko'rinish. Mantiqni buzmasdan ko'rinishni qurish kerak.

---

## 0. Vazifa bir jumlada

OBER — O'zbekistondagi **teskari bozor**. Frontend shu darajada bo'lishi
kerakki, odam saytga kirganda "bu jiddiy mahsulot" desin, "yana bitta
o'zbek sayti" demasin.

**Talab: zamonaviy, minimalistik, lekin ODDIY EMAS.**

Bu ikkisi qarama-qarshi emas. Minimalizm — ortiqchani olib tashlash.
Oddiylik — hech narsa qilmaslik. Farqi kompozitsiya, ritm, tipografika
va harakatda. Bo'sh oq sahifa minimalistik emas, u shunchaki bo'sh.

---

## 1. Brend

Logotip va ikonka fayllari beriladi (`web/brend/` papkasiga qo'ying).

**Belgi:** kvadrat ichida halqa, halqa ikki joydan kesilgan va markazda
to'liq doira. O'qilishi: **halqa — bozor, markaz — so'rov, kesiklar —
so'rovning ikki tomonga (xaridor va sotuvchi) chiqishi.** Bu ma'noni
dizaynda ishlating: yuklanish animatsiyasi, bo'sh holat belgisi, bo'lim
ajratgichi shu shakldan kelib chiqsin.

**So'z belgisi:** `ober` — kichik harflarda, geometrik grotesk, juda
qalin emas, `r` harfi ochiq. Nuqta yo'q, shior yo'q.

### Ranglar

| Rol | Qiymat | Qayerda |
|---|---|---|
| Asos (navy) | `#0B2559` (aniq qiymatni fayldan oling) | logotip, asosiy tugma, urg'u |
| Asos-quyuq | `#081B42` | hover, bosilgan holat |
| Fon | `#FBFBFA` | sahifa foni |
| Sirt | `#FFFFFF` | kartalar |
| Chegara | `#E8E8E6` | ajratgichlar |
| Matn | `#16181D` | asosiy matn |
| Ikkilamchi matn | `#6B7280` | meta, izoh |
| Yashil (tasdiq) | `#0F7A4A` | "BOR", muvaffaqiyat |
| Qizil (rad) | `#C0392B` | "YO'Q", xato |
| Sariq (byudjet) | `#F5A623` | byudjet nishoni |

**DIQQAT:** hozirgi kodda asos rang yashil (`--asos:#0f5c4a`). Uni
**navy'ga almashtiring** — brend shu. Yashil faqat "BOR"/tasdiq uchun
qoladi.

Gradient ishlatilmaydi. Neon, glow, shisha effekti (glassmorphism)
ishlatilmaydi — ular 2021 yil va ular arzon ko'rinadi.

### Tipografika

- Sarlavha: geometrik grotesk (Inter Tight, Manrope yoki shunga o'xshash),
  `font-weight: 700`, `letter-spacing: -0.02em`
- Matn: bir xil oila, `400/500`
- **Faqat lotin va kirill qismini yuklang** (subset). O'zbek foydalanuvchi
  arzon telefonda va 4G'da — 200KB shrift qabul qilinmaydi.
- Zaxira: `-apple-system, "Segoe UI", Roboto, Arial`

Miqyos (mobil / desktop):

```
Ulkan sarlavha   28 / 40
Sarlavha         20 / 24
Kichik sarlavha  16 / 18
Matn             15 / 15
Meta             13 / 13
Mayda            11.5 / 12
```

---

## 2. Nima "oddiy emas" degani — aniq talablar

Quyidagilar bo'lmasa ish qabul qilinmaydi:

1. **Qidiruv maydoni sahifaning qahramoni.** Kichkina yuqoridagi input
   emas. Birinchi ekranda katta, markazda, aniq. Odam nima qilishini
   bir soniyada tushunsin.

2. **Natija chiqqanda sahifa QAYTA QURILADI, sakramaydi.** Qidiruv maydoni
   yuqoriga siljiydi (transform bilan, `position` almashtirmasdan),
   natijalar pastdan chiqadi. Bir tekis, 200-250ms.

3. **Skeleton yuklanish.** "Qidirilmoqda…" yozuvi emas — kartalarning
   kulrang shakli. Odam nima kelishini oldindan ko'radi.

4. **Narx bloki — alohida kompozitsiya.** Hozir u oddiy matn qatori.
   Kerak: katta raqamli oraliq, ostida kichik izoh, yonida mayda
   gistogramma (narxlar qanday taqsimlangani). Bu OBER'ning eng qimmatli
   ekrani — odam shu yerda "ha, bu foydali" deydi.

5. **"So'rovni tushundik" bloki ko'rinsin.** Tizim nimani tushunganini
   ko'rsatish (`mashina: cobalt · qism: fara · 548 ta boshqa mashina
   kesildi`) — bu bizning asosiy farqimiz, uni mayda kulrang matnda
   yashirmang. Nishonlar (chip) ko'rinishida bering.

6. **Karta ustida harakat.** Hover'da ko'tarilish (`translateY(-2px)` +
   yumshoq soya), 120ms. Mobil'da bosilganda `scale(0.98)`.

7. **Bo'sh holat chiroyli bo'lsin.** "Topilmadi" — bu boshi berk ko'cha
   emas, bu so'rov qoldirish uchun eng yaxshi payt. Brend belgisidan
   foydalangan chizma + aniq harakatga chaqiruv.

8. **Sotuvchi javobi kelganda sezilsin.** Yangi javob paydo bo'lganda
   yumshoq urg'u (fon bir marta yorishadi, 400ms), telefon tebranadi
   (`navigator.vibrate(30)`), sarlavhada son o'zgaradi.

---

## 3. Ekranlar

### 3.1 Xaridor — bosh sahifa (`web/index.html`)

**Birinchi ekran (natija yo'q):**
- Logotip chapda, "Sotuvchimisiz?" o'ngda
- Markazda: katta sarlavha + qidiruv maydoni
- Ostida: joy tanlash (ikki bosqichli — viloyat, keyin shahar)
- Ostida: namuna so'rovlar (chip ko'rinishida, bosilsa qidiradi)
- Pastda mayda: bazada nechta e'lon borligi — ishonch signali

**Natija ekrani, tartib bilan:**
1. Narx bloki (oraliq + odatiy narx + eng arzoni + gistogramma)
2. "So'rovni tushundik" nishonlari
3. So'rov qoldirish bloki — **natijalar ORASIDA emas, tepasida yoki
   3-natijadan keyin**. U ko'rinishi kerak, lekin natijani to'smasin.
4. Kartalar to'ri

**Karta:**
- Rasm (nisbat 4:3, `object-fit: cover`, `loading="lazy"`)
- Rasm yo'q bo'lsa — brend belgisidan naqsh, "rasm yo'q" degan bo'sh
  kulrang quti emas
- Nom (2 qatorgacha, keyin `...`)
- Narx — eng katta element kartada
- Meta: joy · sana · nishonlar (DO'KON / yangi / yaqin)

### 3.2 Sotuvchi kabineti (`web/sotuvchi.html`)

**Bu ekranda dizayn muhimroq**, chunki sotuvchi qolishi butun bozorni
hal qiladi.

- Ro'yxatdan o'tish: **ikki savol, 30 soniya.** Bitta ekran, uchta
  maydon, bitta tugma. Kategoriya daraxti YO'Q.
- Tizim nimani tushunganini darhol ko'rsatadi ("Tushundik: fara, stop")
- So'rov kartasi: so'rov matni katta, meta kichik
- **Uchta tugma bir qatorda, barmoq uchun katta (min 48px balandlik):**
  `BOR` (navy, to'ldirilgan) · `YO'Q` (kontur) · `O'XSHASHI BOR` (kontur)
- `BOR` bosilsa — faqat narx maydoni ochiladi, boshqa hech narsa
- Javob berilgach: yashil tasdiq, keyin karta silliq yo'qoladi va
  ro'yxat qayta chiziladi

### 3.3 Mobil (asosiy ekran — trafikning 80%+ shu yerda)

- **Mobil-birinchi qurilsin**, desktop kengaytma sifatida
- Sinish nuqtalari: 360 / 390 / 768 / 1024 / 1280
- Kartalar: mobilda 1 ustun, 768+ da 2, 1024+ da 3
- Barcha bosiladigan element **min 44×44px**
- Qidiruv maydoni mobilda pastda qolib ketmasin — klaviatura
  ochilganda ham ko'rinsin
- Gorizontal skroll BO'LMASIN (360px da tekshiring)

---

## 4. Harakat (motion)

Kam, lekin aniq. Har harakatning sababi bo'lsin.

- Davomiylik: 120ms (mayda), 200ms (o'tish), 400ms (urg'u)
- Egri chiziq: `cubic-bezier(0.2, 0, 0, 1)`
- `prefers-reduced-motion` hurmat qilinsin
- Doimiy aylanuvchi, pulsatsiya qiluvchi bezaklar YO'Q

Yuklanish belgisi — brend halqasi asosida (kesikli halqa aylanadi).

---

## 5. Texnik cheklovlar (buzilmaydi)

- **Bir faylli HTML** — CSS va JS ichida. Build yo'q, npm yo'q, React yo'q.
  Sabab: `CODEX-HANDOFF.md` 2-bo'lim.
- Tashqi kutubxona yuklanmaydi (shriftdan tashqari)
- API o'zgarmaydi — `CODEX-HANDOFF.md` 9-bo'limdagi kelishuv saqlanadi
- Rasm manzillari OLX CDN'idan keladi — `loading="lazy"` majburiy,
  9 000+ e'lon bor
- `localStorage` kalitlari saqlanadi: `ober_viloyat`, `ober_joy`,
  `ober_sorov`, `ober_sorov_matn`, `ober_sotuvchi`

---

## 6. Nima QILINMAYDI

- Gradient fon, neon, glow, glassmorphism
- Aylanuvchi bezaklar, parallaks, skroll animatsiyasi
- Stock fotosuratlar, emoji ikonkalar (📍 dan tashqari — u allaqachon bor,
  uni SVG ga almashtirsangiz yaxshi)
- "Bizning afzalliklarimiz" kabi marketing bloklari — sayt ish qiladi,
  o'zini maqtamaydi
- Modal oynalar (so'rov qoldirish sahifada bo'ladi, modal'da emas)
- Ro'yxatdan o'tishni majburlash — xaridor hech narsa kiritmasdan
  qidira olishi shart

---

## 7. Qabul mezonlari

Ish tugadi deyish uchun quyidagilar tekshirilishi kerak:

1. 360px, 390px, 768px, 1280px kengliklarda gorizontal skroll yo'q
2. Klaviatura bilan to'liq boshqarish mumkin (Tab, Enter), fokus
   ko'rinadi
3. Matn va fon kontrasti WCAG AA (4.5:1)
4. Sekin tarmoqda (Slow 4G) birinchi ekran 2 soniyada chiqadi
5. Skeleton ko'rinadi, sahifa sakramaydi (CLS ~0)
6. To'liq halqa ishlaydi: qidiruv -> so'rov -> sotuvchi javobi ->
   xaridor javobni ko'radi
7. Console'da xato yo'q
8. Haqiqiy telefonda ochib ko'rilgan (emulyator emas)

---

## 8. Ish tartibi (tavsiya)

1. Avval **dizayn tizimi**: ranglar, tipografika, oraliqlar, tugma va
   karta ko'rinishlari — bitta `<style>` blokida CSS o'zgaruvchilari
   bilan
2. Keyin **mobil** ko'rinish, to'liq
3. Keyin **desktop** kengaytma
4. Oxirida **harakat va tafsilotlar**

Har bosqichda skrinshot oling va Azizga ko'rsating. U "sezilarli
o'zgarish yo'q" desa — demak kompozitsiya emas, faqat bezak
o'zgargan. Bu xato allaqachon bir marta qilingan (NAIZA loyihasida).
