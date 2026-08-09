/* OBER — PASTKI TAB NAVIGATSIYASI (2026-08-07)
 *
 * Zamonaviy bozor ilovalari (OLX, Uzum) kabi beshta tab pastda turadi:
 *   Bosh sahifa · Kategoriyalar · ➕ Yangi e'lon · Chat · Profil
 *
 * NEGA KERAK (2026-08-07, Aziz): "hozir ichma-ich bo'lib ketgan
 * sahifalar". Haqiqatan ham: sotuvchi kabinetida yorliqlar, xaridor
 * sahifasida havolalar, takliflar sahifasi alohida — navigatsiya bir
 * joyda emas edi. Endi bitta joyda, beshta tabda. Xaridor ham,
 * sotuvchi ham bir xil ko'radi: bosh sahifa (qidiruv), kategoriyalar
 * (bozor bo'limlari), yangi e'lon (asosiy harakat), takliflar
 * (xabarlar), profil (sotuvchi kabineti).
 *
 * NEGA 5 TA (2026-08-07, Aziz): to'rt tab 5 ustunli gridda 4-ustunni
 * bo'sh qoldirardi — "g'alati joylashuv" degan shikoyat aynan shundan
 * edi. Kategoriyalar qo'shildi: endi hamma ustun to'lgan, ➕ esa
 * markazda turishda davom etadi.
 *
 * NEGA SHU TARTIB: eng muhim harakat — e'lon joylash — markazda va
 * ko'tarilgan. Qolgan to'rttasi xaridor va sotuvchi uchun umumiy.
 *
 * Markazdagi ➕ `?yangi=1` bilan kabinetga boradi — sotuvchi.html
 * uni ko'rib e'lon formasini darhol ochadi.
 */
