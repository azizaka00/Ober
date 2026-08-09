# OBER — o'z marketplace'i: sotuvchi e'lon joylashtirishi

**Sana:** 2026-08-06 · **Holat:** amalga oshirilmoqda · **Muallif:** Buffy

---

## 0. Bosqich holati

| Bosqich | Holat | Eslatma |
|---|---|---|
| 1. Baza funksiyalari + migratsiya | ✅ bajarildi | `egasi`, `elon_holati`, `yangilandi`, `rasmlar_ober` + 5 funksiya |
| 2. API endpointlar | 🔄 davom etmoqda | `/api/elon`, `/api/sotuvchi/elonlari`, tahrir/ochir |
| 3. Kabinet "E'lonlarim" + forma | ⬜ qoldi | Tablar: So'rovlar / E'lonlarim |
| 4. Tahlilga ulash (darhol qidiruvga) | ⬜ qoldi | bitta e'lon uchun tahlil chaqiruv |
| 5. E'lon sahifasi `/elon/{id}` | ⬜ qoldi | rasm galereyasi, telefon, chat |
| 6. MANBA_NOM + badge | ⬜ qoldi | `ober` belgisi |
| 7. To'liq test + deploy | ⬜ qoldi | mobil + desktop + API |

---

## 1. Maqsad

Sotuvchi OBER'da **o'z e'lonini joylashtiradigan** bo'lsin va bu e'lon
OLX/Telegram e'lonlari bilan **bir qatorda qidiruvda chiqsin**.

Bu OBER'ni "yig'uvchi portal"dan **haqiqiy bozor**ga aylantiradi:

- Hozir OBER faqat boshqa bozorlardan e'lon oladi — odam o'z e'lonini
  OBER'da joylashtira olmaydi.
- Agar sotuvchi e'lonni OBER'ga yozsa, OBER endi **rahmat qarzdor
  emas** — uning o'z bazasi o'sadi, OLX'ning o'chirib qo'yish xavfi
  yo'qoladi.
- E'lon egasi **kabinet orqali** narxni o'zgartira oladi, "sotildi"
  deya o'chira oladi — yig'ilgan e'lonlarda bu imkoniyat yo'q.

**Nima EMAS:** bu bosqichda to'lov, premium, banner, bot qidiruv
kerak emas. Eng oddiy ishlaydigan halqa birinchi.

---

## 2. Hozirgi holat (2026-08-06 da o'lchandi)

| Qism | Holat | Izoh |
|---|---|---|
| `elonlar` jadvali | ✅ tayyor | `manba` ustuni bor: `olx` / `telegram`. `sotuvchi_id` ustuni bor. |
| `baza.saqla(e)` | ✅ tayyor | Har qanday adapter shu orqali yozadi. Yangi manba = yangi `manba` qiymati. |
| Qidiruv FTS indeksi | ✅ tayyor | `tahlil.py` → `fts_qur.py`. Yangi e'lon tahlil qilinsa avtomatik kiradi. |
| Sotuvchi kabinet | ✅ tayyor | Telefon + Telegram kodi + token-sessiya. Kabinet mavjud. |
| Rasm yuklash | ✅ tayyor | Chatda ishlaydi: JPG/PNG/WEBP, 5 MB, `_rasm_saqla()`. |
| Joylar daraxti | ✅ tayyor | `joylar.py` — viloyat→shahar→tuman. |
| Xaridor kartasi | ✅ tayyor | `MANBA_NOM` belgisi bilan manba ko'rinadi. |
| Yangi manba adapter | 🔴 yo'q | "ober" manbasi uchun alohida adapter yo'q — **bu rejaning o'zi** |

Muhim kuzatuv: `elonlar` jadvalidagi `sotuvchi_id` ustuni hozir
"manbadagi sotuvchi profili" uchun ishlatiladi (OLX profili). OBER
e'lonlari uchun bu ustunni **OBER'dagi `sotuvchilar.id`** deb
ishlatamiz — yangi ustun kerak emas, `manba='ober'` yetarli farqlovchi.

---

## 3. Foydalanuvchi oqimi (sotuvchi tomonda)

```
Kabinetga kirish (bor)
   └─ "E'lon joylashtirish" tugmasi
        └─ Forma:
             • Nima sotasiz?        (nom — majburiy)
             • Narx                 (so'm, ixtiyoriy — "Kelishiladi")
             • Kategoriya           (tayyor daraxtdan tanlash)
             • Joy                  (viloyat → shahar/tuman)
             • Rasm                 (1-5 dona, 5 MB gacha, ixtiyoriy)
             • Tavsif               (ixtiyoriy, 2000 belgi)
             • Telefon              (kabinetdan avtomatik, ko'rsatiladi)
        └─ Oldindan ko'rish
        └─ "Joylashtirish" → manba='ober' e'lon yoziladi
             └─ E'lon darhol qidiruvga kiradi (avtomatik tahlil)
             └─ Kabinetda "E'lonlarim" ro'yxatida turadi
```

