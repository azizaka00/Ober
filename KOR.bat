@echo off
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - yig'ilgan ma'lumot sifatini tekshirish
echo ============================================================
echo.
python kor.py
if errorlevel 1 (
  echo.
  echo Xato chiqdi. Sinang:  py kor.py
)
echo.
pause
