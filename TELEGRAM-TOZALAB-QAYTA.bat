@echo off
rem FAQAT ASCII! Maxsus belgi bo'lmasin.
rem
rem OBER - Telegram yozuvlarini tozalab, qaytadan yig'adi.
rem
rem SABOQ (2026-08-03): ssh ichiga tirnoqli SQL yozib bo'lmaydi -
rem cmd tirnoqlarni yeb qo'yadi va "incomplete input" chiqadi.
rem Shuning uchun butun ish `deploy/telegram-tozala.sh` faylida,
rem bu yerda faqat ko'chirish va chaqirish.
chcp 65001 >nul
set SERVER=root@77.42.123.90
set LOG=%~dp0data\tozalash-natija.txt

echo OBER Telegram tozalab qayta - %DATE% %TIME% > "%LOG%"
echo ==================================== >> "%LOG%"

echo [1/2] Kod va skript yuklanmoqda >> "%LOG%"
scp -q -r "%~dp0app" %SERVER%:/home/ober/ober/ >> "%LOG%" 2>&1
scp -q "%~dp0deploy\telegram-tozala.sh" %SERVER%:/home/ober/ober/ >> "%LOG%" 2>&1

echo [2/2] Ishlamoqda (10-15 daqiqa) >> "%LOG%"
ssh -o BatchMode=yes %SERVER% bash /home/ober/ober/telegram-tozala.sh >> "%LOG%" 2>&1

echo ---- TUGADI ---- >> "%LOG%"
exit
