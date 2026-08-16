# Saboqlar

## 2026-08-16 — Bosh sahifada `body` suriladi, oyna emas

Tepa panelga navbatli qidiruv qo'shmoqchi bo'ldim: hero qutisi
ekrandan chiqqach tepada ingichka qidiruv paydo bo'lsin.

Yo'lda ikkita narsa bilindi:

1. **`body{overflow:hidden auto}`** — sahifa `body` ichida
   suriladi. `window.scrollTo()` va `document.scrollingElement.
   scrollTop` ISHLAMAYDI, `document.body.scrollTop` kerak. Testim
   uch marta "surildi" deb yolg'on javob berdi.
2. Yopishqoq panel va qidiruvni joylash ishladi, lekin ko'rsatish
   qoidasi ishlamadi. `body` ga sinf qo'yilganda ham hisoblangan
   `visibility` `hidden` bo'lib qolaverdi — garchi `el.matches()`
   true qaytarsa va qoida hujjatda mavjud bo'lsa ham. Sabab
   topilmadi.

Qaytardim. Yarim ishlaydigan funksiya jonli saytda qolgandan
ko'ra, umuman bo'lmagani yaxshi — ayniqsa sabab noma'lum bo'lsa.
Keyingi urinishda `visibility` o'rniga `display` bilan sinash
kerak va avval MAHALLIY nusxada tekshirish, jonli saytda emas.


## 2026-08-16 — "Vizual tekshirdim" deganda ekranni ko'rish kerak

Aziz so'radi: "hammasini vizual test qildingmi?". Javob yo'q edi.
Men kod ichidagi qiymatlarni o'lchagandim, ekranni emas. Bir
soatdan keyin brauzer ishlagach uchta nuqson chiqdi — hech biri
statik tahlilda ko'rinmasdi:

1. **Qidiruv maydoni 250 px o'ngda.** Sarlavha, izoh, tugma va
   raqamlar 203 px da; qidiruv va chiplar 453 px da. `margin-inline:
   auto` + `max-width` — ikkalasi alohida to'g'ri, birga xato.
2. **Raqamlar bloki markazda** — 1180 px keng qutida 664 px dan
   boshlanardi.
3. **Saralash tugmalari BUTUNLAY o'qilmas edi.** Matn #e8eef8,
   fon deyarli oq, kontrast 1.1:1 (AA talabi 4.5:1).

Uchinchisi eng og'ir va u MENING xatom. Natija sahifasidan to'q
ko'k fonni bugun ertalab o'zim olib tashladim, o'sha fonga
tayangan qoidani esa qoldirdim. CLAUDE.md da yozilgan qoidani
buzdim: "Umumiy tamoyilni tuzatganda, u yana qayerda buzilganini
qidir."

Muhimi: bu xatoni EKRANDA HAM ko'rmadim. Skrinshotda tugmalar
"och kulrang" bo'lib tuyulardi — men uni dizayn deb o'yladim.
Faqat `getComputedStyle` bilan kontrastni HISOBLAGANDA chiqdi.

Demak uch bosqich kerak, ikkitasi yetmaydi:
kodni o'qish -> ekranni ko'rish -> hisoblab o'lchash.

Uchalasi ham `web_sinov.py` ga qo'shildi (86 -> 103 tekshiruv).


## 2026-08-16 — Qoida tekshirilmasa, qoida emas

`OBER-DIZAYN-QOIDALARI.md` da "radius faqat tokendan" deb yozilgan
edi. Bugun uchta xom qiymat topildi: `10px`, `4px`, `6px`. Uchalasi
ham tizim qiymatiga YAQIN, lekin teng emas.

Sabab oddiy: qoidani hech kim tekshirmasdi. Yozilgan qoida —
niyat; tekshiriladigan qoida — poydevor. Ikkalasi bir narsa emas.

Endi `web_sinov.py` uni o'zi qo'riqlaydi (86 -> 100 tekshiruv).
Qoida yozganda darhol so'ra: buni nima tekshiradi? Javob "odam
esida tutadi" bo'lsa, u qoida emas — umid.

Yon topilma: `privacy.html` `ober-ui.css` ni umuman ulamaydi va o'z
tokenlarini takrorlaydi — qiymatlari ham farq qiladi (orta 16 vs 14,
katta 20 vs 22). Bir fayl tizimdan chiqib ketsa, uni faqat o'lchov
ko'rsatadi.


## 2026-08-15: Serverni tekshirdim, ekranni tekshirmadim

Aziz "hech narsa chiqmadi" dedi. Men serverdagi HTML'ni tekshirdim —
o'zgarish bor edi. "Deploy o'tdi, kesh muammosi" deb uch marta qayta
yubordim. Uchinchi urinishda RENDER qilib ko'rdim va sabab darhol
chiqdi: `sw.js` dagi kesh nomi `ober-v1` deb qotib qolgan edi va
hech qachon o'zgarmasdi.

`activate` hodisasi nomi CACHE ga teng bo'lmagan keshlarni o'chiradi.
Nom o'zgarmagani uchun o'chiriladigan narsa ham yo'q edi. Ustiga
statik fayllar `stale-while-revalidate` bilan berilardi — ya'ni
foydalanuvchi deploydan keyin ESKI kodni ko'rardi.

Bu faqat mening ishimga emas, HAR BIR foydalanuvchiga tegishli edi.

Saboq: "server to'g'ri javob beryapti" bilan "foydalanuvchi to'g'ri
ko'ryapti" — ikki xil narsa. Frontend o'zgarishidan keyin manba
kodni emas, EKRANNI tekshirish kerak.

## 2026-08-15: O'z test asbobim uch marta yolg'on gapirdi

`srcdoc` stendim: (1) eski hujjatni ushlab qoldi, chunki ramkani
qayta ishlatgandim; (2) `f.onload` srcdoc yuklanishidan OLDIN, bo'sh
`about:blank` uchun ishladi; (3) `location.search` bo'sh bo'lgani
uchun qidiruv umuman yugurmadi.

Har uchalasida ham o'lchov "kod ishlamayapti" deb ko'rsatdi, aslida
STEND ishlamayotgan edi. Bir marta esa `/api/javob/raqam` ni
"himoyasiz" deb belgiladim — tekshirsam, himoya 28 qator pastda edi,
mening vositam blokni erta kesgan.

Saboq: vosita ham tekshirilishi kerak. Kutilmagan natija chiqsa,
avval VOSITANI shubha ostiga ol, keyin kodni.

## 2026-08-15: Qoida haqida yozish qoidani buzadi

`web_sinov` "JS ichida HTML izohi bo'lmasin" qoidasini oddiy matn
qidiruvi bilan tekshiradi. Men uni izohda TUSHUNTIRISH uchun o'sha
belgini yozdim — sinov yiqildi. Keyin `goto` bilan ham, `<!--` bilan
ham takrorladim. Bir kunda to'rt marta.

Va to'rtinchisi HAQIQIY xato edi: sotuvchi sahifasining ro'yxat
kartasi JS shablon satridan chiziladi, men u yerga HTML izohi
qo'ydim. Bu 12-avgustda kabinetni bo'sh ochirgan xatoning aynan
o'zi. Sinov bo'lmaganda buzuq sahifani chiqarib yuborardim.

Saboq: sodda qo'riqchi yolg'on tinchlik bermaydi. Taqiqlangan
naqshni izohda ham yozmang — so'z bilan tushuntiring.

## 2026-08-12: O'ramning o'zi yo'q edi — u qo'shni ettitasini ham cho'zdi

Jonli lenta qatori 1394px balandlikda edi, har karta 144x1384 — jonli
saytda, ulkan bo'sh oq ustunlar. Men buni ko'rmagandim, chunki lenta
telefon ekranining pastida edi va men faqat DOM tuzilmasini
tekshirgandim ("2 qator bor, 14 tadan karta bor — demak ishlaydi").

Sabab: nusxani `<span aria-hidden>` ichiga o'ragandim. O'ram
`.jonli-yol` ning yagona flex bolasi bo'lib qoldi; ichidagi `<a>` lar
endi flex element emas, `flex:0 0 170px` o'lik, vertikal taxlandi.
O'ram 1384px ga cho'zildi va `align-items:stretch` qolgan yettita
SOG'LOM kartani ham o'sha balandlikka tortdi.

Ikki saboq:

1. **"Element bor" ≠ "element to'g'ri".** Sanoq (2 qator, 14 karta)
   to'g'ri edi, o'lcham esa falokat. Endi lenta uchun balandlik ham
   o'lchanadi, faqat sanoq emas.
2. **Bitta noto'g'ri bola butun qatorni buzadi.** Flex `stretch`
   sukut bo'yicha ishlaydi — bir bola cho'zilsa, hammasi cho'ziladi.

Birinchi tuzatishim `align-items:flex-start` edi — noto'g'ri yo'l.
U simptomni yashirar, lekin karta tublarini 21px notekis qilardi
(1 qatorli sarlavha 198px, 2 qatorli 219px). Sabab yo'qolgach
`stretch` xavfsiz va TO'G'RI. Simptomni davolashdan oldin sababni top.

## 2026-08-12: Hover uchun tuzatish yozildi, oddiy holat unutildi

To'q natija sahifasida saralash chiplari oqish dog' bo'lib turardi.
`index.html` da `body.is-results .tartib-btn:hover` bor edi — lekin
ASOSIY qoida yo'q. Telefonda hover bo'lmaydi, demak chiplar hech
qachon to'q holatga o'tmasdi.

Bu 2026-08-04 dagi `.results` padding saboqining aynan o'zi: tuzatish
yozilgan, ammo hech qachon ishlamagan. Yangi qoida: `:hover` yozganda
o'zingdan so'ra — **hover bo'lmaganda nima ko'rinadi?**

## 2026-08-12: Sodda qo'riqchi haqida gapirish ham uni buzadi

`web_sinov` "JS ichida HTML izohi bo'lmasin" qoidasini ODDIY matn
qidiruvi bilan tekshiradi (ilgari aqlliroq variant xatoni ko'rmagan
edi, shuning uchun soddalashtirilgan). Men izohda o'sha belgini
tushuntirish uchun yozdim — sinov darhol yiqildi.

To'g'ri javob: qo'riqchini "aqlli" qilish emas, taqiqlangan naqshni
izohda ham yozmaslik. So'z bilan tushuntir. Sodda qo'riqchi yolg'on
tinchlik bermaydi — bugun u meni ikki marta ushladi.

## 2026-08-10: Bitta belgi butun sahifani o'ldirdi

Aziz: *"yangi e'longa kirsam ham profilga kirsam ham hech narsa
chiqmayapdi"*

Sotuvchi kabineti butunlay bo'sh ochilardi. Sabab men yozgan izohda
edi — shablon satri (template literal) ichiga HTML izohi qo'yganman va
izohda teskari apostrof bor edi:

    $("#asosiy").innerHTML = `...
      <!-- bu yerda `<input placeholder="...">` turardi -->
      ...`;

Birinchi teskari apostrof shablonni YOPADI. Keyingi matn JS deb
o'qiladi: `Uncaught SyntaxError: Unexpected identifier 'placeholder'`.
SyntaxError butun `<script>` blokini ishga tushirmaydi.

Topish qiyin bo'ldi, chunki hamma narsa sog'lom ko'rinardi: server 200
qaytaradi, fayllar joyida, API ishlaydi, sessiya tirik. Men uch marta
noto'g'ri joyni qazdim (kesilgan fayl, service worker kesh, `i18n.js`
yuklanmagan) — hammasi asossiz taxmin edi.

Javobni Caddy jurnali berdi: brauzer `/sotuvchi` ni yuklab, keyin
BIRORTA `/api/sotuvchi/*` so'rovi qilmagan. Demak skript boshlanish
kodiga yetib bormay o'lgan. Aniq xatoni esa sahifaga vaqtinchalik
`window.onerror` qo'yib, xatoni jurnalga yozdirib oldim.

- SABOQ: "sahifa bo'sh" da birinchi savol — **skript umuman ishga
  tushdimi?** Buni tarmoq jurnali ayta oladi: sahifa yuklanib, undan
  keyin hech qanday API so'rovi bo'lmasa, javob shu.
