@echo off
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER ZOND - sahifa tuzilishini aniqlash
echo   3 ta sahifa yuklanadi, ober\data\zond\ ga saqlanadi
echo ============================================================
echo.
python zond.py
if errorlevel 1 (
  echo.
  echo Python topilmadi yoki xato chiqdi.
  echo Agar "python" ishlamasa, quyidagini sinang: py zond.py
)
echo.
pause
