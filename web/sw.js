/* OBER — Service Worker (2026-08-14).
 *
 * IKKI VAZIFA:
 *   1. OFFLINE KESH — PWA talabi. Bosh sahifa, kategoriyalar va asosiy
 *      statik fayllar (CSS/JS/ikon) keshlanadi. Tarmoq bo'lmasa ham
 *      ilova ochiladi — "app hissi" shundan keladi.
 *   2. BILDIRISHNOMA — chat xabarlari uchun push/tab xabarlari.
 *
 * Keshlash strategiyasi: stale-while-revalidate — birinchi ochilishda
 * tarmoqdan, keyin keshdan (fonda yangilanadi). Sahifalar API chaqirib
 * jonli ma'lumot oladi, shuning uchun sahifa HTML'ni uzoq keshlash
 * xavfli emas — faqat ochilish uchun zaxira.
 */

/* KESH NOMI VERSIYALI BO'LISHI SHART (2026-08-15).

   Ilgari bu `"ober-v1"` edi va HECH QACHON o'zgarmasdi. Natijasi:

     `activate` hodisasida biz nomi CACHE ga teng bo'lmagan keshlarni
     o'chiramiz. Nom hech qachon o'zgarmagani uchun o'chiriladigan
     narsa ham bo'lmagan — eski kesh abadiy yashardi.

   Buning ustiga statik fayllar `stale-while-revalidate` bilan
   berilardi: avval KESHDAN, yangisi esa fon rejimida. Ya'ni deploy
   qilingandan keyin foydalanuvchi ESKI kodni ko'rardi va yangisi
   faqat KEYINGI ochilishda kelardi.

   Aziz bugun aynan shuni ko'rdi: sayt serverda yangilangan, ekranda
   esa eski. Men "deploy o'tmadi" deb o'ylab, uch marta qayta
   yubordim — aslida server to'g'ri, kesh eski edi.

   Endi ikki o'zgarish:
     1. Nom versiyali — o'zgarganda eski kesh o'chadi;
     2. O'z JS/CSS'imiz TARMOQDAN birinchi olinadi (pastda).
   Versiyani deploy oldidan qo'lda oshirish SHART EMAS: nom ichida
   sana bor, uni o'zgartirish odat bo'lib qolsin. */
const CACHE = "ober-2026-08-16k";

/* Ofine ochilishi kerak bo'lgan sahifalar va statik manbalar.
 * Dinamik sahifalar (elon/{id}, qidiruv natijalari) keshlanmaydi —
 * ular API'dan jonli ma'lumot oladi va kesh ularni eskirgan ko'rsatadi. */
const KESH_MANZIL = [
  "/",
  "/kategoriyalar",
  "/takliflar",
  "/sotuvchi",
  "/privacy",
  "/brend/icon.png",
  "/brend/icon-192.png",
  "/brend/icon-512.png",
  "/ober-ui.css",
  "/tabbar.js",
  "/i18n.js",
  "/kat-ikonlar.js",
  "/manifest.json",
];

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const kesh = await caches.open(CACHE);
    // Hammasi bajarilmasa ham o'rnatish to'xtamasin — biri 404 bersa
    // qolgani ham yiqilmasin.
    await Promise.allSettled(KESH_MANZIL.map((m) => kesh.add(m)));
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const nomlar = await caches.keys();
    await Promise.all(nomlar
      .filter((n) => n !== CACHE)
      .map((n) => caches.delete(n)));
    await self.clients.claim();
  })());
});

/* Navigatsiya (sahifa ochish): tarmoqdan, bo'lmasa keshdan.
 * Statik fayl: keshdan tez, fonda yangilanadi (stale-while-revalidate). */
