# OBER — ober.uz

**Nima kerak bo'lsa — so'rang, biz topamiz.**

Teskari bozor: xaridor nima kerakligini yozadi → tizim mavjud e'lonlardan topadi →
narx oralig'ini va kontaktlarni ko'rsatadi → sotuvchiga "sizga xaridor bor" xabari boradi.

---

## Holat

**Bosqich:** 0 — ma'lumot yig'ish sinovi
**Boshlandi:** 2026-07-30
**Kategoriya:** avto ehtiyot qismlar (birinchi va yagona)

---

## Nega bu ishlaydi

**Tuxum-tovuq muammosi yechilgan:** sotuvchi yig'ilmaydi — **import qilinadi.**
OLX'da 30 000+ avto qism e'loni bor, Telegram kanallarida har kuni narx yoziladi.
Bu ma'lumot ochiq turibdi, faqat qidirib bo'lmaydigan holatda.

**Og'riq isbotlangan:** OLX sotuvchilari bitta so'zni 4 xil imloda yozadi
("chexol chehol chixol chihol") — chunki qidiruv ishlamaydi va ular buni
qoplashga urinadi. Aralash o'zbek-lotin, o'zbek-kirill, rus tili bir sarlavhada.
**AI aynan shu yerda ustunlik beradi.**

**Google yecholmaydi:** do'kondagi tovar internetda yozilmagan. Google yozilganni
topadi, biz esa biladigan odamdan so'raymiz.

---

## Birinchi versiya — 5 ta ish, ortiqchasi yo'q

1. So'rov qabul qilish (matn yoki rasm)
2. Mavjud e'lonlardan qidirish (indekslangan ochiq manbalar)
3. Natija: narx oralig'i + nechta joyda bor + kontaktlar
4. Topilmasa → navbatga tushadi, qo'lda topiladi (xaridor bilmaydi)
5. Sotuvchiga xabar: "tovaringizga xaridor bor"

**Qurilmaydi:** profil, reyting, to'lov, chat, native ilova.

---

## Qat'iy qoidalar

- **"Eng arzon" deb aytilmaydi.** Faqat: "4 ta taklif topdik: 150 000 – 240 000".
  Isbotlab bo'lmaydigan da'vo ishonchni o'ldiradi.
- **Xaridordan pul olinmaydi.** Hech qachon. U kamyob tomon.
- **Bir tor kategoriya**, unda 90% javob. Keng qamrash = hamma joyda yomon.
- Ma'lumot yig'ishda manbalarning qoidalari hurmat qilinadi.

---

## Daromad (bosqichma-bosqich)

| Vaqt | Nima | Daromad |
|---|---|---|
| 1-6 oy | Foydalanuvchi yig'iladi | 0 (ataylab) |
| 6-12 oy | So'rovlar yoqiladi, sotuvchi bepul | 0 → birinchi |
| 12-18 oy | Sotuvchi obunasi + yuqorida ko'rinish | 250-400 ming/oy har sotuvchidan |
| 18+ oy | Narx tahlilini biznesga sotish | 10 mijoz x 3 mln = 30 mln/oy |

**Trigger sana emas, RAQAM:** 5 000 qidiruv/oy → so'rov tugmasi.
200 so'rov → sotuvchidan pul.

---

## O'lchov (faqat uchta raqam)

1. So'rovning necha %iga javob keldi — **maqsad 80%+**
2. O'rtacha javob vaqti — **maqsad 30 daqiqadan kam**
3. **Necha xaridor QAYTA keldi** — eng muhimi, bozor borligini faqat shu isbotlaydi

---

## Papka tuzilishi

```
ober/
  README.md      bu fayl — loyiha ta'rifi va qarorlar
  docs/          reja, tadqiqot, qarorlar tarixi
  data/          yig'ilgan ma'lumot (e'lonlar, narxlar)
  app/           backend kodi
  web/           sayt (PWA)
```

---

## Yuridik

Kompaniya: **"NAIZA" MChJ** (STIR 313204884) — nom o'zgarmaydi.
Mahsulot brendi: **OBER**. (Alphabet/Google modeli.)

Boshida sotuvchi obunasi → merchant kerak emas, hisob-faktura yetadi.

---

## NAIZA'dan qayta ishlatiladi

`auth.py` (kirish) · `credits.py` (hisob) · `legal.py` (oferta/rekvizit) ·
`storage.py` · Railway + Docker sozlamalari · PWA (manifest, service worker) · Sentry.

NAIZA video **o'chirilmaydi** — jonli qoladi, lekin rivojlantirilmaydi.