- SABOQ: brauzerni ko'ra olmasam — **brauzerni gapirishga majburlayman.**
  Uch marta taxmin qilgandan ko'ra bir marta `window.onerror` qo'yish
  arzonroq edi.
- SABOQ: JS ichida HTML izohining o'rni yo'q. `web_sinov.py` endi
  buni tekshiradi.

## 2026-08-10: O'z tekshirgichimga ishondim, u esa xatoni ko'rmagan edi

Yuqoridagi xatoni ushlash uchun sinov yozdim: "shablon satri ichida
HTML izohi bo'lmasin". Buning uchun kichik JS yuruvchi yozdim.

Sinovni ataylab buzib tekshirdim — **u xatoni KO'RMADI.** Yuruvchim
ichma-ich shablonlarni noto'g'ri hisoblardi.

Yuruvchini butunlay tashladim va qoidani soddalashtirdim: *JS ichida
`<!--` umuman bo'lmasin.* Parser kerak emas, yolg'on o'tkazmaydi.

- SABOQ: himoyani yozgach **uni buzib ko'r.** Ishlamaydigan sinov
  sinovsizlikdan yomonroq — u xotirjamlik beradi.
- SABOQ: qoidani kengaytirib soddalashtirsa bo'lsa — soddalashtir.
  "Shablon ichida bo'lmasin" uchun parser kerak, "umuman bo'lmasin"
  uchun `in` kifoya.

## 2026-08-10: `kiyim` so'zi `kim` ga aylanib, savol so'zini yutib yubordi

Jonli so'rovlarni ko'rib chiqqanda:

    "Nexia 2 fara 300000 so'mga kimda bor"  -> kiyim
    "Samsung s24 ultralar kimda nech pul?"  -> kiyim

`normalla("kiyim")` -> `"kim"`. Qolip so'z BOSHI bo'yicha qidiradi
(`\bkim\w*`), ya'ni "kimda", "kimga", "kimdir" — hammasi tegadi.
"Kimda bor?" esa o'zbekchada eng tabiiy so'rash usuli: fara so'ragan
odam tikuvchiga borardi.

Tuzatish qo'lda emas: **normallashgach to'xtash so'ziga aylanadigan
ibora — ibora emas.** To'xtash ro'yxati savol so'zlarini allaqachon
biladi, shuning uchun qoida o'zi ishlaydi va kelajakdagi to'qnashuvni
ham o'zi tashlaydi.

- SABOQ: normalizatsiya qidiruvni yaxshilaydi, lekin **so'zlarni
  bir-biriga yaqinlashtiradi.** Qisqa iborani prefiks bo'yicha
  qidirish shu yaqinlikni xatoga aylantiradi.
- SABOQ: jonli ma'lumotni o'qish sinovdan ko'ra ko'proq xato topadi.
  Bu xato oylab turgan, birorta test uni ko'rmagan — chunki testlarni
  men yozganman va men "kimda bor" deb yozmaganman.

## 2026-08-10: "Bo'sh ko'rinish" — ma'lumot yo'qligi emas, notog'ri joyda turgani

Aziz: *"Nega profil, yangi e'lonlarga kirib bo'lmayapdi, bo'sh?"*

Men avval frontendga qaradim — 401 ni to'g'ri ushlaydimi, `MEN`
o'rnatiladimi. Hammasi joyida edi. Xato bazada edi:

`sotuvchi_yoz()` har safar YANGI qator qo'shardi, telefon raqami bor-
yo'qligini tekshirmasdi. Azizning bitta raqamida 8 ta hisob to'plangan.
Kirish esa `WHERE aloqa=?` bilan tartibsiz — SQLite eng eskisini
qaytarardi. E'loni bir hisobda, so'rovlari boshqasida edi.

Kirish telefon + Telegram kodi orqali ketadi, ya'ni **raqam allaqachon
shaxsni bildiradi**. Ikkinchi marta "ro'yxatdan o'tish" — aslida
ma'lumotni yangilash.

- SABOQ: "bo'sh ekran" shikoyatida avval ma'lumot BORMI deb so'ra,
  keyin ko'rsatilyaptimi deb. Men teskari tartibda qidirdim va
  frontendda vaqt yo'qotdim.
- SABOQ: kirish kaliti (bu yerda telefon) bazada UNIQUE bo'lishi
  kerak. Bo'lmasa tizim jimgina ikkiga bo'linadi va buni hech kim
  sezmaydi — xato faqat oylar keyin "bo'sh" bo'lib chiqadi.

## 2026-08-10: Ma'lumotga tegishdan oldin uchta narsa meni saqladi

Azizning 8 ta hisobini birlashtirishda ketma-ket uch marta yiqildim:

1. **Zaxira olinmadi** — `mkdir` root nomidan, `sqlite3` esa `ober`
   nomidan ishladi. Yozolmadi. Agar tekshirmasdan davom etganimda
   nusxasiz ishlagan bo'lardim.
2. **UNIQUE cheklovni topolmadim** — `sqlite_master` dan INDEX larni
   so'radim, cheklov esa CREATE TABLE ichida edi. Tranzaksiya
   qaytdi, ma'lumot buzilmadi.
3. **To'qnashuvni noto'g'ri joyda qidirdim** — #104 bilan emas, eski
   hisoblarning O'ZARO orasida edi.

Bundan tashqari `suhbatlar` va `javoblar` dan "takror"ni o'chirmoqchi
bo'lgandim — u yerda UNIQUE umuman yo'q ekan, ya'ni haqiqiy
yozishmani o'chirardim. 0 ta topilgani tasodif edi.

- SABOQ: ma'lumotga yozishdan oldin — ishlaydigan zaxira, tranzaksiya
  va **jadval ta'rifini o'qish** (indekslar ro'yxatini emas).
- SABOQ: "takrorni tozalash" deb yozishdan oldin so'ra: bu ustunda
  haqiqatan cheklov bormi? Bo'lmasa men o'chirayotganim takror emas,
  ma'lumot.

## 2026-08-10: "Kam natija" bilan "ma'nosiz" bir narsa emas

`bozor_izi` ma'nosiz matnga ham kategoriya berardi. Men "kamida 10 ta
natija bo'lsin" degan chegara qo'ydim. Ma'nosiz matn to'xtadi — lekin
haqiqiy noyob so'rov ham to'xtadi. O'lchov ikkalasi BIR XIL SONDA
ekanini ko'rsatdi:

    uzuk kerak oltin   1 ta natija · eng katta ulush 100%   <- haqiqiy
    gilam kerak 3x4    8 ta natija · eng katta ulush 100%   <- haqiqiy
    abcdefg qwerty     8 ta natija · eng katta ulush  38%   <- ma'nosiz
    asdf jkl           2 ta natija · eng katta ulush  50%   <- ma'nosiz

Son ajratmaydi, **jamlanish** ajratadi. Haqiqiy so'rovda hamma natija
bitta kategoriyada, ma'nosiz matnda tarqoq. Chegara son emas, ulush
bo'lishi kerak edi — va namuna kichraygan sari talab oshishi kerak.

- SABOQ: chegara qo'yishdan oldin **ikkala tomonni ham o'lcha.**
  Men faqat to'xtatmoqchi bo'lgan narsani o'lchadim, o'tkazmoqchi
  bo'lganini emas. Shuning uchun chegara noto'g'ri o'qda edi.

## 2026-08-10: Tuzatishni `|` dan oldin qo'ydim, keyin esa unutdim

2026-08-09 da mebelchiga avto oynasi so'rovi borishini tuzatgandim —
`tozalangan()` funksiyasi model va qism birga tanilganda begona
kategoriyalarni olib tashlaydi. Ertasiga xato QAYTDI.

Sabab: server shunday yozgan edi —

    tozalangan(matn, modellar, qismlar) | baza.bozor_izi(matn)

Tozalash `|` dan OLDIN. Ya'ni `bozor_izi` natijasi tozalanmay o'tib
ketardi. Ikkita chaqiruv joyi bor edi va ikkalasida ham shunday.

Yechim: `yonalishlar.belgilar()` — bitta funksiya, ichida ham
qo'shadi, ham tozalaydi. Chaqiruvchi tartibni buza olmaydi.

- SABOQ: qoidani funksiyaga emas, **natijaga** qo'llash kerak. Agar
  chaqiruvchi qoidadan keyin yana narsa qo'sha olsa — qo'shadi.
  To'g'ri tuzatish tartibni chaqiruvchi qo'lidan oladi.

## 2026-08-10: Uchta lug'at qurdim, kerakligi bittasi edi

Aziz: *"o'zi OLX dagi hamma kategoriyalardagi so'zlarni shunchaki olib
mukammal qidiruvga solsakchi, nega lug'at yasayapmiz? Juda
qiyinlashtirayapsan ishni."*

U haq edi va men buni o'zim ko'rmadim.

Uchta tizim bir-birining ustiga mingan edi: avto lug'ati (qo'lda),
20 ta yo'nalish (qo'lda), so'z→kategoriya jadvali (hisoblangan, MEN
qo'shganman). O'sha kuni topilgan xatolarning aksari shu
chalkashlikdan chiqdi.

Eng yomoni uchinchisi: u so'zni YOLG'IZ ko'rardi. `oyna` mebel
e'lonlarida ko'p uchraydi → "Uy va bog'". Natijada *"lacettiga labavoy
oyna kerak"* so'rovi MEBELCHIGA borardi. Jonli testda ko'rdim:
mebelchi bo'lib ro'yxatdan o'tdim, birinchi ko'rgan so'rovim avto
oynasi bo'ldi.

Yechim lug'at yozish emas edi. **Bizda 300 000 e'lon bor va har
birining kategoriyasi ma'lum — bu tayyor lug'at.** `baza.bozor_izi()`
matnni o'z qidiruvimizdan o'tkazadi va natijalar qaysi kategoriyada
ekanini sanaydi. So'zlarni BIRGALIKDA ko'radi: "lacetti + oyna" →
Transport, chunki bozorda shunday. Moslik sinovi 8/8.

- SABOQ: yangi lug'at yozishdan oldin so'ra — **bu ma'lumot menda
  allaqachon bormi?** Odatda bor. Qo'lda yozilgani eskiradi,
  ma'lumotdan hisoblangani o'zi o'sadi.
- SABOQ 2: foydalanuvchi "juda chalkash" desa, odatda haq. Kodni
  yozgan odam murakkablikka ko'nikib qoladi.

## 2026-08-10: Yorliq qo'yishda kategoriyani ishlatmaganmiz

`bamper` qidiruvida oshxona bufeti, kolonka va router chiqardi.
O'lchov: qism yorlig'i bor 30 826 e'lon avto kategoriyasida EMAS edi
(avtoda 15 283) — har uchtadan ikkitasi noto'g'ri.

`eshik`, `sidenie`, `deska`, `kondensioner` — bu so'zlar ikkala
sohada ham bor. Lug'at avto uchun yozilgan va indeks 100% avtoqism
bo'lganda to'g'ri ishlardi. Indeks 11 kategoriyaga kengaygach,
o'sha so'zlar mebel va elektronikaga yopishib qoldi.

Kategoriya bazada ALLAQACHON bor edi — ishlatmaganmiz.
69 527 yorliq tozalandi, relevans testi 8/13 dan 13/13 ga chiqdi.

- SABOQ: bir vertikal uchun yozilgan mantiqni kengaytirganda uni
  CHEGARALASH kerak. "Hamma joyda ishlaydi" deb o'ylash xato.

## 2026-08-10: Bitta `if` butun halqani uzgan

Sotuvchi javob berganda chat xabari FAQAT u izoh yozgan bo'lsa
yaratilardi (`if izoh or rasm:`). Sotuvchi eng ko'p qiladigan ish esa
"BOR" bosib faqat narx yuborish. Bunda `xabarlar` bo'sh qolardi,
bildirishnoma esa faqat shu jadvalga qaraydi — **xaridor javob
kelganini bilmasdi**. Chatni ochsa ham bo'sh chat: narx u yerda yo'q.

Ya'ni so'rov → javob → kelishuv halqasi o'rtasidan uzilgan edi.
`suhbat_sinov.py` buni ko'rsatib turardi, lekin test qizil holda
qolib ketgan.

