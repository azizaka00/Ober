@echo off
rem FAQAT ASCII! Bu faylda o'zbekcha maxsus belgi (o', g', tire) BO'LMASIN.
rem 2026-08-01: bitta uzun tire butun faylni ishlamas qilib qo'ygan edi.
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - indeksni yangilash va ishga tushirish
echo ============================================================
echo.
echo   DIQQAT: server ishlab turgan eski oyna bo'lsa, uni yoping
echo   (o'sha oynada Ctrl+C). Aks holda 8800-port band chiqadi.
echo   Elon yigish oynasiga TEGMANG - u alohida ishlaydi.
echo.
echo [1/2] Yangi elonlar tahlil qilinmoqda va indeksga yozilmoqda...
echo       (100 mingdan ortiq elon bo'lsa bu bir necha daqiqa oladi)
echo.
python tahlil.py
if errorlevel 1 (
  echo.
  echo   Tahlil xato berdi. Sinang:  py tahlil.py
  pause
  exit /b 1
)
echo.
echo [2/2] Server ishga tushmoqda: http://127.0.0.1:8800
echo       To'xtatish uchun shu oynada Ctrl+C.
echo.
python server.py
if errorlevel 1 (
  echo.
  echo   Xato chiqdi. Sinang:  py server.py
  pause
)
