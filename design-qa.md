# OBER ichki bildirishnomalar markazi — Design QA

## Source visual truth

- Mavjud tanlangan OBER chat dizayni: `D:\SUNIYAGENT\ober\audit\2026-08-01-offers-chat\implementation-mobile-final-pass.png`.
- Mavjud inbox dizayn tizimi: `D:\SUNIYAGENT\ober\audit\2026-08-01-offers-chat\implementation-mobile-inbox-final.png`.
- Source pixel/CSS o‘lchami: 390 × 844; device scale factor 1.
- Yangi markaz alohida vizual yo‘nalish emas, shu tasdiqlangan OBER navy/ivory mobil tizimining kengaytmasi.

## Rendered implementation

- URL: `http://127.0.0.1:8800/takliflar?sorov=38`.
- Yangi unread inbox: `D:\SUNIYAGENT\ober\audit\2026-08-01-notifications\mobile-inbox-unread-final.png`.
- Bildirishnomalar markazi: `D:\SUNIYAGENT\ober\audit\2026-08-01-notifications\mobile-notification-center-final.png`.
- Bildirishnomadan ochilgan chat: `D:\SUNIYAGENT\ober\audit\2026-08-01-notifications\mobile-chat-from-notification.png`.
- Implementation pixel/CSS o‘lchami: 390 × 844; device scale factor 1.
- Tekshirilgan holatlar: 3 unread inbox, panel open, kerakli chat open, 2 unread qolishi, barcha bildirishnomani o‘qish, sotuvchi uchun 1 unread.

## Full-view comparison evidence

- Source chat, yangi inbox va ochiq notification sheet bir comparison input’da ko‘rildi.
- Header, logo, navy/ivory ranglar, yumaloq radiuslar, border/soya og‘irligi va matn ierarxiyasi mavjud takliflar/chat dizaynidan uzilmagan.
- Sheet orqa fonni xiralashtiradi, lekin badge va taklif konteksti sezilib turadi; asosiy unread ma’lumotlar bir ekranga sig‘adi.

## Focused comparison evidence

- Header focus: yopiq holatda faqat ixcham sonli badge ko‘rinadi; 390 px kenglikda sarlavha va logo siqilmaydi.
- Panel focus: sarlavha, `Barchasini o‘qish`, push holati va uchta real notification item 844 px balandlikda composer yoki browser chrome’siz to‘liq ko‘rinadi.
- Chat focus: notification item bosilganda GM Parts chat’i ochildi, badge 3 dan 2 ga tushdi va persistent composer saqlandi.

## Findings

- P0/P1/P2 darajasidagi ochiq vizual yoki asosiy notification-center funksional muammo qolmadi.
- Fonts and typography: Inter/system stack, navy 800–900 weight sarlavhalar va 10–13 px meta matnlar mavjud OBER ierarxiyasiga mos; truncation faqat uzun preview’da ishlaydi.
- Spacing and layout rhythm: 18–20 px yon masofa, 10–13 px item gaplari, 16–28 px radiuslar va pastki sheet kompozitsiyasi mavjud chat ritmini davom ettiradi; 390×844 da horizontal overflow yo‘q.
- Colors and tokens: `--navy`, `--ivory`, `--blue`, `--line`, `--green`, `--red` tokenlari qayta ishlatilgan; push blocked holati past kontrastli qizil bilan xavfsiz ko‘rsatilgan.
- Image quality and assets: original OBER logo/icon va mavjud real kolodka rasmi ishlatilgan; placeholder, emoji, inline SVG yoki CSS asset yo‘q.
- Copy and content: `Bildirishnomalar`, `Barchasini o‘qish`, `Xaridordan yangi xabar`, blocked permission yo‘riqnomasi va empty state sodda o‘zbekcha.
- Accessibility: dialog `hidden + inert + aria-hidden` bilan yopiq holatda interaktiv emas; open/close, Escape, `aria-expanded`, live region va touch-friendly tugmalar bor.
- Browser-push holati: service worker’da `message`, `push` va `notificationclick` handlerlari bor. Lokal in-app brauzer Notification API’ni bermagani uchun UI `Bloklangan` holatini va brauzer sozlamasi yo‘riqnomasini ko‘rsatdi. Haqiqiy yopiq-brauzer push yetkazish production HTTPS + VAPID sender bosqichida ulanadi.

## Comparison history

- Pass 1 P1: `Barchasini o‘qish` frontend’da mavjud `role` o‘rniga aniqlanmagan `rol` qiymatini yuborardi; tugma xato toast ko‘rsatardi.
- Fix: request body `rol: role` qilindi, JSON/API xatosi aniq tekshirildi va muvaffaqiyatda panel optimistik bo‘sh holatga o‘tdi.
- Post-fix evidence: badge bo‘sh, notification item 0, `Hammasi joyida` empty state va `Hammasi o‘qildi` status ko‘rindi.
- Pass 1 P2: yopiq panel opacity bilan yashirilsa ham accessibility tree’da qolardi.
- Fix: yopiq holatga `hidden`, `inert`, `aria-hidden=true`; ochiq holatga teskari atributlar qo‘shildi.
- Post-fix evidence: DOM holatida `panelHidden: true`, vizual inbox’da panel yo‘q; ochilganda `panelHidden: false`, `panelOpen: true`.

## Primary interactions tested

- Xaridor 3 ta unread badge va uchta notification item’ni ko‘rdi.
- GM Parts notification item’i aynan GM Parts chat’ini ochdi; badge 3 → 2 bo‘ldi.
- `Barchasini o‘qish` real POST API orqali barcha qolgan unread’ni tozaladi.
- Sotuvchi rolida xaridorning `Bugun olib ketamanmi?` xabari 1 unread notification sifatida ko‘rindi.
- Chat ochilishi mavjud read-state’ni o‘zgartirdi; markaz xabar jadvalini yagona haqiqat manbasi sifatida ishlatadi.
- Service worker `/sw.js` endpointi 200 qaytardi; permission mavjud bo‘lmagan brauzer uchun fallback holati ishladi.
- Brauzer console error/warning: 0.
- Avtomatik testlar: lug‘at 21/21, relevans 13/13, halqa 26/26, yig‘ish 12/12, suhbat+notification 22/22 — jami 94/94.

## Follow-up polish

- P3: production HTTPS domenida VAPID kalitlari va push subscription saqlash/sender qatlamini ulash.
- P3: notification permission berilgan Chrome/Safari/Android qurilmada yopiq-tab delivery qabul sinovi.

final result: passed