- SABOQ: qizil test — ishlamayotgan mahsulot. "Keyin tuzatamiz" deb
  qoldirilsa, xato ko'rinmas bo'lib qoladi.
- SABOQ 2: "ixtiyoriy" maydonga bog'langan shart xavfli — eng ko'p
  uchraydigan yo'l hech narsa yozmaslik.

## 2026-08-10: Manbalarni tekshirdik — hammasi yopiq

uzum, birbir, olcha, mediapark, asaxiy, texnomart, zoodmall —
yettalasi ham avtomatik kirishni to'sadi (Cloudflare 403 yoki
CAPTCHA). Uzum `robots.txt` da ruxsat beradi, lekin amalda CAPTCHA
sahifasiga yo'naltiradi — yozilgan qoida bilan amaldagi to'siq zid,
amaldagisi hal qiladi.

- SABOQ: yangi manba qo'shish kod ishi emas, **hamkorlik ishi**.
  Do'kon tarmoqlariga xaridor oqimi kerak — taklif ularga foydali.
- CAPTCHA yechilmaydi, Cloudflare aylanilmaydi. Bu texnik masala
  emas: sayt egasi "bot kirmasin" deb aytgan.

- 2026-08-08: Tanlov arizasida mahsulotning mavjud ishlaydigan qismi bilan
  kelajak AI-rejasini aralashtirmaslik kerak. OBERning kuchli dalili — real
  prototip, qidiruv, routing, ichki chat va bozor indeksi; AI-router rivoji esa
  halol ravishda keyingi bosqich/KPI sifatida ko‘rsatiladi.
- 2026-08-08: “Barcha e’lonlarni yig‘amiz” gapining o‘zi mahsulotni scraper yoki
  katalogdek ko‘rsatadi. Kuchli pitchda agregatsiya supply qatlami, yagona qidiruv
  va deduplikatsiya qulaylik, teskari talab-routing-chat esa himoyalanadigan
  mahsulot ustunligi sifatida ajratiladi.
- 2026-08-08: Ariza raqamini DBdan qayta o‘lchash kerak; eski handoffdagi 11 ming
  bugungi 126 ming bazaga mos emas. Shu bilan birga dev/QA qidiruvlari va demo
  sotuvchilarni haqiqiy traction deb ko‘rsatish mumkin emas — texnik validatsiya
  va bozor validatsiyasi alohida yoziladi.
- 2026-08-08: Tanlov arizasida lokal baza production haqiqatining o‘rnini
  bosmaydi. `ober.uz` jonli sahifasi 249 ming va OLX+Telegramni tasdiqlagach,
  draft yangilandi; aniq production signal mavjud bo‘lsa eng so‘nggi kuzatilgan
  holat ishlatiladi.
- 2026-08-08: Founder bio kuchli bo‘lishi uchun umumiy sifatlar emas, tekshirilgan
  ketma-ketlik ishlaydi: ta’lim + real tadbirkorlik + texnik/product stack +
  oldingi production natija + hozirgi loyihadagi mas’uliyat. Ikkinchi a’zo haqida
  fakt yo‘q bo‘lsa, soxta CV emas, loyihadagi aniq rol va o‘lchanadigan vazifa
  yoziladi.
- 2026-08-08: Qarindosh jamoa a’zosini arizada qarindoshlik bilan emas,
  mahsulotga qo‘shadigan tekshirilgan kompetensiya va javobgarlik bilan asoslash
  kerak; Lazizbek uchun tadbirkorlik tajribasi Operations & Growth KPIlariga
  bevosita bog‘landi.

## 2026-08-07: CSS min-height o'zaro kurashadi — computed qiymatni o'lchash shart
Chat komposerni ixchamlashtirganda narx input 50px, rasm tugmasi 46px chiqdi —
`height:46px` yozsam ham. Sabab: faylda boshqa joyda umumiy `input{min-height:50px}`
qoidasi bor edi. `min-height` `height` dan kuchli — input 46 bo'lolmasdi.

- SABOQ 1: balandlik farqi ko'rinib turganida (46 vs 50) avval computed CSS'ni
  o'lchash kerak: `getComputedStyle(el).minHeight` va `.height` farqini ko'rish.
  Men yechimga sakrab bordim (align-self:stretch) — ishlamadi. O'lchaganimda
  sabab darhol ko'rindi: min-height:50px boshqa qoidadan.
- SABOQ 2: CSS'da bir xil xossa bir necha qoidada bo'lsa, eng aniq selektor
  yutadi — lekin min-height/height turli xossalar, ikkalasi qo'llanadi va
  min-height ustun turadi. Ikkalasini ham birga yozish kerak
  (`height:46px;min-height:46px`).

## 2026-08-07: "Takliflar" → "Chat" — backend allaqachon bor edi, faqat nom/forma eski edi
Aziz: "takliflarni chat qilib o'zgartirsakchi". Suhbat tizimi (suhbatlar, xabarlar,
rasm, onlayn holat) backendda BOR edi — interfeys hali "taklif" tushunchasida
yashar edi: tab "Takliflar", sotuvchi BOR/YO'Q tugmalari bilan javob berardi.

- SABOQ 1: "yangi tizim qurish" o'rniga avval backendda nima borligini tekshir.
  Chat to'liq ishlagan; kerak bo'lgan narsa — interfeys tili va formani o'zgartirish.
- SABOQ 2: narx majburiy edi (`/api/sotuvchi/javob` da `int()` chaqirilardi) —
  chatda narxsiz ham kelishiladi. `int(...) or None` bilan narx ixtiyoriy bo'ldi;
  `baza.javob_yoz` `narx: int | None` ni qabul qilardi, hech narsa buzilmadi.
  Buni ALOHIDA test bilan sinash kerak edi — umumiy halqa testi doim narx
  yuborardi, narxsiz yo'l sinovsiz qolardi.
