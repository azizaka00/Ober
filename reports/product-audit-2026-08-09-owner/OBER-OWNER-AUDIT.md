# OBER — egasi ko‘zi bilan mahsulot va frontend auditi

Sana: 2026-08-09  
Tekshiruv: `ober.uz`, desktop 1440×900 va telefon 390×844  
Holat: tizimga kirmagan xaridor va yangi sotuvchi yo‘li

## Qisqa hukm

OBERning g‘oyasi kuchli va bosh sahifasi uni yaxshi tushuntiradi: foydalanuvchi oddiy tilda yozadi, OBER esa ochiq e’lonlarni topib, kerak bo‘lsa sotuvchilardan jonli javob yig‘adi. Rasmli qidiruv va 30 soniyalik sotuvchi ro‘yxati ham mahsulotni oddiy agregatordan ajratadi.

Hozirgi eng katta kamchilik bezak emas. Mahsulotning uchta asosiy tushunchasi aralashib qolgan:

- **E’lon** — OLX, Telegram va boshqa manbalardan indekslangan yozuv.
- **Jonli taklif** — OBER ichida sotuvchining narx va mavjudlik javobi.
- **Chat** — xaridor va sotuvchining suhbati.

Qidiruv natijasidagi 674 ta tashqi e’lon “taklif” deb atalmoqda, Chat demo esa tekshiruvda “Ulanib bo‘lmadi” holatini ko‘rsatdi. Shu sabab OBER hozir kuchli qidiruv/agregator sifatida ko‘rinadi, lekin teskari bozor halqasi hali foydalanuvchiga to‘liq isbotlanmaydi.

## Tekshirilgan foydalanuvchi yo‘li

| Qadam | Holat | Kuzatuv |
|---|---|---|
| 1. Bosh sahifada ehtiyojni yozish | Kuchli | Sarlavha, qidiruv va kamera birinchi ekranda. Ro‘yxatdan o‘tmasdan qiymat beriladi. |
| 2. Ochiq e’lonlarni ko‘rish | Aralash | Natija tez va haqiqiy, lekin mahsulot va ta’mirlash xizmati bir natijada aralashadi. Tashqi kartaga bosilganda OBERdan chiqib ketiladi. |
| 3. Kategoriya orqali ko‘rish | Aralash | Qamrov katta, ammo brend, mahsulot turi va xizmat bitta pill ro‘yxatida. Kognitiv yuk yuqori. |
| 4. Sotuvchilardan jonli javob olish | Zaif | CTA mavjud va mobilga yopishqoq joylashtirilgan. Ammo Chat demo ulanish xatosida; yangi foydalanuvchiga login yoki tiklash yo‘li berilmagan. |
| 5. Sotuvchi sifatida boshlash | Kuchli | Kategoriya daraxtisiz ism/biznes, erkin tavsif, hudud va telefon — OBER g‘oyasiga juda mos. |
| 6. Mobil tajriba | Yaxshi, tuzatish kerak | Birinchi natija ekranga sig‘adi. Ayrim sort/filtrlar siqilgan, yopishqoq CTA ikkinchi kartani yopadi. |

## Vizual dalillar

### 1. Bosh sahifa — desktop

![OBER bosh sahifa desktop](01-home-desktop.png)

Yaxshi: qidiruv markazda, brend ishonchli, rasmli qidiruv ko‘rinadi.  
Muammo: desktopda yuqori menyu bilan birga mobil pastki tabbar ham turibdi. “Hozir bozorda” lentasida eski sana, ruscha/o‘zbekcha aralash kontent va sifati turlicha e’lonlar “hozir” va’dasini zaiflashtiradi. Katta ekranda ma’lumot zichligi past.

### 2. Qidiruv natijalari — desktop

![OBER qidiruv natijalari desktop](02-search-results-desktop.png)