(function () {
  "use strict";
  if (document.querySelector(".ober-tabbar")) return;

  var tr = function (t) {
    return (window.OBER_I18N && window.OBER_I18N.t) ? window.OBER_I18N.t(t) : t;
  };
  var path = location.pathname;

  // QAYSI TAB FAQOL — URL dan. Elon sahifasida hech biri (u natijaning
  // davomi, tab emas).
  var faol = "";
  if (path === "/" || path === "/index.html") faol = "bosh";
  else if (path.indexOf("/kategoriyalar") === 0) faol = "kategoriyalar";
  else if (path.indexOf("/takliflar") === 0) faol = "takliflar";
  else if (path.indexOf("/sotuvchi") === 0)
    faol = location.search.indexOf("yangi") >= 0 ? "yangi" : "sotuvchi";
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
    /* 5 ustun: ➕ aynan markazda (50%) tursin. 2026-08-07 o'lchov:
       to'rtta tab 5 ustunli gridda 4-ustunni bo'sh qoldirardi.
       Endi beshta tab — har ustun to'la: Bosh (1) · Kategoriyalar (2)
       · ➕ (3) · Chat (4) · Sotuvchi (5). ➕ matematik jihatdan
       aynan o'rtada: 2.6fr / 5.2fr = 50%. */
    "  display:grid;grid-template-columns:1fr 1fr 1.2fr 1fr 1fr;",
    "}",
    ".ober-tab[data-tab=\"bosh\"]{grid-column:1}",
    ".ober-tab[data-tab=\"kategoriyalar\"]{grid-column:2}",
    ".ober-tab[data-tab=\"yangi\"]{grid-column:3}",
    ".ober-tab[data-tab=\"takliflar\"]{grid-column:4}",
    ".ober-tab[data-tab=\"sotuvchi\"]{grid-column:5}",
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
    /* MARKAZIY ➕ — sahifadagi asosiy harakat. Ko'tarilgan aylana,
       oq halqa bilan ajratilgan (bar bilan qo'shilib ketmasin). */
    ".ober-tab-asosiy .ober-plus{",
    "  width:46px;height:46px;margin-top:-18px;",
    "  border-radius:999px;",
    "  background:var(--navy,#0b2559);color:#fff;",
    "  border:3px solid var(--surface,#fff);",
    "  display:grid;place-items:center;",
    "  box-shadow:0 8px 20px rgba(11,37,89,.25);",
    "  transition:background 160ms var(--ease,cubic-bezier(.2,0,0,1)),",
    "              transform 160ms var(--ease,cubic-bezier(.2,0,0,1));",
    "}",
    ".ober-tab-asosiy .ober-plus svg{width:22px;height:22px}",
    ".ober-tab-asosiy:active .ober-plus{transform:scale(.96)}",
    ".ober-tab-asosiy.faol .ober-plus{",
    "  background:var(--navy-dark,#081b42);",
    "  box-shadow:0 0 0 4px var(--navy-soft,#eaeff8),0 8px 20px rgba(11,37,89,.25);",
    "}",
    "@media (max-width:600px){",
    "  .ober-tabbar-inner{height:56px}",
    "  .ober-tab{font-size:10px}",
    "  .ober-tab-asosiy .ober-plus{width:44px;height:44px;margin-top:-16px}",
    /* Telefonda topbar ortiqcha takrorlanmasin: endi navigatsiya bitta
       joyda — pastki tab barda. 2026-08-07: "Chat" va "Profil"
       havolalari ham tepada, ham pastda chiqardi. Pastkisi qoladi,
       tepadagi ikki havola yashirinadi (logo va qidiruv qoladi). */
    "  .ober-tabbar-joy .messages-link,.ober-tabbar-joy .seller-link,",
    "  .ober-tabbar-joy .buyer-link,.ober-tabbar-joy .xabarlar-link{display:none!important}",
    "}",
    "@media (min-width:901px){",
    "  body.ober-tabbar-joy{padding-bottom:0}",
    "  body.ober-tabbar-joy .results{padding-bottom:34px}",
    "  .ober-tabbar{display:none}",
    "}"
  ].join("\n");
  document.head.appendChild(st);

  var ikon = function (n) {
    var svg = {
      bosh: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 10.5 12 3l9 7.5"/><path d="M5.5 9.5V21h13V9.5"/></svg>',
      kategoriyalar: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="3.5" width="7" height="7" rx="1.6"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.6"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.6"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.6"/></svg>',
      takliflar: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.5 8.5 0 0 1-8.5 8.5 8.4 8.4 0 0 1-3.75-.86L3 21l1.9-5.7A8.5 8.5 0 1 1 21 11.5Z"/></svg>',
      plus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
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
      '<span class="ober-tab-ikon">' + ikon("bosh") + "</span>" + yozuv("Bosh sahifa") + "</a>" +
    '<a class="ober-tab' + (faol === "kategoriyalar" ? " faol" : "") + '" href="/kategoriyalar" data-tab="kategoriyalar"' +
      (faol === "kategoriyalar" ? ' aria-current="page"' : "") + ">" +
      '<span class="ober-tab-ikon">' + ikon("kategoriyalar") + "</span>" + yozuv("Kategoriyalar") + "</a>" +
    '<a class="ober-tab ober-tab-asosiy' + (faol === "yangi" ? " faol" : "") + '" href="/sotuvchi?yangi=1" data-tab="yangi"' +
      (faol === "yangi" ? ' aria-current="page"' : "") + ">" +
      '<span class="ober-plus">' + ikon("plus") + "</span>" + yozuv("Yangi e'lon") + "</a>" +
    '<a class="ober-tab' + (faol === "takliflar" ? " faol" : "") + '" href="/takliflar" data-tab="takliflar"' +
      (faol === "takliflar" ? ' aria-current="page"' : "") + ">" +
      '<span class="ober-tab-ikon">' + ikon("takliflar") + '<span class="ober-tab-nishon" hidden></span></span>' +
      yozuv("Chat") + "</a>" +
    '<a class="ober-tab' + (faol === "sotuvchi" ? " faol" : "") + '" href="/sotuvchi" data-tab="sotuvchi"' +
      (faol === "sotuvchi" ? ' aria-current="page"' : "") + ">" +
      '<span class="ober-tab-ikon">' + ikon("sotuvchi") + "</span>" + yozuv("Profil") + "</a>" +
    "</div>";
  document.body.appendChild(nav);
  document.body.classList.add("ober-tabbar-joy");

  // REGRESSION HIMOYASI (2026-08-07): ➕ tugma bir marta yozilib, ikki
  // marta tushib qolgan edi — 6 element 5 ustunli gridda ➕ ni ustma-ust
  // qo'ygan. Piksel tekshiruvi buni ko'rmaydi (ikkala ➕ ham markazda
  // chiqadi), element SONI esa ko'radi. Beshta bo'lishi shart.
  if (document.querySelectorAll(".ober-tab").length !== 5) {
    console.error("[ober-tabbar] tablar soni 5 emas!",
                  document.querySelectorAll(".ober-tab").length);
  }

  // O'QILMAGANLAR NISHONI — Chat tabida.
  // Aktor localStorage'dan: sotuvchi bo'lsa token, aks holda xaridor
  // so'rovi. Hech narsa yo'q bo'lsa — jim turamiz (nishon yo'q).
  // 30 soniyada bir marta — sahifa ochiq tursa ham yangilanadi.
  var nishon = nav.querySelector(".ober-tab-nishon");
  var topHavola = document.querySelector(".messages-link,.xabarlar-link");
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
    if (s) { actor = s; rol = "sotuvchi"; }
    else if (q) { actor = q; }
    if (!actor) { nishonniKorsat(0); return; }
    fetch("/api/bildirishnomalar?rol=" + rol + "&actor=" + encodeURIComponent(actor))
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        var n = Number((d && d.jami) || 0);
        nishonniKorsat(n);
      })
      .catch(function () {});
  }
  yangila();
  setInterval(yangila, 30000);
})();
