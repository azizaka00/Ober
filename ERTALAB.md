# ERTALAB — 2026-08-03

Aziz, tunda qilingan ish. O'qishga 2 daqiqa.

---

## 1. Birinchi navbatda: ikkita fayl bosing

**`KALIT-QUYISH.bat`** — bir martalik. Parolni **oxirgi marta** kiritasiz.
Undan keyin serverga ulanish parolsiz bo'ladi.

**`YUKLASH.bat`** — tundagi hamma o'zgarish serverga ketadi va server
qayta ishga tushadi. Bir bosish, parol yo'q.

Nega bu kerak edi: men terminalga yozolmayman (tizim cheklovi) va parol
kiritmayman. Kalit qo'yilgach, keyingi safar yuklashni **o'zim** qila
olaman va sizni kutmayman.

---

## 2. Nima qilindi

### Uchala sahifa bitta dizaynga keltirildi

Tunda tekshirganimda ma'lum bo'ldiki, bizda bitta sayt emas, **uchta
boshqa mahsulot** bor edi:

| | Fon | Navy rangi | Shrift | Radiuslar |
|---|---|---|---|---|
| `index.html` | sovuq `#eff2f7` | `#0b2559` | Onest | 4 ta |
| `sotuvchi.html` | **iliq krem** `#f7f5ef` | `#0b2559` | tizim | 9 xil |
| `takliflar.html` | **ivory** `#fffdf8` | **`#08285f`** | **Inter** | **13 xil** |

Xaridor sahifasidan sotuvchi sahifasiga o'tgan odam uzilishni sezardi.
Bu kechagi "professional ko'rinish" ishimizni yarmidan buzardi.

Endi uchalasi bir xil: Onest shrifti, sovuq kulranglar oilasi, ko'kimtir
soyalar, to'rtta burchak qiymati, jadval raqamlari, bosilganda javob.

### Yo'l-yo'lakay olib tashlanganlar

**`sotuvchi.html`** — fon rasmi va **18 soniyalik cheksiz animatsiya**.
`fixed` fon telefonda skrollni sekinlashtiradi, cheksiz animatsiya
batareyani yeydi. Ikkalasi ham hech qanday ma'lumot bermaydi.

**`takliflar.html`** — ikkita issiq radial gradient. Sovuq palitra bilan
to'qnashardi va aynan "AI gradienti" taassurotini berardi.

---

## 3. Sizdan kutilayotgani

**Shrift.** `SHRIFT-TANLOV.html` faylini oching — beshta variant, bir xil
matn. Men **Onest** ni qo'ydim (kirillcha uchun maxsus, kam uchraydi),
lekin bu mening tanlovim. Boshqasi yoqsa bir qatorda almashtiriladi.

**Telegram kanallari.** `data/telegram-kanallar.txt` bo'sh turibdi.
Adapter tayyor, sinovdan o'tgan. Sizdan kanal nomlari kerak, ayniqsa
avto ehtiyot qism bo'yicha. Bu bozorning OLX bilan teng yarmini ochadi.

**Domen.** `ober.uz` DNS'ni `77.42.123.90` ga qaratsangiz, bitta buyruq
bilan HTTPS qo'shiladi. IP manzilni odamga ulashib bo'lmaydi.

---

## 4. Ochiq qolgan kamchiliklar (halol ro'yxat)

**Shrift Google CDN'dan yuklanmoqda.** Bu bizning "tashqi bog'liqlik
yo'q" qoidamizga mos emas. Faylni yuklab o'z serverimizga qo'yish kerak,
~5 daqiqalik ish. Men qila olmadim: sandbox ishlamayapti, ikkilik faylni
yuklab ololmayman.

**Vizual natijani ko'rmadim.** O'zgarishlar hali serverda emas va
brauzer mahalliy faylni ochmadi. Tuzilishni va qiymatlarni tekshirdim,
lekin "chiroylimi" degan savolga javob bera olmayman. Yuklagach birinchi
bo'lib shuni ko'ramiz.

**Sinov sotuvchisi** id **72** bazada turibdi (`SINOV kabinet`).
O'chirish uchun:

    ssh root@77.42.123.90 "sqlite3 /home/ober/ober/data/ober.db \"DELETE FROM sotuvchilar WHERE id=72\""

**Kategoriyalar, qorong'i rejim, katalog** — hali yo'q. Ustuvorligi past.

---

## 5. Server holati

Tunda o'z-o'zidan ishlab turdi: yangilik sikli har 45 daqiqada issiq
kategoriyalarni, sutkada bir marta hammasini yangilaydi va sotilganlarini
o'chiradi. Hech kim hech narsa bosmadi — kechagi asosiy maqsad shu edi.

Holatni ko'rish:

    ssh root@77.42.123.90 "systemctl is-active ober-server ober-yangilik"
