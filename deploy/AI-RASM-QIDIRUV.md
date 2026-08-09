# OBER AI rasm qidiruvini yoqish

Kod kalitsiz ham xavfsiz ishlaydi: kamera tugmasi ko'rinadi, lekin rasm tashqi
AI xizmatiga yuborilmaydi. Matn yozilgan bo'lsa, odatiy OBER qidiruvi davom etadi.

## Faqat Aziz tasdiqlagandan keyin

Windows'da eng sodda va xavfsiz yo'l: loyiha papkasidagi
`AI-KALITNI-YOQISH.bat` faylini oching, OpenAI API kalitini ko'rinmas maydonga
joylang va Enter bosing. Kalit buyruq satrida ko'rinmaydi va lokal faylga
yozilmaydi.

Qo'lda bajarish kerak bo'lsa:

1. Hetzner serverida `/etc/ober-ai.env` yarating.
2. Ichiga quyidagini yozing (kalitni chatga, Git'ga yoki loyiha papkasiga qo'ymang):

   ```env
   OPENAI_API_KEY=sk-...
   OBER_VISION_MODEL=gpt-5.6-luna
   OBER_VISION_DETAIL=low
   ```

3. Faylni himoyalang va xizmatni qayta yuklang:

   ```bash
   chmod 600 /etc/ober-ai.env
   systemctl daemon-reload
   systemctl restart ober-server
   systemctl status ober-server --no-pager
   ```

## Xarajat va maxfiylik

- Har bir yangi rasm odatda bitta AI so'rovini ishlatadi; aynan bir xil rasm va
  izoh server xotirasida vaqtincha keshlanadi.
- Standart `low` tafsilot rejimi xarajat va kechikishni kamaytiradi.
- Brauzer rasmni 1280 px gacha kichraytiradi, JPEG'ga aylantiradi va EXIF'ni
  olib tashlaydi. Server original rasmni diskka yozmaydi.
- Faollashtirishdan oldin foydalanuvchiga rasm AI xizmatiga yuborilishi
  Maxfiylik sahifasida ochiq ko'rsatilishi shart.