- SABOQ 3: i18n regex bilan ishlaydi — dinamik matnni RU dictga qo'shsang
  ISH BOSHLAMAYDI (matching aniq kalit bo'yicha). `(\d+) sotuvchi (?:chatda )?javob
  berdi` kabi regex shaklida qo'shish kerak. Kod review buni ushladi.

## 2026-08-07: ikon() kaliti data-tab bilan mos bo'lmasa — ikonka JIMGINA YO'QOLADI
Aziz: "takliflar tab bar ikonkasi rasmi yo'qmi?" — ha, yo'q edi.
`ikon("takliflar")` deb chaqirilardi, svg kaliti esa `taklif` edi.
`svg[n] || ""` bo'sh qaytardi — ikonka chizilmadi, faqat yorliq qoldi.
Boshqa 4 tabda xato yo'q edi, faqat shu bittasida.

- SABOQ: svg kalitlarini data-tab qiymati bilan BIR XIL nomlash.
  Keyin har ikonka chaqiruvini kalitga solishtirish oson: qo'lda tekshirish
  o'rniga `grep -o 'ikon("[a-z]*")'` bilan chaqiruvlarni, `grep -oE '^ +[a-z]+:'`
  bilan kalitlarni olib, ikkita ro'yxatni solishtirish kifoya.
- Bu xatoni brauzer ham, piksel ham ko'rmaydi — svg bo'sh joy qoldirmaydi,
  yorliq markazda turadi. DOM'da `data-tab="X">...<svg` naqshini qidirish
  kerak: `re.search(r'data-tab="X".{0,150}', html)`.

## 2026-08-07: Piksel tekshiruvi TAKROR elementni ko'rmaydi — son hisoblaydi
Aziz: "tab barlarning joylashgan joylari xato". Haqiqatan ham ➕ tugma
`tabbar.js` da IKKI MARTA yozilib qolgan edi — 6 element 5 ustunli gridda
ikkala ➕ aynan 3-ustunga tushib, ustma-ust turardi.

- SABOQ 1: piksel va DOM pozitsiya tekshiruvi buni KO'RMAYDI — ikkala ➕
  ham markazda chiqqani uchun markaz=249/250 "to'g'ri" ko'rinardi.
  Element SONI tekshiruvi (`querySelectorAll(".ober-tab").length`) yagona
  ishonchli aniqlovchi edi: 6 chiqdi, 5 bo'lishi kerak edi.
- SABOQ 2: endi `tabbar.js` da runtime himoya bor — tablar soni 5 emas
  bo'lsa `console.error` yoziladi. Bu toifadagi xato yana jimgina
  chiqmaydi.
- SABOQ 3: bir xil HTML blokni qo'lda ikki marta yozish — takrorlash
  xavfi. Bitta tugmaga o'xshash blokni nusxalashda uni DOM'da sanab
  ko'rish shart.

- 2026-08-01: Ko‘p tillilikni sahifa oxirida matn almashtirish sifatida emas, barcha statik va API dan keyin chiziladigan UI matnlarini qamrab oladigan markaziy tizim sifatida qurish kerak; foydalanuvchi yozgan kontent esa tarjima qilinmay, asl holida qoladi. Uzun ruscha label’lar albatta haqiqiy mobil viewportda overflow testidan o‘tishi kerak.

- 2026-08-01: Bildirishnomani alohida nusxa sifatida ko‘paytirish o‘rniga chat xabarining rolga xos read-state’idan chiqarish kerak; shunda inbox, badge, mark-all va chat ochilishi bir-biridan ajralmaydi. Permission rad etilishi ham xato emas, foydalanuvchiga keyingi qadamni ko‘rsatadigan aniq UI holati bo‘lishi kerak.

- 2026-08-01: Taklif konversiyasi uchun foydalanuvchi chatga kirmasdan sotuvchi, narx, muddat, oxirgi xabar, rasm va unread holatini ko‘rishi kerak; read-state har rol uchun alohida, tanlangan suhbat esa yangi xabarda joyini yo‘qotmasligi zarur. Chat rasmlari klientga ishonmay, serverda turi va hajmi bo‘yicha tekshiriladi.

- 2026-08-01: Fuzzy lug‘atda noto‘g‘ri ijobiy moslik bo‘sh natijadan xavfliroq; `kolonka → kolodka` kabi bir harfli yaqinlikni alohida aniq kategoriya bilan to‘xtatish va real top natijalarni begona model ro‘yxati bo‘yicha qabul testidan o‘tkazish kerak.

- 2026-08-01: Motion sifatli ko‘rinishi uchun barcha elementni bir paytda uchirish emas, ko‘zni logo → va’da → qadamlar → forma tartibida olib boradigan 70–120 ms stagger ishlatish kerak; reduced-motion esa majburiy.

- 2026-07-31: Interfeysdagi effekt bezak emas, tizimning nima qilayotganini bildirib turadigan signal bo‘lishi kerak; fokus, aniqlash, progress va muvaffaqiyat holatlari yengil motion bilan ko‘rsatiladi.

- 2026-07-31: Responsive dizaynni faqat CSS breakpoint bilan emas, haqiqiy API natijasi va aniq viewportlarda tekshirish kerak; sticky header va natijaga avtomatik scroll birga qidiruv maydonini yopib qo‘yishi mumkin.
- 2026-07-31: OBER’ning uzoq muddatli pozitsiyasini birinchi vertikal bilan adashtirmaslik kerak: avtoehtiyot qismlar — start nuqtasi, OBER esa barcha mahsulotlar, ishlab chiqaruvchilar va xizmatlar bozori.
- 2026-07-31: Universal so‘rovda kategoriya tanilmasa uni barcha sotuvchilarga tarqatish mumkin emas; avval kategoriya aniqlanishi yoki xavfsiz “aniqlashtirish kerak” navbatiga tushishi shart.
- 2026-07-31: Kategoriya tizim ichida kerak, lekin foydalanuvchining boshini qotirmasligi kerak; erkin matn tashqi interfeys, tasdiqlangan yashirin taksonomiya esa routing dvigateli bo‘ladi.
- 2026-07-31: Ko‘p manbali e’lon agregatori reverse marketplace o‘rnini bosa olmaydi; indeks narx va supply konteksti beradi, mahsulot qiymatini esa so‘rovni mos providerga yetkazib, jonli taklif olish halqasi yaratadi.
- 2026-07-31: Marketplace MVPda pulni ushlab turishdan oldin kelishuv halqasini isbotlash kerak; eskrou ishonchni oshiradi, ammo litsenziya, KYC, nizolar va qaytarish operatsiyasini olib keladi, shu sabab uni keyin litsenziyalangan hamkor bilan qo‘shish ma’qul.
- 2026-07-31: Ichki ma’lumot modeli foydalanuvchi vazifasiga aylanmasligi kerak; OBER kelishuv yozuvini avtomatik tuzadi, odam esa faqat tabiiy harakatlar va bir bosishli statuslarni ko‘radi.
- 2026-07-31: Agar marketplace aloqa va javoblarni tashqi messenjerga chiqarib yuborsa, konversiya, xavfsizlik va qayta foydalanish nazoratini yo‘qotadi; OBERning asosiy halqasi bildirishnomadan natijagacha o‘z ichida qoladi.
- 2026-07-31: Boss mahsulotni faqat yakunda emas, har bosqichda xaridor va sotuvchi rolida vizual sinashi kerak; har inkrement ishlaydigan demo, aniq test ssenariysi va mobil ko‘rinish bilan topshiriladi.
- 2026-07-31: Universal marketplace hero tasvirida kategoriyalarni markazga tiqmasdan, qidiruv atrofidagi chet kompozitsiyada ko‘rsatish mahsulot ko‘lamini bir qarashda beradi va asosiy vazifani to‘sib qo‘ymaydi.
- 2026-07-31: Alohida mahsulot cutoutlarini chetlarga terish tezda katalog kollajiga aylanadi; kuchli hero uchun kategoriyalar bitta umumiy vizual metafora yoki yaxlit muhitga birlashtirilishi kerak.
- 2026-07-31: Universal bozorni hero’da ko‘rsatish “hamma narsani oldinga chiqarish” emas; boy kategoriya signallari yaxlit ko‘cha muhitiga qatlamlanadi, markazdagi qidiruv esa sokin va dominant qoladi.
- 2026-07-31: Realistik marketplace hero uchun mashina kabi taniladigan obyektlar rasmiy referens bilan generatsiya qilinishi, desktop va mobil esa bitta rasmni majburan kesish emas, alohida kompozitsiya olishi kerak.
- 2026-07-31: Generativ fonning mayda yuz va mahsulot detallari ishonchsiz ko‘rinsa, uni kattalashtirib ko‘rsatish o‘rniga past opacity bilan atmosfera qatlamiga aylantirish qidiruvni kuchaytiradi va AI izini yashiradi.
- 2026-07-31: Indeks bilmagan kategoriya mavjud vertikalga tushmasligi kerak; noto‘g‘ri natijadan ko‘ra tanilgan yo‘nalish + bo‘sh holat yoki xavfsiz aniqlashtirish foydalanuvchi ishonchini saqlaydi.
- 2026-07-31: Reverse marketplace’da birinchi sotuvchi javobi so‘rovni yopmasligi kerak; har bir mos sotuvchi bir marta javob beradi, xaridor esa bir nechta taklifni taqqoslaydi.
- 2026-07-31: Universal marketplace uchun kategoriya ro‘yxati interfeys emas, yashirin routing tili bo‘lishi kerak; xaridor va sotuvchi erkin yozadi, tizim ikkalasini bir xil intent va capability tuzilmasiga aylantiradi.
- 2026-07-31: Universal ko‘lamni isbotlash uchun barcha kategoriyani chala ochish shart emas; bitta vertikalda ko‘p manba, toza qidiruv va jonli kelishuv halqasini oxirigacha yopish keyingi kategoriyalar uchun takrorlanadigan platforma yaratadi.
- 2026-07-31: Bir xil brend hissi har sahifaga bir xil rasm qo‘yishdan emas, umumiy rang, tipografiya, spacing va motion tizimidan keladi; boy foto hero marketing yuzasida, ishchi sahifalar esa sokin va vazifaga yo‘naltirilgan bo‘lishi kerak.
- 2026-07-31: E’lon nofaolligini bir sahifalik test yoki xatoli yig‘ishdan hisoblash xavfli; faqat manbadan kamida bitta natija olgan, xatosiz to‘liq sikl ko‘rinmagan e’lonlar hisobini oshirishi mumkin.
- 2026-08-08: “Barcha kategoriya” bilan “barcha e’lon sahifasi” bir xil emas. Har kategoriya/viloyatning faqat birinchi sahifasini ko‘rgan yangilovchi ko‘rinmagan eski e’lonni sotilgan deb nofaol qila olmaydi; sotilganlik alohida detail-link tekshiruvi yoki haqiqiy to‘liq crawl bilan tasdiqlanishi kerak.
- 2026-08-08: Matn-almashtirishga asoslangan i18n regressiya testi lug‘atda kalit borligini tasdiqlasa ham real DOMdagi yangi, bo‘lingan yoki dinamik matn tarjimasini kafolatlamaydi. Har release’da rus rejimini brauzerda ko‘rish va UI matnlarini barqaror `data-i18n` kalitlari bilan render qilish kerak.
- 2026-07-31: Qidiruv keshini butun SQLite faylining mtime’i bilan bog‘lash noto‘g‘ri, chunki qidiruv analitikasi ham faylni o‘zgartiradi; kesh faqat yig‘ish+tahlilning tayyor versiya belgisi bilan yangilanishi kerak.

## 2026-08-07: Tab barda ➕ “markazda” deb grid’ni 4 ustun qilish — markazga chiqarmaydi

- To‘rtta teng ustunli grid qilsam ➕ 62% da qolardi — yon tomonda ko‘chib ketgan ko‘rinardi. Markazdagi tugma uchun 5 ustunli grid kerak: ➕ 3-ustunda, oxirgi tab 5-ustunda; 4-ustun bo‘sh spacer. Shunda ➕ aynan 50% da.
- SABOQ: “markazda” degan tasavvurni CSS o‘lchovsiz ishonib bo‘lmaydi. `getBoundingClientRect()` bilan DOM pozitsiyasini o‘lchadim — shundagina xato ko‘rindi. Piksel tahlili esa headless Chrome Windows’da kamida 500px kenglik majbur qilgani uchun chalg‘itdi (390px so‘rasam ham 500px layout ishlaydi).

## 2026-08-07: Sana “Kecha” ko‘rinishi — server UTC, foydalanuvchi Toshkentda

- Server `date` UTC ko‘rsatardi. 19:00 UTC dan keyin (Toshkentda 00:00 bo‘lgach) yangi e'lon “Kecha” bo‘lib ko‘rinardi — kodda xato yo‘q edi, vaqt mintaqasi farqi edi.
- SABOQ: sana yozadigan joyda server vaqtini emas, foydalanuvchi vaqtini ishlatish kerak. O‘zbekiston uchun qat’iy UTC+5 (DST yo‘q) — `time.strftime(localtime)` o‘rniga UTC+5 qo‘shilgan sana.
- SABOQ 2: qidiruvdagi yangilik bonusi ham server vaqtida hisoblanardi — e'lon sanasi Toshkentda bo‘lsa, taqqoslash ham Toshkentda bo‘lishi shart. Ikkala joy birga tuzatildi.

- 2026-08-08: `position:fixed` mobil qatlamning ota elementiga `transform`
  animatsiyasi berilsa, qatlam viewportga emas o‘sha ota konteynerga qamaladi.
  Sahifa darajasidagi motionni chat yoki modal saqlaydigan konteynerga emas,
  xavfsiz ichki bloklarga qo‘llash va haqiqiy mobil viewportda komposerni tekshirish kerak.
- 2026-08-08: Tanlov pitchida tez o‘zgaradigan production sonini exact metrika
  sifatida sarlavhaga qotirishdan ko‘ra `250K+` kabi tekshirilgan, bardoshli
  ko‘rsatkich ishlatish; exact sonni esa sana va jonli demo bilan tasdiqlash kerak.
- 2026-08-09: Marketplace’da AI lug‘atning o‘rnini egallamaydi: vision/LLM
  noma’lum so‘rovni tushunadi, lug‘at va yashirin taksonomiya esa natijani
  canonical nomga bog‘lab, tez, arzon, takrorlanadigan va xavfsiz qidiruvni
  ta’minlaydi. Eng kuchli yechim — gibrid router.
- 2026-08-09: Rasmli qidiruvda “kamera tugmasi ishladi” yetarli emas: brauzerda
  EXIFni olib tashlash, serverda MIME+magic-byte va hajm tekshiruvi, kalitsiz
  tashqi uzatishni to‘xtatish, past ishonchda aniqlashtirish, IP limiti va bir
  xil rasm uchun kesh birgalikda bo‘lmasa AI funksiyasi xarajat va maxfiylik
  xavfiga aylanadi.
- 2026-08-09: Production API kaliti hech qachon chat, repo yoki deploy arxiviga
  yuborilmaydi; foydalanuvchi uni provider panelida yaratadi va serverdagi
  root-only environment fayliga bevosita joylaydi.
- 2026-08-09: Texnik bo'lmagan foydalanuvchiga maxfiy kalit joylatishda
  `echo kalit | ssh` kabi ko'rinadigan buyruq bermaslik kerak. `Read-Host
  -AsSecureString`, redirect qilingan stdin, atomik root-only env fayli va
  xizmat holatini tekshiradigan bir bosishli yordamchi xavfsizroq va tushunarliroq.
- 2026-08-09: PowerShell `Process.StandardInput.Write()` UTF-8 BOM yuborishi
  mumkin; systemd EnvironmentFile birinchi assignmentini shunda yaroqsiz deb
  jurnalga to'liq chiqaradi. Secret env payloadni `UTF8Encoding(false)` bilan
  BaseStreamga byte sifatida yozish va faylni maxfiy bo'lmagan izohdan boshlash kerak.
- 2026-08-09: OpenAI `429`ning hammasi rate limit emas. `error.code`ni o'qib
  `credit_balance_exhausted`, project/org spend limit va haqiqiy request rate
  limitni alohida ko'rsatish kerak; billing xatosini qayta urinish bilan tuzatib bo'lmaydi.
- 2026-08-09: AI modelni qimmatroq variantga oldindan ko'tarmaslik kerak.
  Avval arzon modelni real kategoriyalar bo'yicha sinab, past ishonch va noto'g'ri
  topish holatlarini o'lchash; kuchli modelni faqat shu holatlarga fallback qilish tejamkor.
- 2026-08-09: Marketplace auditida “chiroyli ko‘rinish”dan oldin atamalar va
  halqa tekshiriladi. Indekslangan e’lonni “taklif” deb atash va Chat xatosida
  qayta urinish/kirish yo‘lini bermaslik foydalanuvchiga mahsulotning asosiy
  farqini tushuntirmaydi; `e’lon`, `jonli taklif`, `chat` alohida bo‘lishi kerak.
- 2026-08-09: Kodda aniq token va komponent tili mavjud bo‘lsa, Figma’dagi
  generic UI kitni import/detach qilish tezroq ko‘rinsa ham dizayn manbasini
  ikkiga bo‘ladi. OBER uchun production CSS’dan minimal local foundations
  yaratish va faqat kerakli P0 komponentlarni componentize qilish to‘g‘riroq.

## 2026-08-11: Chat halqasi — tokenning o‘zi ruxsat emas

- Sotuvchi sessiyasi haqiqiy bo‘lsa ham javob faqat unga `yuborishlar` orqali tayinlangan, muddati tugamagan va hali javobsiz so‘rovga yoziladi; valid “yo‘q” javobi invalid urinishdan alohida natija bo‘lishi kerak.
- API uchun telefonni keyin `pop` qilishdan ko‘ra uni `SELECT`ga umuman kiritmaslik xavfsizroq: yangi rol yoki branch maxfiy maydonni tasodifan qaytara olmaydi.
- Bitta qurilmada buyer va seller sessiyasi birga yashaydi; rol query orqali aniq tanlanadi, query bo‘lmasa faol buyer so‘rovi seller tokeni sabab yo‘qolmasligi kerak.
- Suhbat kartasini ochish — read/view amali, taklifni tanlash esa alohida mutatsiya. Ikkalasini bitta clickka bog‘lash foydalanuvchi qarorini soxtalashtiradi.
- Lokal indeks qamrovi og‘ishgan tor mahsulotlarda yashirin taxonomy fallback kerak, lekin u faqat aniq audit holatlariga ishlaydi va ma’nosiz matn/spam himoyasini chetlab o‘tmaydi.

## 2026-08-11: Agregator, Telegram va savdo chegarasi

- OBERning mahsulot modeli uchta: tashqi e’lon havolalari agregatori, teskari bozor va OBERga e’lon joylash. Chat aloqa va aniqlashtirish uchun; to‘lov, yetkazib berish va oldi-sotdi OBER orqali bajarilmaydi. Interfeysdagi “bitim shu yerda” kabi bitta jumla butun modelni noto‘g‘ri ko‘rsatadi.
- Telegram xabarini faqat yuborish emas, natijasini tekshirish kerak. `sendMessage` xato qaytarsa navbat belgilanmaydi va keyingi aylanish qayta urinadi; aks holda bildirishnoma yo‘qoladi, baza esa yolg‘on “yuborildi” deydi.
- Sotuvchiga Telegram orqali ikki signal kerak: yangi mos so‘rov va xaridorning yangi chat xabari. Erkin yozishmani botga ko‘chirish shart emas; xabardagi “OBER chatini ochish” tugmasi rolni va vazifani aniq saqlaydi.
- Vitrina xilma-xillik filtri vaqtincha o‘tkazib yuborgan kartani “ko‘rildi” deb belgilamasligi kerak. Aks holda zaxira to‘ldirish ishlamaydi va bazada yetarli e’lon bo‘lsa ham bosh sahifa skeletda qoladi.
- OBER e’lonida viloyat, shahar va tuman bir xil qiymat bo‘lishi mumkin; ko‘rsatishda takrorlarni olib tashlash kerak. CTA esa qiladigan ishini aniq aytsin: mos sotuvchilarga so‘rov yuborsa, “bitta sotuvchidan so‘rash” deb va’da bermasin.

## 2026-08-11: Bitta odam — ikki rol emas, to‘rtta tushunarli vazifa

- Yangi sotuvchi ro‘yxatdan o‘tgach Telegramni ulash ekrani `#asosiy`ni to‘liq almashtirsa, foydalanuvchi niyat qilgan ishidan uziladi va “boshqa joyga o‘tib ketdim” deb o‘ylaydi. Telegram majburiy sahifa emas: Sotish kabinetidagi ixtiyoriy xabarnoma kartasi bo‘lib, “Hozir emas” bilan yopilishi kerak.
- Bir odam bir paytda qidirishi ham, e’lon joylashi ham mumkin. Global navigatsiya rol nomlari bilan emas, vazifalar bilan bir xil tartibda yoziladi: `Qidirish → Kategoriyalar → Chat → Sotish`. Desktop va mobil tartibi farq qilsa, aynan bir mahsulot ikki xil mantiqdek ko‘rinadi.
- `Sotish` ichidagi ikki ichki vazifa aniq ajraladi: `Xaridor so‘rovlari` — teskari bozor; `E’lonlarim` — OBERning o‘z e’lonlari. E’lon formasi ochilganda ham shu tablar va aktiv `E’lonlarim` holati yo‘qolmasligi kerak.
- 390 px da ikki ustunli forma matematik jihatdan sig‘ishi mumkin, lekin narx inputi va “Kelishiladi” tugmasi birga kelganda input amalda o‘qilmay qoladi. Responsive tekshiruv faqat horizontal overflow emas; har maydonning foydalaniladigan kengligi ham o‘lchanadi. Bu holatda narx va joy telefon uchun bir ustunga o‘tkazildi.
- Brauzer yuzasi viewportni bevosita almashtira olmasa, bir xil originli 390×844 iframe ichida haqiqiy sahifani yuklash media-query, fixed tabbar, scroll va computed widthlarni ishonchli tekshiradi. Sinovdan keyin qobiq, vaqtinchalik route, server va baza to‘liq tozalanadi.

## 2026-08-12: Frontend qoidalari skillga ko'chirildi

- CLAUDE.md + OBER-DIZAYN-QOIDALARI.md har seansda qayta o'qiladi, lekin 2026-08-11 redesign'da o'lchangan YANGI qarorlar (uch qavatli quyuq rejim, amber CTA tili, tabbar amber tokenlari har sahifada bo'lishi shart) hali qo'llanmada yo'q edi. `.agents/skills/ober-frontend/SKILL.md` ga ko'chirildi — endi web/ ishini boshlagan agent ularni avtomatik o'qiydi.
- SABOQ: loyiha qoidalari bir joyda to'plansa, yangi agent (yoki yangi seans) xuddi shu qoidalarga bo'ysunadi. Community skill yuklash shart emas — eng katta qiymat loyihaning O'Z o'lchangan qoidalarini kodlashda.

