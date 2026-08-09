@echo off
rem FAQAT ASCII! Maxsus belgi bo'lmasin.
rem OBER - kodni yuklab, xizmatlarni qayta ishga tushiradi.
rem Natija faylga yoziladi: data\sinov-natija.txt
rem
rem DIQQAT: ssh ichiga tirnoqli murakkab buyruq YOZILMAYDI. cmd `|`,
rem `(`, `)` va tirnoqlarni o'zicha talqin qiladi, natijada masofadagi
rem bash osilib qoladi va oyna qotadi (2026-08-02 da shunday bo'ldi).
rem Murakkab ish kerak bo'lsa - serverdagi .sh faylga yoziladi.
chcp 65001 >nul
set SERVER=root@77.42.123.90
set LOG=%~dp0data\sinov-natija.txt

echo OBER - %DATE% %TIME% > "%LOG%"
echo ==================================== >> "%LOG%"

echo [1/3] app yuklanmoqda >> "%LOG%"
scp -q -r "%~dp0app" %SERVER%:/home/ober/ober/ >> "%LOG%" 2>&1

echo [2/3] web yuklanmoqda >> "%LOG%"
scp -q -r "%~dp0web" %SERVER%:/home/ober/ober/ >> "%LOG%" 2>&1

echo [3/3] xizmatlar qayta ishga tushmoqda >> "%LOG%"
ssh -o BatchMode=yes %SERVER% systemctl restart ober-server ober-yangilik >> "%LOG%" 2>&1
ssh -o BatchMode=yes %SERVER% systemctl is-active ober-server ober-yangilik >> "%LOG%" 2>&1

echo ---- TUGADI ---- >> "%LOG%"
exit
