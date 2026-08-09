@echo off
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - brauzerda ko'rish
echo.
echo   Brauzer o'zi ochiladi: http://127.0.0.1:8800
echo   To'xtatish uchun bu oynada Ctrl+C bosing.
echo ============================================================
echo.
python server.py
if errorlevel 1 (
  echo.
  echo Xato chiqdi. Sinang:  py server.py
  pause
)
