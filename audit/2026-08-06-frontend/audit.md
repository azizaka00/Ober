# OBER frontend auditi — 2026-08-06

Manzil: https://ober.uz (hamma testlar real brauzer va curl bilan)
Usul: Chrome brauzer (desktop 1440x900, mobil 390x844, 320px, 768px),
API testlar curl bilan, kod bilan solishtirish.

## Xulosa

Sayt **ishlayapti va yaxshi holatda**: qidiruv tez va aniq, sotuvchi
ro'yxatdan o'tishi, so'rov yuborish, takliflar/chat — hammasi funksional.
Konsolda **birorta JS xatosi yo'q** (barcha sahifalarda). Responsive
320px dan 1440px gacha buzilmasdan ishlaydi. Quyidagi muammolar
asosan UX/SEO/ishonch masalalari, funksional xato emas.

---

## 1. Ishlayotgan narsalar (test qilingan)

| Narsa | Natija |
|---|---|
| Bosh sahifa yuklanishi | ✅ ~0.5 s, 0 konsol xato |
| Qidiruv "divan" | ✅ 775 natija, ~92 ms API, narx xulosasi + histogramma |
| Qidiruv "kvartira" | ✅ 80 natija |
| Saralash (Avval arzoni) | ✅ ishlaydi |
| Sotuvchilardan so'rash | ✅ POST /api/sorov → 200, 3 sotuvchiga yuborildi |
| Jonli e'lonlar lentasi | ✅ 14 ta karta yuklanadi |
| Sotuvchi ro'yxatdan o'tish | ✅ validatsiya + ro'yxat + dashboard |
| Takliflar sahifasi | ✅ demo chat ochiladi, suhbat ishlaydi |
| Til almashish (O'z/Рус) | ✅ localStorage orqali ishlaydi |
| Responsive 320/390/768/1440 | ✅ hech qanday gorizontal overflow yo'q |
| www.ober.uz → ober.uz | ✅ 301 |
| robots.txt / sitemap.xml / /narx | ✅ 200, 34 KB sitemap |
| og:image, favicon, logo | ✅ barchasi bor |
| Shrift (o'z serverda, preload) | ✅ |
| 404 sahifa | ✅ "Bosh sahifaga qaytish" tugmasi bilan |

---

## 2. Topilgan muammolar

### 🔴 JIDDIY — qidiruv natijalari URL'da saqlanmaydi
`?q=divan` kabi havola sahifani qidiruv natijalari bilan ochmaydi.
Kodda `URLSearchParams` o'qilmaydi — qidiruv faqat localStorage orqali
ishlaydi. Natijalar:

- F5 bosilsa / havola yangilansa natijalar yo'qoladi.
- Havolani Telegram/mijozga ulashib bo'lmaydi (quruq bosh sahifa ochiladi).
- Google qidiruv sahifasini indekslay olmaydi.

**Taklif:** `history.replaceState` bilan URL'ga `?q=...` yozish va
sahifa ochilganda `?q` parametrini o'qib qidiruvni avtomatik boshlash.

### 🟠 Namuna chiplar — hammasi avtoqism
Birinchi ekrandagi namuna so'rovlar:
`kobalt fara, neksiya kolodka, spark rul, matiz bamper, lasetti amortizator`
— barchasi avtoehtiyot qism. Lekin sayt o'zini **universal bozor**
deb e'lon qilgan ("Mahsulotdan xizmatgacha"). Sotuvchi sahifasida bu
allaqachon tuzatilgan ("Mebel yasayman, kir yuvish mashinasi tuzataman,
tort pishiraman"), bosh sahifa eski qoldi. Yangi tashrifchi
"OBER = avtoqism sayti" degan noto'g'ri xulosaga keladi.

**Taklif:** `const NAMUNA` (web/index.html, 1268-qator) ni xilma-xil
qilish: mebel, xizmat, kvartira, qurilish, telefon kabi sohalardan.

### 🟠 Footer yo'q
Bosh sahifada hech qanday footer, kontakt, kompaniya ma'lumoti yo'q.
Sahifa "jonli" bo'limdan keyin tugaydi. Bu:

- Ishonch masalasi: odam "bu kimning sayti?" degan savolga javob
  topolmaydi.
- Aloqa yo'li yo'q (Telegram, email).
- Maxfiylik/qoidalar sahifalari yo'q.

**Taklif:** minimal footer: brend, qisqa tavsif, aloqa (Telegram),
maxfiylik va foydalanish shartlari.

### 🟡 Takliflar?demo=1 — localStorage bo'lsa ishlamaydi
`/takliflar?demo=1` havolasi faqat localStorage **toza** bo'lganda
demo chatni ko'rsatadi. Agar odam avval so'rov yuborgan bo'lsa
(localStorage'da `ober_sorov` bor), demo o'rniga bo'sh ekran
chiqadi. Bu faqat demo havola uchun, lekin chalkashtiradi.

### 🟡 Chatda 404 resurs
Takliflar sahifasida bitta rasm 404 beradi
(`/chat-uploads/...` — eski/yo'q fayl). Demo chatda rasm bor, fayl
yo'q. Konsolda ko'rinadi.

### 🟢 Natija sahifasida H1 qoladi
Qidiruv natijalarida h1 "Siz yozasiz. Bozor javob beradi." bo'lib
qoladi — natija sarlavhasi ("divan — 775 ta natija") h1 emas.
SEO va tushunarlilik uchun h1 qidiruv so'zi bo'lishi kerak.

### 🟢 Til standartida o'zbekcha
Sayt o'zbekcha ochiladi (to'g'ri), rus tili foydalanuvchi tanlaganda
saqlanadi. Brauzer tiliga avtomatik moslashmaydi — bu tanlovmi yoki
tushib qolgan funksiyami, tekshirish kerak.

---

## 3. Qo'shish bo'yicha takliflar (ustuvorlik bilan)

1. **URL'da qidiruv** (`?q=` + history.replaceState) — eng muhimi.
   Natijalarni ulashish, saqlash, Google indeksi.
2. **Namuna chiplarni diversifikatsiya** — universal bozor va'dasiga mos.
3. **Footer + aloqa + maxfiylik sahifalari** — ishonch uchun.
4. **Takliflar sahifasida eski rasm 404'ini tozalash** — konsol toza
   bo'lsin.
5. **Natija h1 ni qidiruv so'zi bilan almashtirish** — SEO.
6. SEO: natija sahifalarida `og:image` va `canonical` qo'shish.

---

## 4. Screenshotlar

Papka: `audit/screenshots/`

- `01-bosh-desktop.png` — bosh sahifa desktop 1440x900
- `02-bosh-mobil.png` — bosh sahifa mobil 390x844
- `03-sotuvchi-desktop.png` — sotuvchi kabineti
- `04-takliflar-desktop.png` — takliflar sahifasi

(Chrome headless orqali olingan; brauzer agentlari skrinshotlarni
o'z sessiyalarida ko'rdi va tasdiqladi.)
