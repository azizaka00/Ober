@echo off
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - to'lqinli yuborish sinovi
echo.
echo   Tekshiriladi:
echo    - so'rov mos sotuvchilarga yuboriladimi
echo    - HAQIQIY son qaytariladimi (yolg'on "30 ta" emas)
echo    - mos kelmagan sotuvchi bezovta qilinmaydimi
echo ============================================================
echo.
python -c "import baza, joylar, lugat, olx, qidiruv, server, tahlil, yonalishlar; print('  kod butun')"
if errorlevel 1 (
  echo.
  echo   KODDA XATO BOR.
  pause
  exit /b 1
)
echo.
python tolqin_sinov.py
echo.
pause
