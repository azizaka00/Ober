# OBER — frontend auditi va redesign rejasi (dsrupt.ru taqqosuvi)

Sana: 2026-08-11
Maqsad: `ober.uz` frontendini vizual jihatdan kuchaytirish — dsrupt.ru ning
premium, minimal, tartibli data-platform uslubidan ilhomlanib, **nusxa
qilmasdan**. Barcha OBER funksiyalari saqlanadi: marketplace e'lonlari,
agregator qidiruvi, teskari marketplace (talab → taklif), chat, sotuvchi
profili, kategoriya va filterlar, qidiruv.

---

## 0. Metod (qanday o'rganildi)

Tekshiruv paytida brauzer skrinshot vositasi muhitda ishlamadi. Shuning
uchun:

- **dsrupt.ru** — HTML/CSS tokenlari va kontent tuzilmasidan tahlil
  qilindi (`/assets/w.db6166b524.css`, `fonts.css`, sahifa matni).
- **OBER** — `web/*.html`, `ober-ui.css`, `tabbar.js`, `i18n.js` kodidan
  va oldingi o'lchangan auditlardan (`reports/` 08-07, 08-08, 08-09).

Bu cheklov qayd etiladi: Faza boshlanganda real brauzerda (desktop 1280
va mobil 390) yangi skrinshotlar olinib, rejadagi da'volar tasdiqlanadi.
Dizayn qoidasiga ko'ra — "yaxshi ko'rinadi" dalil emas, o'lchov shart.

---

## 1. Qisqa hukm

OBER dizayn asosi — **navy + oq + sovuq kulrang, Onest shrifti, pill
chiplar, ko'kimtir soyalar** — to'g'ri va dsrupt.ru bilan bir oilada:
ikkalasi ham "ma'lumot birinchi" degan data-platform yo'nalishida.
To'liq rebrending kerak emas.

Asosiy bo'shliq uch joyda:

1. **Desktop zichlik past** — 3 ustun, katta kartalar, bir tekis kulrang
   fon → sahifa "bo'sh" ko'rinadi (audit 2026-08-09: *"Katta ekranda
   ma'lumot zichligi past"*).
