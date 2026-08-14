# OBER — Play Store uchun TWA qurish yo'riqnomasi

Sana: 2026-08-14 · Holat: **PWA tayyor, TWA qurish qoldi**

TWA (Trusted Web Activity) — PWA'ni Android ilovasiga o'rash usuli. Brauzer
frame'isiz, to'liq ekranli ilova sifatida ochiladi, Play Store orqali
tarqatiladi. Google'ning rasmiy vositasi — **Bubblewrap CLI**.

---

## 0. Tayyorgarlik tekshiruvi (allaqachon bajarilgan)

| Talab | Holat |
|---|---|
| HTTPS (ober.uz) | ✅ 200 |
| Service Worker | ✅ `/sw.js` 200, offline ishlaydi |
| Manifest | ✅ `display: standalone`, `start_url: /`, `scope: /` |
| Ikon 512 (any + maskable) | ✅ `icon-512.png` |
| Theme/bg color | ✅ `#0a2b63` (navy) |
| Privacy policy | ✅ `https://ober.uz/privacy` |

---

## 1. Talab qilinadigan vositalar

| Vosita | Nima uchun | Qayerdan |
|---|---|---|
| **Node.js 18+** | Bubblewrap CLI'ni ishga tushiradi | https://nodejs.org |
| **Java JDK 17** | Android qurilish | Bubblewrap o'zi yuklab oladi (tavsiya) |
| **Android SDK** | AAB qurilish | Bubblewrap o'zi yuklab oladi (tavsiya) |
| **Bubblewrap CLI** | TWA loyihasi + qurish | `npm i -g @bubblewrap/cli` |

> **Muhim:** Bubblewrap birinchi ishga tushganda JDK va Android SDK'ni
> o'zi yuklab olishni so'raydi — **ruxsat bering**. Noto'g'ri versiya
> qurilishni buzadi.

---

## 2. Bubblewrap o'rnatish

```bash
# Windows: Node.js o'rnatilgan bo'lsa
npm install -g @bubblewrap/cli

# Tekshirish
bubblewrap --version
```

---

## 3. Loyihani yaratish

```bash
mkdir twa-ober && cd twa-ober

bubblewrap init --manifest=https://ober.uz/manifest.json
```

Wizard savollariga javoblar (OBER uchun tavsiya):

| Savol | Javob |
|---|---|
| App nomi | `OBER — bir qidiruv, butun bozor` |
| Paket nomi | `uz.ober.app` |
| App versiyasi | `1.0.0` |
| Version code | `1` |
| Display | `standalone` (manifestdan oladi) |
| Orientation | `portrait` |
| Theme color | `#0a2b63` |
| Background color | `#0a2b63` |
| Start URL | `/` |
| Scope | `/` |
| Ikon | 512 PNG (avtomatik o'lchamlanadi) |
| Signing key | Yangi yaratish (default) |

**Signing key (muhim!):**
- Bubblewrap `key.jks` faylini yaratadi
- **Parolni xavfsiz joyda saqlang** — yo'qolsa, ilovani yangilab bo'lmaydi
- Key faylini git'ga **yubormang** (`.gitignore` ga qo'shing)

---

## 4. APK / AAB qurish

```bash
bubblewrap build
```

Natija (loyiha papkasida):

| Fayl | Nima |
|---|---|
| `app-release-bundle.aab` | **Play Store'ga yuklanadigan** fayl |
| `app-release-signed.apk` | Telefonga to'g'ridan-to'g'ri o'rnatish uchun |