## 2026-08-12: User-flow sinovi — API zanjir ishlaydi, agent cheklovi bor

Xaridor va sotuvchi bo'lib to'liq oqim sinandi (lokal 8800): qidiruv -> so'rov -> tarqatish -> javob -> chat -> bildirishnoma. Hammasi ishladi.

- SABOQ: browser_use agenti oddiy tekshiruvda ishlaydi, lekin murakkab interaktiv vazifada (karta bosish, forma to'ldirish) natija qaytarmay qoladi. Ishonchli yo'l: API zanjir (urllib) + DOM tekshiruvi. Brauzer agenti faqat qo'shimcha dalil.
- SABOQ: `/api/sotuvchi/javob` va `/api/suhbat/xabar` da ID emas TOKEN ishlatiladi (`_sotuvchi_ident` isdigit ni rad qiladi) — xavfsizlik to'g'ri, lekin test skripti buni bilmasa 401 oladi. Frontend to'g'ri ishlatadi.
- SABOQ: sinov yozuvlari (sorov, sotuvchi, suhbat, xabarlar) bazani iflos qiladi — testdan keyin tartib bilan tozalash kerak (xabarlar -> suhbatlar -> javoblar -> yuborishlar -> sorovlar -> sotuvchilar).

## 2026-08-12: Qattiq ranglar tokenlarga yig'ildi — ober-frontend skilli ishladi

Skillni ishda sinadik: `linear-gradient(180deg,#ffc24d,#f59e0b)` va `color:#231400` 14+ joyda qo'lda takrorlanardi (index 7, takliflar 5, sotuvchi 4, kategoriyalar 1, tabbar 1). Bitta token — `--cta-gradient`, `--on-cta`, `--amber-yorqin` — butun saytga. "Rangni o'zgartir" endi 1 satr.

- SABOQ: 47 ta aniq-matn almashtirish skript bilan bajarildi, ober-ui.css dagi token ta'riflari himoyalandi. Qoldiq tekshiruv — token ishlatilmagan joyni topdi (0 qoldi).
- SABOQ: kod review topdi: ober-ui.css da `--r-orta:15px/--r-katta:22px`, sahifalarda 14px/20px — ober-ui keyin yuklangani uchun 15/22 yutardi. Hujjatdagi shkala 14/20. Endi hamma joyda 14/20.
- SABOQ: web_sinov.py ga 7-qoida qo'shildi — xom amber CTA rangi sahifalarda qaytib kelmasin (faqat ober-ui.css token ta'rifida). 33→39 tekshiruv.
- SABOQ: 90deg/100deg maxsus gradientlar (tanlangan chip, hero amb, karta chizig'i) ataylab qoldirildi — bitta joyda, takrorlanmaydi.

## 2026-08-12: taste-skill (Leonxlnx) o'rnatildi

- `npx skills add` bilan ikkita skill o'rnatildi: `design-taste-frontend-v1` (barqaror v1) va `redesign-existing-projects`. `.agents/skills/` da saqlanadi — kelajak seanslarda ham bor.
- Ular `ober-frontend` skillini ALMASHTIRMAYDI — faqat to'ldiradi. OBER o'z o'lchangan qoidalariga ega (web_sinov 39 tekshiruv), taste-skill umumiy dizayn intizomi beradi.
- SABOQ: taste-skill React/Next/Framer'ga yo'naltirilgan, OBER esa vanilla HTML+CSS. Uni ishlatganda faqat dizayn QOIDALARI olinadi (rang birligi, typography, interaction states), texnologiya qismi (Tailwind/Framer/GSAP) tashlanadi.

## 2026-08-12: Emoji -> SVG (taste-skill anti-emoji qoidasi)

- Barcha haqiqiy emojilar SVG ga almashtirildi: telefon (call-btn), x (yopish), check (farq jadvali 5 joy). U+2190 (`←`) o'qlari EMOJI EMAS — matn belgisi, qoldirildi.
- SABOQ: `🕐|📍|🏷` tarjima regex'i elon.html SVG ga o'tgach hech qachon ishlamaydigan qoldiq bo'lib qolgan — ishlatilmaydigan regex'lar kod auditi paytida o'chirilishi kerak.
- SABOQ: inline-flex ichida SVG+matn orasini bo'shliq bilan emas, `gap` bilan ajratish kerak (flexbox bo'shliqni yutadi).

## 2026-08-12: window.alert -> inline xabar (sotuvchi kabineti)

- Ikkala alert inline'ga o'tkazildi: e'lon o'chirilmaganda #elon-ro boshiga `understood error` bloki, rasm kattaligida esa mavjud #f-izoh forma izohi.
- SABOQ: review topdi — xato xabari to'g'ri harakatdan keyin ham qolib ketadi. `#f-izoh` muvaffaqiyatli fayl tanlanganda tozalanadi. Forma xatolari ko'rsatilgach, keyingi muvaffaqiyatli harakatda tozalanishi shart.
- `confirm()` tasdiqlash dialogi qoldirildi: skill faqat `window.alert` ni taqiqlaydi, tasdiqlash xato xabari emas.

## 2026-08-12: Skip-link barcha sahifalarga qo'shildi

- `.skip-link` CSS ober-ui.css ga (barcha sahifada yuklanadi): fixed, translateY(-160%) yashirin, focus'da amber outline bilan chiqadi.
- 5 sahifa: index->#natija, kategoriyalar/sotuvchi/takliflar->#asosiy, elon->#sahifa. takliflar main'ga id="asosiy" qo'shildi (yo'q edi).
- SABOQ (review): skip-link manzili `tabindex="-1"` bo'lishi shart — aks holda fokus main'ga o'tmaydi, keyingi Tab header'dan davom etadi. WCAG standart naqshi.
- SABOQ: i18n kaliti va HTML matni apostrofda BIR XIL kod nuqtasida bo'lishi kerak (U+2018) — translate() normalizatsiyasi faqat ASCII ga o'giradi, mos kelmasa tarjima ishlamaydi.
- `:focus-visible` bilan birga `:focus` fallback qo'shildi (eski brauzerlar).

## 2026-08-12: Skeleton 4 sahifaga qo'shildi (kategoriyalar, sotuvchi, takliflar, elon)

- ober-ui.css ga umumiy skeleton tizimi: .sk-blok/.sk-chiziq + shimmer animatsiya + 18 o'lcham sinfi (sk-kat, sk-ustun, sk-elon...). Inline style EMAS — barcha o'lchamlar sinf modifieri.
- SABOQ (review 1): skeleton ichiga aria-hidden qo'yilsa, JS haqiqiy kontent chiqarganda uni REMOVE qilishi shart (kategoriyalar #kat-joy). Aks holda real kartalar screen reader'da ko'rinmay qoladi.
- SABOQ (review 2): qo'shishli padding xatosi — .sk-elon 22px + .sk-ustun 20px = 42px. Ichki konteyner o'z paddingi bor blok ichida yana padding qo'shmasin (.sk-elon .sk-ustun{padding:0}).
- Eski loading (spinner, loading-card, matn 'Yuklanmoqda...') o'rniga skeleton — dead CSS tozalandi.

## 2026-08-12 — OG meta'lar JS'da ishlamaydi, serverda to'ldiriladi
Telegram/Facebook skreperlari JavaScript ishlamaydi. `document.title` ni
yangilab og:title ni setAttribute qilsak ham — ulashilganda eski "E'lon —
OBER" chiqadi. Yechim: `/elon/{id}` route'ida server elon.html ni o'qib,
baza.ober_elon_ol orqali e'lon nomini olib og:title/description/url va
<title> ni almashtiradi. Sotuvchi kiritgan matnni html.escape qilish shart
(XSS). Replace jimgina ishlamay qolmasin — mos kelmasa jurnalga yoziladi.

