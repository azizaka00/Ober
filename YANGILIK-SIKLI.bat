@echo off
rem FAQAT ASCII! Bu faylda o'zbekcha maxsus belgi (o', g', uzun tire) BO'LMASIN.
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - YANGILIK SIKLI
echo.
echo   Har 45 daqiqada: issiq kategoriyalarning 1-sahifasi
echo   Har 24 soatda:   barcha kategoriyalar + sotilganlarni tozalash
echo.
echo   Bu oyna OCHIQ TURISHI kerak. To'xtatish: Ctrl+C
echo ============================================================
echo.
python yangilik.py kuzat
if errorlevel 1 (
  echo.
  echo   Xato chiqdi. Sinang:  py yangilik.py kuzat
  pause
)
