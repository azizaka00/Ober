@echo off
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - 2-bosqich: e'lon sahifalari
echo   Telefon, rasm, qism turi, tavsif, sotuvchi olinadi
echo.
echo   40 ta e'lon, har biri orasida 3 soniya (~2 daqiqa)
echo   Belgilar:  T=telefon  R=rasm  B=do'kon
echo ============================================================
echo.
python olx_detal.py 40
if errorlevel 1 (
  echo.
  echo Xato chiqdi. Sinang:  py olx_detal.py 40
)
echo.
echo ------------------------------------------------------------
echo  Ko'proq o'qish uchun:  python olx_detal.py 200
echo ------------------------------------------------------------
pause