## 2026-08-12 — Logotip: eski PNG 56KB, yangi SVG oilasi ~1KB
Eski logo.png (384x130, #002050) sayt tokeni #0a2b63 bilan mos emas edi —
"ideal emas" hissi aynan shu nomuvofiqlikdan. Yangi: logo.svg / logo-oy.svg
(quyuq uchun) / icon.svg + Pillow bilan render qilingan PNG'lar.
Muhim: header'da 94x29 o'lchamda to'liq kompozitsiya (monogram+so'z+tagline)
o'qilmaydi — ALohida KOMPAKT variant kerak (monogram+so'z, taglinesiz).
Review topdi: logotip kompozitsiyasi ishlatiladigan o'lchamga mos bo'lishi
shart, aks holda kichik o'lchamda shovqinga aylanadi.

## 2026-08-13 ? Frontend auditi: eski skrinshot emas, joriy Chrome o'lchovi

- Skrinshot va frontend faylining vaqtini solishtirish shart. 20:32 dagi
  390px kesilish skrinshotidan keyin kod 23:07 gacha o'zgargan edi; joriy
  Chrome o'lchovi `scrollWidth=390` va to'rt tabning ham sig'ganini isbotladi.
- Faqat CSS/HTML guard yetmaydi: 1280x900 va 390x844 Google Chrome'da
  `scrollWidth`, fixed/sticky qatlamlar, faol nav, console va failed request
  birga o'lchandi. To'liq seller -> e'lon -> buyer qidiruv/so'rov -> seller
  javob -> unread -> rasmli chat -> read-state oqimi har ikki viewportda 7/7.
- Lokal CSS `woff2` URLni ko'rsatib, binar faylni faqat deploy paytida yuklash
  clean clone va lokal Chrome'da yashirin 404 qoldiradi. 65 KB Onest aktivlari
  repoda saqlanadi va `web_sinov` ularning mavjudligini qo'riqlaydi.
- Bitta vazifa sarlavhasini topbarda va kontentda ketma-ket takrorlash
  iyerarxiyani kuchaytirmaydi; mobil Chatda aynan ikki `h1` chiqardi. Bitta
  ko'rinadigan kontekst sarlavhasi qoldi, topbar esa navigatsiya uchun.
- Yetarli rasmli e'lon yo'qligi jonli lenta uchun expected empty state.
  Uni `console.error` qilish haqiqiy E2E xatolarini shovqinda yashiradi;
  blok jim yashirinadi, haqiqiy fetch/render xatosi esa logda qoladi.

## 2026-08-13 — Skrinshot auditi: rejim almashishi emas, vazifa davomiyligi

- Bosh sahifa och, natija esa birdan quyuq bo‘lsa, bu “dark mode” emas:
  foydalanuvchiga boshqa mahsulot yoki boshqa rolga o‘tib ketgandek ko‘rinadi.
  Qidiruv → natija → footer bitta och rang tizimida qolishi kerak. Oldingi
  “quyuq natija” qarorini joriy foydalanuvchi skrinshoti va aniq shikoyati
  bekor qildi; yangi qaror OBER-DIZAYN-QOIDALARI.md ga yozildi.
- 390 px qidiruv ikki qator bo‘lishi shart emas. Qidiruv belgisi kichik
  ekranda yashirilsa, kamera 48 px, Topish 76 px va matn maydoni bir qatorda
  sig‘adi; 16 px input iOS zoomini ham oldini oladi.
- “Sotuvchilardan so‘rash”ni uch joyga ko‘paytirish topiluvchanlik bermadi:
  suzuvchi nusxa kartaning rasmi va narxini yopdi, ro‘yxat orasidagi nusxa
  esa reklamaga o‘xshadi. Bitta ixcham inline CTA natija tepasida yetarli.
- To‘rtta uzun saralash chipini gorizontal kesish o‘rniga mobil select,
  narxni esa bosilganda ochiladigan panel qilish boshqaruvni bitta qatorga
  sig‘dirdi. Narx “dan/gacha” qiymatlari alohida-alohida so‘rov yubormaydi;
  Qo‘llash bilan bir marta yuboriladi.
- Regression: web 65/65, i18n 22/22, suhbat/bildirishnoma 56/56, halqa
  26/26, AI vision 8/8, moslik 51/51. Inline JS Node sintaksis tekshiruvidan
  o‘tdi; izolyatsiyalangan lokal DB nusxasida sahifa 200 va qidiruv API 14
  real “divan” natijasi qaytardi.
- Muhim dalil chegarasi: joriy Chrome boshqaruvi Windows ACL helper xatosi
  bilan ikki marta uzildi. Oldingi Chrome skrinshoti yangi CSS uchun dalil
  emas. Yangi 390×844 va desktop skrinshot olinmaguncha “vizual E2E o‘tdi”
  deb yozilmaydi; blocker ochiq aytiladi.
## 2026-08-13 — Lokal tuzatish live emas: reliz va Telegram self-test

- `D:\OBER`dagi o‘zgarish productionga alohida chiqarilmaguncha `ober.uz` o‘zgarmaydi. Cache’ni taxmin qilishdan oldin live va lokal SHA-256 ni solishtirish kerak: bu safar `index.html`, `tabbar.js`, `i18n.js` aniq eski edi.
- Jonli bazani yoki `data/`ni qayta ko‘chirish shart emas. Farqli source fayllar vaqt-belgili `data/zaxira/*.tar.gz` arxiviga olindi, stage xeshi lokal bilan tekshirildi, keyin faqat o‘sha fayllar `install` qilindi. Telegram relizida server-side `py_compile`, service restart, ichki health-check va rollback yo‘li ishlatildi.
- `no-cache` “kesh yo‘q” degani emas; validator bo‘lsa brauzer yangilikni tekshiradi. Live `tabbar.js` uchun ETag bilan conditional so‘rov `304`, yangi xesh esa oddiy so‘rovda qaytdi.
- Telegram tashxisida barcha `tg_yuborildi=0` yozuvlarni “yangi navbat” deb sanash noto‘g‘ri. 24 soatdan eski 9 chat alohida `tg_chat_eski`, haqiqiy yuboriladigan navbat esa `tg_chat_kutayotgan=0` bo‘ldi.
- `getUpdates` va `sendMessage` alohida threadlarda. Oxirgi HTTP kod umumiy global bo‘lsa polling timeouti yuborishning 403 holatini bosib ketishi mumkin; `threading.local()` va alohida regressiya testi buni qo‘riqlaydi.
- Ulangan sotuvchi endi kabinetdagi “Bildirishnomani sinash” orqali faqat o‘z sessiyasi va o‘z Telegram chatiga test yuboradi. Begona token 401, yuborish xatosi esa `/start` bilan aniq recovery ko‘rsatadi.
- Yakuniy lokal regressiya: web 67/67, i18n 23/23, suhbat/bildirishnoma 61/61, halqa 26/26, AI vision 8/8, moslik 51/51; sotuvchi inline JS `node --check`dan o‘tdi. Live fayllar lokal bilan bir xil, qidiruv 60 natija qaytardi, assetlar 200, 4 service active, Caddy recent 5xx=0.
- Chrome, kengaytma va native-host diagnostikasi toza bo‘lsa ham Codex browser runtime Windows ACL helper xatosida uch marta ishga tushmadi. Bunday holatda HTTP/xesh dalilini vizual E2E deb atamaslik va yangi mobil/desktop skrinshotni foydalanuvchidan olish kerak.

## 2026-08-13 — Marketplace hooki, brend aktivlari va live dalil

- Marketplace/agregator bosh sahifasida editorial serif brend hissini kuchaytirmadi, vazifani sekin o‘qitdi. Lokal Onest 800 sarlavha, `Bir qidiruv. Butun bozor.` hooki va bevosita izoh agregator + teskari bozor modelini bir qarashda tushuntiradi.
- Ochiq e’lon soni va dollar kursi alohida katta dalil kartasi emas, topbarning o‘ngidagi ixcham real ko‘rsatkich bo‘ldi. Raqam `white-space:nowrap` va tabular figures bilan bir qatorda qoladi; telefonda izohlar yashirinib, sonlarning o‘zi saqlanadi.
- Haqiqiy qidiruvlar qidiruv maydonidan oldinga, ikki qatorli haqiqiy e’lonlar hero ortiga ko‘chirildi. Foydalanuvchi va’dadan oldin bozordagi real harakatni ko‘radi; rasmiy quyuq “O‘lchangan…” bloki olib tashlandi.
- Foydalanuvchi bergan 4385×1466 logo va 1335×1335 icon xom holda webga yuklatilmadi. Asl `reports/` fayllari saqlandi, shaffof PNGlar 720×241 va 256×256 ga optimallashtirildi; live xeshlar lokal bilan 1:1 tekshirildi.
- Chrome vizual auditi Windows sandbox ACL xatosida ochilmasa, boshqa browser bilan “o‘tdi” deb bo‘lmaydi. Bunday relizda statik regressiya, JS sintaksisi, cache-bypass live xesh va API dalillari alohida ko‘rsatiladi; Chrome screenshot blokeri halol yoziladi.
- Brend rasmi binar jihatdan yangilansa ham eski URL (`/brend/logo-kompakt.png`) brauzer keshida eski ko‘rinishni saqlashi mumkin. Logo kabi ko‘zga darhol tashlanadigan aktivda xesh tekshiruvi bilan birga versiyalangan yangi fayl nomi ishlatiladi; 2026-08-13 relizida barcha 5 sahifa `/brend/logo-ober-20260813.png` ga o‘tdi.

## 2026-08-13: `flex-start` chiplarni chapda qoldiradi, qidiruv esa markazda

Aziz: *"so'nggi kunlarda qidirilgan chiplar qiyshiq joylashgan"*.

Sabab: `.samples` (chiplar) `justify-content:flex-start; max-width:680px`
edi — qidiruv qutisi bilan BIR XIL kenglikda, lekin O'ZI chapda turardi.
Qidiruv qutisida `margin-inline:auto` bor edi (markazda), chiplarda yo'q.
Natija: qidiruv x=305 dan, chiplar x=50 dan — 250px farq.

O'lchov: qidiruv qutisi navy chegarasi y=282, x=305..974, markaz=639.

Saboq: `max-width` kenglikni cheklaydi, MARKAZNI emas. Bir qatorda
turgan elementlar bir xil `margin-inline` ga ega bo'lishi shart —
aks holda bir xil kenglik ham, bir xil joy emas.

## 2026-08-13 — Yangi manba: adapter yozish yetarli emas, sikl ham chaqirishi kerak

Avtoelon.uz adapteri yozildi va sinovdan o'tdi — e'lonlar bazaga tushdi,
FTS indeksiga kirdi, qidiruvda chiqdi. Lekin serverda `ober-yangilik`
xizmati uni YIG'MAYDI: `yangilik.py` faqat OLX + Telegram chaqiradi,
`yigish.py` runnerini (manbalar papkasidagi adapterlarni) hech kim
chaqirmasdi. Telegram uchun shu xato 2026-08-02 da bo'lgan edi (adapter
bor, chaqiriq yo'q) — avtoelon bilan takrorlandi.

Saboq: adapter yozilgach, `yangilik.py` dagi sikl chaqiruvini tekshir.
Yangi manba = kod emas, ikki joy: `app/manbalar/` fayli + `yangilik.py`
dagi `yigish_sikli()` chaqiruvi.

Ikkinchi saboq: `yigish.main("bosh")` oxirida `tahlil.main()` chaqiradi —
issiq sikl ichida chaqirilsa tahlil ikki marta ishlaydi. Sikl o'z
tahlilini boshqaradi, shuning uchun `yigish_sikli` adapterlarni
to'g'ridan-to'g'ri chaqiradi (yigish.main emas).

Uchinchi saboq: model yo'lidagi qidiruvda sarlavhadagi so'zga ball
berilmasdi. "shazor" so'rovi `byd` modeliga aylanadi va HAMMA byd
e'lonlari deyarli bir xil ball oladi — "Polik so'ng puls" (Chazor yo'q)
1-o'ringa chiqdi, haqiqiy "BYD Chazor 2026" esa 344-o'rinda edi.
Sarlavhada so'rov so'zi bor e'lon yuqoriroq ball oladi (2 ball/so'z).
O'lchov: avtoelon Chazor e'lonlari 344 -> 42-o'rin.

