# OBER P0 — Figma Phase 0 discovery

Sana: 2026-08-09
Figma: https://www.figma.com/design/RePGBOuthzfzPuSsdefCbq

## P0.a — Kod manbasi

- Font: Onest, 400–800 productionda variable; Figma’da Onest Regular, Medium,
  SemiBold, Bold, ExtraBold mavjud.
- Ranglar: navy `#0b2559`, navy-dark `#081b42`, navy-soft `#eaeff8`,
  background `#eff2f7`, surface `#ffffff`, text `#101828`, muted `#667085`,
  line `#e3e8f0`, line-strong `#cdd6e4`, green `#0f7a4a`, red `#c0392b`.
- Radius: 10 / 14 / 20 / pill; chat tail uchun 5.
- Motion: 120–220 ms; faqat opacity, transform va holat feedbacki.
- Layout: desktop content 1180 px; natija kartalari hozir 3 ustun, mobil 1 ustun.

## P0.b — Figma holati

- Yangi file, bitta bo‘sh `Page 1`.
- Local components: 0.
- Local variables: 0.
- Local styles: 0.
- Onest oilasi mavjud.

## P0.c — Kutubxona qidiruvi

Ulangan kutubxonalar: Material 3 va Simple Design System.

Simple Design System’da Button, Input Field, Search, Card, Navigation,
radius variables, body/heading styles va shadow styles bor. Lekin ularning
tipografiyasi, radiuslari, token semantikasi va component API’si OBERning
HTML/CSS manbasi bilan mos emas.

Qaror: remote componentni detach/wrap qilib murakkablashtirmasdan, kichik
lokal OBER kitini koddagi haqiqiy tokenlardan yaratish. Material 3 faqat
zarur bo‘lsa standart ikonlar manbasi bo‘lishi mumkin; OBERning mavjud SVG
ikonlari asosiy manba.

## P0.d — Qulflanadigan v1 scope

### Figma views

1. `Results / Desktop / P0` — 1440×900, desktop top nav, 4 ustunli zich grid,
   `e’lon` atamasi, mahsulot/xizmat intent ajratilishi.
2. `Results / Mobile / P0` — 390×844, birinchi karta ekranda, sort/filtr
   tushunarli, sticky CTA kartani yopmaydi.
3. `Chat / Error Recovery / P0` — ulanish xatosida qayta urinish, kirish va
   bosh sahifaga qaytish harakatlari.

### Lokal Figma komponentlar

- Button: primary / secondary / ghost, default / pressed / disabled.
- Search field: text + camera action + submit.
- Intent chip: default / selected.
- Listing card: desktop / mobile.
- Empty/error state panel.
- Navigation: desktop header va mobile tabbar view ichida.

### Foundations

- OBER colors, spacing, radii, typography va shadows.
- Onest text styles.
- CSS variable code syntaxlari.

## P0.e — Kod ↔ Figma mapping

| Kod | Figma | Qaror |
|---|---|---|
| `--navy`, `--bg`, `--surface`, semantic colors | mavjud emas | Local semantic variables |
| `--r-kichik/orta/katta/pill` | SDS radiuslari boshqa | OBER local radius variables |
| Onest | Figma’da bor | Aynan Onest ishlatiladi |
| `.tartib-btn`, `.filtr-narx` | SDS yaqin, API/visual boshqa | Local OBER components |
| `.card` | SDS Card marketplacega mos emas | Local Listing Card |
| `.ober-tabbar` desktop+mobile | desktopda takrorlanadi | Desktop header only, mobile tabbar only |
| `ta taklif` tashqi natijalar uchun | semantik konflikt | `ta e’lon`; `jonli taklif` alohida |
| Chat catch state faqat matn | keyingi harakat yo‘q | Retry + Login + Home actions |

## P0.f — Gap analysis

Kodda ishlab turgan OBER visual tizimi bor, lekin Figma’da uning hech qanday
token, komponent yoki view ko‘rinishi yo‘q. Remote kutubxonada generic web
komponentlar bor, ammo ular OBERning Onest, navy, radius va marketplace
zichligiga mos emas. Eng to‘g‘ri yo‘l — to‘liq katta design system emas,
P0 viewlar uchun zarur minimal lokal OBER foundations + 5 reusable komponent.

## Phase 0 chiqish qarori

Figma va frontend uchun bitta manba: production CSS. Figma koddan ajralib
ketadigan yangi brend yoki boshqa vizual til yaratmaydi. P0 tasdiqlansa,
Phase 1’da token/style foundations yaratiladi; keyin viewlar komponentlar
orqali yig‘iladi va shu maketlar bo‘yicha frontend patch qilinadi.
