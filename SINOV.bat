@echo off
chcp 65001 >nul
cd /d "%~dp0app"
echo ============================================================
echo   OBER - SINOVLAR
echo ============================================================
echo.
echo [1/3] Lug'at sinovi (xato yozilgan so'zlar tanilyaptimi)...
python lugat_sinov.py
if errorlevel 1 goto :xato
echo.
echo [2/3] Qidiruv sinovi...
python sinov.py
if errorlevel 1 goto :xato
echo.
echo [3/3] AI rasm qidiruv sinovi (internet va API xarajatisiz)...
python ai_vision_sinov.py
if errorlevel 1 goto :xato
goto :yakun

:xato
echo.
echo Xato chiqdi. Sinang: py lugat_sinov.py, py sinov.py va py ai_vision_sinov.py

:yakun
echo.
pause
