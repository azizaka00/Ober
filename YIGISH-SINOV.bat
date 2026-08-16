@echo off
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - YIG'ISH VA FAOLLIK SINOVI
echo ============================================================
echo.
python yigish_sinov.py
if errorlevel 1 goto :yakun
echo.
python relevans_sinov.py
if errorlevel 1 goto :yakun
echo.
python sinonim_sinov.py
if errorlevel 1 goto :yakun
echo.
python suhbat_sinov.py
if errorlevel 1 goto :yakun
echo.
python i18n_sinov.py
if errorlevel 1 goto :yakun
echo.
python ai_vision_sinov.py
:yakun
echo.
pause
