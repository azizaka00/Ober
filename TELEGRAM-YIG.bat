@echo off
rem FAQAT ASCII! Maxsus belgi bo'lmasin.
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - TELEGRAM KANALLARINI YIGISH
echo.
echo   Kanal ro'yxati: data\telegram-kanallar.txt
echo   U yerga o'zingiz bilgan savdo kanallarini qo'shing.
echo ============================================================
echo.
python telegram_yig.py %*
echo.
echo ============================================================
pause
