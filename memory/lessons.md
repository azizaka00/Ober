# Saboqlar

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
