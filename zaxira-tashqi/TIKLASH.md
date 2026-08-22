# Tashqi zaxira — nima bor va qanday tiklanadi

Bu papkadagi fayllar **serverdan tashqarida** turadi. Serverdagi
`data/zaxira/ober-1..7.db` (kunlik to'liq nusxa) faqat "o'chirib
yubordim" holatidan himoya qiladi — server yoki disk yiqilsa ular
ham birga yo'qoladi. Shu papka aynan o'sha holat uchun.

## Ichida nima bor

| Fayl | Nima | Qayta tiklanadimi |
|---|---|---|
| `ober-odamlar-YYYYMMDD.sql.gz` | sotuvchilar, so'rovlar, javoblar, suhbatlar, xabarlar, yuborishlar, push obunalari, sozlama, qidiruvlar | **YO'Q** — bular odamlar |
| `ober-narx-YYYYMMDD.sql.gz` | `narx_tarix` — 1.3 mln+ qator | **YO'Q** — kechagi narxni bugun o'lchab bo'lmaydi |

**E'lonlar (`elonlar`, 680 000+) ATAYLAB YO'Q.** Ular OLX va
Telegramdan qayta yig'iladi, ya'ni 1.3 GB ni har kuni tashqariga
ko'chirishning ma'nosi yo'q. Zaxira 20 MB atrofida qoladi.

**Sessiya tokenlari va kirish kodlari ham ataylab yo'q** — zaxirada
yotgan token qo'shimcha xavf, foydasi esa nol.

## Qanday tiklanadi

Bo'sh bazaga to'liq yuklanadi (2026-08-22 da sinovdan o'tkazilgan):

```bash
zcat ober-odamlar-20260822.sql.gz | sqlite3 yangi.db
zcat ober-narx-20260822.sql.gz    | sqlite3 yangi.db
```

Yoki Python bilan (Windows'da qulayroq):

```python
import gzip, sqlite3
c = sqlite3.connect("yangi.db")
for f in ("ober-odamlar-20260822.sql.gz", "ober-narx-20260822.sql.gz"):
    with gzip.open(f, "rt", encoding="utf-8") as fh:
        c.executescript(fh.read())
c.commit()
```

E'lonlarni keyin yig'uvchi to'ldiradi. Ya'ni to'liq tiklanish =
shu zaxira + bir necha soatlik yig'ish.

## Nusxa buzilmaganini tekshirish

```bash
gzip -t ober-narx-20260822.sql.gz     # jim bo'lsa — butun
sha256sum ober-*.sql.gz
```

2026-08-22 nusxalari:

    narx     1e027ff69e64e82aed32e35365adba834ef0ccf5be4716aade80cc6c08a6af3c
    odamlar  97f52634429491ede8a8a52d5b8fefc171ab16c8b4c721b4314fb1b388533606

## Serverda

`app/zaxira_shaxsiy.py` — shu fayllarni yasaydi, 14 kunlik nusxani
saqlaydi. `ober-zaxira-tashqi.timer` uni **har kuni 06:45 UTC** da
yugurtiradi (2026-08-22 da o'rnatildi va yoqildi).

Tekshirish:

    systemctl list-timers ober-zaxira-tashqi.timer

## DIQQAT — o'sib borayotgan chegara

`narx_tarix` o'sib boradi. 2026-08-17 da 15.7 MB edi, 22-avgustda
**19.35 MB**. Fayl ko'chirish chegarasi bitta faylga **20 MB**.
Ya'ni keyingi safar bitta bo'lakda sig'maydi.

Yechim ikkita:
1. `zaxira_shaxsiy.py` ga bo'lakka bo'lish qo'shish (`split`), yoki
2. `narx_tarix` ni oxirgi N oy bilan cheklash va eskisini alohida,
   kamdan-kam ko'chiriladigan arxivga chiqarish.

Bugun ikki bo'lakka bo'lib ko'chirildi (`split -n 2`), keyin
birlashtirildi va SHA-256 bilan tekshirildi.
