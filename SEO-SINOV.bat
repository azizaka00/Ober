@echo off
chcp 65001 >nul
cd /d "%~dp0app"
rem DIQQAT: bu faylda FAQAT ASCII belgilar ishlatilsin.
echo ============================================================
echo   OBER - narx sahifalari (SEO o'sish dvigateli)
echo.
echo   Thumbtack va Carwow asosan shu yo'l bilan o'sgan.
echo   Bizda ular bermaydigan narsa bor: NARX ORALIG'I.
echo ============================================================
echo.
python -c "import baza, qidiruv, seo, server; print('  kod butun')"
if errorlevel 1 (
  echo.
  echo   KODDA XATO BOR.
  pause
  exit /b 1
)
echo.
python seo_sinov.py
echo.
pause
