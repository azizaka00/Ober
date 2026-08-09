@echo off
chcp 65001 >nul
cd /d "%~dp0app"
rem DIQQAT: bu faylda FAQAT ASCII belgilar ishlatilsin.
rem Uzun tire yoki qiyshiq apostrof cmd parserini buzadi va
rem "'ho' is not recognized" degan xato chiqadi (2026-08-01 da bo'ldi).
echo ============================================================
echo   OBER - TUZATISHLAR
echo.
echo   1) Ko'rinmas e'lonlar: bazada 11500, qidiruvda 3030 edi.
echo      Tahlil qilinmagan e'lon qidiruvda umuman chiqmaydi.
echo   2) Soxta narxlar: 9999999 kabi "qo'ng'iroq qiling" raqamlari
echo      narx oralig'ini buzardi.
echo   3) Lug'at: tumanka endi faradan ajratildi.
echo ============================================================
echo.
echo   [1/3] Kod tekshiruvi...
python -c "import baza, joylar, lugat, olx, qidiruv, server, tahlil, narx_tozala, tg; print('    kod butun')"
if errorlevel 1 (
  echo.
  echo   KODDA XATO BOR. Xatoni menga ko'rsating.
  pause
  exit /b 1
)
echo.
echo   [2/3] Soxta narxlarni tozalash...
python narx_tozala.py
echo.
echo   [3/3] Tahlil - lug'at o'zgargani uchun TO'LIQ QAYTA...
echo         (biroz uzoqroq ketadi)
python tahlil.py qayta
echo.
echo ------------------------------------------------------------
echo   Tayyor. Endi KOR-BRAUZERDA.bat ni bosing.
echo ------------------------------------------------------------
pause
