# OBER — Play Console yo'riqnomasi (bosingma-bosing, 2026-08-14)

> Bu yo'riqnoma `TWA-YORIQNOMA.md` ning amaliy davomi — Play Console'da
> app yaratishdan to'liq ekran rejimigacha, ekranga bosiladigan har
> tugma bilan.

---

## 0. YUKLASHDAN OLDIN — 3 ta narsani tekshiring

| Narsa | Holat | Agar yo'q bo'lsa |
|---|---|---|
| `twa-ober/app-release-bundle.aab` | ✅ bor | `TWA-QUR.bat` ni ishga tushiring |
| `twa-ober/android.keystore` + parol | ⚠️ parol `twa-ober/parol.txt` da | Avval parolni saqlang — **kalitsiz ilova yangilanmaydi** |
| `https://ober.uz/privacy` | ✅ ishlayapti | `web/privacy.html` yuklanganmi tekshiring |

### 0.1. ⚠️ PUSH UCHUN QAYTA QURISH (2026-08-14 da topildi)

`twa-ober/twa-manifest.json` da hali:

```json
"enableNotifications": false
```

Web Push qo'shilgan — ilovada bildirishnoma to'g'ri ishlashi uchun
(Chrome emas, OBER nomi bilan, ilova yopiq bo'lsa ham) buni yoqish kerak:

1. `twa-ober/twa-manifest.json` ni oching va:
   - `"enableNotifications": false` → `true`
   - `"features": {}` → `"features": {"notifications_delegation": {"enabled": true}}`
2. `TWA-QUR.bat` ni ishga tushiring (parol so'rasa, `parol.txt` dagini)
3. Yangi `app-release-bundle.aab` yasaladi — **shuni** yuklaysiz

> Buni yuklashdan oldin qiling: versiya kodi `2` bir martagina o'zgaradi.
> Avval yuklab, keyin qayta qursangiz, versiya kodini `3` ga oshirish
> kerak bo'ladi (Play qayta yuklashda kod oshishini talab qiladi).

---

## 1. Developer akkaunt (birinchi marta)

1. **play.google.com/console** → "Go to Play Console" → kirish (Google akkaunt)
2. **"Create account" / "Ro'yxatdan o'tish"** → $25 (bir martalik)
3. Developer nomi: **NAIZA MChJ** (STIR 313204884 — rekvizit tayyor)
4. Aloqa ma'lumotlari: email + telefon (moderatorlar shu orqali bog'lanadi)
5. Ro'yxatdan o'tish 48 soatgacha davom etishi mumkin — kuting

> Eslatma: Play Console interfeysi o'zbekcha emas (EN/RU bor). Quyidagi
> nomlar inglizcha menyu bo'yicha.

---

## 2. App yaratish (Create app)

1. **"Create app"** tugmasi (yuqori o'ng)
2. Formani to'ldiring:
   - **App name:** `OBER — bir qidiruv, butun bozor`
   - **Default language:** Uzbek
   - **App or game:** App
   - **Free or paid:** Free
3. Pastdagi **deklaratsiyalar** kataklarini belgilang (ikki xil: "content
   guidelines", "US export laws")
4. **"Create app"** tugmasi

---

## 3. App content (Setup → App content) — 6 bo'lim

Chap menyuda **Setup → App content** oching. Har bo'lim alohida forma:

| Bo'lim | Javob |
|---|---|
| **Privacy policy** | "Start" → URL: `https://ober.uz/privacy` |
| **Ads** | "No" — OBER'da reklama yo'q |
| **App access** | "All functionality is available without special access" (yoki to'g'ri javobni tanlang — akkaunt talab qilinadi) |
| **Data safety** | Forma: telefon raqami (ro'yxatdan o'tish), chat xabarlari, e'lon matnlari, rasmlar. To'lov ma'lumotlari — **yo'q** |
| **Target audience** | Yoshi 13+, "no" o'yin |
| **News apps / Government apps** | Ikkalasi ham "No" |

> Data safety'da **to'g'ri** javob bering — "ma'lumot yig'maymiz" deyish
> noto'g'ri (telefon raqami yig'iladi). Yolg'on ko'rsatish — ilovani
> olib tashlash sababi.

---

## 4. AAB yuklash (Internal testing)

**Avval sinov track'ida** — production'ga to'g'ridan-to'g'ri chiqmang.

1. Chap menyu: **Testing → Internal testing**
2. **"Create release"** tugmasi
3. **"Upload"** → `app-release-bundle.aab` ni tanlang (0-qadamdagi yangisi!)
4. **Release notes:** `Birinchi versiya — 450 000+ e'lon, rasm bilan qidirish, teskari bozor`
5. **"Save"** → **"Review release"** → **"Start rollout to Internal testing"**
6. Endi **Testers** bo'limi: "Create email list" → o'zingizning (va
   Azizning) email'ini qo'shing → "Save changes"
7. Sahifada **opt-in link** paydo bo'ladi (ko'rish uchun "How testers
   join" ni oching) — telefon bilan ochiladi

> Yuklash 10-30 daqiqada tekshiriladi. Xato bo'lsa, "Releases" bo'limida
> sabab ko'rsatiladi (masalan: target API past, tavsif yo'q).

---

## 5. SHA-256 izini olish — ENG MUHIM QADAM

Bu iz sayt va ilova o'rtasidagi **egalik aloqasi** uchun kerak
(`assetlinks.json`). **Noto'g'ri iz → ilova brauzer paneli bilan ochiladi.**

1. Chap menyu: **Setup → App signing**
2. **"App signing key certificate"** bo'limi
3. **"SHA-256 certificate fingerprint"** ni nusxalang
   (masalan: `14:6D:E9:83:C5:73:06:50:D8:EE:B9:95:2F:34:FC:64:...`)
4. **Bu izni saqlang** — keyingi qadamda kerak

> ⚠️ **App signing key** izini oling, **Upload key** izini emas!
> Google ilovani App signing key bilan qayta imzolaydi — sayt aloqasi
> shu kalit orqali tekshiriladi.

---

## 6. assetlinks.json — serverga qo'yish va tekshirish

### 6.1. Faylni tayyorlash

`web/.well-known/assetlinks.json` (loyihada papka bor):

```json
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "uz.ober.app",
      "sha256_cert_fingerprints": ["<5-qadamdagi IZ>"]
    }
  }
]
```

- IZ ikki nuqtali, katta harf bilan (Play'da qanday ko'rsatilsa, o'shanda)
- **Probel bo'lmasin**

### 6.2. Serverga joylash va tekshirish

```bash
curl https://ober.uz/.well-known/assetlinks.json
```

- Javob: `200` + yuqoridagi JSON
- **Oldindan tekshirish vositasi:** Google Digital Asset Links
  Generator (qidiruvda "Digital Asset Links generator" deb qidiring) —
  sayt URL va izni qo'yib tekshirishingiz mumkin

> Server marshruti allaqachon tayyor (commit `07903a4` da qo'shilgan).
> Faqat faylni yuklash qoldi. SHA-256 izini olishingiz bilan menga
> ayting — `assetlinks_yoz.py` bilan faylni tayyorlab qo'yaman.

---

## 7. Telefonda sinash

**Yo'l A — Play orqali (to'g'ri):**
1. Internal testing opt-in link'ini telefonda oching
2. Play'da "OBER" → **Install**

**Yo'l B — APK to'g'ridan-to'g'ri (tez, Play'ni kutmasdan):**
1. `twa-ober/app-release-signed.apk` ni telefonga yuboring (Telegram/USB)
2. Telefonda "Noma'lum manbalar" ruxsatini bering → o'rnating

**Tekshiradigan narsalar:**
- [ ] Ilova **to'liq ekranda** ochiladi (yuqorida Chrome paneli yo'q)
- [ ] Qidiruv ishlaydi, kartalar chiqadi
- [ ] Bildirishnoma ruxsati so'raladi (push yoqilgan bo'lsa)
- [ ] Offline'da ham ochiladi (kesh bor)

> To'liq ekran emas, lekin ishlayapti → assetlinks noto'g'ri. 5-6
> qadamni qayta tekshiring.

---

## 8. Production release

1. **Testing → Closed testing** (ixtiyoriy, yana bir hafta sinov)
2. **Testing → Production → Create release** → yangi `app-release-bundle.aab`
   → release notes → **Start rollout to Production**
3. **Content rating** so'rovnomasi (5 daqiqa): "Shopping", yoshi 13+,
   zo'ravonlik yo'q
4. **Store listing**: tavsiflar va ekran rasmlar
   `DOKON-MATERIALLARI.md` dan tayyor:
   - 2+ ekran rasm (390x844 format tayyor)
   - Qisqa tavsif (80 belgi): *«Yozasiz — bozor javob beradi. 450 000+
     e'lon bitta qidiruvda»*
   - To'liq tavsif (uz/ru tayyor)
5. **Monetization**: "Products" yo'q (bepul), xarid yo'q

> Production'ga chiqishdan oldin: Internal testing'da kamida 1-2 kun
> jonli ishlatilsin. Xato release'ni "Rollback" bilan qaytarib olish
> mumkin, lekin foydalanuvchi ko'rgan xatoni o'chirib bo'lmaydi.

---

## 9. Qadamlar ro'yxati (tekshiruv)

- [ ] `enableNotifications: true` + qayta qurish (0-qadam)
- [ ] Developer akkaunt ($25) — NAIZA MChJ
- [ ] App yaratish: `OBER — bir qidiruv, butun bozor`, bepul
- [ ] App content: privacy, ads=no, data safety, yoshi 13+
- [ ] Internal testing: AAB yuklash, testers, opt-in link
- [ ] **SHA-256 izini olish (App signing key)** → menga yuborish
- [ ] `assetlinks.json` serverga → `curl` tekshiruvi
- [ ] Telefonda: to'liq ekran + push + offline
- [ ] Content rating so'rovnomasi
- [ ] Store listing: tavsif + ekran rasmlar
- [ ] Production release

---

## Tez-tez xatolar

| Ko'rinish | Sabab | Yechim |
|---|---|---|
| `Your app doesn't meet target API level requirements` | Target API < 36 | Bubblewrap'ni yangilang, qayta quring (build-tools 36.1.0 bor) |
| Ilova brauzer paneli bilan ochiladi | assetlinks noto'g'ri / iz App signing key'dan olinmagan | 5-6 qadamni qaytadan |
| `App not available in your country` | Internal testing'da siz testers'da yo'qsiz | Testers email'ini tekshiring |
| Bildirishnoma kelmaydi | `enableNotifications: false` qolgan | 0.1-qadam, qayta quring |
| AAB yuklanmayapti (xato: version code) | Qayta qurishda kod o'zgarmagan | `twa-manifest.json` da `appVersionCode` ni +1 |
