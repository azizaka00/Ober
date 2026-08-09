@echo off
chcp 65001 >nul
cd /d "%~dp0app"
rem DIQQAT: bu faylda FAQAT ASCII belgilar ishlatilsin.
echo ============================================================
echo   OBER - jalb qilish uchun sotuvchilar ro'yxati
echo.
echo   Thumbtack aynan shundan boshlagan: kataloglarni yig'ib,
echo   ta'minotchilarni topib, o'zi borgan. Talab isbotini kutmagan.
echo.
echo   Bizda ham shu boylik bor - yig'ilgan e'lonlarda sotuvchi
echo   nomi, do'konmi va nechta e'loni bori yozilgan.
echo ============================================================
echo.
python sotuvchi_royxat.py 150
echo.
pause
