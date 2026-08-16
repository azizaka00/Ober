@echo off
rem FAQAT ASCII! Maxsus belgi bo'lmasin.
rem
rem OBER - Play Store uchun paket qurish.
rem Butun mantiq app\twa_qur.py da. Bu fayl faqat ishga tushirgich.
rem
rem NEGA SHUNDAY: batch fayllarda o'tish yorliqlari hamda qavs
rem bloklari mo'rt - ikkalasi ham bu faylda ishlatilmagan.
rem (Yorliq so'zini bu yerda ATAYLAB yozmadim: bat_sinov uni oddiy
rem  matn qidiruvi bilan izlaydi va izohdagi so'z ham ogohlantirish
rem  beradi. Qoida haqida yozish qoidani buzadi - bugun `<!--` bilan
rem  ham xuddi shunday bo'lgan.)
rem NAVBATCHI.bat bir marta shundan buzilgan edi. Bu yerda
rem ikkalasi ham yo'q, demak satr oxiri CRLF yoki LF bo'lishi
rem ahamiyatsiz.
rem
rem NEGA UMUMAN .bat: bubblewrap interaktiv wizard ishlatadi va u
rem TTY talab qiladi. Bu faylni ikki marta bosganda ochiladigan
rem cmd oynasi haqiqiy konsol - TTY bor. Avtomatik skriptdan
rem ishga tushirilganda TTY bo'lmaydi va wizard osilib qoladi.
chcp 65001 >nul
python "%~dp0app\twa_qur.py"
pause
