# OBER — xaridor va sotuvchi oqimi auditi

## Audit scope

- Surface: lokal OBER xaridor sahifasi va sotuvchi kabineti.
- User goal: banner so‘rovini noto‘g‘ri avto natijalarisiz yuborish, mos banner sotuvchisidan narx olish va javobni OBER ichida ko‘rish.
- Accessibility target: mobil reflow, aniq label, 44 px+ boshqaruvlar, ko‘rinadigan fokus va shaxsiy ma’lumotni oshkor qilmaslik.
- Browser evidence: 390 × 844 mobil viewport; 1280 × 800 desktop reflow ham tekshirildi.

## Steps and health

1. **Bosh sahifa — yaxshi.** Hero, qidiruv va joy tanlash birinchi ekranda aniq. Dalil: `01-bosh-sahifa.png`.
2. **Eski banner natijasi — P0 xato edi.** Banner so‘roviga 66 ta avto e’lon va soxta narx oralig‘i chiqardi. Dalil: `02-banner-xato-natija.png`.
3. **Sotuvchi onboarding — tuzatildi.** Biznes/ism maydoni, mahsulot yoki xizmat erkin matni, joy va maxfiy telefon izohi qo‘shildi. Dalil: `03-sotuvchi-onboarding-yakuniy.png`.
4. **Banner qidiruvi — yaxshi.** Endi 0 ta noto‘g‘ri karta, tanilgan `Banner va tashqi reklama` yo‘nalishi va jonli so‘rov CTA chiqadi. Dalil: `04-banner-togri-jonli-sorov.png`.
5. **Sotuvchiga routing — yaxshi.** Banner so‘rovi banner sotuvchisiga yetadi; xaridor telefoni ko‘rinmaydi. Dalil: `05-banner-sotuvchiga-yetdi.png`.
6. **Sotuvchi javobi — yaxshi.** `BOR` uchun narx majburiy, 280 000 so‘mlik taklif yuborildi va karta ro‘yxatdan chiqdi. Dalil: `06-sotuvchi-javobi.png`.
7. **Xaridor so‘rov yuborishi — yaxshi.** So‘rov qabul qilingani va mos sotuvchilarga yuborilgani aniq ko‘rsatiladi. Dalil: `07-xaridor-sorov-yubordi.png`.
8. **Xaridor javob olishi — yaxshi.** 275 000 so‘mlik taklif polling orqali chiqdi; sotuvchi telefoni ochilmadi. Dalil: `08-xaridor-taklifni-kordi.png`.

## Strengths

- Qidiruv noto‘g‘ri ishonch bermaydi: indeks bilmagan narsani “bilaman” demaydi.
- Kategoriya daraxti foydalanuvchiga chiqarilmadi; routing ichki yo‘nalish tegi bilan ishlaydi.
- Xaridor va sotuvchi telefonlari API javoblaridan olib tashlandi.
- Birinchi sotuvchi `BOR` degach so‘rov boshqa mos sotuvchilardan yashirilmaydi; bir nechta taklif yig‘ilishi mumkin.
- Mobil kartalar, tugmalar va label’lar tiqilib qolmaydi; 390 va 1280 px da gorizontal overflow yo‘q.

## UX and accessibility risks resolved

- **P0 — noto‘g‘ri kategoriya:** banner → avto narxi xatosi xavfsiz bo‘sh holat bilan almashtirildi.
- **P0 — maxfiylik:** xaridor telefoni sotuvchi API’sidan, sotuvchi telefoni xaridor javobidan olib tashlandi.
- **P1 — onboarding:** sotuvchi nomi va joylashuvi majburiy qilindi; xizmat ko‘rsatuvchi copy’si qo‘shildi.
- **P1 — takliflar soni:** birinchi javobdan keyin ham boshqa mos sotuvchilar so‘rovni ko‘radi.
- **P1 — narxsiz BOR:** klient va server darajasida bloklandi.
- **P2 — mobil label:** uzun yordamchi matn mobilda alohida qatorda ko‘rsatiladi.

## Evidence limits

- Screen reader va real mobil klaviatura bilan to‘liq accessibility auditi qilinmadi.
- Web-push, akkaunt tasdiqlash va real ichki yozishma bu bosqich scope’iga kirmadi.
- Banner uchun tashqi e’lon indeksi hali ulanmagan; hozir banner yo‘nalishi jonli sotuvchi halqasi orqali ishlaydi.

## Next product opportunity

- Keyingi katta bosqich: tanlangan taklifdan OBER ichidagi yozishmaga o‘tish va sotuvchiga web-push bildirishnoma. Buning uchun alohida visual target va oqim dizayni kerak.
