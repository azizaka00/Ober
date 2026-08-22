# OBER — tashqi xizmatlar va to'lovlar

2026-08-22 da serverdan va koddan yig'ilgan. Bu ro'yxat **texnik
ulanish** bo'yicha — qaysi xizmat OBERga haqiqatan tegishli.
Tarif va summalar bu yerda yo'q, chunki ular hisob-kitob
kabinetlarida va men ularni ko'rmayman. Summani o'zingiz
qo'shib qo'ying.

## To'xtasa OBER YIQILADI

| Xizmat | Nima uchun | Dalil | Muddat |
|---|---|---|---|
| **Hetzner** | server (77.42.123.90) | Ubuntu 26.04, 1 CPU, 1.9 GB RAM, 38 GB disk, KVM | oylik, avtomatik |
| **ober.uz domeni** | saytning manzili | registrator **SUVAN NET** | **04-avgust 2027** |

Domen tugasa sayt butunlay ochilmaydi va pochta ham o'ladi.
Hetzner to'lovi o'tmasa server to'xtaydi — ma'lumot darhol
yo'qolmaydi, lekin sayt ishlamaydi.

## To'xtasa BIR QISMI ishlamaydi

| Xizmat | Nima uchun | Dalil | To'lov turi |
|---|---|---|---|
| **OpenAI API** | rasm bilan qidirish | `OPENAI_API_KEY`, `api.openai.com/v1/responses`, `app/ai_vision.py` | sarfga qarab |
| **Sentry** | xatolar haqida xabar | `/etc/ober-sentry.env`, loyiha `naiza-api` | bepul yoki oylik |

OpenAI kaliti tugasa qolgan hamma narsa ishlayveradi — faqat
rasmli qidiruv o'chadi (`ai_vision.yoqilganmi()` false qaytaradi
va kod buni kutadi). Sentry o'chsa sayt ishlaydi, lekin xatolar
jimgina yo'qoladi — bu eng xavfli holat, chunki hech narsa
buzilganday ko'rinmaydi.

## Bepul — pul ketmaydi

| Xizmat | Nima uchun |
|---|---|
| Telegram Bot API | sotuvchi bildirishnomalari (`t.me`) |
| Let's Encrypt | HTTPS sertifikati — Caddy o'zi yangilaydi (hozirgi muddat 2-noyabr 2026) |
| Firebase Cloud Messaging | brauzer push (`fcm.googleapis.com`) — bepul chegara |
| GitHub | `azizaka00/Ober` — ochiq repo |
| cbu.uz | Markaziy bank dollar kursi — ochiq API |

## Bir martalik

| Xizmat | Izoh |
|---|---|
| Google Play Console | dasturchi hisobi — bir marta $25. APK va assetlinks tayyor, ya'ni hisob ochilgan bo'lsa kerak |

## Alohida — OBERga tegishli emas, lekin ish uchun kerak

Claude (Anthropic) obunasi — kod yozish va shu seanslar uchun.
OBER serveri unga bog'liq emas.

---

## "Hammasini bittada to'lasam bo'ladimi?"

**Yo'q.** Bular turli kompaniyalar, turli valyuta va turli
davrlarda: Hetzner Germaniyada oylik, domen O'zbekistonda yillik,
OpenAI AQShda sarfga qarab. Ularni bitta hisob-fakturaga
yig'adigan xizmat yo'q.

Amalda qilinadigan narsa boshqacha — **unutishni yo'qotish**:

1. **Hammasini BITTA kartaga bog'lang** va har birida avtomatik
   to'lovni yoqing. Shunda faqat bitta karta muddatini kuzatasiz.
2. **Karta tugash sanasini kalendarga yozing.** Amalda eng ko'p
   uchraydigan nosozlik — xizmat emas, kartaning muddati tugashi.
   O'shanda hammasi bir vaqtda to'xtaydi.
3. **Yillik to'lovlarga eslatma qo'ying.** Oyliklar o'zi yechiladi
   va o'tmasa pochta keladi; yilliklar esa unutiladi. Bu yerda
   yolg'iz yillik — domen, 2027-yil 4-avgust.
4. **Hisob-kitob pochtasini alohida papkaga yig'ing** va uni
   oyiga bir marta ko'rib chiqing. Hetzner, OpenAI va Sentry
   to'lov o'tmasa avval POCHTA yuboradi — o'sha xat o'qilmasa
   xizmat keyin o'chadi.

Eng katta xavf pul emas, **e'tibor**: to'rttadan uchtasi (Hetzner,
OpenAI, Sentry) to'xtaganini sayt darhol ko'rsatmaydi.
