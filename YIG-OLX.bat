@echo off
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - OLX'dan ma'lumot yig'ish
echo   13 ta viloyat, har biridan 3 sahifa (~1500 e'lon)
echo   Manbani yuklamaslik uchun har so'rov orasida 2.5 soniya
echo   Taxminan 3-4 daqiqa davom etadi
echo ============================================================
echo.
python olx.py 3
if errorlevel 1 (
  echo.
  echo Xato chiqdi. "python" ishlamasa quyidagini sinang:  py olx.py 3
)
echo.
echo ------------------------------------------------------------
echo  Faqat bitta viloyat kerak bo'lsa, masalan:
echo     python olx.py 5 Toshkent
echo     python olx.py 3 Samarqand
echo ------------------------------------------------------------
pause
