@echo off
chcp 65001 >nul
cd /d "%~dp0app"
rem DIQQAT: bu faylda FAQAT ASCII belgilar ishlatilsin.
echo ============================================================
echo   OBER - qidiruv tezligini o'lchash
echo   (serverni yopish shart emas, lekin yopiq bo'lsa aniqroq)
echo ============================================================
echo.
python tezlik_sinov.py
echo.
pause
