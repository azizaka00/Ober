/* OBER — KATEGORIYA IKONLARI (2026-08-16)
 *
 * Bitta umumiy manba: kategoriyalar sahifasi va bosh sahifadagi
 * kategoriya to'ri bir xil ikonlarni ko'rsatadi. Ilgari ikonlar
 * faqat kategoriyalar.html ichida edi — bosh sahifaga to'r
 * qo'shilganda ularni nusxalash o'rniga shu faylga chiqarildi.
 *
 * BIRTA OILA: 24x24, 1.8px stroke, feather uslubi. Emoji
 * ishlatilmaydi (2026-08-11 audit): emoji vizual tilni pasaytiradi.
 */
(function () {
  "use strict";
  window.OBER_KAT_IKONLAR = {
    transport: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 11 7.6 6.4A2 2 0 0 1 9.4 5.4h5.2a2 2 0 0 1 1.8 1L19 11"/><rect x="3" y="11" width="18" height="6.5" rx="2"/><circle cx="7.5" cy="17.5" r="1.7"/><circle cx="16.5" cy="17.5" r="1.7"/></svg>',
    nedvizhimost: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3 11 9-8 9 8"/><path d="M5 10.5V20a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-9.5"/><path d="M10 21v-6h4v6"/></svg>',
    elektronika: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="3.5" width="19" height="13" rx="2"/><path d="M8.5 21h7M12 16.5V21"/></svg>',
    "dom-i-sad": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 11V8.5A2.5 2.5 0 0 1 6.5 6h11A2.5 2.5 0 0 1 20 8.5V11"/><rect x="2.5" y="11" width="19" height="5.5" rx="2"/><path d="M6 16.5V20M18 16.5V20"/></svg>',
    "detskiy-mir": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.5 21 7.5v9l-9 5-9-5v-9Z"/><path d="M12 11.5 21 7.5M12 11.5 3 7.5M12 11.5v10"/></svg>',
    "moda-i-stil": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5.5 8.5 3H4.5v3L8 8.5V20.5h8V8.5L19.5 6V3h-4Z"/><path d="M8.5 3a3.5 3.5 0 0 0 7 0"/></svg>',
    uslugi: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="6" r="2.5"/><circle cx="6" cy="18" r="2.5"/><path d="M20 4 8.5 15.5M14.5 14.5 20 20M8.5 8.5 12 12"/></svg>',
    rabota: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="7" width="19" height="13.5" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2M2.5 13h19"/></svg>',
    zhivotnye: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="5" cy="9.5" r="2.4"/><circle cx="9" cy="4.8" r="2.4"/><circle cx="15" cy="4.8" r="2.4"/><circle cx="19" cy="9.5" r="2.4"/><path d="M12 10.5c2.4 0 4.9 2.1 4.9 5.1 0 1.6-1.3 2.9-2.9 2.9-1 0-1.8-.5-2-1.3-.2.8-1 1.3-2 1.3-1.6 0-2.9-1.3-2.9-2.9 0-3 2.5-5.1 4.9-5.1Z"/></svg>',
    "hobbi-otdyh-i-sport": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9.5"/><path d="M12 2.5v19M2.5 12h19M5 5.5c2.3 2.3 3.9 5.2 3.9 6.5s-1.6 4.2-3.9 6.5M19 5.5c-2.3 2.3-3.9 5.2-3.9 6.5s1.6 4.2 3.9 6.5"/></svg>',
    "otdam-darom": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="8" width="18" height="4" rx="1"/><path d="M5 12v9h14v-9M12 8v13"/><path d="M12 8s-4.5 0-4.5-2.5A2.5 2.5 0 0 1 12 8Zm0 0s4.5 0 4.5-2.5A2.5 2.5 0 0 0 12 8Z"/></svg>',
    "obmen-barter": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m17 3.5 3.5 3.5-3.5 3.5"/><path d="M20.5 7H8a4.5 4.5 0 0 0-4.5 4.5M7 20.5 3.5 17l3.5-3.5"/><path d="M3.5 17H16a4.5 4.5 0 0 0 4.5-4.5"/></svg>',
    boshqa: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/></svg>'
  };
})();
