@echo off
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - TO'LIQ HALQA SINOVI
echo.
echo   Qidiruv -> so'rov -> sotuvchi -> javob -> xaridor
echo   Brauzer kerak emas. Sinov ma'lumoti oxirida o'chiriladi.
echo ============================================================
echo.
python halqa_sinov.py
if errorlevel 1 (
  echo.
  echo Xato bor - yuqoridagi [XATO] qatorlarini Claude'ga ko'rsating.
)
echo.
pause
