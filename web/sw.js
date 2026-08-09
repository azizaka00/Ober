const CACHE_VERSION = "ober-notify-v1";

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", event => event.waitUntil(self.clients.claim()));

function bildirish(payload = {}) {
  const title = payload.title || "OBER’da yangi xabar";
  return self.registration.showNotification(title, {
    body: payload.body || "Yangi taklif yoki xabar keldi.",
    icon: "/brend/icon.png",
    badge: "/brend/icon.png",
    tag: `ober-chat-${payload.chatId || "new"}`,
    renotify: true,
    data: {url: payload.url || "/takliflar"},
  });
}

self.addEventListener("message", event => {
  if (event.data?.type === "OBER_NOTIFICATION") {
    event.waitUntil(bildirish(event.data.payload));
  }
});

// Keyingi HTTPS/VAPID bosqichi uchun tayyor qabul nuqtasi. Hozirgi lokal
// prototip notification’ni sahifadagi real-time polling orqali yuboradi.
self.addEventListener("push", event => {
  let payload = {};
  try { payload = event.data?.json() || {}; } catch (_) {
    payload = {body: event.data?.text() || "Yangi xabar keldi."};
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
