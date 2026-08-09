# OBER — audit tuzatishlar va sotuvchi login (2026-08-06)

Boshlang'ich: `audit/2026-08-06-frontend/audit.md` (topilmalar)
Ushbu hujjat: qilingan o'zgarishlar va tekshiruv natijalari.

## Nima tuzatildi

### 1. 🔴 Qidiruv natijalari endi URL'da saqlanadi
- `web/index.html`: har qidiruvda `history.replaceState` bilan `?q=` URL'ga
  yoziladi; sahifa `?q=divan` bilan ochilsa qidiruv avtomatik boshlanadi.
- `?tuman=viloyat|joy` ham saqlanadi va ochilganda joylar ro'yxati
  yuklangach tanlanadi (race condition 2026-08-06 kod-reviewda tuzatildi).
- Natija: F5'da natijalar saqlanadi, havolani Telegram/mijozga ulashib
  bo'ladi, Google indekslay oladi.
- **Brauzer testi (Chrome):** `?q=divan` → avtomatik qidiruv, 13 ta karta,
  URL'da `?q=divan` saqlanadi.

### 2. 🟠 Namuna chiplar endi universal
- Eski: `kobalt fara, neksiya kolodka, spark rul, matiz bamper, lasetti
  amortizator` — hammasi avtoqism.
- Yangi: `divan, kir yuvish mashinasi, velosiped, 2 xonali kvartira,
  telefon ekrani` — mebel, maishiy texnika, transport, ko'chmas mulk,
  elektronika. "Universal bozor" va'dasiga mos.
- **Brauzer testi:** 5 ta yangi chip ko'rinadi.

### 3. 🟠 Footer + maxfiylik/qoidalar sahifalari
- `web/index.html`: minimal footer (brend, qisqa tavsif, Sotuvchilar
  uchun / Takliflar demo / Maxfiylik / Qoidalar havolalari).
- `app/server.py`: `/maxfiylik` va `/qoidalar` sahifalari (server
  tomonda, Google JS'siz o'qiy oladi). `_oddiy_sahifa()` yordamchisi.
- **Test:** ikkala sahifa 200, bosh sahifada footer bor.

### 4. 🔴 Sotuvchi kabineti — telefon + bir martalik kod
Eski holat (xavfsizlik teshigi): kabinet ID raqami faqat localStorage'da —
boshqa qurilmada kabinet yo'qolardi, ID'ni bilgan har kim istalgan
kabinetga kira olardi.

Yangi:
- **Kirish ekrani** (`web/sotuvchi.html`): telefon raqam → "Kod olish" →
  Telegram'ga kelgan kodni kiritish → kabinet. "Ro'yxatdan o'tish" ham
  shu ekrandan.
- **Backend:**
  - `app/baza.py`: `kirish_kodlari` va `sessiyalar` jadvallari +
    `kirish_kod_yarat/tekshir`, `sessiya_yarat/sotuvchisi`,
    `sotuvchi_aloqasi` funksiyalari.
  - `app/server.py`: `POST /api/sotuvchi/kirish` (kod so'rash) va
    `POST /api/sotuvchi/tasdiq` (kodni tasdiqlash → sessiya token).
    Ro'yxatdan o'tish endi token qaytaradi.
  - `app/tg.py`: `yubor()` endi muvaffaqiyatni qaytaradi — kod yuborilmasa
    "yuborildi" deb yolg'on aytilmaydi.
- **Telefon normalizatsiya:** `+998 90 123 45 67` va `+998901234567` endi
  bir xil hisoblanadi.
- **Xavfsizlik:** soatiga 20 ta kod so'rov/IP, bitta raqamga soatiga 5 ta
  kod (boshqa odam kodlarni bekor qilib qo'ymasligi uchun), enumeration
  himoyasi (raqam ro'yxatdami — aytilmaydi), kod 10 daqiqa amal qiladi,
  sessiya 30 kun.
- **Eski qurilmalar:** localStorage'da ID raqami saqlangan bo'lsa ham
  ishlayveradi (backward compatible).
- **Test:** butun halqa (kirish→kod→tasdiq→token→kabinet) o'tdi;
  noto'g'ri kod 401 qaytaradi; ro'yxatda yo'q raqam bir xil javob oladi.
  Brauzerda kirish ekrani to'g'ri ko'rsatiladi.

### 5. 🟡 Takliflar `?demo=1` — endi localStorage bo'lsa ham ishlaydi
- `web/takliflar.html`: `demoMode` localStorage'dan `ober_sotuvchi` va
  `ober_sorov` o'qishni o'chiradi.
- Sotuvchi `actorId` endi token bo'lishi mumkin (raqam emas) — server
  `_sotuvchi_ident` ikkalasini ham tushunadi.
- **Test:** `?demo=1` → `/takliflar?sorov=60` ga yo'naltirildi, 3 taklif,
  chat ochiq, konsolda xato yo'q.

### 6. 🟡 Demo chat 404 rasm
- `app/suhbat_demo.py`: eski `/chat-uploads/demo-nexia-kolodka-v1.png`
  (serverda yo'q) o'rniga `/brend/seller-navy-panel.webp` (har doim bor).
- **Test:** demo chatda konsol xatolari yo'q.

### 7. 🟢 Natija H1 qidiruv so'zi bo'ladi
- `web/index.html`: `qidir()` natija paytida `#hero-title` → `"divan"`,
  `document.title` → `"divan" — OBER`.
- **Test:** H1 = `“divan”`, title = `“divan” — OBER`.

## Hali qilingan ishlar (keyingi bosqich)

- **Uzum + Avtoelon adapterlari** (foydalanuvchi tanladi: keyingi bosqich).
  Texnik tekshiruv: uzum.uz va avtoelon.uz e'lon sahifalari crawlab,
  ichki JSON API'lari bor; `app/manbalar/` interfeysi tayyor.
  birbir.uz Cloudflare bilan himoyalangan (403) — alohida yondashuv kerak.
- **O'z marketplace** (foydalanuvchi tanladi: keyinroq). Reja qog'ozda
  tayyorlanadi.
- **Sessiya bekor qilish (logout)** — hozir chiqish faqat brauzerdagi
  tokenni o'chiradi; server tomonida sessiyani o'chirish endpointi keyingi
  bosqichda qo'shiladi (kod-review taklifi).

## Tekshiruv xulosasi

- Python: `py_compile` barcha o'zgartirilgan fayllarda o'tdi.
- JS: `node --check` index.html, sotuvchi.html, takliflar.html, i18n.js —
  hammasi o'tdi.
- Backend halqa testi: kirish→kod→tasdiq→token→kabinet o'tdi.
- Brauzer testlari: qidiruv URL, H1, footer, maxfiylik/qoidalar,
  takliflar demo, kirish ekrani — hammasi ishlaydi.
- Bilinarli 404: `/shrift/*.woff2` font fayllari — mahalliy muhitda yo'q,
  `deploy/shrift-yuklab-ol.sh` bilan tiklanadi (production'da bor).
