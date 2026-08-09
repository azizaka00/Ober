@echo off
chcp 65001 >nul
cd /d "%~dp0app"
rem DIQQAT: bu faylda FAQAT ASCII belgilar ishlatilsin.
echo ============================================================
echo   OBER - narx sifatini tuzatish
echo.
echo   Muammo: "kobalt fara" so'roviga 135-170 MLN so'mlik
echo   e'lonlar chiqardi. Ular fara emas, BUTUN MASHINA edi.
echo.
echo   Sabab 1: lug'atda "svet" fara deb yozilgan. O'zbekchada
echo            "oq svet" - RANG, chiroq emas. Olib tashlandi.
echo   Sabab 2: "qism so'ralganda butun narsa chiqmasin" degan
echo            qoida yo'q edi. Qo'shildi.
echo ============================================================
echo.
echo   [1/2] Kod tekshiruvi...
python -c "import baza, lugat, qidiruv, seo, server, tahlil; print('    kod butun')"
if errorlevel 1 (
  echo.
  echo   KODDA XATO BOR. Xatoni menga ko'rsating.
  pause
  exit /b 1
)
echo.
echo   [2/2] Lug'at o'zgardi - teglar QAYTA hisoblanadi...
python tahlil.py qayta
echo.
echo ------------------------------------------------------------
echo   Tayyor. Serverni qayta ishga tushiring (KOR-BRAUZERDA.bat)
echo ------------------------------------------------------------
pause
