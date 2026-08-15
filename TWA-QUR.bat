@echo off
rem FAQAT ASCII! Maxsus belgi bo'lmasin.
rem
rem OBER - Play Store uchun paket qurish.
rem Butun mantiq app\twa_qur.py da. Bu fayl faqat ishga tushirgich.
rem
rem NEGA SHUNDAY: batch fayllarda goto va qavs bloklari mo'rt.
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