Xaridor tomonda hech narsa o'zgarmaydi — e'lon oddiy karta bo'lib
chiqadi, belgisi "OBER" bo'ladi, manba havolasi OBER'ning o'z
sahifasiga boradi.

---

## 4. Baza o'zgarishlari (minimal)

### 4.1. Yangi ustunlar — `elonlar` jadvaliga

```sql
ALTER TABLE elonlar ADD COLUMN egasi INTEGER;     -- OBER sotuvchilar.id
ALTER TABLE elonlar ADD COLUMN elon_holati TEXT NOT NULL DEFAULT 'faol';
--   'faol' | 'sotildi' | 'ochirildi'
ALTER TABLE elonlar ADD COLUMN yangilandi REAL;   -- egasi tahrir qilgan vaqt
ALTER TABLE elonlar ADD COLUMN rasmlar_ober TEXT; -- OBER yuklangan rasmlar
```

- DIQQAT: `holat` ustuni BAND (OLX: yangi/b_u), shuning uchun yangi
  e'lon holati uchun `elon_holati` ishlatiladi.
- `manba='ober'` bo'lganda `egasi` to'ldiriladi, aks holda NULL.
- `elon_holati` — e'lon egasi "sotildi" deb belgilashi uchun. Nofaol e'lon
  qidiruvda chiqmaydi (mavjud `faol` logikasi bilan).
- `tashqi_id` — `manba='ober'` uchun `'ober-' + elon_id` shaklida,
  UNIQUE(manba, tashqi_id) buzilmasin.

### 4.2. Yangi funksiyalar — `baza.py` ga

```python
def ober_elon_yoz(egasi: int, e: dict) -> int:
    """Sotuvchi o'z e'loni. manba='ober'. Yozadi va qaytaradi elon_id."""

def ober_elon_yangila(egasi: int, elon_id: int, e: dict) -> bool:
    """Faqat egasi o'zgartira oladi. Ruxsatsiz -> False."""

def ober_elon_ochir(egasi: int, elon_id: int) -> bool:
    """holat='ochirildi'. E'lon qidiruvdan tushadi."""

def ober_elonlari(egasi: int) -> list[dict]:
    """Kabinetdagi "E'lonlarim" ro'yxati."""
```

