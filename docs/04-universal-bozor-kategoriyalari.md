# OBER — universal bozor kategoriyalari

Sana: 2026-07-31

Bu hujjat OBER faqat avtoehtiyot qismlari yoki xizmatlar sayti emasligini mustahkamlaydi. OBER mahsulot, xizmat, ish, ko‘chmas mulk, transport va boshqa bozor obyektlarini bitta ichki taksonomiyaga moslaydi.

## Asosiy manba guruhlari

- [Bolalar dunyosi](https://www.olx.uz/oz/detskiy-mir/): kiyim, oyoq kiyimi, kolyaska, avtoo‘rindiq, mebel, o‘yinchoq, bolalar transporti, oziqlantirish, maktab mahsulotlari.
- [Ko‘chmas mulk](https://www.olx.uz/oz/nedvizhimost/): sutkalik ijara, kvartira, xususiy uy, yer, garaj/turargoh, tijorat binosi, dacha.
- [Transport](https://www.olx.uz/oz/transport/): yengil avtomobil, ehtiyot qismlar, shina/disk, moto, avtobus, yuk mashinasi, tirkama, maxsus va qishloq xo‘jaligi texnikasi, suv transporti.
- [Ish](https://www.olx.uz/oz/rabota/): savdo, logistika, qurilish, restoran, moliya, xavfsizlik, uy xodimi, sport/go‘zallik, turizm, ta’lim, tibbiyot, IT, marketing, ishlab chiqarish, HR/ofis, avtoservis va boshqa bandlik turlari.
- [Hayvonlar](https://www.olx.uz/oz/zhivotnye/): it, mushuk, baliq, qush, kemiruvchi, qishloq xo‘jaligi hayvoni, mahsulot va xizmatlar, tekin hayvonlar.
- [Uy va bog‘](https://www.olx.uz/oz/dom-i-sad/): mebel, tomorqa, interyer, qurilish/ta’mirlash, asboblar, o‘simlik, idish-tovoq, bog‘ va xo‘jalik jihozlari, oziq-ovqat, basseyn.
- [Elektr jihozlari](https://www.olx.uz/oz/elektronika/): telefon, kompyuter, foto/video, TV, audio, aqlli qurilma, o‘yin, maishiy va oshxona texnikasi, iqlim qurilmalari, aksessuarlar.
- [Xizmatlar](https://www.olx.uz/oz/uslugi/): AI, avto-moto, go‘zallik/salomatlik, tozalash, maishiy, enaga/parvarish, uskuna va biznes, material, ta’mirlash, tashish/ijara, prokat, qurilish/usta, biznes, ta’lim, moliya, hayvonlar, tarjima/matn, tadbir/foto/video, turizm, yuridik, taom yetkazish, sport.
- [Moda va stil](https://www.olx.uz/oz/moda-i-stil/): kiyim, to‘y, soat, aksessuar, sovg‘a, go‘zallik va salomatlik.
- [Xobbi, dam olish va sport](https://www.olx.uz/oz/hobbi-otdyh-i-sport/): antikvar, musiqa, sport, kitob, media, chipta.
- [Tekinga beraman](https://www.olx.uz/oz/otdam-darom/).
- [Ayirboshlash](https://www.olx.uz/oz/obmen-barter/).
- Maxsus kesimlar: konditsioner, aviachipta, qurilish mahsulotlari, dacha, oziq-ovqat va oshxona.

## Backend qoidasi

1. Tashqi manba kategoriyasi o‘z holicha foydalanuvchiga majburlanmaydi.
2. Har adapter `source_category` va `source_subcategory`ni saqlaydi, keyin ularni OBERning ichki yashirin taksonomiyasiga moslaydi.
3. Ichki yuqori darajali `intent_type`: `product`, `service`, `job`, `property`, `vehicle`, `rental`, `free`, `barter`.
4. Taksonomiya hardcode qilingan yopiq ro‘yxat bo‘lmaydi; yangi manba va kategoriya qo‘shilganda kengaya oladi.
5. Xaridor kategoriya daraxtini tanlamaydi. U erkin yozadi; OBER intent, kategoriya va parametrlarni aniqlaydi.
6. Kategoriya ishonchli aniqlanmasa noto‘g‘ri natija qaytarilmaydi; aniqlashtiruvchi savol beriladi.
7. Har manba adapteri manbaning foydalanish shartlari, ruxsatlari va texnik cheklovlariga alohida rioya qiladi.

## Hero uchun qoida

Hero har bir subkategoriyani alohida ko‘rsatmaydi. U universal bozorni bir yaxlit mahalliy ko‘cha orqali his qildiradi; yaqinroq qaralganda bolalar, moda, hayvonlar, uy, transport, elektronika, oziq-ovqat va xizmatlar ko‘rinadi. Markazdagi qidiruv baribir asosiy harakat bo‘lib qoladi.
