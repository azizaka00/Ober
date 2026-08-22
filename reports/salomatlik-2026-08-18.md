# OBER — salomatlik tekshiruvi 2026-08-18

O'lchov urinishi: 11:21–11:28 (Toshkent).
**Hech narsa o'zgartirilmadi.** Faqat kuzatuv.

## XULOSA: tekshiruv BAJARILMADI

Serverga yagona yo'l — `NAVBATCHI.bat` — **ishlamayapti**.
Ya'ni bugun server holati haqida hech qanday raqam yo'q.

Bu "sayt o'chdi" degani EMAS. Bu "sayt tirikmi, bilmaymiz" degani.

## Dalil

`data\buyruq.txt` 11:21 da yozildi va **7 daqiqa davomida
qo'l tegmay turdi**. NAVBATCHI har 3 soniyada tekshiradi —
ishlayotgan bo'lsa 3 soniyada olardi.

Ikkinchi dalil, kuchliroq: `NAVBATCHI.bat` buyruqni ko'rishi
bilan **eng birinchi ish** — `javob.txt` ni yangi sarlavha bilan
qayta yozish (skriptning 31-qatori, `bajarish`dan oldin).

    javob.txt oxirgi o'zgargan: 17.08.2026 22:56

Ya'ni javob fayli kechagi zaxira ishidan qolgan holida turibdi —
navbatchi buyruqni **umuman ko'rmagan**. Agar u ishlab, so'ng
serverga ulanolmay qotgan bo'lsa, `javob.txt` bugungi sana bilan
yangilangan bo'lardi. Yangilanmagan.

Sabab: oyna yopilgan (kompyuter o'chgan, qayta yuklangan yoki
oyna qo'lda yopilgan).

## Nima qilish kerak

`D:\OBER\NAVBATCHI.bat` ni oching va oynani ochiq qoldiring.

Buyruq fayli **o'z joyida qoldirildi** — men uni o'chirmadim.
Oyna ochilishi bilan tekshiruv o'zi yugurib, natija
`data\javob.txt` ga tushadi. Qayta yozish shart emas.

Buyruqda kechagi saboq hisobga olingan: hamma `sqlite3`
`-readonly` bilan, hamma buyruqda `timeout` / `--max-time` bor
(17.08 da buyruq 8 daqiqa qotib qolgan edi).

## Sentry — hamon ulanmagan

Kechagi hisobotdagi holat o'zgarmagan, hatto biroz aniqroq:

Cowork'da **Sentry konnektori umuman yo'q** — konnektor
registrida `sentry` bo'yicha qidiruv 0 natija berdi. Ya'ni
`naiza` / `naiza-api` loyihasidagi xatolarni bu yerdan o'qish
imkoni yo'q.

Zaxira tekshiruv (`journalctl -u ober-server` da
"Sentry yoqilgan" bormi) ham bajarilmadi — u ham serverga
ulanishni talab qiladi.

Ulash kerak bo'lsa: claude.ai → konnektor sozlamalari.
Eslatma, 17.08 hisobotidan: server tomonida DSN va drop-in
tayyor, lekin `sentry_sdk` o'rnatilmagan (loyiha qoidasi
`pip install` yo'q), shuning uchun yuborish `urllib` bilan
qo'lda yozilishi kerak.

## E'lon soni — taqqoslash yo'q

| Sana | Faol e'lon |
|---|---|
| 2026-08-17 | 547 673 |
| 2026-08-18 | **o'lchanmadi** |

Kechagi hisobotda "ertadan boshlab taqqoslash aniq bo'ladi"
deb yozilgan edi. Afsuski qator uzildi — birinchi taqqoslash
NAVBATCHI qayta ochilgandan keyin bo'ladi.

## Ochiq qolgan, kechagidan

Bularning holati bugun tekshirilmadi, lekin yopilgani ma'lum
emas — 17.08 hisobotida batafsil:

1. **O'lik havola nazorati hech narsani nofaollashtirmayapti.**
   Ikkinchi tasdiq uchun butun indeks aylanishi kerak —
   hozirgi tezlikda ~2 yil 4 oy. 26 ta e'lon `olik_soni=1` da
   qotgan. Qaror Azizniki (3 ta variant kechagi hisobotda).
2. **Sentry ulanmagan** — yuqorida.