E'lon yozilgach `tahlil.py` dagi bitta e'lon uchun funksiya chaqiriladi
(`fts` indeksiga darhol qo'shish uchun) — qidiruvda kechiktirmasdan
chiqishi kerak.

---

## 5. API o'zgarishlari — `server.py` ga

| Endpoint | Usul | Vazifa |
|---|---|---|
| `/api/elon` | POST | Yangi e'lon. Token bilan. `{nom, narx, kategoriya, tuman, rasm1..5, tavsif}` |
| `/api/elon/{id}` | PUT | Tahrirlash. **Faqat egasi** (token → egasi tekshiriladi) |
| `/api/elon/{id}` | DELETE | O'chirish (holat='ochirildi'). Faqat egasi |
| `/api/sotuvchi/elonlari` | GET | Kabinetdagi "E'lonlarim" |
| `/api/elon/{id}/sotildi` | POST | "Sotildi" belgilash |

Xavfsizlik:
- Tezlik chegarasi: `/api/elon` — soatiga 10 ta (ro'yxat bilan bir xil).
- Token tekshiruvi: `_sotuvchi_ident` mavjud — `sid==0` bo'lsa 401.
- Egalik tekshiruvi: `egasi` ustuni token'dagi sotuvchiga mos kelishi shart.
- Rasm: mavjud `_rasm_saqla()` (5 MB, JPG/PNG/WEBP cheki bor).

---

## 6. Frontend o'zgarishlari

### 6.1. `sotuvchi.html` — kabinetga "E'lonlarim" bo'limi (TAB'lar)

Kabinet ikkita yorliqdan iborat bo'ladi — aralashib ketmasligi uchun:

```
[ So'rovlar ] [ E'lonlarim ]
```

- **So'rovlar** — hozirgi "Xaridorlar kutyapti" ekrani (o'zgarmaydi).
- **E'lonlarim** — yangi bo'lim: rasmi, nomi, narxi, holati
  ("Faol" / "Sotildi" / "Yashirin"), tahrirlash/o'chirish tugmalari,
  **"Yangi e'lon"** tugmasi → forma.
- "Xabarlar" alohida sahifa bo'lib qoladi (takliflar.html).

Funksiyalar alohida nomlanadi: `elonlarim()`, `elonForma()`, `elonTahrir()`.
Kodda `# ── E'LONLARIM ──` bo'limi ostida turadi.

### 6.2. Yangi forma (sotuvchi.html ichida yoki alohida bo'lim)

- Nom (input), Narx (input, so'm) + "Kelishiladi" tanlovi.
- Kategoriya: `joylar.py` daraxtiga o'xshash, lekin kategoriya daraxti —
  `docs/04-universal-bozor-kategoriyalari.md` dan olinadi (tayyor).
- Joy: mavjud viloyat→shahar→tuman select'lari (qidiruvdagidek).
- Rasm: 1-5 dona, preview bilan, 5 MB limit — chatdagi rasm logikasi
  qayta ishlatiladi.
- Tavsif: textarea.
- Oldindan ko'rish karta + "Joylashtirish".

### 6.3. `index.html` — MANBA_NOM

```js
const MANBA_NOM = {olx:"OLX", telegram:"Telegram", uzum:"Uzum",
                   birbir:"BirBir", ober:"OBER"};
```

OBER e'lonlari uchun badge "OBER" ko'rinadi. Karta bosilganda — e'lon
sahifasi (yangilay boshlaydi: `/elon/{id}`) yoki modul.

---

## 7. Bosqichlar (nima birinchi)

### 7.1. MVP — 1-bosqich (asosiy, shuni qilamiz)

1. Baza: 4 ustun + 4 funksiya.
2. API: `/api/elon` POST + `/api/sotuvchi/elonlari` GET + `/api/elon/{id}` PUT/DELETE.
3. Kabinetga "E'lonlarim" + "Yangi e'lon" formasi.
4. Tahlilga ulash: e'lon yozilishi bilan darhol qidiruvga kiradi.
5. `MANBA_NOM` ga "OBER".
6. **E'lon sahifasi `/elon/{id}`** — rasm galereyasi, tavsif, telefon
   (`sotuvchi_id` orqali kabinetdan), chatga ulanish. OBER e'loni kartasi
   shu sahifaga boradi; OLX/Telegram e'loni eski tartibda tashqi havolaga.
7. Brauzerda to'liq test: joylashtirish → qidiruvda topish → sahifani
   ochish → tahrirlash → sotildi.

### 7.2. 2-bosqich (keyin)

- E'lon muddati (masalan 30 kun), avtomatik "muddati tugadi".
- "Sotildi" tugmasi xaridorga ham ko'rinsin.
- Ko'rishlar soni (e'lon sahifasida).

### 7.3. 3-bosqich (uzoq)

- Ko'tarish / premium (narx kiritish).
- Statistika: ko'rishlar, qo'ng'iroqlar, chatlar.
- Sotuvchi reytingi.

---

## 8. Xatarlar va yechimlar

| Xatar | Yechim |
|---|---|
| **Spam e'lonlar** (eng katta) | Tezlik chegarasi (10/soat), yangi sotuvchida e'lon moderatsiya belgisi, havola spam filtri (matnda `http` bo'lsa ogohlantirish) |
| **Takror e'lon** (sotuvchi OLX'da ham, OBER'da ham) | 1-bosqichda qabul qilamiz — ikkalasi ham qidiruvda chiqadi, xaridor tanlaydi. Keyin "bir xil nom+narx+joy" deduplikatsiya |
| **O'chirilgan e'lon qidiruvda qolishi** | `holat='ochirildi'` → FTS dan olib tashlash (tahlil siklida yoki darhol) |
| **Baza o'sishi** | Bitta e'lon ~2 KB — 10 000 ta OBER e'loni ~20 MB, muammo emas |
| **Rasm xotirasi** | Har rasm o'rtacha 100-300 KB (5 MB cheklangan), diskda 40 GB bor |

---

## 9. Qabul mezonlari (MVP tugadi deb hisoblash uchun)

1. Sotuvchi kabinetdan e'lon joylashtira oladi (rasm bilan).
2. E'lon darhol qidiruvda "OBER" belgisi bilan chiqadi.
3. Boshqa sotuvchi boshqa birovning e'lonini tahrirlay **olmaydi**.
4. "Sotildi" bosilgach e'lon qidiruvdan tushadi.
5. `/elon/{id}` sahifasi ochiladi: rasm galereyasi, narx, joy, tavsif,
   telefon (faqat egasi ko'rsatilganda xaridorga ko'rinadi).
6. Telefonda (390px) va kompyuterda (1440px) forma va e'lon sahifasi ishlaydi.
7. Konsol xatolari yo'q.
8. Yangi e'lon baza'da `manba='ober'`, `egasi` to'g'ri yoziladi.

---

## 10. Ulashish nuqtasi: bu bosqichda NIMA qilinmaydi

- To'lov va premium — yo'q.
- Sotuvchi reytingi — 3-bosqichga.
- Avtomatik deduplikatsiya — 2-bosqichga.
- Telegram orqali e'lon joylashtirish — keyin (sotuvchi saytni
  ochmasligi ma'lum, lekin MVP saytda boshlanadi — Telegram bu yerga
  qo'shimcha qatlam).

---

## 11. Taxminiy hajm

| Qism | Taxminiy ish |
|---|---|
| Baza (4 funksiya + migratsiya) | 1 soat |
| API (6 endpoint + tezlik) | 1.5 soat |
| Frontend (E'lonlarim + forma) | 2-3 soat |
| E'lon sahifasi `/elon/{id}` | 2-3 soat |
| Tahlilga ulash | 1 soat |
| Test (brauzer, API, mobil) | 1 soat |
| Serverga chiqarish | 30 daqiqa |
| **Jami** | **~10-11 soat** (bir yarim ish kuni) |