**Tez sinov** (telefon USB orqali ulangan bo'lsa):
```bash
bubblewrap install
```

---

## 5. Play Console'ga yuklash

1. **Play Console** → [play.google.com/console](https://play.google.com/console)
   — developer akkaunt kerak (bir martalik $25)
2. **Create app**:
   - Nom: `OBER — bir qidiruv, butun bozor`
   - Til: o'zbekcha
   - Turi: App (o'yin emas)
   - Narx: Bepul
3. **Setup → App content**: privacy policy URL'ga `https://ober.uz/privacy`
   qo'ying
4. **Setup → App signing**: Play App Signing — **yoqish** (tavsiya)
5. **Testing → Internal testing**:
   - Testers ro'yxati (o'zingizning email)
   - `app-release-bundle.aab` yuklash
   - Release yaratish → rollout

---

## 6. Digital Asset Links — to'liq ekran rejimi uchun (SHART)

TWA to'liq ekran (brauzer panelisiz) ishlashi uchun sayt va ilova
o'rtasida egalik aloqasi kerak. Bu `.well-known/assetlinks.json` fayli
orqali o'rnatiladi.

### 6.1. SHA-256 izini olish

**Play App Signing yoqilgan bo'lsa** (tavsiya):
- Play Console → Releases → Setup → **App integrity**
- *App signing key certificate* → **SHA-256 certificate fingerprint** ni
  nusxalash

**Play App Signing o'chirilgan bo'lsa:**
```bash
keytool -list -v -keystore key.jks -alias twa -storepass <parol>
```
`SHA256:` qatoridagi qiymat kerak (ikki nuqtasiz, katta harf bilan).

### 6.2. assetlinks.json yaratish

```json
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "uz.ober.app",
      "sha256_cert_fingerprints": ["<SHA-256 IZI>"]
    }
  }
]
```

### 6.3. Serverga joylash

Faylni `web/.well-known/assetlinks.json` ga qo'ying (server.py allaqachon
`/manifest.json` kabi servis qiladi — `.well-known` uchun ham marshrut
qo'shiladi).

**Tekshiruv:**
```bash
curl https://ober.uz/.well-known/assetlinks.json
# → 200, JSON to'g'ri
```

### 6.4. To'liq ekran tekshiruvi

Ilovani qayta o'rnatib, to'liq ekranda ochilishini tekshiring. Agar
assetlinks noto'g'ri bo'lsa, ilova brauzer paneli bilan (TWA emas)
ochiladi — lekin ishlashda davom etadi.

---

## 7. Play Store talablari (2026)

- **Target API 36 (Android 16)** — 2026-08-31 gacha yangilash shart.
  Bubblewrap'ning yangi versiyasi buni o'zi hal qiladi; qurilishda
  xato bersa, SDK'ni yangilang.
- **Content rating** — Play Console'da so'rovnomani to'ldirish (5 daqiqa)
- **Data safety** — yig'iladigan ma'lumotlar: telefon raqami, e'lon
  matnlari, chat xabarlari, rasmlar
- **Tavsif va ekran rasmlar** — `DOKON-MATERIALLARI.md` dan tayyor

---

## 8. Xato holatlari

| Xato | Yechim |
|---|---|
| `SDK not found` | Bubblewrap'ga o'zi yuklab olishga ruxsat bering |
| `targetSdkVersion too low` | Bubblewrap yangilang, SDK 36 kerak |
| `assetlinks 404` | `.well-known/assetlinks.json` joylanmagan yoki noto'g'ri yo'l |
| Ilova brauzer paneli bilan ochiladi | SHA-256 noto'g'ri yoki Play App Signing izi olingan |
| `key.jks` yo'qoldi | Ilovani yangilab bo'lmaydi — yangi ilova yaratish kerak |

---

## 9. Xulosa — qadamlar ro'yxati

- [ ] Node.js + Bubblewrap o'rnatish
- [ ] `bubblewrap init --manifest=https://ober.uz/manifest.json`
- [ ] Wizard: `uz.ober.app`, key yaratish, parolni saqlash
- [ ] `bubblewrap build` → `app-release-bundle.aab`
- [ ] Play Console: developer akkaunt ($25), app yaratish
- [ ] Privacy policy URL: `https://ober.uz/privacy`
- [ ] AAB yuklash → Internal testing
- [ ] SHA-256 izini olish → `assetlinks.json` → serverga joylash
- [ ] To'liq ekran tekshiruvi
- [ ] Production release (beta → stable)

**Eslatma:** App Store uchun bu yo'l ishlamaydi — Apple PWA'ni qabul
qilmaydi, Capacitor + macOS + Xcode kerak. Alohida bosqich.
