# Natija — 2026-08-16

## 0. Kompyuterda o'lchangan (production tayyorligi)

REJA.md ning texnik qismi haqiqiy qurilmadan oldin server darajasida
o'lchandi. Bular PWA/TWA ishlashining SHARTI — barchasi tasdiqlandi:

| # | Tekshiruv | O'lchov | Holat |
|---|---|---|---|
| 0.1 | Service worker xizmat qiladi | `GET /sw.js` → **200** | ✅ |
| 0.2 | Push kalit mavjud | `GET /api/push-kalit` → `{"kalit": "BCmX..."}` (64 bayt) | ✅ |
| 0.3 | Manifest xizmat qiladi | `GET /manifest.json` → **200** | ✅ |
| 0.4 | Kesh manzillari (13 ta) | `/`, `/kategoriyalar`, `/takliflar`, `/sotuvchi`, `/privacy`, ikonlar, css/js — **barchasi 200** | ✅ |
| 0.5 | SW registratsiya kodi | `index.html` da `navigator.serviceWorker.register("/sw.js",{scope:"/"})` | ✅ |
| 0.6 | Offline logika | sw.js: `fetch` → tarmoq, yiqilsa kesh zaxirasi (`KESH_MANZIL`), bosh sahifa fallback | ✅ |
| 0.7 | Push bildirishnoma | `push` hodisasi → `showNotification` (`userVisibleOnly` sharti bajariladi), `vibrate:[200,100,200]` (jingirlash) | ✅ |
| 0.8 | Privacy sahifasi | `GET /privacy` → **200** (Play Store talabi) | ✅ |

**Eslatma:** headless Chrome'da SW registratsiyasi o'lchanmadi (SW
secure context + real brauzer talab qiladi) — bu quyidagi qurilma
bandlarida tekshiriladi.

---

## 1. Qurilma ma'lumotlari

| Qurilma | Android | iPhone |
|---|---|---|
| Model | (to'ldiring) | (to'ldiring) |
| Versiya | (to'ldiring) | (to'ldiring) |
| Yo'l | TWA APK / Chrome PWA | Safari PWA |

## 2. O'rnatish va ochilish

- [ ] `app-release-signed.apk` o'rnatildi
- [ ] OBER ikonkasi bosh ekranda
- [ ] To'liq ekran (brauzer panelisiz) ochiladi — assetlinks to'g'ri
- [ ] Status bar (soat/batareya) tepa panel bilan ustma-ust tushmaydi
- [ ] Pastki tabbar safe-area chizig'ini yopmaydi (iPhone'da)
- [ ] Yorqinlik/qorong'ulik rejimiga moslashadi (agar qo'llasa)

## 3. Bosh sahifa

- [ ] Hero va qidiruv maydoni to'g'ri joylashgan
- [ ] Qidiruv maydoniga bosilganda virtual klaviatura layoutni buzmaydi
- [ ] Jonli lenta: 2 qator — 1-satr o'ngdan chapga, 2-satr chapdan o'ngga yuradi
- [ ] Lentaga teging — to'xtaydi; surib qo'ysangiz davom etadi
- [ ] Kategoriya to'ri bosiladi, to'g'ri sahifaga o'tadi
- [ ] "So'rov yuborish" tugmasi ko'rinadi va bosiladi

## 4. Qidiruv

- [ ] "divan" yozib qidirish — natijalar chiqadi
- [ ] Natija kartalari 1-2 ustunda to'g'ri ko'rinadi
- [ ] Saralash chiplari bosiladi, ishlaydi
- [ ] Filtrlar ochiladi/yopiladi
- [ ] E'lon kartasiga o'tish va orqaga qaytish ishlaydi
- [ ] Rasm bilan qidirish: kamera ruxsati so'raladi, surat olinadi

## 5. Xaridor oqimi

- [ ] "menga divan kerak 3x4" so'rov yuborildi
- [ ] Chat bo'limida "so'rovingizga N ta sotuvchi javob berdi" bloki
- [ ] Sotuvchi javob berganida push bildirishnoma keldi (ovoz/vibratsiya)
- [ ] Bildirishnomani bossangiz chat ochiladi
- [ ] Chatda yozish, rasm yuborish ishlaydi

## 6. Sotuvchi oqimi

- [ ] `/sotuvchi` → kirish → telefon raqami
- [ ] Telegram'da kod keldi, kirish o'tdi
- [ ] Yangi e'lon qo'shish: nom, narx, kameradan rasm
- [ ] Kabinetda e'lon ko'rinadi, tahrirlash/o'chirish ishlaydi
- [ ] Xaridor so'roviga bildirishnoma keldi

## 7. Offline

- [ ] Samolyot rejimi yoqildi
- [ ] Ilova ochildi — bosh sahifa zaxiradan chiqdi (buzilmadi)
- [ ] Internet yoqilgach o'z-o'zidan tuzaladi

## 8. Til (uz/ru)

- [ ] O'zbekcha ko'rinish to'g'ri
- [ ] Ruschaga o'tish (agar sozda bo'lsa) to'g'ri
- [ ] Ruschada ham layout buzilmaydi (uzun so'zlar)

## 9. Tezlik (4G/Wi-Fi)

**Server tomondan o'lchov (2026-08-16, ober.uz dan):**

| Tekshiruv | O'lchov (3 ta o'rtacha) | Holat |
|---|---|---|
| Bosh sahifa (issiq) | **0.72–0.75 s** | ✅ 3 s me'yoridan ancha past |
| Qidiruv API ("divan") | **0.73–0.92 s** | ✅ 2 s me'yoridan past |
| Rasm (logo) | **0.75 s** | ✅ bloklamaydi |

> Server tomondan cheklov yo'q — qolgan tekshiruv haqiqiy 4G
> qurilmada hissiyot uchun (TTSB ~0.7 s + 4G kechikish).

- [ ] Bosh sahifa 3 soniyada ko'rinadi (issiq kesh)
- [ ] Qidiruv natijasi 2 soniyada chiqadi
- [ ] Rasm yuklanishi bloklamaydi

---

## Topilgan xatolar

| # | Sahifa | Xato | Skrinshot |
|---|---|---|---|
| | | | |

---

## Xulosa

(To'ldiring: nima ishladi, nima buzildi, #2 yopiladimi)