self.addEventListener("fetch", (event) => {
  const soz = event.request;
  if (soz.method !== "GET") return;

  const url = new URL(soz.url);
  if (url.origin !== location.origin) return;

  // Faqat GET navigatsiya va o'z statik fayllarimizni keshlaymiz.
  // /api/ chaqiriqlari jonli bo'lishi kerak — ularni keshlash eski
  // ma'lumot ko'rsatardi.
  if (url.pathname.startsWith("/api/")) return;
  if (url.pathname.startsWith("/chat-uploads/")) return;

  event.respondWith((async () => {
    const kesh = await caches.open(CACHE);

    // Navigatsiya so'rovlari — tarmoq birinchi, kesh zaxira.
    if (soz.mode === "navigate") {
      try {
        const jonli = await fetch(soz);
        // Faqat muvaffaqiyatli sahifani keshlaymiz (404 ni emas).
        if (jonli.ok) kesh.put(soz, jonli.clone());
        return jonli;
      } catch (_) {
        const zaxira = await kesh.match(soz);
        if (zaxira) return zaxira;
        const bosh = await kesh.match("/");
        if (bosh) return bosh;
        throw new Error("Oflayn — hech qanday zaxira yo'q");
      }
    }

    /* O'Z KODIMIZ — TARMOQDAN BIRINCHI (2026-08-15).

       Ilgari bu yerda `stale-while-revalidate` edi: avval keshdan,
       yangisi fonda. Rasm va shrift uchun bu to'g'ri — ular
       o'zgarmaydi. Lekin `ober-ui.css`, `tabbar.js`, `push.js`,
       `i18n.js` HAR DEPLOYDA o'zgaradi va o'sha eski nusxa
       foydalanuvchida qolib ketardi.

       Bu fayllarda endi ETag bor, ya'ni o'zgarmagan bo'lsa server
       304 qaytaradi — tana yo'q, trafik deyarli nol. Shuning uchun
       tarmoqdan so'rash arzon, kesh esa faqat ZAXIRA bo'lib qoladi
       (tarmoq yo'q bo'lsa ishlaydi). */
    const ozKodimiz = /\.(css|js)$/.test(url.pathname);
    if (ozKodimiz) {
      try {
        const jonli = await fetch(soz);
        if (jonli.ok) kesh.put(soz, jonli.clone());
        return jonli;
      } catch (_) {
        const zaxira = await kesh.match(soz);
        if (zaxira) return zaxira;
        throw new Error("Oflayn — kesh ham yo'q");
      }
    }

    // Rasm, shrift, ikonka — kesh birinchi, fonda yangilash.
    // Bular o'zgarmaydi (o'zgarsa nomi ham o'zgaradi).
    const eski = await kesh.match(soz);
    const yangilash = fetch(soz).then((javob) => {
      if (javob.ok) kesh.put(soz, javob.clone());
      return javob;
    }).catch(() => eski);
    return eski || yangilash;
  })());
});

/* ── BILDIRISHNOMA (eskidan saqlanadi) ─────────────────────────────── */

function bildirish(payload = {}) {
  const title = payload.title || "OBER — yangi xabar";
  return self.registration.showNotification(title, {
    body: payload.body || "Chatda yangi xabar bor.",
    icon: "/brend/icon-192.png",
    badge: "/brend/icon-192.png",
    /* `tag` + `renotify`: bir suhbatning xabarlari bir-birining
       ustiga tushadi (ro'yxat to'lib ketmasin), lekin HAR SAFAR
       qayta ogohlantiradi — aks holda ikkinchi xabar jimgina
       kelardi. */
    tag: `ober-chat-${payload.chatId || "new"}`,
    renotify: true,
    /* Tebranish — Aziz aynan shuni so'radi ("jingirlab tursin").
       Telefon jimlik rejimida bo'lsa ham seziladi. Naqsh
       Telegramnikiga yaqin: qisqa-pauza-qisqa. */
    vibrate: [200, 100, 200],
    data: {url: payload.url || "/takliflar"},
  });
}

self.addEventListener("message", event => {
  if (event.data?.type === "OBER_NOTIFICATION") {
    event.waitUntil(bildirish(event.data.payload));
  }
});

/* PUSH — server bo'sh xabar yuboradi (2026-08-14).
 *
 * `event.data` odatda NULL bo'ladi va bu ataylab: payloadni
 * shifrlash ECDH + AES-GCM talab qiladi, ular Python standart
 * kutubxonasida yo'q (sabab `app/push.py` izohida). Bo'sh push
 * service worker'ni uyg'otadi, xolos.
 *
 * Yon foyda: xabar matni Google serveridan umuman o'tmaydi.
 *
 * SHART: `push` hodisasida ALBATTA bildirishnoma ko'rsatilishi
 * kerak (`userVisibleOnly`). Ko'rsatilmasa brauzer obunani
 * bekor qiladi — "jim push" ruxsat etilmaydi. Shuning uchun
 * bu yerda hech qanday shart yo'q: har doim ko'rsatamiz.
 */
self.addEventListener("push", event => {
  let payload = {};
  if (event.data) {
    try { payload = event.data.json() || {}; } catch (_) {
      payload = {body: event.data.text() || ""};
    }
  }
  event.waitUntil(bildirish(payload));
});

self.addEventListener("notificationclick", event => {
  event.notification.close();
  const target = event.notification.data?.url || "/takliflar";
  event.waitUntil((async () => {
    const windows = await self.clients.matchAll({type: "window", includeUncontrolled: true});
    for (const client of windows) {
      if ("navigate" in client) await client.navigate(target);
      return client.focus();
    }
    return self.clients.openWindow(target);
  })());
});
