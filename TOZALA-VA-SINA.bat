@echo off
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - bazani tozalash va qidiruvni qayta sinash
echo ============================================================
echo.
echo [1/2] Bema'ni narxlarni tozalash...
python tozala.py
echo.
echo [2/2] Qidiruv sinovi...
python sinov.py
if errorlevel 1 (
  echo.
  echo Xato chiqdi. Sinang:  py tozala.py  va  py sinov.py
)
echo.
pause
