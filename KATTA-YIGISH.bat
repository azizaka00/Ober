@echo off
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - KATTA YIG'ISH (yangi parser)
echo.
echo   Endi ma'lumot HTML kartalardan emas, sahifaning ichidagi
echo   holat blokidan o'qiladi. Har e'londa: rasm, shahar, TUMAN,
echo   tavsif, qism turi, do'konmi, sotuvchi, aniq narx va sana.
echo.
echo   O'lchandi: rasm 51/52, shahar 52/52, tuman 38/52.
echo   Eskisi:    rasm 12%%,   tuman 8%%.
echo.
echo   Har viloyatdan 25 sahifa. Vaqti: ~15-20 daqiqa.
echo ============================================================
echo.
echo   [1/4] Kod va adapter tekshiruvi...
python -c "import baza, joylar, lugat, olx, qidiruv, server, tahlil, yigish, manbalar.olx; print('    kod va adapterlar butun')"
if errorlevel 1 (
  echo.
  echo   KODDA XATO BOR - yig'ish boshlanmadi. Xatoni menga ko'rsating.
  pause
  exit /b 1
)
python yigish_sinov.py
if errorlevel 1 (
  echo.
  echo   FAOLLIK YOKI ADAPTER SINOVI YIQILDI - yig'ish boshlanmadi.
  pause
  exit /b 1
)
python relevans_sinov.py
if errorlevel 1 (
  echo.
  echo   QIDIRUV RELEVANSI SINOVI YIQILDI - yig'ish boshlanmadi.
  pause
  exit /b 1
)
python sinonim_sinov.py
if errorlevel 1 (
  echo.
  echo   SINONIM QATLAMI SINOVI YIQILDI - yig'ish boshlanmadi.
  pause
  exit /b 1
)
python suhbat_sinov.py
if errorlevel 1 (
  echo.
  echo   ICHKI CHAT SINOVI YIQILDI - yig'ish boshlanmadi.
  pause
  exit /b 1
)
python i18n_sinov.py
if errorlevel 1 (
  echo.
  echo   O'ZBEK/RUS TIL SINOVI YIQILDI - yig'ish boshlanmadi.
  pause
  exit /b 1
)
echo.
echo   [2/4] Bir sahifalik sinov (5 soniya)...
python yigish.py sinov 1 olx Toshkent
if errorlevel 1 (
  echo.
  echo   SINOV YIQILDI - katta yig'ish boshlanmadi. Xatoni menga ko'rsating.
  pause
  exit /b 1
)
echo.
echo   Sinov o'tdi. Yuqorida "rasm" va "tuman" sonlarini ko'ring.
echo.
echo   [3/4] Katta yig'ish...
python yigish.py chuqur 25
if errorlevel 1 (
  echo.
  echo Xato chiqdi. Sinang:  python yigish.py chuqur 25
  pause
  exit /b 1
)
echo.
echo   [4/4] Sifat hisoboti...
python kor.py
echo.
echo ------------------------------------------------------------
echo   Tayyor. Endi KOR-BRAUZERDA.bat ni bosing.
echo ------------------------------------------------------------
pause
