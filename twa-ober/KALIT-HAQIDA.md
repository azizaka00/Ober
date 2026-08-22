# APK imzo kaliti — nima qilish kerak

**Fayl:** `twa-ober/android.keystore` (2 724 bayt, 2026-08-14)
**SHA-256:** `12780773c20ae93585736031187604696c9f7eed1aa1dd0d5e3ff6d5aa901c44`
**Tur:** PKCS#12, parol bilan himoyalangan (parolsiz ochilmadi — tekshirildi)

## Nega bu fayl muhim

Bu kalit bilan `app-release-signed.apk` imzolangan. Uning sertifikat izi:

    66:19:41:AE:D4:D0:31:81:71:9B:25:6F:E8:83:39:1A:
    80:44:15:E1:62:A8:AC:76:7D:16:71:A3:DC:E5:1D:A3

Aynan shu iz `https://ober.uz/.well-known/assetlinks.json` da turibdi
(2026-08-17 da joylashtirildi). Ya'ni kalit va sayt bir-biriga
bog'langan.

Kalit yo'qolsa ikki narsa buziladi:

1. **Play Store'dagi ilovani hech qachon yangilab bo'lmaydi.** Google
   yangilanish uchun aynan o'sha imzoni talab qiladi. Yagona yo'l —
   yangi paket nomi bilan YANGI ilova chiqarish va hamma
   o'rnatganlarni qaytadan yig'ish.
2. **assetlinks mos kelmay qoladi.** Yangi kalit bilan qurilgan APK
   to'liq ekranda ochilmaydi — tepada brauzer manzil satri chiqadi,
   xato xabari esa BO'LMAYDI, shunchaki ishlamaydi.

## Hozirgi holat — XAVFLI

Bu faylning YAGONA nusxasi shu diskda. `.gitignore` uni git'ga
tushirmaydi (to'g'ri qaror — kalit repoda turmasligi kerak), lekin
zaxirasi ham yo'q.

## Nima qilish kerak

1. Faylni parol menejeriga qo'shing (1Password, Bitwarden, KeePass —
   fayl biriktirish imkoni bor) YOKI shifrlangan disk / USB ga
   nusxalang. Bulutga shifrlanmagan holda tashlamang.
2. **Parolni ALOHIDA saqlang.** Fayl parol bilan himoyalangan, ya'ni
   fayl o'g'irlansa ham parolsiz foydasiz — lekin parol yo'qolsa fayl
   ham foydasiz. Ikkalasi ham kerak.
3. Nusxa to'g'ri ko'chganini yuqoridagi SHA-256 bilan tekshiring:

       sha256sum android.keystore

## Eslatma

Play Store'ga chiqarganda Google App Signing yoqilsa, Google paketni
O'Z kaliti bilan qayta imzolaydi. O'shanda Play Console →
Test and release → Setup → App signing dan "App signing key
certificate" SHA-256 ni olib, assetlinks'ga IKKINCHI iz sifatida
qo'shish kerak:

    python app/assetlinks_yoz.py <google-izi> <yuqoridagi-iz>