2. **Vizual til yarim** — emoji ikonkalar (`📍🏷🕐`), `elon.html` da
   `--radius:16px` (tizimda yo'q!), navbatdagi "Profil" atamasi,
   `sotuvchi.html` da xom radius qiymatlari. Sayt "saranjom" ko'rinmaydi
   (CLAUDE.md ochiq muammo #1).
3. **Rang iyerarxiyasi yassi** — navy hamma narsada: sarlavha, tugma,
   havola, chip, badge. Urg'u hamma joyda bo'lsa — urg'u yo'q.

---

## 2. Hozirgi OBER — nima bor (asos, buzilmaydi)

| Qatlam | Qiymat | Izoh |
|---|---|---|
| Rang | `--navy:#0b2559`, `--bg:#eff2f7`, `--surface:#fff` | sovuq oila, bir tizim |
| Shrift | Onest (variable 400–800), o'z serverda | qoida, o'zgarmaydi |
| Burchak | 4 ta: 10/14/20/999px | qoida, yangisi qo'shilmaydi |
| Soyalar | ko'kimtir (`rgba(11,37,89,…)`) | qora soya yo'q |
| Motion | 120–220ms, transform/opacity | reduced-motion himoya bor |
| Mobil | pastki 4 tab, sticky saralash, suzuvchi "So'rash" | o'lchangan, yopishqoq 1 ta |

**Allaqachon kuchli tomonlar** (dsrupt bilan bir xil fikrlash):

- hero'da **jonli raqamlar** — 276 726+ ta e'lon, dollar kursi, haqiqiy
  qidiruv chiplari lentasi ("dalil blok");
- jadval raqamlari (`font-variant-numeric:tabular-nums`);
- 4 holat: yuklanmoqda / bor / yo'q / xato, skeletonlar;
- `[hidden]{display:none!important}` har sahifada (web_sinov qo'riqlaydi);
- har bosiladigan elementda `:active` javobi;
- `prefers-reduced-motion` himoyasi.

Bu — dsruptning "Не мнения — цифры" falsafasining OBER versiyasi.
Saqlanadi va kuchaytiriladi.

---

## 3. dsrupt.ru o'lchangan tokenlari (referens)

Manba: `dsrupt.css` (81 KB), `fonts.css`, bosh sahifa matni.

| Qatlam | Qiymat |
|---|---|
| Shrift | Montserrat (display, 100–900) + Manrope (body, 200–800) |
| Fon | `#FFFFFF`, bo'limlar `#F6F8FC` |
| Matn | `--ink:#171A22` → `--ink2:#5B6474` → `--mut:#98A0AF` → `--faint:#C4CAD5` |
| Chiziq | hairline `#EAEEF5`, `#F0F3F8` |
| Ko'k urg'u | `#2563EB` / `#3B82F6` / `#1D4ED8`, gradient `135deg` |
| Semantik | `--good:#16A34A`, `--bad:#EF4444`, `--warn:#E8850C` (soft fonlar bilan) |
| Radius | pill 999 (chiplar/tugmalar), 14/16/18/20/22 (kartalar), 8 (kichik) |
| Soyalar | `--sh1:0 10px 30px rgba(30,52,110,.08)`, `--sh2:0 18px 46px rgba(30,52,110,.13)`, `--sh-blue:0 14px 30px rgba(37,99,235,.30)` |
| Tracking | sarlavhalar `-0.02/-0.03em`, eyebrow `0.06–0.08em` |
| CTA | gradient ko'k + `--sh-blue` glow, qisqa fe'l |
| Breakpointlar | 400, 480, 560, 700, 860, 960, 980, 1080 |

**Kontent tuzilmasi (home):** hero'da qarama-qarshi raqamlar
("bitta zaявка 60 ₽ va 5 000 ₽"), stats qator (227/31/133/56/469),
raqamlangan qadamlar ("Шаг 1/2/3"), har qadamda "Открыть→" CTA,
mahsulot trio, tayyor ro'yxatlar, kirish (Telegram, 0 ₽), FAQ, footer.
Hech qanday bo'sh so'z — hamma da'vo raqam bilan.

---

## 4. OBER vizual kamchiliklari (dalil bilan)

### P0 — eng ko'zga tashlanadigan

1. **Desktop bo'shligi.** `index.html` natijalari desktopda 3 ustun,
   karta 124px rasm + katta matn. Audit 08-09: *"Desktop kartalari juda
   katta, narx va hudud birinchi ekranda yetarli zichlikda ko'rinmaydi."*
2. **Fon ritmi yo'q.** Butun sayt bitta `#eff2f7`. Bo'limlar orasida
   "nafas" farqi yo'q. dsrupt: oq tuval ↔ yumshoq kulrang bo'lim
   almashinuvi (`#FFFFFF` ↔ `#F6F8FC`).
3. **Emoji ikonkalar.** `elon.html` meta qatorida `📍🏷🕐`, chatda `📷`
   `📍` tugmalar. Emoji yagona SVG oilasiga almashtiriladi
   (dsruptda emoji yo'q).
4. **Hero fon rasm "design debt".** `ober-market-street.webp` CSS'da
   turibdi, ustida `.84–.94` shaffoflikdagi gradient + `saturate(.72)` —
   rasm deyarli ko'rinmaydi, lekin yuklanadi. Izohda "olib tashlandi"
   deyilgan, kodda turibdi. Qaror kerak: butunlay olib tashlash yoki
   to'g'ri ishlatish.
5. **Kategoriyalar — bitta daraja.** Har kartada 12+ pill ("brend,
   mahsulot turi va xizmat bitta pill ro'yxatida"). Ikki darajali
   tuzilma kerak: 10–12 yuqori kategoriya + ichida pastki daraja.

### P1 — tizim intizomi

6. **`elon.html` va `sotuvchi.html` tizimdan chetda.** `elon.html`:
   `--radius:16px` (tizimda yo'q), `--ease:cubic-bezier(.4,0,.2,1)`
   (boshqacha), xom `8px/10px/12px` radiuslar, tepada hali **"Profil"**
   tugmasi (eski atama). `sotuvchi.html`: xom `14px/10px/16px`
   radiuslar. `web_sinov.py` radius qoidasini hali tekshirmaydi.
7. **CTA urg'usi yagona emas.** Navy gradient "Topish" yonida navy
   `sora-btn`, navy `tel-ochish`, navy linklar — qaysi biri asosiy
   harakat ekani bitta qarashda bilinmaydi.
8. **"Hozir bozorda" va'dasi zaiflashgan.** Lenta sifati asosan kontent
   tomoni (eski sana, aralash til, takrorlar), lekin vizual tomoni ham:
   tor kartalar, bir xil takror shablon.
9. **Chat xato holati yo'l ko'rsatmaydi** (audit 08-09: "Ulanib
   bo'lmadi" — sabab, qayta urinish, kirish yo'li yo'q). Qisman
   tuzatilgan (409 holatlar), holatlar tilini yakunlash kerak.

---

## 5. dsrupt.ru dan olinadigan prinsiplar (moslashtirilgan)

| # | dsrupt prinsipi | OBERga moslashuvi |
|---|---|---|
| 1 | **Oq tuval + soft bo'limlar** — bo'limlar orasida ritm | Bo'limlar `#eff2f7` ↔ oq panellar almashsin; katta bloklar oq yuzada |
| 2 | **Matn qatlami: ink → muted → faint** | Sarlavha `--text`, yordamchi `--muted`, 3-daraja `--faint:#98a0af` (yangi token); navy faqat harakatda |
| 3 | **Bitta urg'uli CTA + glow** | "Topish"/"So'rash" yagona gradient CTA, hover'da ko'kimtir glow; qolganlari pill-outline |
| 4 | **Ma'lumot birinchi ekranda** — qarama-qarshi raqamlar + stats qator | Dalil blokini hero'ning o'zida stats qator qilish: e'lonlar, kategoriyalar, javob vaqti |
| 5 | **Raqamlangan qadamlar + yo'naltirilgan CTA** ("Открыть→") | `qadamlar` bo'limiga har qadamda aniq CTA ("So'rov yuborish", "Kabinet ochish") |
| 6 | **Hairline chegara + yumshoq ko'kimtir soya** | Kartalar "suzsin": 1px `--line` + mavjud `--shadow-card` (izchil qo'llash) |
| 7 | **Pill filter + tanlanmaganlar xiralashadi (dim)** | Filtr chiplariga "boshqalari xiralashadi" interaksiyasi, sonlar bilan |
| 8 | **Zich desktop** — 4 ustunli ma'lumot | Natija kartalari desktopda 4 ustun, tor kartalar, narx+hudud bitta qarashda |
| 9 | **Yagona SVG ikon oilasi, emoji yo'q** | `📍🏷🕐📷` emojilari → bitta 24px/1.7px stroke SVG to'plami |
| 10 | **Kichik tracking, tabular figures, nafas** | h1 `-0.04em` (bor), h2 `-0.02em`, narxlar tabular (bor) — barcha sahifalarga |

**Nima OLINMAYDI** (OBER qoidalariga zid):

- eyebrow/kicker sarlavhalar (taqiqlangan — `OBER-DIZAYN-QOIDALARI.md`);
- AI generatsiya qilingan fon rasmlari, testimonial/bento bloklar;
- scroll-animatsiyalar va og'ir parallax;
- dark mode majburiyligi (ustuvorligi past);
- landing uslubidagi bo'sh bo'limlar — OBER ish quroli, zichlik 8/10 qoladi.

---

## 5.1 Ichki sahifalar tahlili (2026-08-11 qo'shimcha)

Bosh sahifadan tashqari dsrupt.ru ning oltita ichki sahifasi o'rganildi
(havolalar, HTML tuzilma va o'sha sahifalarning o'z CSS chunklaridan):
`/istochniki` (227 kanal katalogi), `/istochniki/telegram-ads` (kanal
detali), `/karta-trafika` (filtrli xarita), `/instrumenty` (56 xizmat +
jadval), `/minus-slova` (tayyor ro'yxat), `/voronki` (22 sxema).

### Yangi prinsiplar (bosh sahifa auditiga qo'shimcha)

1. **Filtr guruhlari + sonli chiplar (katalog sahifasi).** Uchta filtr
guruhi (Byudjet / Natija / Kim uchun), har guruhda birinchi chip
"barchasi", qolganlari qiymatlar. Tanlangan chip: gradient + oq matn +
ko'k glow (`.fc.on{background:var(--grad);color:#fff;box-shadow:var(--sh-blue)}`),
bosilganda `scale(.985)`. **Reset tugmasi** filtr faol bo'lgandagina
ko'rinadi (`.freset`). OBERga: natija sahifasidagi saralash chiplarini
shu tizimga ko'tarish — tanlangan chip oddiy navy fon o'rniga
gradient+glow ("yagona urg'u" tili), narx filtri uchun reset tugmasi.

2. **Filtr variantida natija soni (`.fcount`).** `font-size:13px;
font-weight:750;color:var(--blue);font-variant-numeric:tabular-nums` —
har variant yonida qancha natija chiqishi turadi ("Moslik (1 240) ·
Arzon (1 240)"). Odam tanlashdan oldin kutganini biladi. OBERga:
saralash pill'lariga son qo'shish — `d.jami` allaqachon qaytadi.

3. **Bo'sh holat — misol + tozalash (`.fempty`).** `max-width:520px;
margin:56px auto;text-align:center` — markazda qisqaroq so'rov misoli
("«avito» o'rniga «авито доска объявлений» emas") va **"Сбросить всё"**
tugmasi. OBERga: bo'sh holatga konkret misol ("Qisqaroq yozing:
«avto ehtiyot qism» o'rniga «fara»") + "Filtrlarni tozalash" tugmasi.

4. **Raqamlangan guruhlangan ro'yxat (katalog).** Katta kartalar emas —
guruh sarlavhasi + son ("Соцсети и мессенджеры 29"), ichida raqamlangan
ixcham qatorlar (`08 VK Реклама [разбор]`). Qator balandligi ~30 px —
juda zich va skanerlanadigan. OBERga: kategoriya 2-daraja uchun (masalan
Transport — 65 bo'lim) kartalar emas, raqamlangan qatorlar to'g'ri.

5. **Detal sahifada metrika chiplari (`.tldr-facts`).** Soft fonli chiplar
(border, radius 14, padding 12/14), ichida katta ko'k raqam (21 px 800)
+ kichik label (12 px): "↑1011% ROI / €250 порог входа". OBERga:
`elon.html` ko'rsatkichlari yoki sotuvchi kabinetidagi "Sizning
yo'nalishingizda bu hafta 47 ta qidiruv" shu uslubda.

6. **Mos / mos emas ikki qator (`.tldr-fit`).** Yuqorisi yashil, pasti
qizil; label 11 px 800 uppercase, `letter-spacing:.06em`, grid `112px 1fr`.
OBERga: sotuvchi kabinetida "Sizga keladigan so'rovlar / Kelmaydiganlar"
(past ustuvorlik).

7. **Breadcrumb + orqaga strelka (`.crumb`).** "← На карту трафика /
Источники трафика / 227 каналов в базе" — orqaga tugmasi hover'da
`translateX(-2px)`. OBERga: kategoriya drill-in'ida "← Kategoriyalar /
Transport / 65 ta bo'lim".

### Kategoriya ikki darajali rejasiga ta'siri (yangilangan qaror)

- 2-daraja **raqamlangan ixcham qatorlar** bilan (kartalar emas) — prinsip 4;
- Orqaga tugmasi **breadcrumb** ko'rinishida — prinsip 7;
- Bo'sh holatga **qisqaroq so'rov misoli** + tozalash tugmasi — prinsip 3;
- Ixtiyoriy: filtr/saralash chiplariga **son** — prinsip 2.

### Olinmaydiganlari

- Suzuvchi filtr popover'lari (`.fcard`, position:absolute) — OBER filtrlari
  inline va sahifada turishi to'g'ri;
- Nav'dagi "NEW" yorliqlar — OBER yangi funksiyani boshqa kanalda e'lon qiladi;
- Muallif bloki ("Артём · автор") — OBER marketpleys, shaxsiy brend emas.

---

## 6. Qaysi sahifalar qayta ishlanadi

| Sahifa | Daraja | Nima qilinadi |
|---|---|---|
| `index.html` (3089 satr) | **P0** | Hero rasm qarori; dalil blok → stats qator; natija kartalari 4 ustun (desktop); emoji→SVG; bo'lim ritmi; CTA iyerarxiyasi |
| `kategoriyalar.html` | **P0** | Bir daraja → ikki daraja: 10–12 ikonli yuqori kategoriya, ichida pastki bo'limlar; pill "dim" interaksiyasi |
| `elon.html` | **P1** | Tizimga keltirish: `--radius:16px`→14px, `--ease` birlash, xom radiuslar→tokenlar, emoji→SVG, "Profil"→"Sotish", sidebar layout |
| `sotuvchi.html` (1926 satr) | **P1** | Xom radius→tokenlar; forma/holat kartalari tizimga; atama yaxlitligi |
| `takliflar.html` (chat) | **P1** | Holatlar (bo'sh/xato/ulanish) aniq yo'l bilan; komposer/ikonlar tizimga; spacing |
| `ober-ui.css` | **P0** | Yangi tokenlar: `--faint`, tipografiya shkalasi, icon oilasi, bo'lim ritmi klasslari |

---

## 7. Yangi dizayn tizimi (taklif)

**Saqlanadi:** Onest, navy urg'u, 4 radius (10/14/20/999), ko'kimtir
soyalar, pill tili, motion qoidalari, `[hidden]`, reduced-motion.

**Qo'shiladi:**

```
--faint:#98a0af            /* 3-darajali matn (ikon label, orqa ma'lumot) */
--surface-tuya:#f6f8fc     /* oq bo'limlar orasidagi kulrang (allaqachon bor) */
--cta-glow:0 12px 28px rgba(8,27,66,.30)  /* asosiy CTA hover soyasi */
--icon-stroke:1.7px        /* yagona ikon qalinligi */
--container-birlik:1200px  /* 1180/980 larni birlashtirish */
```

**Tipografiya shkalasi** (Onest): h1 `clamp(28px,4.5vw,44px)` weight 770,
tracking `-0.04em`; h2 `20px` 740, `-0.02em`; body `15px` 1.5; yordamchi
`12–13px`; raqamlar tabular-nums (saqlanadi).

**Bo'lim ritmi:** kulrang fon (app) ↔ oq panellar (katta bloklar) ↔
`#f6f8fc` (ikkilamchi). Kategoriya kartalari, dalil bloklari, qadamlar
oq yuzada; sahifa foni kulrang qoladi.

---

## 8. Komponentlar ro'yxati (har biri 4 holat bilan)

**Foundation:** tokenlar · ikon to'plami (12–16 belgi) · tipografiya shkalasi

**Navigatsiya:** topbar (desktop pill nav) · pastki tabbar (4 tab, nishon) ·
til tugmasi

**Qidiruv:** hero qidiruv paneli · rasmli qidiruv · joy select ·
jonli qidiruv chiplari lentasi

**Kartalar:** e'lon kartasi (4 ustun variant) · kategoriya kartasi
(2 daraja) · stats/dalil bloki · jonli taklif kartasi · so'rov kartasi ·
empty/xato kartalari

**Filterlar:** saralash pill'lari · narx oralig'i pill'i · kategoriya
chiplari (dim interaksiyasi) · filtr chiplari son bilan

**Tugmalar:** primary (gradient+glow) · secondary (pill outline) ·
ghost (link-tugma) · icon tugma (kamera, rasm, joy)

**Chat:** inbox ro'yxati · chat paneli · xabar pufagi · komposer
(matn+rasm+joy+yuborish) · holat satri

**Sotuvchi:** register karta · Telegram karta (ixtiyoriy) · e'lon
formasi · so'rovlar ro'yxati · "E'lonlarim" karta

**Holatlar:** skeleton · spinner · empty (keyingi qadam bilan) · xato
(sabab + qayta urinish) · toast

---

## 9. Desktop/mobile reja (fazali, o'lchov bilan)

### Faza 1 — P0 vizual asos (`ober-ui.css` + `index.html`)

1. Yangi tokenlar + `--faint` + CTA glow; emoji→SVG (birinchilardan
   `index`'da).
2. Natija kartalari desktop 4 ustun, toraytirilgan karta, narx/hudud
   birinchi qatorda.
3. Hero rasm qarori (olib tashlash yoki to'g'ri ishlatish); dalil blok
   stats qator shaklida.
4. **O'lchov:** desktop 1280da birinchi karta balandligi va 4 ustun
   sig'imi; 390×844 da oldingi ko'rinish buzilmasligi (e2e iframe usuli
   — `tmp/e2e_launcher.py`).

### Faza 2 — kategoriyalar + e'lon

1. Kategoriyalar: ikki daraja, ikonlar, sonlar; API yangi tuzilmaga
   mosligi tekshiriladi (`kategoriya_top`, `/api/kategoriyalar`).
2. `elon.html`: radius/ease/atamalar tizimga, SVG ikonlar.
3. Sinov: `web_sinov.py` + brauzer (desktop+mobile) + `i18n_sinov`.

### Faza 3 — sotuvchi + chat

1. `sotuvchi.html`: xom radiuslar, forma, holat kartalari.
2. `takliflar.html`: bo'sh/xato holatlari, komposer tizimga.
3. Sinov: `suhbat_sinov` (56), `halqa_sinov` (26), rus rejimi.

### Faza 4 — yakuniy tekshiruv va yuklash

1. Barcha `_sinov.py` yashil; konsolda xato yo'q; 390px va desktopda
   skrinshot.
2. `NAVBATCHI` orqali serverga yuklash.
3. `memory/lessons.md` ga bitta xulosa.

**Qoida:** har faza — "yaxshi ko'rinadi" emas, **o'lchov** bilan
tasdiqlanadi (`getBoundingClientRect`, 390px, 1280px).

---

## 10. Xulosa

OBER dizayn ildizi to'g'ri — dsrupt.ru dan kerakli narsa **zichlik,
bo'lim ritmi, rang iyerarxiyasi va ikon intizomi**. Rebrending emas,
tartibga keltirish + ikki sahifani (kategoriyalar, elon) tizimga
qaytarish. OBER funksiyalari va qoidalari (`OBER-DIZAYN-QOIDALARI.md`)
buzilmaydi — yangi uslub shu qoidalar ichida quriladi.
