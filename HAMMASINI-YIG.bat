@echo off
chcp 65001 >nul
cd /d "%~dp0app"
rem DIQQAT: bu faylda FAQAT ASCII belgilar ishlatilsin.
echo ============================================================
echo   OBER - BARCHA KATEGORIYALARNI YIG'ISH
echo.
echo   ~85 kategoriya x 13 viloyat.
echo   Bu UZOQ ish: bir necha soat ketishi mumkin.
echo.
echo   Istalgan payt Ctrl+C bilan to'xtating.
echo   Shu faylni QAYTA bosganingizda qolgan joydan davom etadi -
echo   boshidan boshlamaydi, bitta ham juftlik qolib ketmaydi.
echo ============================================================
echo.
echo   [1/3] Kod tekshiruvi...
python -c "import baza, olx, kategoriyalar, hammasi, qidiruv, tahlil; print('    kod butun')"
if errorlevel 1 (
  echo.
  echo   KODDA XATO BOR. Xatoni menga ko'rsating.
  pause
  exit /b 1
)
echo.
echo   [2/3] Yig'ish - har juftlikdan 3 sahifa...
echo.
echo         Tartib: avval TRANSPORT (bizning nishamiz), keyin
echo         elektronika, ko'chmas mulk va boshqalar.
echo         Ya'ni yarmida to'xtatsangiz ham eng kerakli qismi
echo         olingan bo'ladi.
echo.
echo         Chuqurroq kerak bo'lsa keyin:  python hammasi.py 25
python hammasi.py 3
echo.
echo   [3/3] Tahlil...
python tahlil.py
echo.
echo ------------------------------------------------------------
echo   Tugamagan bo'lsa - shu faylni yana bosing.
echo   Holat: python -c "import baza;print(baza.yigish_hisoboti())"
echo ------------------------------------------------------------
pause
