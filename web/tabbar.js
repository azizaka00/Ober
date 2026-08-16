/* OBER — PASTKI TAB NAVIGATSIYASI (2026-08-07)
 *
 * To'rtta yo'nalish va bitta tezkor amal tabiiy tartibda turadi:
 *   Qidirish · Kategoriyalar · + E'lon · Chat · Sotish
 *
 * NEGA KERAK (2026-08-07, Aziz): "hozir ichma-ich bo'lib ketgan
 * sahifalar". Haqiqatan ham: sotuvchi kabinetida yorliqlar, xaridor
 * sahifasida havolalar, takliflar sahifasi alohida — navigatsiya bir
 * joyda emas edi. Endi bitta joyda, beshta tabda. Xaridor ham,
 * sotuvchi ham bir xil ko'radi: bosh sahifa (qidiruv), kategoriyalar
 * (bozor bo'limlari), yangi e'lon (asosiy harakat), takliflar
 * (xabarlar), sotish (xaridor so'rovlari va o'z e'lonlari).
 * Bitta odam xaridor ham, sotuvchi ham bo'lishi mumkin; tablar rolni
 * almashtirmaydi, faqat bajariladigan ishni ochadi.
 */
(function () {
  "use strict";
  if (document.querySelector(".ober-tabbar")) return;

  var tr = function (t) {
    return (window.OBER_I18N && window.OBER_I18N.t) ? window.OBER_I18N.t(t) : t;
  };
  var path = location.pathname;
  var qidiruv = new URLSearchParams(location.search);

  // QAYSI TAB FAQOL — URL dan. Elon sahifasida hech biri (u natijaning
  // davomi, tab emas).
  var faol = "";
  if (path === "/" || path === "/index.html") faol = "bosh";
  else if (path.indexOf("/kategoriyalar") === 0) faol = "kategoriyalar";
  else if (path.indexOf("/takliflar") === 0) faol = "takliflar";
  // SOTUVCHI TOMONIGA BITTA ESHIK (2026-08-11, Aziz).
  //
  // Ilgari ikkita edi: "+ E'lon" (`?yangi=1`) va "Sotish". Ikkalasi ham
  // shu sahifaga borardi va RO'YXATDAN O'TMAGAN odam uchun ekran
  // harfma-harf bir xil chiqardi — ya'ni yangi kelgan har bir odam
  // uchun navigatsiyaning ikki tugmasi bitta ish qilardi.
  //
  // Aziz "+ E'lon" ni tanladi: u nima bo'lishini aytadi, "Sotish" esa
  // faqat qayerga borishini. Kabinet yo'qolmaydi — e'lon formasi
  // ustida "Xaridor so'rovlari / E'lonlarim" yorliqlari turadi.
  else if (path.indexOf("/sotuvchi") === 0) faol = "elon";
  else if (path.indexOf("/elon/") === 0) faol = "";

  var st = document.createElement("style");
  st.textContent = [
    "/* OBER pastki tabbar — yengil va bir xil, 2026-08-13 */",
    "[hidden]{display:none!important}",
    /* TEPA PANELDAGI QIDIRUV (2026-08-15) — ichki sahifalarda.
       Logotip bilan amallar orasida, qolgan joyni oladi. Telefonda
       ham sig'sin: `min-width:0` bo'lmasa flex element qisqarmaydi
       va panel chetdan chiqib ketadi. */
    ".ober-top-qidiruv{",
    "  flex:1 1 auto;min-width:0;display:flex;align-items:center;gap:6px;",
    "  max-width:520px;margin:0 12px;padding:0 4px 0 12px;",
    "  min-height:40px;border:1px solid rgba(10,43,99,.14);",
    "  border-radius:var(--r-pill,999px);background:rgba(255,255,255,.72);",
    "  -webkit-backdrop-filter:var(--shisha);backdrop-filter:var(--shisha);",
    "  box-shadow:inset 0 1px 0 rgba(255,255,255,.8);",
    "  transition:border-color 140ms ease,box-shadow 140ms ease;",
    "}",
    ".ober-top-qidiruv:focus-within{",
    "  border-color:var(--navy,#0a2b63);",
    "  box-shadow:0 0 0 3px rgba(10,43,99,.10);",
    "}",
    ".ober-top-qidiruv input{",
    "  flex:1;min-width:0;align-self:stretch;border:0;outline:0;",
    "  background:transparent;color:var(--text,#111a2c);",
    "  font:inherit;font-size:13.5px;",
    "}",
    ".ober-top-qidiruv input::placeholder{color:var(--faint,#98a0af)}",
    ".ober-top-qidiruv button{",
    "  flex:none;width:32px;height:32px;border:0;border-radius:50%;",
    "  display:grid;place-items:center;cursor:pointer;",
    "  background:var(--navy,#0a2b63);color:#fff;",
    "}",
    ".ober-top-qidiruv svg{width:15px;height:15px}",
    /* 380px dan tor ekranda logotip + qidiruv + til bir qatorga
       sig'maydi. Qidiruv o'z qatoriga tushadi. */
    "@media (max-width:400px){",
    "  .topbar-inner{flex-wrap:wrap;row-gap:8px}",
    "  .ober-top-qidiruv{order:9;flex-basis:100%;margin:0 0 8px;max-width:none}",
    "}",
    /* TEPA PANELDA "SO'ROV YUBORISH" (2026-08-16) — IndiaMART'ning
       "Post Requirement" tugmasi. Qidiruv qatorida turadi: odam
       topilmasa darhol so'ray oladi, boshqa sahifaga o'tmaydi.

       `flex:none` — qidiruv qisqarsin, tugma siqilmasin. Matn
       ikki qavat: keng ekranda "So'rov yuborish", 600px dan torida
       "So'rov" (telefonda tepa panelda joy kam). */
    ".ober-sora-cta{",
    "  flex:none;display:inline-flex;align-items:center;justify-content:center;",
    "  min-height:40px;padding:0 16px;border-radius:999px;",
    "  background:var(--navy,#0a2b63);color:#fff;",
    "  font-size:12.5px;font-weight:800;white-space:nowrap;",
    "  text-decoration:none;box-shadow:0 6px 16px rgba(10,43,99,.22),inset 0 1px 0 rgba(255,255,255,.14);",
    "  transition:transform 120ms var(--ease),box-shadow 120ms var(--ease);",
    "}",
    "@media (hover:hover){",
    "  .ober-sora-cta:hover{transform:translateY(-1px);box-shadow:0 8px 20px rgba(10,43,99,.28)}",
    "}",
    ".ober-sora-cta:active{transform:scale(.97)}",
    "@media (max-width:600px){",
    "  .ober-sora-cta{min-height:36px;padding:0 12px;font-size:11.5px}",
    "}",
    ".ober-sora-cta .uzun{display:inline}",
    ".ober-sora-cta .qisqa{display:none}",
    "@media (max-width:520px){",
    "  .ober-sora-cta .uzun{display:none}",
    "  .ober-sora-cta .qisqa{display:inline}",
    "}",
    /* BOSH SAHIFA — YOPISHQOQ TEPA PANEL + NAVBATLI QIDIRUV
       (2026-08-16).

       `--navbat` sinfi faqat bosh sahifada qo'yiladi. Boshlanishi
       yashirin: hero'da katta quti bor, ikkitasi birga chalkash.
       Hero qutisi surilib ketgach `body` ga `ober-tepa-qidiruv-
       ochiq` qo'shiladi va bu ochiladi.

       `visibility` ham kerak: faqat `opacity:0` bo'lsa maydon
       ko'rinmasa ham Tab bilan fokus olardi va ekran o'quvchi uni
       o'qirdi. */
    "body.ober-bosh-yopishqoq .topbar{",
    "  position:sticky;top:0;z-index:30;",
    "  background:rgba(255,255,255,.9);",
    "  -webkit-backdrop-filter:var(--shisha-quyuq);",
    "  backdrop-filter:var(--shisha-quyuq);",
    "}",
    ".ober-top-qidiruv--navbat{",
    "  opacity:0;visibility:hidden;",
    "  transform:translateY(-6px);",
    "  transition:opacity .18s ease,transform .18s ease,visibility .18s;",
    "}",
    "body.ober-tepa-qidiruv-ochiq .ober-top-qidiruv--navbat{",
    "  opacity:1;visibility:visible;transform:none;",
    "}",
    /* Harakatni kamaytirish so'ralgan bo'lsa — siljish yo'q. */
    "@media (prefers-reduced-motion:reduce){",
    "  .ober-top-qidiruv--navbat{transition:none;transform:none}",
    "}",
    "body.ober-tabbar-joy{padding-bottom:calc(70px + env(safe-area-inset-bottom));}",
    "body.ober-tabbar-joy .results{padding-bottom:calc(92px + env(safe-area-inset-bottom));}",
    ".ober-tabbar{",
    "  position:fixed;left:0;right:0;bottom:0;z-index:25;",
    "  background:rgba(250,252,255,.94);",
    "  -webkit-backdrop-filter:var(--shisha-quyuq);",
    "  backdrop-filter:var(--shisha-quyuq);",
    "  border-top:1px solid rgba(11,37,89,.10);",
    "  box-shadow:0 -8px 28px rgba(11,37,89,.08);",
    "  padding-bottom:env(safe-area-inset-bottom);",
    "}",
    ".ober-tabbar-inner{",
    "  max-width:560px;margin:0 auto;height:62px;",
    "  display:grid;grid-template-columns:1fr 1fr 1.12fr 1fr;",
    "}",
    ".ober-tab[data-tab=\"bosh\"]{grid-column:1}",
    ".ober-tab[data-tab=\"kategoriyalar\"]{grid-column:2}",
    ".ober-tab[data-tab=\"elon\"]{grid-column:3}",
    ".ober-tab[data-tab=\"takliflar\"]{grid-column:4}",
    ".ober-tab{",
    "  display:flex;flex-direction:column;align-items:center;justify-content:center;",
    "  gap:3px;text-decoration:none;color:var(--muted,#667085);",
    "  font-size:10.5px;font-weight:700;line-height:1.15;",
    "  -webkit-tap-highlight-color:transparent;touch-action:manipulation;",
    "  transition:color 140ms var(--ease,cubic-bezier(.2,0,0,1)),transform 120ms var(--ease);",
    "}",
    ".ober-tab:active{transform:translateY(1px) scale(.97)}",
    ".ober-tab-ikon{",
    "  position:relative;width:38px;height:27px;border-radius:999px;",
    "  display:grid;place-items:center;",
    "  transition:background 140ms var(--ease,cubic-bezier(.2,0,0,1)),color 140ms var(--ease);",
    "}",
    ".ober-tab svg{width:21px;height:21px;display:block}",
    ".ober-tab:not(.ober-tab-asosiy).faol{color:var(--navy,#0b2559)}",
    ".ober-tab:not(.ober-tab-asosiy).faol .ober-tab-ikon{",
    "  background:var(--navy-soft,#edf2fa);color:var(--navy,#0b2559);box-shadow:none;",
    "}",
    ".ober-tab-asosiy{transform:translateY(-4px);color:var(--navy,#0b2559)}",
    ".ober-tab-asosiy:active{transform:translateY(-3px) scale(.97)}",
    ".ober-tab-asosiy .ober-tab-ikon{",
    "  width:42px;height:42px;border:2px solid var(--surface,#fff);",
    "  background:var(--cta-gradient);color:var(--on-cta);",
    "  box-shadow:0 6px 16px rgba(245,166,35,.26),inset 0 1px 0 rgba(255,255,255,.5);",
    "}",
    ".ober-tab-asosiy.faol .ober-tab-ikon{",
    "  background:linear-gradient(180deg,#ffcf6b,#f5a623);",
    "  box-shadow:0 0 0 3px var(--amber-soft,#fff6e3),0 6px 16px rgba(245,166,35,.28);",
    "}",
    ".ober-tab-nishon{",
    "  position:absolute;top:-2px;right:-7px;min-width:16px;height:16px;padding:0 4px;",
    "  border-radius:999px;background:var(--amber-deep,#e08d00);color:#fff;",
    "  font-size:9.5px;font-weight:800;line-height:16px;text-align:center;",
    "  box-shadow:0 0 0 2px var(--surface,#fff);",
    "}",
    ".messages-link,.xabarlar-link{position:relative}",
    ".ober-top-nishon{",
    "  position:absolute;top:-7px;right:-8px;min-width:18px;height:18px;padding:0 5px;",
    "  border-radius:999px;display:grid;place-items:center;",
    "  background:var(--amber-deep,#e08d00);color:#fff;font-size:9.5px;font-weight:850;",
    "  line-height:18px;box-shadow:0 0 0 3px var(--surface,#fff);",
    "}",
    "@media (max-width:600px){",
    "  .ober-tabbar-inner{height:58px}",
    "  .ober-tab{font-size:10px}",
    "}",
    "@media (max-width:900px){",
    "  .ober-tabbar-joy .messages-link,.ober-tabbar-joy .seller-link,",
    "  .ober-tabbar-joy .buyer-link,.ober-tabbar-joy .xabarlar-link{display:none!important}",
    "}",
    ".ober-desktop-nav{display:none}",
    "@media (min-width:901px){",
    "  body.ober-tabbar-joy{padding-bottom:0}",
    "  body.ober-tabbar-joy .results{padding-bottom:34px}",
    "  .ober-tabbar{display:none}",
    "  .ober-desktop-nav{",
    "    display:inline-flex;align-items:center;min-height:38px;padding:0 12px;",
    "    border-radius:999px;color:var(--navy,#0b2559);text-decoration:none;",
    "    font-size:12.5px;font-weight:760;white-space:nowrap;transition:background 120ms ease;",
    "  }",
    "  .ober-desktop-nav:hover{background:var(--navy-soft,#eaeff8)}",
    "  .ober-desktop-nav:active{transform:translateY(1px)}",
    "  .ober-desktop-nav.faol{background:var(--navy-soft,#eaeff8)}",
    "  .ober-desktop-nav.asosiy{background:var(--navy,#0b2559);color:#fff}",
    "  .ober-desktop-nav.asosiy:hover{background:var(--navy-dark,#081b42)}",
    "  .ober-desktop-nav.asosiy.faol{box-shadow:0 0 0 3px var(--navy-soft,#eaeff8)}",
    "  .ober-tabbar-joy .messages-link,.ober-tabbar-joy .seller-link,",
    "  .ober-tabbar-joy .buyer-link,.ober-tabbar-joy .xabarlar-link{display:none!important}",
    "}"
  ].join("\n");
  document.head.appendChild(st);

  var ikon = function (n) {
    var svg = {
      bosh: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 10.5 12 3l9 7.5"/><path d="M5.5 9.5V21h13V9.5"/></svg>',
      kategoriyalar: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="3.5" width="7" height="7" rx="1.6"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.6"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.6"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.6"/></svg>',
      plus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
      takliflar: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.5 8.5 0 0 1-8.5 8.5 8.4 8.4 0 0 1-3.75-.86L3 21l1.9-5.7A8.5 8.5 0 1 1 21 11.5Z"/></svg>',
      sotuvchi: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4.5 20.5c.8-3.6 3.9-5.5 7.5-5.5s6.7 1.9 7.5 5.5"/></svg>'
    };
    return svg[n] || "";
  };

  var yozuv = function (t) {
    return '<span class="ober-tab-yozuv">' + tr(t) + "</span>";
  };

  var nav = document.createElement("nav");
  nav.className = "ober-tabbar";
  nav.setAttribute("aria-label", "Asosiy navigatsiya");
  nav.innerHTML =
    '<div class="ober-tabbar-inner">' +
    '<a class="ober-tab' + (faol === "bosh" ? " faol" : "") + '" href="/" data-tab="bosh"' +
      (faol === "bosh" ? ' aria-current="page"' : "") + '>' +
      '<span class="ober-tab-ikon">' + ikon("bosh") + "</span>" + yozuv("Qidirish") + "</a>" +
    '<a class="ober-tab' + (faol === "kategoriyalar" ? " faol" : "") + '" href="/kategoriyalar" data-tab="kategoriyalar"' +
      (faol === "kategoriyalar" ? ' aria-current="page"' : "") + ">" +
      '<span class="ober-tab-ikon">' + ikon("kategoriyalar") + "</span>" + yozuv("Kategoriyalar") + "</a>" +
    '<a class="ober-tab ober-tab-asosiy' + (faol === "elon" ? " faol" : "") + '" href="/sotuvchi?yangi=1" data-tab="elon"' +
      (faol === "elon" ? ' aria-current="page"' : "") + ">" +
      '<span class="ober-tab-ikon">' + ikon("plus") + "</span>" + yozuv("E’lon") + "</a>" +
    '<a class="ober-tab' + (faol === "takliflar" ? " faol" : "") + '" href="/takliflar" data-tab="takliflar"' +
      (faol === "takliflar" ? ' aria-current="page"' : "") + ">" +
      '<span class="ober-tab-ikon">' + ikon("takliflar") + '<span class="ober-tab-nishon" hidden></span></span>' +
      yozuv("Chat") + "</a>" +
    "</div>";
  document.body.appendChild(nav);
  document.body.classList.add("ober-tabbar-joy");

  function faolQil(kalit) {
    document.querySelectorAll(".ober-tab,.ober-desktop-nav").forEach(function (a) {
      var shu = a.getAttribute("data-tab") === kalit;
      a.classList.toggle("faol", shu);
      if (shu) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    });
  }
  window.OBER_TAB_FAOL = faolQil;

  // ── DESKTOPDA NAVIGATSIYA YO'QOLIB QOLMASIN ──────────────────────
  //
  // 2026-08-08 auditida "desktopda mobil tabbar" kamchilik deb yozilgan
  // va tabbar 901px dan yuqorida yashirilgan. Qaror to'g'ri: pastda
  // yopishib turgan tab bar telefon uslubi, katta ekranda u saytni
  // "cho'zilgan telefon ilovasi" qilib ko'rsatadi.
  //
  // Lekin havolalar boshqa joyga KO'CHIRILMAGAN. Desktop tepa panelida
  // atigi uchtasi bor edi: logo, Chat, Profil. Ikkitasiga umuman yo'l
  // qolmagan:
  //     Kategoriyalar   — bozor bo'limlari
  //     Yangi e'lon     — sotuvchi e'lon qo'shadigan asosiy harakat
  //
  // Ya'ni desktopdagi sotuvchi e'lon joylashtira olmasdi.
  //
  // Nega shu faylda tuzatilyapti: navigatsiya ikki joyda yozilgani
  // uchun ular bir-biridan uzoqlashib ketdi. Endi barcha manzil
  // FAQAT shu yerda e'lon qilinadi — tepadagi havolalar ham shu
  // ro'yxatdan yasaladi, demak yana ajralib keta olmaydi.
  var desktopTablar = [
    {yol: "/",              nom: "Qidirish",      kalit: "bosh"},
    {yol: "/kategoriyalar", nom: "Kategoriyalar", kalit: "kategoriyalar"},
    {yol: "/sotuvchi?yangi=1", nom: "+ E’lon",   kalit: "elon", asosiy: true},
    {yol: "/takliflar",     nom: "Chat",          kalit: "takliflar"}
  ];
  // HAR SAHIFADA TEPA PANEL BOSHQACHA YOZILGAN.
  // Birinchi urinishda faqat `.top-actions` qidirilgan edi — u esa
  // atigi bosh sahifada bor. Natijada `/sotuvchi`, `/takliflar` va
  // `/kategoriyalar` da havolalar qo'yilmadi (o'lchandi: top-actions
  // topilgan sahifa 1 ta, qolgan uchtasida 0).
  //
  // Hamma sahifada uchraydigan yagona narsa — til tugmasi (`.lang-slot`).
  // Shuning uchun tayanch shu: uning ota elementi tepa paneldagi
  // havolalar joyi bo'ladi.
  var joy = document.querySelector(".top-actions");
  if (!joy) {
    var til = document.querySelector(".topbar .lang-slot, .lang-slot");
    joy = til ? til.parentElement : document.querySelector(".topbar-inner");
  }

  // TEPA PANELDA QIDIRUV — ICHKI SAHIFALARDA (2026-08-15).
  //
  // O'lchov: qidiruv maydoni faqat `index` va `kategoriyalar` da bor.
  // `sotuvchi`, `takliflar`, `elon` da UMUMAN yo'q. E'lonni o'qib
  // turgan odam boshqa narsa qidirmoqchi bo'lsa, avval bosh sahifaga
  // qaytishi kerak edi.
  //
  // IndiaMART qidiruvni TEPA PANELDA saqlaydi — u har sahifada bor va
  // odam kontekstni tark etmaydi. Aziz aynan shuni ko'rsatdi.
  //
  // BOSH SAHIFA — 2026-08-16 da QO'SHILDI.
  //
  // Ilgari bu yerda "bosh sahifada qo'yilmaydi, ikkitasi chalkash"
  // deb yozilgandi. Aziz "ikkalasi ham bo'lsin" dedi va u haq —
  // lekin ikkalasi BIR VAQTDA ko'rinsa chindan chalkash bo'ladi.
  //
  // Yechim: navbat bilan. Hero qutisi ekranda turganda tepa
  // qidiruv yashirin; u yuqoriga surilib ketgach tepa panel
  // yopishadi va ingichka qidiruv paydo bo'ladi. Ya'ni qidiruv
  // HECH QACHON yo'qolmaydi, lekin hech qachon ikkilanmaydi ham.
  //
  // Bosh sahifada tepa panel ilgari umuman yopishmasdi — pastga
  // surganda ketib qolardi va qidiruvga qaytish uchun tepaga
  // qaytish kerak edi.
  // 2026-08-16: bosh sahifaga qo'shish BOSHLANDI VA QAYTARILDI.
  // Yopishqoq panel va qidiruvni joylash ishladi, lekin ko'rsatish
  // qoidasi ishlamadi: `body.ober-tepa-qidiruv-ochiq` sinfi
  // qo'yilganda ham hisoblangan `visibility` `hidden` bo'lib
  // qolaverdi. Selektor mos keladi (`el.matches()` -> true), qoida
  // hujjatda bor, xususiylik yuqori — sababi topilmadi.
  // Yarim ishlaydigan narsa jonli saytda qolmasin.
  var boshSahifa = false;
  var ichkiSahifa = boshSahifa ||
                    path.indexOf("/sotuvchi") === 0 ||
                    path.indexOf("/takliflar") === 0 ||
                    path.indexOf("/elon") === 0;
  var topbarIchi = document.querySelector(".topbar-inner");
  if (ichkiSahifa && topbarIchi && !document.querySelector(".ober-top-qidiruv")) {
    var forma = document.createElement("form");
    forma.className = "ober-top-qidiruv";
    forma.setAttribute("role", "search");
    forma.action = "/";
    forma.method = "get";
    var maydon = document.createElement("input");
    maydon.name = "q";
    maydon.type = "search";
    maydon.autocomplete = "off";
    maydon.placeholder = tr("Nima kerak?");
    maydon.setAttribute("aria-label", tr("Qidirish"));
    var tugma = document.createElement("button");
    tugma.type = "submit";
    tugma.setAttribute("aria-label", tr("Qidirish"));
    tugma.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"'
      + ' stroke-width="2.2" stroke-linecap="round" aria-hidden="true">'
      + '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>';
    forma.appendChild(maydon);
    forma.appendChild(tugma);
    // Bo'sh so'rov bilan bosh sahifaga o'tib ketmasin.
    forma.addEventListener("submit", function (e) {
      if (!maydon.value.trim()) { e.preventDefault(); maydon.focus(); }
    });
    // Logotipdan KEYIN, amallardan OLDIN — IndiaMART tartibi.
    var brend = topbarIchi.querySelector(".brand");
    if (brend && brend.nextSibling) topbarIchi.insertBefore(forma, brend.nextSibling);
    else topbarIchi.appendChild(forma);

    // BOSH SAHIFA: navbat bilan ko'rsatish (2026-08-16).
    //
    // Hero'dagi katta quti ekranda ekan — tepa qidiruv yashirin.
    // U ketgach tepa panel yopishadi va qidiruv paydo bo'ladi.
    //
    // `IntersectionObserver` ishlatiladi, `scroll` hodisasi emas:
    // scroll har kadrda o'qiladi va telefonni qizdiradi, observer
    // esa faqat chegara kesib o'tilganda uyg'onadi.
    var heroQidiruv = boshSahifa
      && document.querySelector(".hero .search-panel");
    if (heroQidiruv && "IntersectionObserver" in window) {
      document.body.classList.add("ober-bosh-yopishqoq");
      forma.classList.add("ober-top-qidiruv--navbat");
      new IntersectionObserver(function (yozuvlar) {
        var korinmoqda = yozuvlar[0].isIntersecting;
        document.body.classList.toggle("ober-tepa-qidiruv-ochiq",
                                       !korinmoqda);
      }, {rootMargin: "-8px 0px 0px 0px"}).observe(heroQidiruv);
    }
  }
  // "SO'ROV YUBORISH" — HAR SAHIFADA TEPA PANELDA (2026-08-16).
  //
  // IndiaMART'ning "Post Requirement" tugmasi: qidiruv natijasida
  // ham, e'lon o'qiyotganda ham, chatda ham — xaridor istalgan
  // joydan so'rov yuboradi, "topilmasa nima?" degan savolga javob
  // har doim tepada turadi.
  //
  // `/?sora=1` ga yo'naltiradi: bosh sahifa bu parametrni ko'rib
  // qidiruvga fokus beradi va so'rash amalini ochadi (index.html
  // oxiridagi qoida).
  //
  // `joy` top-actions — hamma sahifada bor (lang-slot orqali
  // topiladi). Tugma til tugmasi yonida turadi, desktop nav'lar
  // undan keyin qo'shiladi.
  if (joy && !document.querySelector(".ober-sora-cta")) {
    var sora = document.createElement("a");
    sora.className = "ober-sora-cta";
    sora.href = "/?sora=1";
    sora.setAttribute("role", "button");
    sora.innerHTML = '<span class="uzun">' + tr("So‘rov yuborish")
      + "</span><span class=\"qisqa\">" + tr("So‘rov") + "</span>";
    var oldin = joy.querySelector(".lang-slot");
    if (oldin) joy.insertBefore(sora, oldin); else joy.appendChild(sora);
  }
  if (joy) {
    desktopTablar.forEach(function (x) {
      var a = document.createElement("a");
      a.className = "ober-desktop-nav" + (x.asosiy ? " asosiy" : "")
                  + (faol === x.kalit ? " faol" : "");
      a.href = x.yol;
      a.textContent = x.nom;
      a.setAttribute("data-tab", x.kalit);
      if (faol === x.kalit) a.setAttribute("aria-current", "page");
      // Mobil va desktopda bitta tartib: Qidirish -> Kategoriyalar ->
      // + E'lon -> Chat -> Sotish. Eski maxsus havolalar CSS bilan
      // yashiriladi; til va Chiqish vazifa navigatsiyasidan keyin qoladi.
      var oldin = joy.querySelector(".lang-slot");
      if (oldin) joy.insertBefore(a, oldin); else joy.appendChild(a);
    });
  }    // REGRESSION HIMOYASI (2026-08-07): plus tugma bir marta yozilib, ikki
  // marta tushib qolgan edi — element ustma-ust chiqqan. Piksel
  // tekshiruvi buni ko'rmaydi, element SONI esa ko'radi.
  // Markazdagi + E'lon faqat bir marta bo'lishi va jami 4 tab qolishi shart.
  if (document.querySelectorAll(".ober-tab").length !== 4) {
    console.error("[ober-tabbar] tablar soni 4 emas!",
                  document.querySelectorAll(".ober-tab").length);
  }

  // O'QILMAGANLAR NISHONI — Chat tabida.
  // Aktor localStorage'dan: sotuvchi bo'lsa token, aks holda xaridor
  // so'rovi. Hech narsa yo'q bo'lsa — jim turamiz (nishon yo'q).
  // 30 soniyada bir marta — sahifa ochiq tursa ham yangilanadi.
  var nishon = nav.querySelector(".ober-tab-nishon");
  var topHavola = document.querySelector('.ober-desktop-nav[href="/takliflar"],.messages-link,.xabarlar-link');
  var topNishon = null;
  if (topHavola) {
    topNishon = document.createElement("span");
    topNishon.className = "ober-top-nishon";
    topNishon.hidden = true;
    topNishon.setAttribute("aria-hidden", "true");
    topHavola.appendChild(topNishon);
  }
  function nishonniKorsat(son) {
    var matn = son > 99 ? "99+" : String(son || "");
    nishon.hidden = !son;
    nishon.textContent = matn;
    if (topNishon) {
      topNishon.hidden = !son;
      topNishon.textContent = matn;
      topHavola.setAttribute("aria-label", son ? tr("Chat") + " · " + son : tr("Chat"));
    }
  }
  function yangila() {
    var actor = "";
    var rol = "xaridor";
    var s = localStorage.getItem("ober_sotuvchi");
    var q = localStorage.getItem("ober_sorov");
    if (/^\d+$/.test(s || "")) { localStorage.removeItem("ober_sotuvchi"); s = ""; }
    if (/^\d+$/.test(q || "")) { localStorage.removeItem("ober_sorov"); q = ""; }
    // Bitta telefonda xaridor ham, sotuvchi ham bo'lishi mumkin. Nishon
    // doim saqlangan sotuvchini ustun qo'ysa, xaridor chatida aynan
    // sotuvchining unread soni ko'rinardi. Aktor hozirgi ISH kontekstidan:
    // Sotish sahifasi/sotuvchi chatida — sotuvchi; qolgan joyda — xaridor.
    var sotuvchiKontekst = path.indexOf("/sotuvchi") === 0 ||
      (path.indexOf("/takliflar") === 0 && qidiruv.get("rol") === "sotuvchi");
    if (sotuvchiKontekst && s) { actor = s; rol = "sotuvchi"; }
    else if (q) { actor = q; rol = "xaridor"; }
    else if (s) { actor = s; rol = "sotuvchi"; }
    if (!actor) { nishonniKorsat(0); return Promise.resolve(); }
    return fetch("/api/bildirishnomalar?rol=" + rol + "&actor=" + encodeURIComponent(actor))
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        var n = Number((d && d.jami) || 0);
        nishonniKorsat(n);
      })
      .catch(function () {});
  }
  window.OBER_BILDIRISH_YANGILA = yangila;
  yangila();
  setInterval(yangila, 30000);
})();