Yaxshi: haqiqiy rasm, narx, hudud, sana va saralash mavjud.  
Muammo: “Elektr jihozlari” va “Maishiy texnika ta’miri” niyati aralash. Desktop kartalari juda katta, narx va hudud birinchi ekranda yetarli zichlikda ko‘rinmaydi. Tashqi manba havolasi OBER kontekstini darhol yo‘qotadi.

### 3. Kategoriyalar — desktop

![OBER kategoriyalar desktop](03-categories-desktop.png)

Yaxshi: qamrov kattaligi ko‘rinadi.  
Muammo: foydalanuvchiga birdaniga juda ko‘p pill berilgan. “Transport” ichida transport turi va avtomobil brendi bir darajada. Har bir karta ichidagi pill alohida boshqaruvga o‘xshaydi, lekin amalda umumiy bo‘lim havolasining bir qismi.

### 4. Chat xato holati — desktop

![OBER chat xato holati](05-chat-desktop.png)

“Ulanib bo‘lmadi” xabari bor, ammo sabab, qayta urinish tugmasi, login talabi yoki yordam yo‘li yo‘q. Bu OBERni oddiy qidiruvdan bozorga aylantiradigan eng muhim halqani uzadi.

### 5. Bosh sahifa — telefon

![OBER bosh sahifa telefon](06-home-mobile.png)

Yaxshi: sarlavha, qidiruv, joylashuv va real e’lonlar bir ekranga yaqin joylashgan.  
Muammo: misol chiplarining oxiri kesiladi; “Hozir bozorda” kartalari tor va bir nechta tilda. Pastki tabbar to‘g‘ri, lekin u faqat telefonda qolishi kerak.

### 6. Natijalar — telefon

![OBER natijalari telefon](07-results-mobile.png)

Yaxshi: birinchi karta 844 px ekran ichida ko‘rinadi va jonli so‘rov CTA doim qo‘l ostida.  
Muammo: sort variantlari yon tomonda yashirinadi, narx filtri noaniq, yopishqoq “Sotuvchilardan so‘rash” tugmasi ikkinchi kartani yopadi.

### 7. Sotuvchi ro‘yxatdan o‘tishi — telefon

![OBER sotuvchi ro‘yxati telefon](09-seller-register-mobile.png)

Bu auditdagi eng to‘g‘ri oqimlardan biri. Faqat bitta muhim qo‘shimcha kerak: erkin tavsifdan keyin AI foydalanuvchiga “Sizga mana shunday so‘rovlarni yuboramiz” deb 3–5 ta tushunarli yo‘nalishni ko‘rsatib, tahrirlash imkonini berishi kerak.

## Men egasi bo‘lganimda birinchi bo‘lib qiladigan o‘zgarishlar

### P0 — mahsulotni tushunarli va ishonchli qilish

1. **Atamalarni ajrataman.** Natijada “674 ta e’lon”; OBER sotuvchisidan kelganda “3 ta jonli taklif”; xabarlar bo‘limida “Chat”.
2. **Chat va so‘rov halqasini tuzataman.** Xato holatiga “Qayta urinish”, “Kirish” va aniq sabab; yangi foydalanuvchiga so‘rov holatini telefon orqali qayta ochish.
3. **Desktop navigatsiyani tozalayman.** Desktopda faqat yuqori menyu; telefonda faqat 5 bo‘limli pastki tabbar.
4. **Qidiruv niyatini ajrataman.** “Kir yuvish mashinasi” uchun `Sotib olish` va `Ta’mirlash xizmati` chiplarini ko‘rsataman. AI ishonchi yuqori bo‘lsa o‘zi tanlaydi, noaniq bo‘lsa bitta savol beradi.
5. **Natija kartalarini zichlashtiraman.** Desktop 4 ustun, tablet 2, telefon 1; rasm, narx, hudud va yangiligi bitta qarashda.
6. **OBER ichki preview qo‘shaman.** Kartaga bosilganda yon panel yoki ichki detail ochiladi; asl manbaga o‘tish ikkinchi tugma bo‘ladi. Bu saqlash, taqqoslash va jonli so‘rovga o‘tishni OBER ichida qoldiradi.
7. **“Hozir bozorda”ni nazorat qilaman.** Faqat yaqinda tekshirilgan, rasmi va narxi ishonchli, takrorlanmagan, turli kategoriyadagi e’lonlar. Eski sana bo‘lsa “hozir” deb ko‘rsatilmaydi.

