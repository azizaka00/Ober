# OBER — haqiqiy qurilmada sinash rejasi (2026-08-16)

CLAUDE.md dagi ochiq muammo **#2 qoldig'i**: iframe o'lchovi (390px,
yopishqoq element, overflow) brauzerni simulyatsiya qiladi, lekin
haqiqiy qurilma farqlarini ko'rsatmaydi:

- **Teginish** — hover yo'q, bosish maydoni kichik bo'lsa xato
- **Virtual klaviatura** — input fokuslanganda ekran siljishi
- **Safe-area** — iPhone'da pastki chiziq (home indicator), yon qirralar
- **Status bar** — PWA/TWA to'liq ekranda tepadagi soat/batareya bilan
  ustma-ust tushish
- **Kamera** — rasm bilan qidirish va e'lon rasmlari
- **Push bildirishnomalar** — brauzer so'rovchi ruxsat oynasi
- **Offline** — PWA service worker
- **Tezlik** — haqiqiy 4G/Wi-Fi, emulyator emas

---

## 1. Tayyorgarlik

### 1.1. Nima kerak

| Narsa | Izoh |
|---|---|
| Android telefon (7.0+) | Asosiy sinov qurilmasi — TWA va PWA ikkalasi |
| iPhone (ixtiyoriy, 12+) | Safari PWA — safe-area va status bar tekshiruvi |
| OBER APK | `twa-ober/app-release-signed.apk` (allaqachon qurilgan) |
| USB kabel | Chrome DevTools remote debugging uchun |
| O'zbek SIM/Wi-Fi | Push olish uchun internet kerak |

### 1.2. Production yangilanganini tekshirish

Sinovdan oldin ober.uz da oxirgi o'zgarishlar borligini tasdiqlang:

```
curl -s https://ober.uz/ | grep -o 'topbar{position:static}' | head -1
# -> topbar{position:static}   (elon.html mobil tuzatishi, 61cea1b)
```

---

## 2. Sinash yo'llari (3 xil)

### 2.1. Android — TWA ilova (asosiy)

Production'ga chiqariladigan yo'l — Play Store'da shu ko'rinadi:

1. `app-release-signed.apk` ni telefonga yuboring (USB yoki Telegram'da o'zingizga)
2. Faylni oching → "Noma'lum manbalardan o'rnatish" ruxsatini bering
3. **OBER** ikonkasini toping, oching
4. To'liq ekran (brauzer panelisiz) ochilishini tekshiring

### 2.2. Android — Chrome PWA (tezkor variant)

TWA o'rnatilmagan bo'lsa yoki tez tekshirish kerak bo'lsa:

