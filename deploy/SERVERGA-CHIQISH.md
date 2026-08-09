# OBER — serverga chiqish

Aziz, 2026-08-02: *"yangi e'lonlarni har doim tugmani bosib kiritishimiz
kerak, orqada qolib ketyapti"*.

Shu hujjat aynan shuni tugatadi. Server ishga tushgach **hech kim hech
narsa bosmaydi**: e'lonlar 45 daqiqada bir yangilanadi, sotilganlari
o'chadi, kompyuteringiz o'chiq bo'lsa ham sayt ishlab turadi.

---

## 1. Server olish (10 daqiqa)

Kerak bo'lgani: **2 GB RAM, 2 yadro, 40 GB disk, Ubuntu 24.04**.
Narxi oyiga ~5–6 $.

Joylashuv bo'yicha maslahat: **Germaniya yoki Finlyandiya** (Hetzner).
Toshkentgacha ping ~90 ms — sezilmaydi. O'zbekistondagi hosting tezroq,
lekin qimmatroq va imkoniyati torroq.

Server olgach qo'lingizda bo'ladi: **IP manzil** va **root paroli**.

> Men server hisobini o'zim ocholmayman va to'lov qilolmayman —
> buni siz qilasiz. Qolgan hamma narsa tayyor.

## 2. Kodni yuklash

Windows'da PowerShell ochib (SERVER_IP o'rniga o'z IP'ingizni yozing):

```powershell
scp -r D:\SUNIYAGENT\ober\app    root@SERVER_IP:/home/ober/ober/
scp -r D:\SUNIYAGENT\ober\web    root@SERVER_IP:/home/ober/ober/
scp -r D:\SUNIYAGENT\ober\deploy root@SERVER_IP:/home/ober/ober/
scp    D:\SUNIYAGENT\ober\data\*.txt root@SERVER_IP:/home/ober/ober/data/
```

**Bazani ham ko'chiring** — 115 000 e'lon tayyor holda boradi, serverda
noldan yig'ish shart emas:

```powershell
scp D:\SUNIYAGENT\ober\data\ober.db root@SERVER_IP:/home/ober/ober/data/
```

Fayl kattaligi bir necha yuz MB bo'lishi mumkin — internet tezligiga
qarab 10–40 daqiqa oladi. Ko'chirishdan oldin uydagi serverni
to'xtating, aks holda yarim yozilgan fayl ketadi.

## 3. O'rnatish (bitta buyruq)

Serverga kiring va:

```bash
ssh root@SERVER_IP
bash /home/ober/ober/deploy/ornatish.sh
```

Skript o'zi: Python va Caddy o'rnatadi, `ober` foydalanuvchisini
yaratadi, ikkita xizmatni yoqadi, HTTPS ni sozlaydi, kunlik zaxira
nusxani qo'yadi.

## 4. Domen

`ober.uz` (yoki hozircha ishlatadigan domeningiz) DNS yozuvida:

```
A    @      SERVER_IP
A    www    SERVER_IP
```

Caddy sertifikatni **o'zi** oladi va **o'zi** yangilaydi. Certbot ham,
cron ham, 90 kunlik eslatma ham kerak emas.

---

## Ishlayotganini tekshirish

```bash
systemctl status ober-server      # sayt
systemctl status ober-yangilik    # e'lonlarni yangilash
journalctl -u ober-yangilik -f    # jonli jurnal
```

Yangilik siklining jurnalida har 45 daqiqada shunday satrlar chiqadi:

```
[ISSIQ] 39 kategoriya x 14 viloyat = 546 juftlik, har biridan 1 sahifa
      Avto ehtiyot qismlar    Toshkent shahri   ko'rildi 44 · yangi 6
```

Mana shu — bosiladigan tugma yo'qligining isboti.

---

## Nima o'zgardi kodda

**`OBER_HOST` va `OBER_PORT`** — endi muhit o'zgaruvchisi bilan
boshqariladi. Serverda Python faqat `127.0.0.1` da eshitadi; tashqariga
Caddy chiqaradi. Ya'ni Python serveriga internetdan to'g'ridan-to'g'ri
ulanib bo'lmaydi.

**Tezlik chegarasi** — uyda kerak emas edi. Internetda esa himoyasiz
POST degani: bir kishi bir soatda 100 000 ta soxta sotuvchi yozib
bazani ishlatib bo'lmaydigan qilishi mumkin. Hozirgi chegaralar:
soatiga 5 ta yangi sotuvchi, 20 ta so'rov, 120 ta chat xabari bitta IP
dan. Haqiqiy odam bunga hech qachon urilmaydi.

**Kunlik zaxira** — baza bizning butun boyligimiz. Har kuni nusxa
olinadi, 7 kunlik tarix saqlanadi.

---

## Hali yetishmayotgan narsalar (halol ro'yxat)

Bu hujjat saytni **ishga tushiradi**, lekin quyidagilar hali yo'q:

- **Sotuvchi hisobi va parol.** Hozir kabinetga havola bilan kiriladi.
  Havolani bilgan odam ko'ra oladi. Real sotuvchilar ko'paygach
  autentifikatsiya shart bo'ladi.
- **Rasm yuklashda tekshiruv.** Hajm cheklangan, lekin mazmun emas.
- **Xato kuzatuvi.** Serverda nimadir sinsa, biz buni faqat jurnalga
  kirganimizda bilamiz.

Bularni real foydalanuvchi paydo bo'lgach, ustuvorlik bo'yicha
qo'shamiz. Hozir ularni kutib turish — saytni umuman chiqarmaslik
degani bo'lardi.
