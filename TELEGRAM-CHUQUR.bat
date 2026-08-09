@echo off
rem FAQAT ASCII! Maxsus belgi bo'lmasin.
rem OBER - Telegram kanallarini CHUQUR yig'ish (6 sahifa).
rem Bir martalik ish: eski e'lonlarning narxini ham tuzatadi.
rem Odatiy holatda 1 sahifa yetadi - yangi xabarlar o'sha yerda.
chcp 65001 >nul
set SERVER=root@77.42.123.90
set LOG=%~dp0data\telegram-chuqur.txt

echo OBER Telegram CHUQUR - %DATE% %TIME% > "%LOG%"
echo ==================================== >> "%LOG%"

echo [1/2] Kod yuklanmoqda >> "%LOG%"
scp -q -r "%~dp0app" %SERVER%:/home/ober/ober/ >> "%LOG%" 2>&1

echo [2/2] 6 sahifadan yigilmoqda (10-15 daqiqa) >> "%LOG%"
ssh -o BatchMode=yes %SERVER% cd /home/ober/ober/app ^&^& python3 telegram_yig.py 6 >> "%LOG%" 2>&1

echo ---- TUGADI ---- >> "%LOG%"
exit
