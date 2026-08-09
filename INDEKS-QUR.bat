@echo off
chcp 65001 >nul
cd /d "%~dp0app"
rem DIQQAT: bu faylda FAQAT ASCII belgilar ishlatilsin.
echo ============================================================
echo   OBER - QIDIRUV INDEKSI (FTS5)
echo.
echo   Ilgari qidiruv hamma e'lonni xotiraga yuklardi.
echo   11500 e'londa bu ishlardi, 100000 da xotira yetmaydi.
echo   Indeks bilan xotiraga hech narsa yuklanmaydi.
echo ============================================================
echo.
echo   [1/3] Kod tekshiruvi...
python -c "import baza, lugat, qidiruv, tahlil, fts_qur, hammasi, kategoriyalar; print('    kod butun')"
if errorlevel 1 (
  echo.
  echo   KODDA XATO BOR. Xatoni menga ko'rsating.
  pause
  exit /b 1
)
echo.
echo   [2/3] Tahlil (yangi ustunlar uchun)...
python tahlil.py
echo.
echo   [3/3] Indeks qurilmoqda...
python fts_qur.py
echo.
echo ------------------------------------------------------------
echo   Endi KOR-BRAUZERDA.bat ni bosing va qidiruvni tekshiring.
echo   Keyin HAMMASINI-YIG.bat ni bosish mumkin.
echo ------------------------------------------------------------
pause
