@echo off
rem FAQAT ASCII! Maxsus belgi bo'lmasin.
rem OBER - kanal ro'yxatini yuklab, Telegramdan yig'adi.
rem Natija: data\telegram-natija.txt
chcp 65001 >nul
set SERVER=root@77.42.123.90
set LOG=%~dp0data\telegram-natija.txt

echo OBER Telegram - %DATE% %TIME% > "%LOG%"
echo ==================================== >> "%LOG%"

echo [1/3] Kod yuklanmoqda >> "%LOG%"
rem Kanal ro'yxati bilan birga KOD ham yuklanishi shart. 2026-08-03:
rem parser tuzatildi, lekin bat faqat ro'yxatni yuklardi va server
rem eski kod bilan ishlab, tuzatish sinalmay qoldi.
scp -q -r "%~dp0app" %SERVER%:/home/ober/ober/ >> "%LOG%" 2>&1

echo [2/3] Kanal ro'yxati yuklanmoqda >> "%LOG%"
scp -q "%~dp0data\telegram-kanallar.txt" %SERVER%:/home/ober/ober/data/ >> "%LOG%" 2>&1

echo [3/3] Yigilmoqda (bir necha daqiqa) >> "%LOG%"
ssh -o BatchMode=yes %SERVER% cd /home/ober/ober/app ^&^& python3 telegram_yig.py >> "%LOG%" 2>&1

echo ---- TUGADI ---- >> "%LOG%"
exit
