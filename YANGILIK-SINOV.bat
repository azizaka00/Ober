@echo off
rem FAQAT ASCII! Maxsus belgi bo'lmasin.
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - yangilik sikli SINOVI (3 ta juftlik, ~30 soniya)
echo   Hech narsa o'chirilmaydi, faqat yangi elon qo'shiladi.
echo ============================================================
echo.
python yangilik.py sinov
echo.
echo ============================================================
pause
