# OBER — loyiha konteksti

Bu fayl har seans boshida o'qiladi.

## OBER nima

Teskari marketplace. Xaridor kategoriya daraxtini titkilamaydi — **o'z
so'zi bilan yozadi**: "menga soat kerak bambino 6, kim 800 000 so'mga
beradi?". OBER ikki ish qiladi:

1. **Indeksdan qidiradi** — OLX va ochiq Telegram kanallaridan yig'ilgan
   270 mingdan ortiq e'lon, har 45 daqiqada yangilanadi.
2. **Topilmasa — so'raydi.** Talab mos sotuvchilarga boradi, ular OBER
   ichidagi chatda narx, muddat va rasm bilan javob beradi.

Telefon raqami almashilmaydi. Bitim OBER ichida qoladi.

**Bu faqat avtoqism sayti EMAS.** Avtoqism birinchi vertikal edi —
bozor zichligini yaratish uchun tanlangan. Maqsad: har qanday mahsulot,
xizmat va usta.

## FRONTEND ISHIDAN OLDIN — MAJBURIY

`web/` ichida biror narsa o'zgartirishdan oldin
**`OBER-DIZAYN-QOIDALARI.md` ni to'liq o'qi.**

Undagi har qoida yonida o'lchov va sana turibdi. Sababsiz qoida yo'q —
har biri bir marta buzilgan, o'lchangan va tuzatilgan narsa.

Eng ko'p takrorlangan xatolar:
- `[hidden]{display:none!important}` — har sahifada bo'lishi shart.
  Bu xato uch marta takrorlangan (index, takliflar, elon).
- Burchak radiusi faqat `--r-kichik/orta/katta/pill`. Xom `12px` yozilmaydi.
- Layout xossalari (`max-height`, `padding`, `width`) animatsiya qilinmaydi.
- Telefonda yopishqoq element **bitta**.
- `@media` ichidagi qoida avtomatik ustun emas — faylda keyingisi yutadi.

## Texnologiya — o'zgartirilmaydi

- Frontend: bitta HTML fayl, CSS va JS ichida. Framework yo'q, build yo'q.
- Backend: Python **standart kutubxonasi**. `pip install` yo'q.
- Baza: SQLite + FTS5, WAL rejimida.
- Yangi bog'liqlik qo'shishdan oldin: **busiz bo'ladimi?** Odatda bo'ladi.

## Production

- Sayt: https://ober.uz — Hetzner (77.42.123.90), Caddy + HTTPS
- Xizmatlar: `ober-server`, `ober-yangilik` (issiq sikl),
  `ober-toliq` (sutkalik qamrov), `ober-qorovul.timer` (tiriklik nazorati)
- **Serverga ulanish:** `NAVBATCHI.bat` ni oching. U `data/buyruq.txt` ni
  kutadi, serverda bajaradi, natijani `data/javob.txt` ga yozadi.
  Kod yuklash uchun buyruq fayliga bitta so'z: `yuklash`

## Sirlar — git'ga hech qachon tushmaydi

`.gitignore` himoya qiladi, lekin bilib turish kerak:

| Fayl | Nima |
|---|---|
| `data/bot-token.txt` | Telegram bot kaliti |
| `tmp/*token*` | jonli sotuvchi sessiya tokenlari |
| `data/ober.db` | baza — foydalanuvchi ma'lumotlari bilan |

AI kaliti loyihada **umuman yo'q** — u serverda `/etc/ober-ai.env`
(chmod 600). Kalitsiz ham kod ishlaydi, rasm tashqariga yuborilmaydi.

## Ishlash uslubi

- **O'lchov majburiy.** "Yaxshi ko'rinadi" — dalil emas. Har layout
  qarori raqam bilan tasdiqlanadi.
- **Sekinlikning sababi ko'pincha kodda emas, muhitda.** Avval o'lch,
  keyin optimallashtir.
- **Umumiy tamoyilni tuzatganda, u yana qayerda buzilganini qidir.**
  Bitta faylni tuzatib "tugadi" deyish — saboqni yarim o'rganish.
- Har ishdan keyin `memory/lessons.md` ga bitta xulosa.

## Ochiq muammolar (2026-08-09)

1. **Relevans testi qizil: 13 dan 5 tasi.** `relevans_sinov.py`.
   Kerakli natija ham kesilyapti ("Nexia kolodkasi qoldi" xato beradi).
2. **28 089 e'longa noto'g'ri avto yorlig'i.** Avto lug'ati avto
   bo'lmagan kategoriyalarga ham yorliq yopishtiryapti: "Доски" →
   `deska`, "LG XBOOM" → `rul_kolonka`, "Super" → `bamper`.
   Yechim: yorliq faqat e'lon avto kategoriyasida bo'lsa qo'yilsin.
3. **Chat bildirishnomasi buzilgan.** `suhbat_sinov.py` yiqilyapti:
   sotuvchi javob beradi, xaridorga bildirishnoma bormaydi.
4. Dizayn tizimida 24 ta tizimdan tashqari radius qiymati.

## Til

Aziz bilan muloqot — o'zbekcha, aniq va qisqa.
Interfeys — o'zbekcha, ruscha tarjima `web/i18n.js` orqali.
Raqamlar bo'shliq bilan: `127 360 so'm`. `toLocaleString` ishlatilmaydi.
