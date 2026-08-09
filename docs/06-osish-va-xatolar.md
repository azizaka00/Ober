# OBER — O'SISH YO'LI VA BOSHQALARNING XATOLARI

Sana: 2026-08-02

Oldingi hujjat (`05`) raqobatchilar nima qilayotgani haqida edi.
Bu hujjat ikkita boshqa savolga javob beradi:
**nega bunday loyihalar o'ladi** va **birinchi sotuvchilar qayerdan olinadi**.

---

## 1. NEGA TESKARI BOZORLAR O'LADI

Muvaffaqiyat hikoyalaridan ko'ra o'lim sabablari foydaliroq.

### 1.1 Asosiy sabab bitta: likvidlik

> Ikki tomonlama bozorlar ishga tushgandan keyin **likvidlik** sababli
> o'ladi: xaridor qidiradi, mos sotuvchi topmaydi, ketadi va **qaytmaydi**.

Kod yomonligidan yoki brend zaifligidan emas. Xaridor va sotuvchi
bir-birini **ishonchli topa olmaganidan**.

**Bizga:** aynan shuning uchun indeks qurdik. Xaridor birinchi kuniyoq
12 297 e'lon va odatiy narxni ko'radi — bo'sh ekran emas. Bu likvidlik
muammosini **vaqtincha yopadi**, lekin hal qilmaydi. Haqiqiy yechim —
javob beradigan sotuvchilar.

### 1.2 To'rtta o'ldiruvchi xato

| Xato | Bizda holat |
|---|---|
| **Erta hududiy kengayish** | Xavf bor: 13 viloyatga birdan yoyildik. Bir shaharda ishlagan narsa boshqasida o'lik — u yerda sotuvchi yo'q. |
| **Noto'g'ri tomonni birinchi urug'lash** | To'g'ri qildik: indeks (ta'minot ko'rinishi) birinchi. |
| **Platformadan sizib chiqish** | Bizda ATAYLAB shunday: qo'ng'iroq va naqd. Qaror to'g'ri, lekin o'lchov kerak (`raqam_ochildi`). |
| **Komissiyani noto'g'ri belgilash** | Hozir bepul. Zaarly aynan shundan yiqilgan — komissiya modeli oyiga $15k bergan, o'sishga yetmagan. |

### 1.3 Likvidlik o'lim spirali

Sotuvchi kam → tanlov yomon → xaridor kam → sotuvchi yana kam.

**Bizga aniq xulosa:** hududni tarqatmaslik kerak. Boshida
**Toshkent + avtoqism**da zichlik yaratish, keyin kengayish.
Hozir biz 13 viloyat × 137 kategoriyaga yoyilyapmiz — bu **indeks**
uchun to'g'ri (kontekst kerak), lekin **sotuvchi jalb qilish** uchun
noto'g'ri. Sotuvchini faqat Toshkentdan yig'ish kerak.

---

## 2. BIRINCHI SOTUVCHILAR QAYERDAN — Thumbtack yo'li

Thumbtack minglab kategoriya va yuzlab shaharda, **hech qanday talab
isbotisiz** boshlagan. Nima qilgan:

1. **Kataloglarni yig'ib, ta'minotchilarni topgan va o'zi bog'langan.**
   Ommaviy ravishda, qo'lda emas.
2. **Butun stavkani SEO'ga qo'ygan** — millionlab sahifa:
   "Denverdagi santexniklar", "Austindagi to'y fotografi".
   Xaridorga mo'ljallangan sahifalar **talab isbotini** yaratgan —
   shu isbot ta'minotchilarni jalb qilgan.
3. **Sotuvchi-niyatli reklama** — "qanday ko'proq mijoz topish mumkin"
   kabi so'rovlar. Raqobatchilar bu so'rovlarga umuman e'tibor bermagan.

### Bizda bu boylik ALLAQACHON BOR

Yig'ilgan e'lonlarda: sotuvchi nomi, do'konmi (`biznes`), nechta e'loni
bor, qaysi hududda, nima sotadi, OLX havolasi.

Ya'ni **"kimni OBER'ga taklif qilish kerak" ro'yxati bazamizda turibdi**
va biz uni ishlatmayapmiz.

Shu uchun `app/sotuvchi_royxat.py` yozildi (`JALB-QILISH.bat`):
eng ko'p e'lonli va do'kon maqomidagi sotuvchilarni chiqaradi.

**Nima deyish kerak:** *"Sizning yo'nalishingizda OBER'da so'rovlar
bor. Telegramga ulaning — 30 soniya, bepul, so'rov o'zi keladi."*

Kuchli tomoni: bu sotuvchilar OLX'ga **pul to'layapti**. Bizda esa
hozircha bepul va xaridor o'zi keladi.

---

## 3. MAHALLIY MANZARA (2026)

| | Holat |
|---|---|
| **Uzum Market** | Eng kattasi, oyiga 15 mln tashrif |
| **Uzum Avto** | Yangi, alohida ilova. AI bilan **soxta va takroriy e'lonni bloklaydi** |
| **BirBir** | $10 mln investitsiya olgan |
| **OLX.uz** | TBC Bank JV ga sotildi (24-iyul 2026) |
| **Sello, Wildberries UZ** | Market, klassifayd emas |

### Bozor o'sishi — bizning yelkanimiz

- Elektron tijorat: 2023 da $543 mln → 2027 ga $1 mlrd
- 2023 da **450 000 yangi avtomobil** sotilgan
- Hukumat rejasi: 2030 ga **yiliga 1 mln**

Avtopark ikki barobar o'ssa, ehtiyot qism talabi ham shuncha o'sadi.
Bizning birinchi nishamiz to'g'ri tanlangan.

### Uzum Avto'dan olinadigan narsa

Ular AI bilan **takroriy va soxta e'lonni bloklaydi**. Bizda ham
takrorni birlashtirish rejada bor (`CODEX-ISH-TOPSHIRIGI` 4-bosqich) —
lekin biz uni **foyda** sifatida ko'rsatamiz: *"Telegram'da 50 000
arzonroq"*. Ular yashiradi, biz taqqoslaymiz.

---

## 4. SHU HUJJATDAN CHIQADIGAN QARORLAR

**Darhol:**
- [ ] `JALB-QILISH.bat` yuritilsin, ro'yxat olinsin
- [ ] Ro'yxatdan **Toshkentdagi** do'konlar tanlansin (hudud tarqatilmasin)
- [ ] Birinchi 20 tasiga qo'lda murojaat — bu qo'lda ish, avtomatlashtirilmaydi

**Yaqin:**
- [ ] SEO narx sahifalari (Thumbtack va Carwow ikkalasida ham asosiy dvigatel)
- [ ] Sotuvchi-niyatli qidiruvlar uchun sahifa: "avtoqism sotaman, mijoz
      qayerdan topaman"

**Prinsip sifatida yozib qo'yiladi:**
- Indeks 13 viloyatdan yig'iladi — kontekst uchun
- **Sotuvchi faqat Toshkentdan jalb qilinadi** — zichlik uchun
- Toshkentda halqa aylanmaguncha boshqa viloyatga sotuvchi jalb
  qilinmaydi
