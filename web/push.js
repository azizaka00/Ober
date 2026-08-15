/* OBER — push bildirishnomasiga obuna bo'lish (2026-08-14).
 *
 * Sahifa yuklanganda AVTOMATIK ruxsat SO'RALMAYDI. Sabab: brauzer
 * darhol chiqadigan "ruxsat berasizmi?" oynasini odam o'ylamasdan
 * rad etadi va Chrome uni BIR YILGA bloklaydi — keyin qayta so'rab
 * bo'lmaydi. Bir marta noto'g'ri so'rash kanalni butunlay yopadi.
 *
 * Shuning uchun: `OBER_PUSH.sora()` faqat foydalanuvchi ongli
 * harakat qilganda chaqiriladi (masalan chatga kirganda yoki
 * "Bildirishnomani yoqish" tugmasini bosganda).
 */
(function () {
  "use strict";

  const QOLLAB = ("serviceWorker" in navigator)
    && ("PushManager" in window)
    && ("Notification" in window);

  function b64ToBayt(b64) {
    // VAPID kaliti base64url, to'ldiruvchisiz keladi.
    const tekis = (b64 + "=".repeat((4 - b64.length % 4) % 4))
      .replace(/-/g, "+").replace(/_/g, "/");
    const xom = atob(tekis);
    const bayt = new Uint8Array(xom.length);
    for (let i = 0; i < xom.length; i++) bayt[i] = xom.charCodeAt(i);
    return bayt;
  }

  async function ishchi() {
    const reg = await navigator.serviceWorker.getRegistration();
    return reg || navigator.serviceWorker.register("/sw.js");
  }

  /* Obunani serverga yozadi. `token` — sessiya tokeni; server
     undan ID ni O'ZI aniqlaydi. ID mijozdan olinmaydi (birov
     boshqaning bildirishnomasini o'ziga burib yubormasin). */
  async function serverga(obuna, rol, token) {
    const j = obuna.toJSON();
    const r = await fetch("/api/push-obuna", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        endpoint: j.endpoint,
        p256dh: (j.keys || {}).p256dh || "",
        auth: (j.keys || {}).auth || "",
        rol: rol,
        token: token,
      }),
    });
    return r.ok;
  }

  /* Ruxsat allaqachon berilgan bo'lsa — jimgina qayta obuna
     bo'ladi. Bu kerak: obuna muddati tugashi yoki brauzer uni
     tozalashi mumkin, o'shanda foydalanuvchi hech narsa
     sezmasligi kerak. */
  async function tikla(rol, token) {
    if (!QOLLAB || Notification.permission !== "granted") return false;
    return ulan(rol, token);
  }

  async function ulan(rol, token) {
    try {
      const kalitJavob = await fetch("/api/push-kalit");
      if (!kalitJavob.ok) return false;
      const {kalit} = await kalitJavob.json();
      if (!kalit) return false;

      const reg = await ishchi();
      let obuna = await reg.pushManager.getSubscription();

      /* Kalit o'zgargan bo'lsa eski obuna ishlamaydi — uni
         bekor qilib qaytadan yozilamiz. Busiz foydalanuvchi
         "obuna bor" deb o'ylab, hech narsa olmasdi. */
      if (obuna) {
        const eski = new Uint8Array(obuna.options.applicationServerKey || []);
        const yangi = b64ToBayt(kalit);
        let mos = eski.length === yangi.length;
        for (let i = 0; mos && i < eski.length; i++) {
          if (eski[i] !== yangi[i]) mos = false;
        }
        if (!mos) { await obuna.unsubscribe(); obuna = null; }
      }

      if (!obuna) {
        obuna = await reg.pushManager.subscribe({
          userVisibleOnly: true,          // majburiy: jim push taqiqlangan
          applicationServerKey: b64ToBayt(kalit),
        });
      }
      return serverga(obuna, rol, token);
    } catch (e) {
      console.warn("[ober] push obunasi:", e);
      return false;
    }
  }

  /* Foydalanuvchi harakatidan keyin chaqiriladi. Qaytaradi:
     "yoqildi" | "rad" | "qollamaydi" | "xato" */
  async function sora(rol, token) {
    if (!QOLLAB) return "qollamaydi";
    if (Notification.permission === "denied") return "rad";
    if (Notification.permission !== "granted") {
      const javob = await Notification.requestPermission();
      if (javob !== "granted") return "rad";
    }
    return (await ulan(rol, token)) ? "yoqildi" : "xato";
  }

  window.OBER_PUSH = {qollab: QOLLAB, sora: sora, tikla: tikla};
})();
