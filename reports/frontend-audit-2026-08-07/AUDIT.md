# OBER Frontend Audit — 2026-08-07

## Tekshirilgan narsalar

Real brauzer (Chrome CDP) orqali ober.uz hamda mahalliy server tekshirildi:
- Bosh sahifa, kategoriyalar, sotuvchi kabineti, chat (takliflar), e'lon sahifasi
- Mobil (390×844) va desktop (1440×900) ko'rinishlari
- 5 tabli pastki tabbar
- Qidiruv oqimi
- Sotuvchi ro'yxatdan o'tish → e'lon joylash → chat halqasi (API darajasida 7/7 PASS)
- Konsol xatolari, overflow, buzilgan linklar
- O'zbek va rus tillari

## Hal qilingan kamchiliklar

### 1. Rus tilida ko'p matnlar o'zbekcha qolardi (ENG KATTA KAMCHILIK)
Dastlab rus rejimida 19+ matn o'zbekcha edi:
- Bosh sahifa: "Hozir bozorda", "Eng so'nggi qo'shilgan e'lonlar", "Nega OBER?", farq jadvali, footer havolalari ("Sotuvchilar uchun", "Chat demo", "Maxfiylik", "Qoidalar")
- Namuna chiplari (divan, kir yuvish mashinasi...)
- Sotuvchi kabineti: "So'rovlar", "E'lonlarim", "Telegramga ulash", "Chatda yozing"
- Chat: "Suhbatlar", "Vaqtim ko'rsin", "Joylashuv", "Sotuvchi bilan yozishmalar shu yerda."
- E'lon sahifasi: "Qidiruvga qaytish", "Rasm yo'q", "SOTUVCHI", "Bugun/Kecha"
- Kategoriyalar sahifasi: 116 ta OLX kichik bo'lim nomi

**Yechim:** `web/i18n.js` ga ~150 ta ruscha tarjima qo'shildi (389 ta kalit).
Tutuq belgisi (`‘` U+2018 va `'` U+0027) farqlarini hal qilish uchun RU_NORM
normalizatsiya lug'ati qo'shildi. Sana, "N kun oldin" (ruscha ko'plik bilan:
1 kun → день, 2-4 → дня, 5+ → дней, 21 → день), emoji prefikslar ("🕐 Bugun")
va "so'm" uchun regex qoidalari qo'shildi.

**Natija:** barcha sahifalarda rus rejimi toza. Qolgan o'zbekcha matnlar —
viloyat/shahar nomlari (joy nomlari), e'lon sarlavhalari (foydalanuvchi matni),
brend nomlari (Audi, Aito...) — ular tarjima qilinmasligi TO'G'RI.

### 2. i18n.js da dublikat kalitlar
4 ta kalit ikki marta yozilgan edi (Tekinga beraman, Ayirboshlash, Sotuvchi,
Xaridorlar bilan suhbatlar). Tozalandi.

### 3. "Vaqtim ko'rsin" tugmasi tarjima qilinmasdi
Sabab: HTML'da "ko'rinsin" (rin bilan), lug'atda "ko'rsin" (rinsiz) yozilgan edi.
Tuzatildi. Tugmaning ikkinchi holati "Vaqtim yashirin" ham qo'shildi.

### 4. Qidiruv sahifasida birinchi natija nomuvofiq ko'rindi
Tekshiruvda "divan" qidiruvida birinchi karta "Запчасти для ноутбуков" chiqqan
edi — bu bosh sahifadagi namuna bo'limi edi, qidiruv emas. API darajasida
qidiruv to'g'ri: "divan" → 13 ta mos natija (Spalni Divan sotiladi va boshqalar).
Haqiqiy kamchilik emas.

### 5. "241 635 ta" soni tarjima qilinmasdi
Regex `^(\d+) ta$` probelsiz sonni kutardi. `^([\d\s]+) ta$` ga kengaytirildi.

## Tasdiqlangan ishlash (PASS)

- **Qidiruv oqimi:** "divan" → 13 mos natija, birinchi karta konteyner ichida
- **Sotuvchi oqimi (API):** ro'yxatdan o'tish, kod, kirish, e'lon joylash, e'lonlar ro'yxati — 7/7 PASS
- **Chat halqasi (API):** so'rov, javob, suhbat, xabar — 7/7 PASS
- **Tabbar:** mobil va desktopda ➕ aynan markazda (195/720), 5 tabda ham ikon bor
- **E'lonlarim:** e'lon ko'rinadi, Ko'rish/Tahrirlash/O'chirish tugmalari bor
- **Bosh sahifa:** birinchi karta mobil 571px, desktop 535px (700px chegarasidan yuqori — ko'rinadi)
- **Suzuvchi "So'rash" tugmasi:** natija sahifasida ishlaydi
- **Konsol xatolari:** yo'q
- **Overflow:** barcha sahifalarda yo'q
- **Script balansi:** barcha HTML fayllarda to'g'ri

## Deploy

- `web/i18n.js` production'ga yuklandi (38 056 bayt, 389 kalit)
- Sayt 200, xizmat active
- Test yozuvlari bazadan tozalandi (sotuvchilar 25→14, suhbatlar 10→7)

## Qo'shimcha yaxshilanishlar (2026-08-07 davomi)

### 6. E'lon sahifasida telefon maxfiyligi
Ilgari telefon raqami to'g'ridan-to'g'ri ko'rsatilardi — spam-botlar uchun ochiq
edi. Endi "Telefon raqamini ko'rsatish" tugmasi orqasida: bosilgandagina raqam
va `tel:` havola ko'rinadi. Production'da sinaldi (yashirin → bosilganda
ko'rinadi, konsol xatosi yo'q, rus tilida "Показать номер телефона").

### 7. Kategoriyalar sahifasiga jonli filtr
Qidiruv maydoni qo'shildi: yozilgan so'z bo'yicha kartalar filtrlanadi
(nom + namuna chiplar bo'yicha), "Hech narsa topilmadi" bo'sh holati ko'rinadi.
Kod-review topgan xato tuzatildi: bo'sh holat klassining `display:none`
JS `hidden` atributini o'chirishni bekor qilardi — endi to'g'ri ko'rinadi
(computed style bilan tasdiqlandi). Production'da sinaldi (12→3→bo'sh→12).

### 8. Chat kompozeri mobil tekshiruvi
Mobil (390×844) o'lchov: matn maydoni to'liq kenglikda tepada, rasm+
joylashuv+yuborish tugmalari pastda bir qatorda. Overflow yo'q, konsol xatosi
yo'q. Joylashuv to'g'ri.

### 9. Bosh sahifa desktop tuzilishi
Hero→jonli bo'lim→qadamlar→footer zanjiri to'g'ri, bo'sh joy yo'q.
Avvalgi "390-1020px bo'sh joy" kuzatuvi yuklanayotgan jonli bo'lim edi.

## Qolgan kuzatuvlar (dizayn qarorlari, o'zgartirilmadi)

1. **Bosh sahifada so'rov formasi yo'q** — "So'rash" faqat natijalar sahifasida.
   Bu dizayn qarori: bosh sahifa qidiruvdan boshlanadi.
2. **Viloyat nomlari rus tilida o'zbekcha** — joy nomlari, tarjima qilinmaydi.
3. **Qidiruv kartalari tashqi havolalarga o'tadi** (OLX, Telegram) — ichki
   `/elon/` sahifasi faqat OBER e'lonlari uchun, OLX e'lonlari uchun 404
   qaytishi to'g'ri.
