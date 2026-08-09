@echo off
chcp 65001 >nul
cd /d "%~dp0app"
rem DIQQAT: bu faylda FAQAT ASCII belgilar ishlatilsin.
echo ============================================================
echo   OBER - Telegram bot tekshiruvi
echo ============================================================
echo.
python -c "import baza, tg, server, qidiruv; print('  kod butun')"
if errorlevel 1 (
  echo.
  echo   KODDA XATO BOR.
  pause
  exit /b 1
)
echo.
python bot_tekshir.py
echo.
echo ------------------------------------------------------------
echo   Token bor bo'lsa: KOR-BRAUZERDA.bat bosing.
echo   Bot serverning ichida o'zi ishga tushadi.
echo ------------------------------------------------------------
pause