## 2026-08-13 — B tur (do'kon) manbasi: Asaxiy.uz

Avtoelon (A tur — e'lonlar taxtasi) dan farqli: Asaxiy — B tur (do'kon),
ya'ni sotuvchi emas, NARX beradi. OBER uchun qiymati "bozor narxi qancha"
degan savolga tayanch dalil.

Saboq 1: sayt tuzilishi o'zgarishi mumkin — eski URL (`/ru/category/...`)
2026-08-13 da 404 qaytardi, yangisi `/product/{slug}`. Audit sanasi bilan
adapter ichida URL naqshi hujjatlashtirilishi kerak.

Saboq 2: B tur uchun ro'yxat sahifasi yetarli — `data-actual-price`
so'mda, `biznes=1` belgilanadi. Tovar sahifasi (574KB) faqat chuqur
rejimda tavsif uchun olinadi.

Saboq 3: `yigish_sikli` adapterlarni avtomatik topadi — yangi manba
qo'shilsa kod o'zgarmaydi, faqat `app/manbalar/` fayli kerak. Ammo
`yigish_sinov` shartnomani qo'riqlaydi — har yangi manba uchun u yerda
tekshiruv qo'shilishi kerak.

## 2026-08-13 — CHUQUR_SAHIFA: adapter o'z qamrovini e'lon qiladi

`yigish_sikli(toliq=True)` avval hamma adapterga `chuqur(3)` berardi.
Avtoelon uchun 10 kerak edi, asaxiy uchun 3 yetarli (tovar sahifalari
katta). Yechim: adapter `CHUQUR_SAHIFA` atributini e'lon qiladi,
`yigish_sikli` `getattr(adapter, "CHUQUR_SAHIFA", 3)` ishlatadi.

Saboq: har bir manbaning qamrov chuqurligi boshqacha — umumiy son
emas, adapterning o'zi aytadi. Qo'lda har adapter uchun alohida son
yozish shart emas.

## 2026-08-13 — Asaxiy serverda bloklangan

Asaxiy.uz adapteri lokalda 200 bilan ishladi, serverda (Hetzner
77.42.123.90) esa 403 — IPv4 ham, IPv6 ham. Bu saytning o'z himoyasi
(retro-403 sahifa), Cloudflare emas. "Lokal ishlayapti" serverda ham
ishlaydi degani emas — har yig'ish sikli boshqa IP'dan keladi.

Saboq 1: yangi manbani faqat lokalda emas, SERVERDAN ham tekshirish
kerak. Adapter yozilib "yashil sinovlar" ko'rsatilganda ham — asosiy
savol: "server uni o'qiya oladimi?".

Saboq 2: bloklanganda adapter to'xtashi kerak, 16 bo'limni urib saytni
bosmasligi kerak. `_Bloklandi` — birinchi 403'da darhol to'xtash.
Aks holda har 45 daqiqada 16 ta 403 so'rov — bu saytga hujumdek.

Saboq 3: NAVBATCHI "yuklash" faqat ober-server'ni restart qilardi —
ober-yangilik va ober-toliq eski kod bilan qolaverardi. Endi uchalasi
birga restart bo'ladi (NAVBATCHI.bat 2026-08-13).

## 2026-08-13 — Asaxiy serverda bloklangan

Asaxiy.uz adapteri lokalda 200 bilan ishladi, serverda (Hetzner
77.42.123.90) esa 403 — IPv4 ham, IPv6 ham. Bu saytning o'z himoyasi
(retro-403 sahifa), Cloudflare emas. "Lokal ishlayapti" serverda ham
ishlaydi degani emas — har yig'ish sikli boshqa IP'dan keladi.

Saboq 1: yangi manbani faqat lokalda emas, SERVERDAN ham tekshirish
kerak. Adapter yozilib "yashil sinovlar" ko'rsatilganda ham — asosiy
savol: "server uni o'qiya oladimi?".

Saboq 2: bloklanganda adapter to'xtashi kerak, 16 bo'limni urib saytni
bosmasligi kerak. `_Bloklandi` — birinchi 403'da darhol to'xtash.
Aks holda har 45 daqiqada 16 ta 403 so'rov — bu saytga hujumdek.

Saboq 3: NAVBATCHI "yuklash" faqat ober-server'ni restart qilardi —
ober-yangilik va ober-toliq eski kod bilan qolaverardi. Endi uchalasi
birga restart bo'ladi (NAVBATCHI.bat 2026-08-13).

## 2026-08-13 — Shahar.uz: yangi vertikal (ko'chmas mulk)

Uchinchi adapter — ko'chmas mulk (kvartira, uy, dacha). Serverdan ochiq
(200), narx dollarda — dollar_kursi() orqali so'mga (avtoelon'dagi kabi).

Saboq 1: bo'lim slug'i bilan havola naqshi MOS KELMASLIGI mumkin.
`/arenda-kvartir` sahifasida `/kvartira/...` havolalar, `/arenda-domov`
da `/doma/...`. Kartani `property_wrapper` orqali kesish to'g'ri —
havola ichidan olinadi.

Saboq 2: sarlavhaga kategoriya prefiksi qo'shish XATO — qidiruv ballini
pasaytiradi (qisqa sarlavha bonusi + so'z pozitsiyasi). Kategoriya
alohida maydonda, FTS'ga tahlil qo'shadi.

Saboq 3: `normalla("ijara")` -> "izara", `normalla("Аренда")` -> "arenda"
— o'zbek/rus so'zlari FTS'da bir-birini topmaydi. Bu qidiruv tizimining
umumiy masalasi (atama xaritasi faqat xususiyatlar uchun). Yechim:
erkin rejimda so'rov so'zlariga atama juftini qo'shish.

## NAVBATCHI.bat ochilmay qoldi — izoh satridan `rem` tushib ketgan (2026-08-13)

Oyna "ochilib darhol yopiladi" edi. Sabab: `if exist (...)` blokidagi
uch qatorli izohning uchinchi satridan `rem` prefiksi tushib ketgan
edi — satr bajariladigan buyruqqa aylanib, ichidagi `).` blokni buzdi
(`. was unexpected at this time.`). Xulosa: `.bat`dagi ko'p qatorli
izoh `rem` bilan boshlangan HAR satrda `rem` yozilishi shart — blok
ichida bitta satr ham buzilsa butun fayl ishlamaydi. Tekshiruv usuli:
`timeout 8 cmd //c NAVBATCHI.bat` — xato darhol ko'rinadi.

## Har commit oldidan .bat tekshiruvi — pre-commit hook (2026-08-13)

NAVBATCHI.bat xatosidan keyin `app/bat_sinov.py` yozildi, lekin
qo'lda ishga tushirilsa unutiladi. Yechim: `hooks/pre-commit` +
`git config core.hooksPath hooks` — har commitda avtomatik ishlaydi,
xato topsa commitni bloklaydi. Xulosa: qo'lda bajariladigan sinov
tezda unutiladi; qo'riqchi git hook bo'lishi kerak. Sinov: buzilgan
.bat bilan commit bloklandi ✓, toza holatda o'tdi ✓.

## 2026-08-13 — Glotr.uz adapteri: nom regex'i non-greedy kesadi
Glotr karta nomini `title=.\s*([^"'<]{5,150}?)\s*.` bilan oldim —
`{5,150}?` eng qisqa moslikni oladi, natijada nomlar kesildi:
"Склад телефон и планшеты" → "Склад". Yig'ish 1100+ e'lon bilan
"muvaffaqiyatli" o'tdi, lekin baza kesilgan nomlar bilan to'ldi.
Sababni "zaryadka qidiruvda chiqmayapti" deb qidirib topdim.
Yechim: `title=["']([^"']+)["']` — atribut qiymatini to'liq olish.
Xulosa: regex qolipida non-greedy kvantifikator ishlatganda kesilgan
qiymat xavfi bor — atribut qiymatini chegaralovchilar ichida olish.

## 2026-08-13 — O'zbekcha↔ruscha kanonik sinonim (normalla darajasida)
Yangi manbalar (Shahar.uz, Glotr) ruscha nom olib keladi: "Аренда",
"Зарядное устройство", "Холодильник". O'zbekcha so'rov ularni topa
olmasdi: FTS prefiks qidiruvi ildiz bir, qo'shimcha boshqa bo'lganda
mos kelmaydi (zariadka vs zariadnoe, izara vs arenda).
Yechim normalla() darajasida: ruscha shakl o'zbekcha KANONIK shaklga
keladi ("arenda" -> "izara"). FTS indeksi ham shu normalla bilan
qurilgani uchun ikkala tomon bir xil bo'ladi — qidiruv ham, indeks ham.
MUHIM: normalla() o'zgarganda FTS QAYTA TAHLIL qilinishi shart
(`tahlil.py qayta`) — aks holda eski indeks yangi normalla bilan
mos kelmaydi (serverda 64 soniya).
Xulosa: til moslashuvi muammosini qidiruv qatlamida emas, NORMALLA
darajasida hal qilish kerak — bir joyda o'zgarish, hamma joyda ishlaydi.

## 2026-08-14 — Avizinfo.uz adapteri: karta chegarasi product-info bo'lishi kerak
Avizinfo karta kesishda dastlab `ru-i-offer` havolasidan kesdim —
natijada narx/sana chiqmadi (ular `product-info` klassida, havoladan
keyin). Yechim: `product-info` klassidan kesish (har kartada bittadan,
ichida ID ham, narx ham, sana ham bor).
Xulosa: ro'yxat sahifasida karta chegarasini eng TO'LIQ maydon
joylashgan klassdan kesish kerak — havola chegarasi narx/sana kabi
maydonlarni tashlab qo'yishi mumkin.

## 2026-08-14 — Yangi manba bonusini keng o'lchov (14 so'rov, production)

Bonus (+12 ball, faqat ishonchli) noto'g'ri moslikni tepaga chiqarmaydi:
tekshiruvda bonus olgan HAR bir e'lon nomida so'rov so'zi bor edi.
"telefon"/"mebel"/"karavot" da bonus olgan 0 ta — sabab to'g'ri:
Glotr'da "karavot" e'lonlari umuman yo'q, "mebel" e'lonlari nomida
"mebel" so'zi yo'q (ofis texnikasi — ishonchsiz), "telefon" da OLX
862 ta — adolatli raqobat. Xulosa: bonus ishonchlilik qo'riqchisi
bilan birga ishonchli — yangi manba o'z so'rovida ko'rinadi, lekin
noto'g'ri e'lon siqib chiqarilmaydi. O'lchov vositasi:
`app/olchov_bonus.py` (serverda ishlatiladi, lokal bazada yangi
manba e'lonlari yo'q).

## Glotr chuqur yig'ish sekin edi — tavsif faqat yangi e'lonlar uchun (2026-08-14)

Har karta uchun tovar sahifasi ochilardi: 21 bo'lim x 10 sahifa x 56 karta
= 11 760 so'rov ≈ 8 soat. `baza.saqla` mavjud e'lonning tavsifini
YO'QOTMAYDI (bo'sh qiymat eski tavsifni saqlab qoladi) — shuning uchun
qayta olish shart emas. Endi faqat `yangi` qaytargan e'longa tavsif
olinadi: birinchi chuqur sikl sekin, keyingilari faqat yangilarni o'qiydi.

Yana bir saboq: yangi manba qo'shilgach, `bosh()` (1-sahifa) ishlaydi-yu,
lekin chuqur sahifalar (10-sahifagacha) faqat sutkalik sikl orqali yig'iladi.
Glotr'ning mebel bo'limida divan/krovat/matras 10-sahifagacha tarqalgan —
baza'da faqat 1-sahifa (61 ta) bor edi, "Mebel bo'sh" degan xulosa noto'g'ri
edi. To'liq qamrov uchun chuqur sikl ishga tushirilishi shart.

## PWA — Play/App Store tayyorgarligi (2026-08-14)

