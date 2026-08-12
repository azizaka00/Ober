# Saboqlar

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