### P1 — foydalanuvchini qaytaradigan komfortlar

1. **Saqlangan qidiruv va ichki bildirishnoma.** Yangi e’lon, arzonroq narx yoki yangi sotuvchi javobi kelganda OBER ichida badge va inbox. Telegramga majburiy operatsion xabar yuborilmaydi.
2. **Taqqoslash.** 2–4 e’lon yoki jonli taklifni narx, hudud, holat, yetkazish va javob tezligi bo‘yicha yonma-yon ko‘rish.
3. **Rasmli qidiruvning tushuntirilgan holati.** “AI rasmda Malibu 2 old farasini aniqladi” degan tahrirlanadigan chiplar; noto‘g‘ri bo‘lsa foydalanuvchi bir tegishda tuzatadi.
4. **Mening so‘rovlarim.** Ochiq so‘rovlar, kelgan takliflar, saqlangan e’lonlar va chatlar bitta timeline’da.
5. **Haqiqiy hudud filtri.** Viloyatdan keyin tuman, masofa, olib ketish/yetkazib berish va xizmat radiusi.
6. **Sotuvchi tez javobi.** `Bor`, `Yo‘q`, `O‘xshashi bor`; keyin narx, bitta rasm va qisqa izoh. Javob 10–20 soniya ichida tugashi kerak.
7. **Sotuvchi ishonchi.** Telefon tasdiqlangan, ish vaqti, javob tezligi, bajarilgan buyurtmalar, portfolio va shikoyat holati. Pullik ko‘tarish ishonch reytingini bosib ketmasligi kerak.

### P2 — OBERni agregatordan aqlli bozorga aylantirish

1. **Bir xil e’lonlarni birlashtirish.** OLX, Telegram va boshqa manbalardagi bir mahsulotni bitta klasterda ko‘rsatish; ichida manbalar va narxlar alohida.
2. **Ko‘p manbali adapterlar.** Har yangi manba uchun yangilanish vaqti, xato darajasi va dublikat ulushi o‘lchanadi. Manba soni emas, foydali va yangi e’lon soni maqsad bo‘ladi.
3. **AI marshrutlash.** Xaridor matni/rasmi va sotuvchi erkin tavsifi embedding/klassifikatsiya orqali moslanadi; lug‘at fallback va nazorat vositasi bo‘lib qoladi.
4. **Sifatli reyting.** Moslik + yangilik + masofa + sotuvchining javob tezligi + ishonch. Pul to‘lagan sotuvchi faqat “Reklama” belgisi bilan alohida ko‘tariladi.
5. **Talab xaritasi.** Sotuvchiga “Sizning yo‘nalishingizda bu hafta 47 ta qidiruv bo‘ldi” degan real analitika. Bu sotuvchini jalb qiladigan eng kuchli dalil.

## Frontend yo‘nalishi

To‘liq rebrending shart emas. OBERning navy + oq + yumshoq kulrang tizimi, Onest shrifti va katta qidiruv bloki yaxshi. Men quyidagicha davom ettirardim:

