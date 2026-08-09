@echo off
chcp 65001 >nul
title OBER - AI kalitni xavfsiz yoqish

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0AI-KALITNI-YOQISH.ps1"
set NATIJA=%ERRORLEVEL%

echo.
if not "%NATIJA%"=="0" (
  echo Muammo chiqdi. Oynani yopmasdan xatoni Codexga ayting.
)
pause
exit /b %NATIJA%
