@echo off
rem FAQAT ASCII! Maxsus belgi bo'lmasin.
rem
rem OBER - o'zgarishlarni serverga yuklash. Bir bosishda.
rem Avval KALIT-QUYISH.bat bajarilgan bo'lishi kerak (bir marta).
chcp 65001 >nul
setlocal
set SERVER=root@77.42.123.90
set MASOFA=/home/ober/ober

echo ============================================================
echo   OBER - serverga yuklash
echo ============================================================
echo.

echo   [1/4] Sahifalar (web)...
scp -q -r "%~dp0web" %SERVER%:%MASOFA%/
if errorlevel 1 goto xato

echo   [2/4] Dastur (app)...
scp -q -r "%~dp0app" %SERVER%:%MASOFA%/
if errorlevel 1 goto xato

echo   [3/4] Ro'yxatlar (data\*.txt)...
scp -q "%~dp0data\*.txt" %SERVER%:%MASOFA%/data/
if errorlevel 1 echo   (ro'yxat fayllari o'tmadi - muhim emas)

echo   [4/4] Xizmatlar qayta ishga tushmoqda...
scp -q -r "%~dp0deploy" %SERVER%:%MASOFA%/
if errorlevel 1 goto xato
ssh %SERVER% "cp %MASOFA%/deploy/ober-server.service /etc/systemd/system/ && cp %MASOFA%/deploy/ober-yangilik.service /etc/systemd/system/ && cp %MASOFA%/deploy/ober-toliq.service /etc/systemd/system/ && systemctl daemon-reload && systemctl enable ober-toliq >/dev/null && systemctl restart ober-server ober-yangilik ober-toliq"
if errorlevel 1 goto xato

timeout /t 4 /nobreak >nul
echo.
echo   Tekshiruv:
ssh %SERVER% "systemctl is-active ober-server && systemctl is-active ober-yangilik && systemctl is-active ober-toliq"

echo.
echo ============================================================
echo   TAYYOR.  http://77.42.123.90
echo.
echo   Brauzerda eski ko'rinish chiqsa Ctrl+F5 bosing.
echo ============================================================
pause
exit /b 0

:xato
echo.
echo   XATO. Sabablari:
echo     - internet yo'q
echo     - KALIT-QUYISH.bat hali bajarilmagan
echo     - server o'chgan
echo.
pause
exit /b 1
