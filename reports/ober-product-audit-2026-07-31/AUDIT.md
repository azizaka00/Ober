# OBER mahsulot auditi — 2026-07-31

## Xulosa

`CODEX-ISH-TOPSHIRIGI.md` texnik jihatdan tartibli, ammo hozirgi ketma-ketlik OBERni avvalo e’lon agregatoriga aylantiradi. Aziz belgilagan asosiy mahsulot esa universal teskari marketplace: xaridor ehtiyojini yozadi, tizim uni tushunadi, mos sotuvchi yoki xizmat ko‘rsatuvchiga yuboradi va jonli takliflarni taqqoslaydi.

Shuning uchun agregatsiya OBERning foydali ma’lumot qatlami bo‘lib qolishi kerak, lekin mahsulotning yuragi emas.

## Tekshirilgan oqim

### 1. Xaridor kirishi — umumiy holat yaxshi, pozitsiya tor

![Xaridor bosh sahifasi](./01-xaridor-bosh-sahifa.png)

- Mobil kompozitsiya, vizual ierarxiya va asosiy CTA aniq.
- Biroq bosh ekran OBERni “avtoehtiyot qismlar uchun teskari bozor” deb ta’riflaydi; bu universal mahsulot va xizmatlar g‘oyasiga zid.
- Misollar ham faqat avtomobil qismlariga bog‘langan.

### 2. Banner so‘rovi — kritik mahsulot xatosi

![Banner so‘rovi natijasi](./02-banner-sorovi-natijasi.png)

Sinov so‘rovi: “menga 25 kv banner kerak, 5 ga 5 metr, fayli tayyor, 300 000 so‘mga kim qilib beradi?”

- Tizim so‘rovni “Umumiy qidiruv” deb belgiladi.
- Mos banner xizmatini topish yoki aniqlashtirish o‘rniga avtomobil e’lonlaridan narx statistikasi va 30 ta natija qaytardi.
- Bu foydalanuvchida OBER so‘rovni tushundi degan noto‘g‘ri ishonch uyg‘otadi.

P0 qoida: kategoriya yoki xizmat ishonchli aniqlanmasa, hech qanday umumiy natija ko‘rsatilmasin. Tizim bitta qisqa aniqlashtiruvchi savol bersin yoki so‘rovni moderatsiya/navbatga yuborsin.

### 3. Sotuvchi kirishi — to‘g‘ri yo‘nalish, ozgina to‘ldirish kerak

![Sotuvchi ro‘yxatdan o‘tishi](./03-sotuvchi-royxatdan-otish.png)

- Kategoriya daraxti yo‘q; foydalanuvchi “Nima sotasiz?” degan erkin maydonda yozadi. Bu to‘g‘ri qaror.
- Hozirgi sahifa sodda va mobil qurilmada tushunarli.
- Yetishmayotgan muhim ma’lumotlar: ism yoki biznes nomi, telefon/Telegram, xizmat radiusi yoki yetkazib berish hududi.
- Tizim yashirin kategoriyani aniqlagach, sotuvchiga qisqa tasdiq ko‘rsatishi kerak: “Tushundik: banner chop etish · tashqi reklama · montaj”.

## Kuchli tomonlar

- Manba adapterlari uchun yagona interfeys.
- Bir xil e’lonlarni birlashtirish rejasi.
- Yo‘qolgan va eskirgan e’lonlarni boshqarish.
- Manbaga havola va ehtiyotkor yig‘ish bo‘yicha etik cheklovlar.
- Bosqichma-bosqich ishga tushirish va o‘lchovlar mavjud.

## Asosiy xavflar

1. **Mahsulot yo‘nalishi:** reja “eng katta qidiruv agregatori”ni quradi, “xaridor so‘rovi → mos sotuvchi → jonli taklif” halqasini esa kechiktiradi.
2. **Bildirishnoma juda kech:** sotuvchiga Telegram xabari 7-bosqichda emas, birinchi ishlaydigan pilotning ichida bo‘lishi kerak.
3. **Real vaqt va’dasi:** tashqi saytlarning ruxsati, API mavjudligi va bloklash siyosati sabab “barcha saytlar real vaqtida” kafolatlanmaydi. OBER real vaqt deb faqat tekshirilgan yangilanish vaqtini ko‘rsatishi kerak.
4. **Xizmat javobi yetarli emas:** faqat `BOR`/`YO‘Q` custom ishlab chiqarish va xizmatlarda kamlik qiladi; `BOR`dan keyin narx va tayyor bo‘lish muddati zarur.
5. **Muddat:** 12–17 kunlik baho deploy, bir nechta barqaror adapter, Telegram parser, deduplikatsiya va notificationni birga sifatli yakunlash uchun optimistik.
6. **Filtrlar:** rasmsiz yoki narxsiz e’lonni avtomatik yomon deb hisoblash xizmatlar uchun noto‘g‘ri; sifat qoidalari kategoriya bo‘yicha farqlanishi kerak.

## Tavsiya etilgan ketma-ketlik

1. Universal so‘rovni strukturalash: nima kerak, parametrlar, narx, joy, muddat.
2. Noma’lum kategoriya uchun xavfsiz aniqlashtirish; auto natijalarga tushib ketishni yopish.
3. Soddalashtirilgan sotuvchi/xizmat ko‘rsatuvchi onboarding va yashirin kategoriya tasdig‘i.
4. Mos sotuvchilarga Telegram bildirishnomasi; javob: mavjudlik, narx, muddat.
5. Banner/poligrafiya kabi bitta hududdagi zich pilotda jonli halqani isbotlash.
6. Shundan keyin OLX/Telegram/BirBir kabi agregat manbalarni narx-kontekst va qo‘shimcha supply qatlami sifatida kengaytirish.
7. Keyin deduplikatsiya va yangi vertikallar.

## To‘g‘ri muvaffaqiyat mezonlari

- birinchi javobgacha vaqt;
- kamida 3 ta mos taklif olgan so‘rovlar ulushi;
- sotuvchilarning javob berish foizi;
- kelishuvga aylangan so‘rovlar;
- takroriy xaridorlar.

## Accessibility chegarasi

Ko‘rilgan mobil sahifalarda gorizontal chiqish yo‘q va asosiy elementlar yirik. Skrinshotlar klaviatura navigatsiyasi, screen reader nomlari, fokus holati va aniq kontrast nisbatini tasdiqlamaydi; bular alohida texnik tekshiruv talab qiladi.