1. Chrome'da `ober.uz` ni oching
2. Menyu (⋮) → **Bosh ekranga qo'shish** (Add to Home screen)
3. Bosh ekrandagi OBER ikonkasidan oching (brauzer paneli yo'q)

### 2.3. iPhone — Safari PWA

1. Safari'da `ober.uz` ni oching
2. Ulashish (⬆) → **Bosh ekranga qo'shish**
3. Safe-area tekshiruvi: pastki chiziq tabbarni yopmasligi kerak

---

## 3. Sinov ro'yxati — sahifalar

Har sahifa uchun: **ikkala til (uz/ru)** + **portret va yotiq rejim**.
Yo'tiq rejim: `orientation: portrait` manifestda — yotiqda qanday
chiqishini tekshiring (mayli, o'ralib turadi — lekin buzilmasin).

| # | Sahifa | URL | Nima tekshiriladi |
|---|---|---|---|
| 1 | Bosh sahifa | `/` | Hero, qidiruv maydoni, jonli lenta (2 qator, yurishi, tegib to'xtashi), kategoriya to'ri, "So'rov yuborish" tugmasi |
| 2 | Qidiruv natijalari | `/?q=divan` | Kartalar 1-2 ustun, saralash chiplari, filtrlar, bo'sh holat |
| 3 | E'lon kartasi | `/elon/1` | Rasm, narx, manba havolasi, yopilgan e'lon holati |
| 4 | Kategoriyalar | `/kategoriyalar` | 2 daraja, breadcrumb, sonlar, bo'sh holat |
| 5 | Chat/takliflar | `/takliflar` | Suhbat ro'yxati, talab bloki (ikkala rol), yozish maydoni |
| 6 | Sotuvchi kabineti | `/sotuvchi` | Kirish (Telegram kodi), e'lon qo'shish, kabinet |
| 7 | Push ruxsati | — | Brauzer so'rovchi oynasi, tasdiqlash, bildirishnoma kelishi |

### 3.1. Bosh sahifa (qidiruv)

- [ ] Qidiruv maydoniga bosing — virtual klaviatura ochilganda layout buzilmaydi
- [ ] "divan" yozing — takliflar real vaqtda chiqadi
- [ ] Natijaga bosing — kartaga o'tadi, orqaga qaytadi (back tugmasi)
- [ ] Rasm bilan qidirish (kamera) — ruxsat so'raladi, surat olinadi

### 3.2. Jonli lenta

- [ ] 2 qator: 1-satr o'ngdan chapga, 2-satr chapdan o'ngga yuradi
- [ ] Qatorga teging — to'xtaydi; surib o'ngga/chapga — yurish davom etadi
- [ ] Yurish batareyani tez yemaydi (60 soniya kuzatish)

### 3.3. Sotuvchi bo'lib (muhim oqim)

1. [ ] `/sotuvchi` → "Kirish" → telefon raqamini kiriting
2. [ ] Telegram'da kod keladi → kiritasiz → kabinet ochiladi
3. [ ] "Yangi e'lon" → nom, narx, rasm (kameradan) → joylashtirish
4. [ ] Kabinetda e'lon ko'rinadi, tahrirlash/o'chirish ishlaydi
5. [ ] Bildirishnoma: xaridor so'rov yuborganda push keladi (ovoz bilan)

### 3.4. Xaridor bo'lib (muhim oqim)

1. [ ] Bosh sahifada "menga divan kerak 3x4" yozib so'rov yuborasiz
2. [ ] Chat bo'limida "so'rovingizga N ta sotuvchi javob berdi" bloki
3. [ ] Sotuvchi javob berganida push bildirishnoma keladi
4. [ ] Chatda javob, narx, rasm almashish ishlaydi

---

## 4. Texnik tekshiruvlar (barcha sahifalar)

### 4.1. Teginish va layout

- [ ] Barcha tugmalar barmoq bilan bosiladigan kattalikda (44px+)
- [ ] Ikkita yopishqoq element yo'q — faqat tabbar
- [ ] Horizontal sirpanish (overflow) yo'q
- [ ] Status bar bilan ustma-ust tushish yo'q (PWA/TWA to'liq ekranda)

### 4.2. PWA/offline

1. [ ] Samolyot rejimini yoqing
2. [ ] Ilovani oching — "o'chirilgan" xabar chiqadi, buzilmaydi
3. [ ] Internet yoqilgach — o'z-o'zidan tuzaladi

### 4.3. Push bildirishnoma

1. [ ] Birinchi ochishda ruxsat so'raladi (TWA'da `enableNotifications`)
2. [ ] Ruxsat berilgach — test bildirishnoma keladi (ovoz bilan)
3. [ ] Ilova yopiq bo'lsa ham bildirishnoma ko'rinadi

### 4.4. Tezlik (real qurilmada)

- [ ] Bosh sahifa 3 soniyada ko'rinadigan bo'ladi (4G, issiq kesh)
- [ ] Qidiruv natijasi 2 soniyada chiqadi
- [ ] Rasm yuklanishi bloklamaydi (lazy loading)

---

## 5. Natijani yozish

Sinovdan keyin shu papkada `NATIJA.md` yarating:

```markdown
# Natija — 2026-08-16

| Qurilma | Android | iPhone |
|---|---|---|
| Model | ... | ... |
| Versiya | ... | ... |
| Yo'l | TWA APK | Safari PWA |

## Topilgan xatolar

| # | Sahifa | Xato | Skrinshot |
|---|---|---|---|
| 1 | ... | ... | ... |

## O'tgan tekshiruvlar

- [ ] 3.1 — ...
- [ ] 3.3 — ...
```

**Har xato uchun skrinshot** (telefonning power+volume-down tugmalari) —
faylni `reports/qurilma-sinov-2026-08-16/` ga tashlang.

---

## 6. Qurilma yo'q bo'lsa — muqobil

Haqiqiy telefon bo'lmasa, Chrome DevTools **Device Mode** (F12 → telefon
ikonkasi) + **touch emulyatsiyasi** eng yaqin muqobil. Lekin safe-area,
kamera, push va haqiqiy teginishni u ko'rsatmaydi — bu #2 ning qoldig'i
shu sabab ochiq.

**Android emulyator** (Android Studio) — kamera va push'ni simulyatsiya
qiladi, lekin o'rnatish og'ir (2+ GB). TWA APK bor bo'lsa, haqiqiy
telefon arzonroq yo'l.

---

## 7. O'tish mezoni (#2 ni yopish)

Quyidagilarning hammasi bajarilsa, #2 to'liq yopiladi:

1. [ ] Android'da TWA o'rnatildi va to'liq ekranda ochildi
2. [ ] 3.1–3.4 oqimlari (xaridor + sotuvchi) ishladi
3. [ ] Push bildirishnoma keladi (ovoz bilan)
4. [ ] Offline holati buzilmaydi
5. [ ] Ikkala til (uz/ru) to'g'ri ko'rinadi
6. [ ] Safe-area/status bar ustma-ust tushishi yo'q (iPhone'da)
7. [ ] `NATIJA.md` yozildi, topilgan xatolar tuzatildi va yuklandi
