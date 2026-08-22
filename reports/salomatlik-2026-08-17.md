# OBER — salomatlik tekshiruvi 2026-08-17

O'lchov vaqti: 14:00–14:04 (Toshkent), server 09:00–09:04 UTC.
**Hech narsa o'zgartirilmadi.** Faqat kuzatuv.

## Umumiy holat

Sayt ishlaydi, hamma xizmat tirik, javob vaqti normadan yaxshi.
Ikkita narsa Azizning qaroriga muhtoj (pastda).

## Raqamlar

| O'lchov | Qiymat | Norma |
|---|---|---|
| `ober-server` · `ober-yangilik` · `ober-toliq` | uchalasi `active` | active |
| Faol e'lon | **547 673** | — |
| Nofaol e'lon | 127 255 | — |
| Jami yozuv | 674 928 | — |
| Disk | 12G / 38G — **34%** | < 80% |
| Load average | 0.16 / 0.17 / 0.16 | — |
| Uptime | 14 kun 19 soat | — |
| Baza hajmi | 1.3 GB (+ WAL 16 MB) | — |

Sahifalar — hammasi `200`:

| Sahifa | Kod | Vaqt |
|---|---|---|
| `/` | 200 | 0.0018 s |
| `/?q=divan` | 200 | 0.0010 s |
| `/api/holat` | 200 | 0.0350 s |
| `/api/kurs` | 200 | 0.0005 s |
| `/sotuvchi` | 200 | 0.0015 s |
| `/takliflar` | 200 | 0.0009 s |
| `/kategoriyalar` | 200 | 0.0019 s |

Eng sekin sahifa 35 ms — 0.1 s normasidan 3 barobar tez.

## E'lon soni — o'sganmi?

**O'sgan.** `CLAUDE.md` da 2026-08-16 o'lchovi 519k deb yozilgan;
bugun 547 673 → **+~28 000 (~5%)**.

O'sish jonli: 14:00 da 547 496, 14:03 da 547 673 edi — uch daqiqada
+177 (issiq sikl ishlayotgani uchun).

> Diqqat: bu birinchi salomatlik hisoboti, shuning uchun "kechagi son"
> `CLAUDE.md` dagi eslatmadan olindi, aniq o'lchovdan emas. **Ertadan
> boshlab taqqoslash aniq bo'ladi — bugungi tayanch: 547 673.**

## DIQQAT 1 — o'lik havola nazorati hech narsani o'chirmayapti

Ikki yugurish bo'lgan (xizmat 2026-08-16 da qo'shilgan):

| Vaqt (UTC) | tirik | o'lik javob | nofaollashdi |
|---|---|---|---|
| 16.08 21:33 | 189 | 11 | **0** |
| 17.08 03:37 | 185 | 15 | **0** |

26 ta e'lon "o'lik" degan **birinchi** tasdiqni oldi
(`olik_soni=1`), lekin ikkinchisini hech biri olmadi.

Sabab kodda, `havola_nazorat.py:120-123`:

    ORDER BY COALESCE(tekshirildi, 0) ASC, id ASC LIMIT ?

Ya'ni "eng uzoq tekshirilmagani birinchi" — navbat. To'g'ri tanlov,
lekin ikkinchi tasdiq uchun **butun indeks bir marta aylanishi kerak**.

O'lchov: 200 ta / yugurish × 4 yugurish / kun = **800 ta / kun**.
674 928 yozuv ÷ 800 = **843 kun ≈ 2 yil 4 oy** bitta aylanishga.

Ya'ni hozirgi tezlikda `olik_soni=1` dagi 26 ta e'lon ikkinchi
tasdiqni ~2.3 yildan keyin oladi. **Amalda hech qachon
nofaollashmaydi.**

Hozircha 400 tasi tekshirilgan (674 928 dan). O'lim ulushi
26/400 = **6.5%** — `CLAUDE.md` dagi birinchi 4% o'lchovidan
yuqori. 547 673 faol e'londa bu **~35 000 chirigan havola**.

"Faqat aniq dalil o'chiradi" tamoyili to'g'ri va buzilmasligi kerak.
Muammo tamoyilda emas — **tezlikda**. Qaror Azizniki, variantlar:

1. Yugurishdagi sonni oshirish (200 → masalan 2000). Manbaga hurmat
   saqlanadi: 2 s/so'rov × 2000 = ~67 daqiqa, kuniga 4 marta.
2. `olik_soni>=1` bo'lganlarni navbatning oldiga qo'yish — ikkinchi
   tasdiq kunlar ichida keladi, butun aylanish kutilmaydi.
3. Ikkinchi tasdiqni vaqt bilan bog'lash (masalan birinchi tasdiqdan
   24 soat o'tsa qayta tekshirish).

Men **hech narsa o'zgartirmadim** — bu kuzatuv hisoboti.

## DIQQAT 2 — Sentry ulanmagan

Server tomonida sozlama **to'liq tayyor**:

- `/etc/ober-sentry.env` bor (chmod 600, root)
- `ober-server.service.d/sentry.conf` drop-in bor,
  `EnvironmentFile` ko'rsatilgan
- DSN jarayon muhitida mavjud (`/proc/<pid>/environ` da topildi),
  format to'g'ri: `https://***@o4511755094458368.ingest.de.sentry.io/4511755791040592`

**Lekin jurnalda "Sentry yoqilgan" qatori yo'q** — ya'ni kod DSN'ni
o'qib ishlatmayapti. Sozlama bor, ulanish yo'q.

Bu kutilgan bo'lishi mumkin: loyiha qoidasi "Python standart
kutubxonasi, `pip install` yo'q" — `sentry_sdk` o'rnatilmagan. Ya'ni
Sentry'ga yuborish qo'lda (`urllib` bilan) yozilishi kerak.

Qo'shimcha: **Cowork'da Sentry konnektori ulanmagan** — shuning uchun
`naiza-api` loyihasidagi xatolarni bu yerdan o'qiy olmadim. Ulash
kerak bo'lsa claude.ai konnektor sozlamalaridan.

## DIQQAT 3 — kichik, lekin bilib turish kerak

Birinchi tekshiruv buyrug'i **8 daqiqadan ko'p javob bermadi va
tashlandi**. Ikkinchi urinish, xuddi shu tekshiruvlar bilan, 100
soniyada tugadi.

Yagona muhim farq: `sqlite3` **`-readonly`** bilan ochildi va hamma
buyruqqa `timeout` / `curl --max-time` qo'yildi.

Ikki holatda ham `ober-yangilik` va `ober-toliq` bir xil darajada
band edi (jurnalda ko'rindi: `ober-toliq` [9491/10426] da, sekundda
bir yozuv). Ya'ni sabab yuklama emas — **1.3 GB bazani yozish
huquqi bilan ochish** bo'lishi ehtimoli katta.

Bu OBER kodiga tegishli emas, faqat NAVBATCHI orqali qo'l bilan
so'rov yuborishga tegishli. Xulosa: **jonli bazadan o'qiganda har
doim `sqlite3 -readonly` va `timeout` ishlatilsin** — aks holda
buyruq navbatni qotirib qo'yadi.

## Qo'riqchilar joyida

- `ober-havola.timer` — keyingi 09:23 UTC, oxirgi 03:29 UTC (5s 30d oldin)
- `ober-qorovul.timer` — har 2 daqiqada, oxirgi 3 soniya oldin
