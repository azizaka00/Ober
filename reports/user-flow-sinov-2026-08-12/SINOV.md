# User-flow sinov — 2026-08-12

Xaridor va sotuvchi bo'lib to'liq interaktiv sinov. Muxit: lokal server
(127.0.0.1:8800, real baza). Brauzer (Chrome) + API zanjiri birgalikda.

## XARIDOR oqimi

| Qadam | Natija |
|---|---|
| Bosh sahifa ochiladi | ✅ quyuq navy, sarlavha, qidiruv maydoni ("Masalan: 25 m² banner") |
| Qidiruv: "divan" | ✅ 14 ta natija, yo'nalish: Mebel |
| Natija sahifasi | ✅ `body.is-results` (quyuq), 14 ta karta, birinchi: "Audit divan yangi 2 orinli" |
| Saralash chiplari | ✅ 4 ta: "Mosligi bo'yicha 14 / Avval arzoni 14 / Yangisi 14 / Yaqini 14" — sonlar bilan |
| Tanlangan chip | ✅ amber gradient (computed `rgba(0,0,0,0)` — gradient background-image da, kutilgan) |
| So'rov yuborish formasi | ✅ "Sotuvchilardan so'rash" tugmasi bor |
| So'rov API | ✅ so'rov 134 → 4 ta mos sotuvchiga tarqatildi ("tarqatildi" holati) |

## SOTUVCHI oqimi

| Qadam | Natija |
|---|---|
| Ro'yxatdan o'tish | ✅ token qaytaradi, yo'nalishlar: "Uy va bog'", "Mebel" |
| Kabinet: kelgan so'rovlar | ✅ yangi so'rov ro'yxatda ko'rindi |
| Javob yuborish (750 000 so'm) | ✅ javob yozildi, suhbat ochildi |
| Chat xabari (sotuvchi) | ✅ "Assalomu alaykum! Divan 750 000 so'm..." saqlandi |
| Xaridor o'qiydi | ✅ 2 ta xabar ko'rindi (avto javob + yangi) |
| Xaridor javob yozadi | ✅ "Yaxshi, ertaga olaman" |
| Sotuvchi bildirishnoma | ✅ 1 ta yangi bildirishnoma keldi |

## Xavfsizlik tekshiruvi (qo'shimcha yutuq)

- **401 to'g'ri ishlaydi**: so'rov yuborilmagan sotuvchi javob bera olmaydi
  (so'rov 133 da sinandi — 401, kutildi).
- **Token talab**: `/api/sotuvchi/javob` ID raqamni emas, tokenni talab
  qiladi — `_sotuvchi_ident` `isdigit()` ni rad qiladi (taxmin qilib
  bo'lmasin).

## UI sahifalari (brauzer)

| Sahifa | Natija |
|---|---|
| `/` | ✅ quyuq hero, qidiruv maydoni |
| `/?q=divan` | ✅ quyuq natija, kartalar, amber chip |
| `/takliflar` | ✅ "OBER — Chat", bo'sh holat "Faol xaridor so'rovi yo'q" |
| `/sotuvchi` | ✅ forma to'liq (nom, nima, tuman, aloqa), amber gradient 4 joyda |
| `/kategoriyalar` API | ✅ 12 guruh, ikki daraja, real sonlar (Transport 40 413, pastki 14 ta) |

## Topilgan kamchiliklar

1. **`/favicon.ico` 404** — brauzer avtomatik so'raydi, sayt
   `brend/icon.png` ishlatadi. Zararsiz, lekin tuzatish oson:
   serverda `/favicon.ico` so'roviga `brend/icon.png` qaytarish.
2. **E'lon kartasi ochilishi** — brauzer agenti karta bosilishini
   tekshira olmadi (agent cheklovi). API darajasida `/api/elon/{id}`
   to'g'ri ishlaydi (o'z e'lonlari); tashqi e'lon havolasi asl manbaga
   ochiladi (dizayn bo'yicha).

## O'lchovlar

- web_sinov: **33/33** ✅
- i18n_sinov: **13/13** ✅
- Baza: sinov yozuvlari tozalandi (xabarlar, suhbatlar, javoblar,
  yuborishlar, sorovlar, sotuvchi) — qoldiq 0.
- Konsol xatolari: faqat favicon.ico 404 (yuqoridagi kamchilik).

## Xulosa

Asosiy halqa (qidiruv → so'rov → tarqatish → javob → chat →
bildirishnoma) to'liq ishlaydi. Quyuq/amber UI barcha sahifada joyida.
Sinovda backend xatosi topilmadi — topilgan yagona narsa favicon.ico
404 (kosmetika).
