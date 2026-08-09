# 01 — Ma'lumot tekshiruvi (OLX)
_2026-07-30 · birinchi texnik tekshiruv_

## Savol

Avto ehtiyot qismlar bo'yicha narx va e'lon ma'lumotini yig'sa bo'ladimi?

## Javob: HA

`olx.uz/transport/avtozapchasti-i-aksessuary` sahifasi to'liq o'qildi.

### Hajm

| Bo'lim | E'lonlar soni |
|---|---|
| Avtozapchasti | 30 859 |
| Aksessuarlar | 26 383 |
| Avtozvuk | 5 247 |
| GPS/registrator | 2 303 |
| **Toshkent viloyati (jami kategoriya)** | **46 966** |

Boshqa viloyatlar: Samarqand 4 156 · Buxoro 3 215 · Farg'ona 2 282 ·
Xorazm 1 587 · Qashqadaryo 1 460 · Navoiy 1 088 · Andijon 909 ·
Qoraqalpog'iston 811 · Namangan 665 · Jizzax 645 · Surxondaryo 645 · Sirdaryo 485

### Har e'londan olinadigan ma'lumot

- Sarlavha (mahsulot nomi)
- **Narx** — so'mda, "Договорная" (kelishiladi) bayrog'i bilan
- Holati — Yangi / B.u.
- **Joylashuv — tuman darajasida** (Sergeli, Chilonzor, Yakkasaroy, Mirzo Ulug'bek...)
- Sana va vaqt ("Bugun 10:47")
- E'lon havolasi

Ya'ni **proximity (yaqinlik) bo'yicha moslashtirish mumkin** — bu katta ustunlik.

### Qidiruv URL tuzilishi

```
/transport/avtozapchasti-i-aksessuary/q-<so'rov>/
/transport/avtozapchasti-i-aksessuary/?page=N        (25 sahifagacha)
/transport/avtozapchasti-i-aksessuary/<viloyat>/
```

Sahifalar server tomonda render qilinadi — JS ishga tushirmasdan o'qiladi.

---

## Eng muhim topilma — og'riq ekranda ko'rinadi

Sotuvchilar bitta so'zni **bir necha imloda** yozadi:

> "BYD avto **chexol, chehol chixol chihol** авто чехол чехлы"
> "Akumlyator Gentra Cobalt Spark Nexia **Акумлятор** Kia Byd Hyundai 24/7"
> "Спарк учун бар холати яхшт" (o'zbekcha, kirillda)

**Sabab:** qidiruv ishlamaydi. Xaridor qaysi imloda yozishini bilmaydi, shuning uchun
sotuvchi hammasini sanab chiqadi.

Bu bizning g'oyamizning **eng kuchli dalili** — muammo taxmin emas, ko'rinib turibdi.
Va aynan shu joyda AI ustunlik beradi: aralash til va imloni tushunish.

---

## Muammolar

**1. Takroriy spam.** Bitta BYD chexol e'loni 7 marta, narxi ozgina farq bilan:
1 100 421 / 1 112 382 / 1 124 343 / 1 148 266 / 1 160 227 / 1 172 188 / 1 184 149.
Avtomatik yasalgan. Filtrlash kerak (bir xil sotuvchi + o'xshash sarlavha).

**2. Dollardan o'girilgan narxlar.** 119 611 = $10 (kurs ~11 961), 598 055 = $50,
1 794 165 = $150. Ya'ni ba'zi sotuvchi dollarda narxlaydi, OLX o'giradi.
Narx tahlilida buni hisobga olish kerak (kurs o'zgarsa narx "o'zgargandek" ko'rinadi).

**3. Huquqiy tomon.** OLX foydalanish shartlariga ega. To'g'ri yondashuv:
sekin so'rov yuborish, robots.txt hurmat qilish, manba ko'rsatish va havola qaytarish
(ularga trafik beramiz). Uzoq muddatda — rasmiy hamkorlik yoki API so'rash.

---

## Keyingi qadam

Bitta aniq so'rov bo'yicha sinov: masalan "Neksiya kolodka" —
qidiruv natijasi qanday chiqadi, nechta mos e'lon topiladi, narx oralig'i mantiqiymi.

## Boshqa manbalar (hali tekshirilmagan)

- Telegram savdo kanallari (eng katta manba bo'lishi mumkin)
- Uzum Market
- Do'konlarning o'z saytlari