Saytda manifest yo'q edi, sw.js faqat push uchun edi, theme-color redesign'dan
oldingi eski rangda qolgan edi. Play Store TWA va App Store o'ramlari PWA
talab qiladi: manifest.json, 192/512/180 ikonlar, standalone display, offline
cache. Ikonlar Chrome headless orqali SVG'dan generatsiya qilindi
(--default-background-color=00000000 flag shaffof fon beradi, aks holda oq
fon qo'shadi). `time.sleep` xatosi avtoelon/shahar/avizinfo'da ham bor —
Glotr'da tuzatildi, boshqalarida keyingi bosqich.

## Play/App Store do'kon materiallari (2026-08-14)

Privacy policy sahifasi yaratildi (`web/privacy.html`), serverga
`/privacy` va `/maxfiylik` marshrutlari qo'shildi. Footer'da allaqachon
`/maxfiylik` havolasi bor edi — endpoint yo'q edi, ular mos keldi.

Do'kon materiallari `reports/play-market-2026-08-14/DOKON-MATERIALLARI.md`:
tavsiflar uz/ru, kalit so'zlar, ekran rasmlari ro'yxati. Skrinshotlar
Chrome headless bilan: Play uchun 390x844, App Store uchun
`--window-size=430,932 --force-device-scale-factor=3` → 1290x2796 (6.5" talab).

Saboq: App Store skrinshoti uchun window-size ni shunchaki kattalashtirish
yetmaydi — device-scale-factor kerak, aks holda CSS layout desktop bo'lib qoladi.


## 2026-08-16 — Sinonim qatlami: ruscha shakllarni qo'lda hisoblamang

O'zbekcha-ruscha sinonim xaritasini kengaytirishda (kitob/kniga,
soat/chasi, eshik/dver...) har juftlikning normallashgan shaklini
QO'LDAN hisoblash xato beradi. `normalla()` qoidalari kutilmagan
joyda ishlaydi: "часы" -> "shasi" (ч->ch, c->s), "кирпич" ->
"kirpish" (ч->ch, c->s), "цепочка" -> "seposhka" (ts->s, c->s).
"chasi" deb yozilsa sinov yiqilardi.

Yechim: `sinonim_sinov.py` har juftlikni ASL yozuvdan (kirillcha
ruscha + lotincha o'zbekcha) hisoblab, ikkala shakl tengligini
tekshiradi. Qo'lda hisoblanadigan narsani sinovga topshirdik.

Ikkinchi saboq: `_KANONIK` o'zgarishi normalla'ni HAMMA joyda
(bozor_izi, yonalishlar, soz_kategoriya) o'zgartiradi — shuning
uchun faqat bir ma'noli juftliklar kiritiladi ("ручка" qalam ham,
eshik tutqichi ham; "стекло" oyna ikki ma'noli — ikkalasi ham
kiritilmadi), va o'zgarishdan keyin indeks `tahlil.py qayta`
bilan to'liq qayta quriladi (519 408 e'lon, 98 soniya; yo'lda
3.3 million nofaol FTS yozuvi ham tozalandi).

Uchinchi saboq: NAVBATCHI buyrug'i bilan ishlaganda javob.txt
ESKI yuklash matnini ko'rsatsa, buyruq skript sifatida bajarilganini
aniqlash uchun skript boshiga MARKER qo'yish kerak — `yuklash`
va ixtiyoriy skript ikkalasi ham javob yozadi.


## 2026-08-16 — Yetim yozuvlar: xom DELETE zanjirni uzadi

O'chirilgan sotuvchilarga tegishli 47 yuborishlar, 24 suhbatlar, 3
javoblar qolib ketgan edi (CLAUDE.md #5). Sabab: test skriptlari
`DELETE FROM sotuvchilar` bilan faqat sotuvchini o'chirardi, bog'liq
jadvallarga tegmasdi.

Ikki saboq:
1. O'chirish — har doim ZANJIR bo'ylab: xabarlar -> suhbatlar ->
   javoblar -> yuborishlar -> push_obunalar -> sotuvchilar. Endi
   `baza.sotuvchi_ochir()` buni bitta tranzaksiyada qiladi, server esa
   har startda `yetimlarni_tozala()` bilan eski qoldiqlarni yig'ishtiradi.
2. `sotuvchi_ochir` o'z `ulan()` ini ochadi — uni BOSHQA `with
   baza.ulan()` ichida chaqirsa "database is locked" chiqadi (SQLite
   bitta yozuvchi). Test skriptlarida qo'sh ulanish xatosi shundan
   topildi va tuzatildi.

Uchinchi saboq: `javoblar.sotuvchi` — TEXT ustun, ichida id saqlanadi.
Eski yozuvlarda NOM bo'lishi mumkin. Tozalashda faqat raqamli qiymatlar
solishtiriladi (`sotuvchi GLOB '*[0-9]*' AND NOT GLOB '*[^0-9]*'`) —
nomli eski javob "yetim" deb o'chib ketmasligi uchun sinov bilan
qo'riqlanadi.

## 2026-08-16 — Qidiruv sekinligining uchta asl aybdori

"Qidiruv 4+ so'zda ~200 ms" muammosi uch xil joyda edi, uchalasi ham
o'lchov bilan topildi:

1. **AND bosqichiga umumiy so'z kirardi.** `fts_erkin` ning 1-bosqichi
   (6 so'z AND) "iphone 13 pro max yangi original" uchun 7 157 ms oldi —
   aybdor `pro` va `yangi` (indeksning 5% idan ortiq e'londa bor). FTS5
   AND kesishmasi umumiy so'zning butun postings ro'yxatini ko'rib
   chiqadi, natija bor bo'lsa ham. Yechim: `_umumiy_soz` filtrini AND
   bosqichiga qo'llash (7 157 -> 7 ms).

2. **OR bosqichida `ORDER BY rank` butun to'plamni bm25 bilan baholaydi.**
   "kvartira* OR xonali*" 458 ms, "iphone* OR 13* OR max* OR original*"
   1167 ms — oddiy LIMIT esa 8-9 ms. FTS rank'i oxirida ishlatilmaydi
   (Python qayta ballaydi), shuning uchun OR bosqichida tashlandi.

3. **`faol=1 AND id IN (...)` SQLite'ni noto'g'ri indeksga tashladi.**
   ix_faol_manba orqali butun faol to'plamni ko'rib chiqadi (4000 id
   uchun 20 129 ms). `id IN` birinchi bo'lsa PK indeks ishlaydi (405 ms).

Saboq: FTS5 optimallashtirishda "so'rov uzun — OR ga tushadi" degan
taxmin noto'g'ri edi. Asl qiymat umumiy so'zning postings ro'yxati
o'lchamida va `ORDER BY rank` baholashida. Har bosqich alohida
o'lchanmasa, xato manbai ko'rinmaydi.

## 2026-08-16 — "Indeks o'sgach o'zi to'g'rilanadi" — amalga oshdi, lekin bir qo'shimcha kerak bo'ldi

`gilam sotaman` muammosi (kat:Xizmatlar yorlig'i) CLAUDE.md da
"indeks o'sgach o'zi to'g'rilanadi" deb yozilgan edi. Indeks 519k ga
o'sgach nisbat haqiqatan to'g'rilandi: Xizmatlar 85% -> 20%, Uy va
bog' yetakchiga chiqdi (77%). Lekin mutlaq ulush (15%) qoidasi
ikkinchi darajali kategoriyani ham qoldirdi — Xizmatlar 20% o'tib
ketdi.

Saboq: indeks o'sishi asosiy signalni to'g'riladi, lekin chegara
mutlaq bo'lsa (15%) shovqin hali ham qoladi. Yechim: yolg'iz so'z
yo'lida NISBAT qoidasi (yetakchidan 0.75 dan past kategoriya
tashlanadi). Production'da 8 so'z o'lchandi: faqat gilam va oltin
o'zgardi, karavot ikkalasini saqladi (42/55=0.76). O'zgarish kichik
va o'lchov bilan — butun bozor_izi qayta sozlanmadi.

## 2026-08-16 — Tartibsiz LIMIT eski e'lonlarni qaytaradi; prefiks aniqdan ustun chiqardi

OR bosqichida `ORDER BY rank` ni tashlagach ikkita yashirin xato chiqdi:

1. **Tartibsiz `LIMIT` FTS'ni rowid O'SISH bo'yicha o'qiydi** — "kvartira"
   3212 mos, plain LIMIT 900 eng ESKI 900 ni oldi (rowid <= 109 736).
   Barcha yangi e'lonlar nomzodga kirmasdi — yangilik bonusi ularga
   yetib bormasdi. Yechim: `ORDER BY rowid DESC` (4 ms, rank hisobi yo'q).

2. **Prefiks-mos aniq so'zdan yuqori ball oldi** — "divan charm" da
   "Charmhoo" (charm PREFIKSI) "Audit divan" (aniq divan) dan yuqori
   chiqdi. `x == w or x.startswith(w)` ikkalasini bir xil hisoblardi.
   Buni moslik_sinov 5-bo'limi ushladi (yangi deterministik erkin
   qidiruv testi). Yechim: aniq 10 ball, prefiks 2.5 ball.

Saboq: tezlik uchun rank'ni olib tashlash — bu "bir xil natija, tezroq"
emas. Tartib natijani belgilaydi (eski vs yangi) va sinov buni
qo'riqlamasa, jimgina yomonlashib boradi. Har tartib o'zgarishidan
keyin NATIJA (qaysi e'lonlar chiqadi), faqat vaqt emas, tekshiriladi.

## 2026-08-16 — Mobil audit: yopishqoq element qoidasi iframe bilan o'lchanadi

O'lchov: har sahifa 390px iframe'da ochilib, computed style bo'yicha
`position:fixed|sticky` va haqiqiy ko'rinish (opacity, pointer-events,
ekran maydoni) tekshirildi. Boshqa sahifalar `.topbar{position:static}`
qilgan edi — elon.html qilmagan, topbar + tabbar ikkalasi yopishqoq
edi (121px doim band). CSS qoidasini "ko'z bilan" emas, iframe
o'lchovi bilan qo'riqlash kerak — dump-dom'ning regex'i yetarli emas,
chunki yashirin elementlarni (scrim, toast, skip-link) ajrata olmaydi.
Tuzatish: elon.html 880px media blokiga `.topbar{position:static}`.

## 2026-08-16 — Model yo'lida ham aniq so'z prefiksdan ustun

Erkin yo'lda `x == w` aniq (10 ball), `x.startswith(w)` prefiks
(2.5 ball) deb ajratilgan edi. Model yo'lida esa `w in n_matn`
QISM-SATR tekshiruvi turardi — "kolodka" so'rovi "KolodkaX"
(begona so'z, kolodka PREFIKSI) ni ham to'liq mos deb ballardi
va aniq "Nexia tormoz kolodka" bilan bir xil ball olardi.
O'lchov: ikkalasi 105.0 — farq yo'q edi. Tuzatish: so'zlarga
bo'lib aniq (4.0/2.0) va prefiks (1.0/0.5) alohida hisoblanadi.
relevans_sinov 6-bo'limi (13 -> 15) qo'riqlaydi. Xulosa: bir
yo'lda tuzatilgan sifat xatosi boshqa yo'lda qolishi mumkin —
har yo'lning o'z qo'riqchisi bo'lishi shart.

## 2026-08-16 — Yangi e'lon FTS'ga darhol tushishi shart

Audit production'da 46 ta yangi OLX e'loni FTS'da yo'qligini topdi —
ular qidiruvda umuman ko'rinmasdi. Sabab: `saqla()` FTS'ga yozmasdi,
e'lon indeksga `tahlil_qil()` orqali tushardi — u yo 500 ta yangi
e'lon yig'ilganda, yo butun issiq sikl tugaganda ishlaydi. Issiq
sikl 5+ soat davom etganda yangi e'lonlar yarim kun ko'rinmaydi.
Yechim: `saqla()` yangi/qaytgan e'lonni FTS'ga o'zi yozadi
(`_fts_tez_yoz`, teg tahlilga qoldiriladi). Xulosa: yig'ilgan
ma'lumot qidiruvga tushmasa, butun yig'ish ma'nosiz — FTS sinxron
bo'lishi shart, oraliq tahlilga tayanib bo'lmaydi.
