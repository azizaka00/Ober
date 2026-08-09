# OBER — yig‘ish adapterlari

## Maqsad

`app/yigish.py` barcha ochiq ma’lumot manbalarini bir xil usulda yuritadi.
Mavjud OLX parseri o‘zgartirib tashlanmadi; `app/manbalar/olx.py` orqali
umumiy runnerga ulandi.

## Adapter shartnomasi

Har `app/manbalar/<manba>.py` modulida quyidagilar bo‘ladi:

- `MANBA` — bazadagi barqaror kalit;
- `NOM` — foydalanuvchiga ko‘rinadigan nom;
- `bosh(cheklov, faqat)` — tez/partial yig‘ish, e’lonlarni nofaol qilmaydi;
- `chuqur(sahifalar, faqat)` — to‘liq yig‘ish va faollik sikli.

Bir adapter yiqilsa, runner qolgan adapterlarni davom ettiradi. Xato bo‘lgan
to‘liq sikl e’lonlarning `korilmadi` hisobini oshirmaydi.

## Faollik qoidasi

1. Ko‘rilgan e’lon: `faol=1`, `korilmadi=0`.
2. Muvaffaqiyatli to‘liq siklda ko‘rinmagan e’lon: `korilmadi + 1`.
3. Ketma-ket uch to‘liq siklda ko‘rinmasa: `faol=0`.
4. Qayta ko‘rinsa: darhol `faol=1`, `korilmadi=0`.
5. Sinov, partial yoki nol natijali sikl: hech narsani nofaol qilmaydi.

## Buyruqlar

```text
python yigish.py sinov 1 olx Toshkent
python yigish.py bosh 1
python yigish.py chuqur 25
python yigish_sinov.py
```

`KATTA-YIGISH.bat` birinchi buyruq bilan OLXni tez tekshiradi, keyin barcha
adapterlarda chuqur yig‘ishni yuritadi. Umumiy runner yangi e’lonlarni darhol
tahlil qiladi; batch oxirida `kor.py` faol e’lonlar bo‘yicha sifat hisobotini
chiqaradi.

Tahlil hali tugamagan yangi e’lonlar qidiruvning issiq yo‘liga kiritilmaydi.
Bu parallel yig‘ish paytida fuzzy lug‘atning minglab e’lonni qayta tahlil qilib,
qidiruvni bir necha soniyaga cho‘zib yuborishidan saqlaydi.

`tahlil.py` tugagach `data/qidiruv-kesh.version` belgisini yangilaydi. Server
faqat shu belgi o‘zgarganda e’lon keshini qayta yuklaydi; oddiy qidiruv
statistikasi yoki hali tugamagan yig‘ish keshni bekor qilmaydi.
