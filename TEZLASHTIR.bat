@echo off
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - qidiruvni tezlashtirish
echo.
echo   Har e'lon BIR MARTA tahlil qilinadi va bazaga yoziladi.
echo   Shundan keyin qidiruv 3-5 soniya emas, bir zumda ishlaydi.
echo ============================================================
echo.
python tahlil.py
if errorlevel 1 (
  echo.
  echo Xato chiqdi. Sinang:  py tahlil.py
)
echo.
echo ------------------------------------------------------------
echo  Lug'at o'zgargandan keyin:  python tahlil.py qayta
echo ------------------------------------------------------------
pause
