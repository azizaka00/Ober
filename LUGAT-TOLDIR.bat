@echo off
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - lug'atni ma'lumotdan to'ldirish
echo.
echo   E'lonlarda tez uchraydigan, lekin lug'atда yo'q
echo   so'zlarni topadi. Taxmin emas - haqiqiy ehtiyoj.
echo ============================================================
echo.
python nomalum.py 50
if errorlevel 1 (
  echo.
  echo Xato chiqdi. Sinang:  py nomalum.py 50
)
echo.
pause
