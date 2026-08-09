@echo off
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - TALAB HISOBOTI
echo.
echo   Nima qidirilyapti, nima topilmayapti, qayerda talab bor.
echo   Sotuvchini olib keladigan dalil shu yerdan chiqadi.
echo ============================================================
echo.
python talab.py
if errorlevel 1 (
  echo.
  echo Xato chiqdi. Sinang:  py talab.py
)
echo.
pause
