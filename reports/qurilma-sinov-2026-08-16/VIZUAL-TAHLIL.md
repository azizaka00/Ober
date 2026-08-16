# Skrinshotlar vizual tahlili — 2026-08-16

## Usul

Har sahifa headless Chrome bilan ochilib, PNG'ga olindi. Tahlil PIL
bilan qilindi: bandlar bo'yicha rang xilma-xilligi, yorug'lik o'rtachasi,
asosiy ranglar.

**Muhim texnik saboq:** dastlabki tahlil noto'g'ri chiqdi — qo'lda
yozilgan PNG parseri FTS filter qatlamlarini hisobga olmadi va hamma
skrinshotni "qora + sof RGB" deb ko'rsatdi. PIL bilan qayta tahlil
to'g'ri: **sayt yorug' va toza**.

## Natija jadvali

| Fayl | Hajm | Yorug'lik | Asosiy rang | Bandlar | Xulosa |
|---|---|---|---|---|---|
| bosh (1280) | 1280x1400 | 227 | `#f0f4fa` (6%) | 10/10 to'la | ✅ hero, qidiruv, lenta to'liq |
| natija (1280) | 1280x1400 | 212 | `#fefeff` (8%) | 10/10 to'la | ✅ kartalar, chiplar to'liq |
| kategoriyalar (1280) | 1280x1400 | 243 | `#fafbfe` (27%) | 8/10 | ✅ 2 daraja to'liq, pastki bo'sh (sahifa tugashi) |
| chat (1280) | 1280x1400 | 243 | `#f0f4fa` (40%) | 7/10 | ✅ suhbatlar bor, pastki bo'sh |
| sotuvchi (1280) | 1280x1400 | 213 | `#f0f4fa` (33%) | 7/10 | ✅ hero to'liq, pastki bo'sh |
| elon-ober (1280) | 1280x1400 | 243 | `#f0f4fa` (56%) | 4/10 | ✅ kontent yuqorida, pastki bo'sh (e'lon qisqa) |
| bosh (390) | 390x1600 | 221 | `#fcfdff` (5%) | 10/10 to'la | ✅ mobil to'liq |
| natija (390) | 390x1600 | 219 | `#ffffff` (24%) | 10/10 to'la | ✅ kartalar to'liq |
| kategoriyalar (390) | 390x1600 | 241 | `#f1f5fa` (14%) | 10/10 | ✅ to'liq |
| chat (390) | 390x1600 | 241 | `#f1f5fa` (64%) | 3/10 + tabbar | ✅ suhbatlar bor, pastki bo'sh |
| sotuvchi (390) | 390x1600 | 197 | `#ffffff` (14%) | 10/10 | ✅ to'liq |
| elon (390) | 390x1600 | 243 | `#f1f5fa` (77%) | 2/10 + tabbar | ✅ to'g'ri e'lon |

## Kuzatishlar

1. **Sayt butunlay yorug' rejimda** — `--bg:#f1f5fa` hamma sahifada
   asosiy fon. Quyuq rejim emas (rejaga ko'ra yorug' qoladi).
2. **Barcha sahifalar mazmun bilan to'lgan** — bo'sh/yiqilgan sahifa yo'q.
   Rang xilma-xilligi (969–1060) matn + kartalar + rasm borligini
   ko'rsatadi.
3. **Pastki bo'sh joylar normal** — chat, sotuvchi, kategoriyalar
   sahifalarida kontent ekran balandligidan qisqa. Bu sahifalar
   scroll qilinadi, "bo'sh" emas.
4. **elon/1 = "E'lon topilmadi"** — to'g'ri: `/elon/{id}` faqat OBER'ning
   o'z e'lonlari (manba='ober') uchun. Tashqi e'lonlar (OLX/Asaxiy)
   asl manba havolasiga o'tadi. `elon-ober` (126214) esa to'liq
   kontent bilan ochiladi.

## Xulosa

Vizual jihatdan sayt **toza va yorug'** — dizayn qoidalariga mos,
bo'sh sahifa yoki buzilgan layout yo'q. Skrinshotlar shu papkada:
`skrinshotlar/` (13 fayl).
