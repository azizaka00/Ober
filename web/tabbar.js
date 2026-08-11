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
    "/* OBER pastki tab bar — 2026-08-07 */",
    "[hidden]{display:none!important}",
    "body.ober-tabbar-joy{padding-bottom:calc(66px + env(safe-area-inset-bottom));}",
    /* Telefonda suzuvchi \"So'rash\" tugmasi tab bar ustida turadi.
       2026-08-07: tab bar qo'shildi — tugma uning orqasida qolmasligi
       uchun pastki chegarasi ko'tarildi. */
    "body.ober-tabbar-joy .tez-sora{bottom:calc(72px + env(safe-area-inset-bottom));}",
    "body.ober-tabbar-joy .results{padding-bottom:calc(142px + env(safe-area-inset-bottom));}",
    ".ober-tabbar{",
    "  position:fixed;left:0;right:0;bottom:0;z-index:25;",
    "  background:rgba(255,255,255,.96);",
    "  -webkit-backdrop-filter:saturate(140%) blur(14px);",
    "  backdrop-filter:saturate(140%) blur(14px);",
    "  border-top:1px solid var(--line,#e3e8f0);",
    "  padding-bottom:env(safe-area-inset-bottom);",
    "}",
    ".ober-tabbar-inner{",
    "  max-width:560px;margin:0 auto;height:60px;",
    /* TO'RT USTUN — HAR BIRI BOSHQA MANZIL (2026-08-11).
       Markazdagi + E'lon bo'lim emas: u e'lon formasini bevosita
       ochadigan tezkor amal. "Sotish" olib tashlandi — u ham shu
       sahifaga borardi va kirmagan odam uchun aynan bir xil ekran
       chiqarardi. */
    "  display:grid;grid-template-columns:1fr 1fr 1.2fr 1fr;",
    "}",
    ".ober-tab[data-tab=\"bosh\"]{grid-column:1}",
    ".ober-tab[data-tab=\"kategoriyalar\"]{grid-column:2}",
    ".ober-tab[data-tab=\"elon\"]{grid-column:3}",
    ".ober-tab[data-tab=\"takliflar\"]{grid-column:4}",
    ".ober-tab{",
    "  display:flex;flex-direction:column;align-items:center;justify-content:center;",
    "  gap:2px;text-decoration:none;",
    "  color:var(--muted,#667085);",
    "  font-size:10.5px;font-weight:700;line-height:1.2;",
    "  -webkit-tap-highlight-color:transparent;touch-action:manipulation;",
    "  transition:color 160ms var(--ease,cubic-bezier(.2,0,0,1));",
    "}",
    ".ober-tab:active{transform:translateY(1px)}",
    ".ober-tab-ikon{",
    "  position:relative;width:40px;height:26px;border-radius:999px;",
    "  display:grid;place-items:center;",
    "  transition:background 160ms var(--ease,cubic-bezier(.2,0,0,1));",
    "}",
    ".ober-tab svg{width:22px;height:22px;display:block}",
    ".ober-tab.faol{color:var(--navy,#0b2559)}",
    ".ober-tab.faol .ober-tab-ikon{background:var(--navy-soft,#eaeff8)}",
    ".ober-tab-asosiy{transform:translateY(-8px);color:var(--navy,#0b2559)}",
    ".ober-tab-asosiy:active{transform:translateY(-7px)}",
    ".ober-tab-asosiy .ober-tab-ikon{",
    "  width:44px;height:44px;border:3px solid var(--surface,#fff);",
    "  background:var(--navy,#0b2559);color:#fff;",
    "  box-shadow:0 8px 20px rgba(11,37,89,.24);",
    "}",
    ".ober-tab-asosiy.faol .ober-tab-ikon{background:var(--navy-dark,#081b42);",
    "  box-shadow:0 0 0 4px var(--navy-soft,#eaeff8),0 8px 20px rgba(11,37,89,.24)}",
    /* O'QILMAGAN NISHON — Chat tabida. Faqat raqam bor bo'lsa
       ko'rinadi (hidden bilan yopiladi). */
    ".ober-tab-nishon{",
    "  position:absolute;top:-2px;right:-7px;",
    "  min-width:16px;height:16px;padding:0 4px;border-radius:999px;",
    "  background:var(--navy,#0b2559);color:#fff;",
    "  font-size:9.5px;font-weight:800;line-height:16px;text-align:center;",
    "  box-shadow:0 0 0 2px var(--surface,#fff);",
    "}",
    ".messages-link,.xabarlar-link{position:relative}",
    ".ober-top-nishon{",
    "  position:absolute;top:-7px;right:-8px;",
    "  min-width:18px;height:18px;padding:0 5px;border-radius:999px;",
    "  display:grid;place-items:center;background:var(--navy,#0b2559);color:#fff;",
    "  font-size:9.5px;font-weight:850;line-height:18px;",
    "  box-shadow:0 0 0 3px var(--surface,#fff);",
    "}",
    "@media (max-width:600px){",
    "  .ober-tabbar-inner{height:56px}",
    "  .ober-tab{font-size:10px}",
    /* Telefonda topbar ortiqcha takrorlanmasin: endi navigatsiya bitta
       joyda — pastki tab barda. 2026-08-07: "Chat" va "Profil"
       havolalari ham tepada, ham pastda chiqardi. Pastkisi qoladi,
       tepadagi ikki havola yashirinadi (logo va qidiruv qoladi). */
    "  .ober-tabbar-joy .messages-link,.ober-tabbar-joy .seller-link,",
    "  .ober-tabbar-joy .buyer-link,.ober-tabbar-joy .xabarlar-link{display:none!important}",
    "}",
    /* Tepadagi qo'shimcha havolalar FAQAT desktopda ko'rinadi.
       Telefonda ular pastki tab barda bor — ikki joyda takrorlash
       aynan 2026-08-07 da tuzatilgan xato edi. */
    ".ober-desktop-nav{display:none}",
    "@media (min-width:901px){",
    "  body.ober-tabbar-joy{padding-bottom:0}",
    "  body.ober-tabbar-joy .results{padding-bottom:34px}",
    /* Tab bar shu yerda yo'qoladi — havolalar aynan shu yerda paydo
       bo'ladi. Ikkalasi bitta chegara: navigatsiya hech qachon
       yo'qolmaydi. */
    "  .ober-tabbar{display:none}",
    "  .ober-desktop-nav{",
    "    display:inline-flex;align-items:center;min-height:38px;",
    "    padding:0 12px;border-radius:999px;",
    "    color:var(--navy,#0b2559);text-decoration:none;",
    "    font-size:12.5px;font-weight:760;white-space:nowrap;",
    "    transition:background 120ms ease;",
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
  }

  // REGRESSION HIMOYASI (2026-08-07): ➕ tugma bir marta yozilib, ikki
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