- **Fon:** AI yasagan xira bozor manzarasi o‘rniga haqiqiy e’lon rasmlaridan boshqariladigan yengil mozaika yoki haqiqiy mahalliy ko‘cha fotosi. Mobil internetda rasm o‘chsa ham qidiruv qiymati yo‘qolmasin.
- **Zichlik:** desktopda bo‘sh joyni kamaytirib, birinchi ekranda 6–8 haqiqiy natija ko‘rsatish; reklama landingiga o‘xshatmaslik.
- **Kategoriyalar:** avval 10–12 yuqori kategoriya, ikonka va 2–3 mashhur misol; ichiga kirganda keyingi daraja. Bir kartada 12 ta pill bermaslik.
- **Rang:** navy — asosiy harakat; yashil — mavjud/tasdiqlangan; sariq — javob kutilmoqda; qizil — xato. Bezash uchun qo‘shimcha rang ishlatmaslik.
- **Harakat:** 160–220 ms opacity/transform; skeleton, AI aniqlash va saqlash feedbacki. Scroll-shou va og‘ir parallax kerak emas.
- **Matn:** kulrang yordamchi yozuvlar kontrastini oshirish, 14 px dan kichik asosiy ma’lumot bermaslik, tugma va chip tap targetlarini kamida 44 px qilish.
- **Holatlar:** yuklanmoqda, natija bor, natija yo‘q, xato — har bir blokda aniq keyingi harakat bilan.

## O‘sishni mahsulotning o‘ziga tikish

- So‘rov yoki taqqoslash natijasini havola qilib ulashish.
- Hech kim javob bermasa, foydalanuvchi bilgan sotuvchini OBERga taklif qilish havolasi.
- Shahar + kategoriya uchun SEO sahifalari, lekin faqat real yangi e’lon va real sotuvchi qamrovi bo‘lsa.
- Dastlab bitta zich yo‘nalishda — masalan Toshkentdagi avto ehtiyot qismlar — “so‘rov → 3 jonli taklif → chat” halqasini oxirigacha ishlatish; keyin kategoriyalarni kengaytirish.

## O‘lchanadigan asosiy ko‘rsatkichlar

- Qidiruvdan haqiqiy natija ko‘rishgacha vaqt.
- Qidiruv → e’lon preview ochilishi.
- Qidiruv → sotuvchilardan so‘rash.
- Birinchi jonli javobgacha vaqt.
- Kamida 3 javob olgan so‘rovlar ulushi.
- Sotuvchi javob berish darajasi va median javob vaqti.
- 7/30 kunlik qaytish.
- Rasmli qidiruvda AI natijasini tuzatish darajasi.

## Hozircha qilmas edim

- Escrow va ichki to‘lovni halqa ishlamasdan oldin qurmas edim.
- Barcha kategoriya va MDH bozorini bir vaqtda sotuvchi bilan to‘ldirmas edim.
- Frontendga ko‘p effekt, bento, testimonial va bezak bloklari qo‘shmas edim.
- Foydalanuvchini birinchi qidiruvdan oldin ro‘yxatdan o‘tishga majbur qilmas edim.
- AI javobini tahrirsiz “haqiqat” sifatida ko‘rsatmas edim.

## Accessibility qaydlari

Kuchli tomonlar: qidiruv textboxi va kamera tugmasining accessible nomi bor, sahifalarda heading va region strukturalari mavjud.  
Xavflar: mayda kulrang yordamchi matnlar kontrasti past; desktopdagi takror navigatsiya keyboard foydalanuvchini ortiqcha tab aylanishiga majbur qiladi; mobil sticky CTA kontentni yopadi; ayrim chiplar 44 px tap targetdan kichik ko‘rinadi; ruscha holatda `Asosiy navigatsiya` aria-label tarjima qilinmagan.

Bu vizual va oqim auditi WCAG muvofiqligini to‘liq isbotlamaydi. To‘liq accessibility tekshiruvi uchun keyboard-only, screen reader, focus order, zoom 200% va kontrast o‘lchovi alohida sinovdan o‘tkazilishi kerak.

## Tekshiruv chegarasi

Auditda ro‘yxatdan o‘tish, OTP yuborish, sotuvchi yaratish yoki xabar jo‘natish bajarilmadi. Shu sabab autentifikatsiyadan keyingi sotuvchi kabineti, haqiqiy taklif yuborish, rasmli chat va xaridorga notification yetib borishi tekshirilmagan. Chat demo tekshiruv vaqtida ulanish xatosida edi.
