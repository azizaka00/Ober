# OBER mahsulot auditi — 2026-08-08

## Qisqa hukm

OBER endi oddiy qidiruv maketi emas: xaridor qidiradi, tizim so'rovni
tushunganini ko'rsatadi, sotuvchilardan taklif so'raydi, unread badge bilan
ichki chat ochadi va ikki tomon rasm yubora oladi. Mobil ko'rinish zamonaviy,
brend bir xil va asosiy oqim tushunarli. Umumiy tayyorlik: **4/5**.

Public launch oldidan ikki katta qatlam qolgan: sessiya xavfsizligi va ruscha
matnlarning yangi funksiyalarda aralashib qolishi.

## Tekshirilgan oqimlar

1. Xaridor bosh sahifasi — desktop va 390x844 mobil.
2. `cobalt fara` qidiruvi, tushunilgan model/qism, narx va saralash.
3. Sotuvchi kirishi va kategoriyasiz 30 soniyalik ro'yxatdan o'tish.
4. Takliflar/chat — unread badge, dialog ro'yxati, rasm, geolokatsiya,
   bildirishnomalar markazi.
5. Kategoriyalar — qidiruv va bozor bo'limlari.
6. Konsol xatolari va mobil gorizontal overflow.

## Kuchli tomonlar

- Qidiruvdan keyin `Avtomobil: cobalt`, `Detal: fara`, `Kategoriya: Transport`
  ko'rinadi. Bu AI nimani tushunganini foydalanuvchiga isbotlaydi.
- Noto'g'ri avtomobillar kesilgani son bilan ko'rsatiladi; birinchi natijalar
  so'rovga mos va narx/joy/sana skaner qilish oson.
- Sotuvchi formasi Aziz xohlagandek: nom, nima sotadi/xizmati, joy va telefon;
  kategoriya daraxti yo'q.
- Chatda yangi xabar soni chatga kirmasdan ko'rinadi. Dialog ochilganda unread
  kamayadi. Xaridor ham, sotuvchi ham rasm yubora oladi.
- Bildirishnoma markazi aniq bottom-sheet ko'rinishida; "hammasini o'qildi"
  amali bor.
- Kategoriyalar bozorning umumiyligini yaxshi ko'rsatadi: transport,
  ko'chmas mulk, elektronika, uy-bog', bolalar, xizmatlar, ish va boshqalar.
- Mobil joylashuvda overflow va konsol xatolari topilmadi.

## Kamchiliklar va ustuvorlik

### P0 — launchdan oldin

1. Sotuvchi API hali raqamli ID'ni sessiya tokeni o'rniga qabul qiladi.
   ID taxmin qilinsa begona kabinet ma'lumoti ochilishi mumkin. Legacy ID
   fallbackni migratsiya muddati bilan butunlay yopish kerak.
2. Xaridor tomonda oddiy ketma-ket `sorov_id` actor sifatida ishlatiladi.
   So'rov/chat uchun ham alohida taxmin qilib bo'lmaydigan token kerak.

### P1 — keyingi dizayn/UX sprinti

1. Rus rejimida yangi matnlar aralash: sotuvchi intro matni, `30 soniya...`,
   placeholderlar, telefon izohi, `Ismingiz?`, `Yana 60 ta ko'rsatish`,
   `1 soat oldin`. Joriy i18n testi 13/13 o'tadi, lekin bu dinamik matnlarni
   ushlamaydi. Matnni DOM bo'yicha almashtirish o'rniga `data-i18n` kalitlari
   bilan render qilish kerak.
2. Mobil natijada suzuvchi `Sotuvchilardan so'rash` tugmasi ikkinchi kartani
   yopadi va pastki tabbar bilan raqobat qiladi. Uni natija sarlavhasi ostidagi
   oddiy sticky panelga aylantirish ma'qul.
3. Desktopda ham mobil 5-tabbar chiqadi. Desktop headerning o'zi yetarli;
   pastki tabbarni faqat `max-width` breakpointda ko'rsatish kerak.
4. Sotuvchi kirish sahifasida birinchi renderda bo'sh ekran kuzatildi; keyin
   karta paydo bo'ldi. Darhol skelet yoki server-render qilingan asosiy karta
   ko'rsatish kerak.
5. Ro'yxatdan o'tishdagi `So'rovlarni ko'rish` CTA formani saqlashini aniq
   aytmaydi. `Ro'yxatdan o'tish va so'rovlarni ko'rish` tushunarliroq.

### P2 — sayqallash

1. Mobil bosh sahifadagi `126 153` e'lon soni ikki qatorga sinadi.
2. Desktop chatda dialog tanlanmagan holatda o'ng tomon katta bo'sh qoladi;
   `Suhbatni tanlang` empty-state kerak.
3. Demo chatdagi mahsulot rasmi o'rniga brend teksturasi ko'rinadi; real
   mahsulot rasmi demo ishonchliligini oshiradi.
4. Kategoriya kartalarida yuzlab kichik bo'lim chipi ko'p; foydalanuvchiga
   eng ommabop 6-8 tasi va `Barchasi` ochilishi yengilroq bo'ladi.

## Funksional sinovlar

- `yigish_sinov.py`: 13/13 PASS.
- `suhbat_sinov.py`: yangi rolli bildirishnoma sarlavhasiga moslashtirildi,
  22/22 PASS.
- `i18n_sinov.py`: 13/13 PASS, lekin yuqoridagi real brauzer auditi uning
  dinamik matnlar bo'yicha qamrovi yetarli emasligini ko'rsatdi.
- Brauzer konsoli: error/warning yo'q.

## Keyingi mahsulot komfortlari

1. Xaridor so'rovini yuborishdan oldin AI aniqlashtiruvchi chiplar bersin:
   o'lcham, byudjet, muddat, hudud, yetkazib berish.
2. Takliflarni bitta jadvalda solishtirish: narx, tayyor vaqt, masofa,
   reyting va kafolat.
3. Sotuvchiga bir tegishli tez javoblar: `Bor`, `Narxi ...`, `Bugun tayyor`,
   `Yetkazib beraman`.
4. Ishonch signallari: tasdiqlangan sotuvchi, oxirgi faollik, o'rtacha javob
   vaqti, bajarilgan buyurtmalar.
5. OBER ichidagi kuzatuv: saqlangan qidiruv yoki so'rovga yangi mos taklif
   kelganda ichki bildirishnoma.

## Skrinshotlar

- `01-xaridor-bosh-desktop.png`
- `02-xaridor-bosh-mobile.png`
- `03-xaridor-qidiruv-mobile.png`
- `04-xaridor-qidiruv-desktop.png`
- `06-sotuvchi-royxat-desktop.png`
- `07-sotuvchi-royxat-mobile.png`
- `09-chat-suhbat-desktop.png`
- `10-chat-suhbat-mobile.png`
- `11-bildirishnoma-mobile.png`
- `12-kategoriyalar-mobile.png`
