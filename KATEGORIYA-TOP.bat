@echo off
chcp 65001 >nul
cd /d "%~dp0app"
rem DIQQAT: bu faylda FAQAT ASCII belgilar ishlatilsin.
echo ============================================================
echo   OBER - kategoriyalarni OLX'dan o'qish
echo.
echo   Qo'lda yozilgan ro'yxatda 8 tadan 4 tasi 404 edi.
echo   OLX bosh sahifasida BUTUN daraxt turibdi (915 kategoriya) -
echo   uni o'qib olamiz, taxmin qilmaymiz.
echo ============================================================
echo.
python kategoriya_top.py
echo.
echo ------------------------------------------------------------
echo   TO'LIQ chuqurlik: eng past kategoriyalar (~800 ta).
echo.
echo   Nega chuqur: OLX har manzilga ~25 sahifa beradi. Ota
echo   kategoriya 1300 e'lon bersa, uning 10 bolasi 13000 beradi.
echo.
echo   Tartib: avval transport (bizning nishamiz), keyin
echo   elektronika, ko'chmas mulk va boshqalar. Ya'ni yig'ish
echo   yarmida to'xtasa ham eng qimmatlisi olingan bo'ladi.
echo.
echo   Qisqaroq ro'yxat kerak bo'lsa:  python kategoriya_top.py 2
echo ------------------------------------------------------------
pause
