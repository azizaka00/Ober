@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM ============================================================
REM  OBER -> GitHub. Hamma qadam bitta joyda, tartib bilan.
REM
REM  Har qadamdan keyin xato tekshiriladi. Biror joyda xato
REM  bo'lsa skript TO'XTAYDI va nima bo'lganini aytadi -
REM  yarim bajarilgan holatda qoldirmaydi.
REM ============================================================

echo.
echo ============================================================
echo   OBER -^> GitHub
echo ============================================================
echo.

REM ---- 1. To'g'ri joydamizmi ---------------------------------
if not exist ".git" (
    echo   XATO: bu papkada git repo yo'q.
    echo   Skript D:\OBER ichida turishi kerak.
    pause & exit /b 1
)
if not exist "app\server.py" (
    echo   XATO: app\server.py topilmadi. Noto'g'ri papka.
    pause & exit /b 1
)
echo   [1/7] Papka to'g'ri: %CD%

REM ---- 2. Kim commit qilyapti --------------------------------
for /f "delims=" %%i in ('git config user.name 2^>nul') do set KIM=%%i
if "!KIM!"=="" (
    git config --global user.name "azizaka00"
    git config --global user.email "azizaka00@users.noreply.github.com"
    echo   [2/7] Identity o'rnatildi: azizaka00
) else (
    echo   [2/7] Identity: !KIM!
)

REM ---- 3. Nima commit bo'ladi --------------------------------
git add . >nul 2>&1
for /f "tokens=1" %%i in ('git diff --cached --numstat ^| find /c /v ""') do set SONI=%%i
echo   [3/7] Commitga tayyor fayllar: !SONI!

if "!SONI!"=="0" (
    git log -1 --oneline >nul 2>&1
    if errorlevel 1 (
        echo   XATO: commit qiladigan narsa yo'q.
        pause & exit /b 1
    )
    echo         ^(yangi o'zgarish yo'q - avvalgi commit ishlatiladi^)
)

REM ---- 4. Commit --------------------------------------------
git log -1 --oneline >nul 2>&1
if errorlevel 1 (
    git commit -q -m "OBER - teskari marketplace MVP"
    if errorlevel 1 (
        echo   XATO: commit bajarilmadi.
        pause & exit /b 1
    )
    echo   [4/7] Commit qilindi
) else (
    if not "!SONI!"=="0" (
        git commit -q -m "Yangilanish"
        echo   [4/7] Yangi commit qilindi
    ) else (
        echo   [4/7] Commit allaqachon bor
    )
)

REM ---- 5. Tarmoq nomi ---------------------------------------
git branch -M main
echo   [5/7] Tarmoq: main

REM ---- 6. GitHub'da repo ochish ------------------------------
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo.
    echo   [6/7] Endi GitHub'da repo ochish kerak.
    echo.
    echo         Brauzer ochiladi. Quyidagicha to'ldiring:
    echo           Repository name : ober
    echo           Public          : BELGILANG
    echo           README          : belgilamang
    echo           .gitignore      : belgilamang
    echo           License         : belgilamang
    echo.
    echo         "Create repository" bosing, keyin shu oynaga qayting.
    echo.
    pause
    start "" "https://github.com/new"
    echo.
    echo   Repo ochilgach Enter bosing...
    pause >nul
    git remote add origin https://github.com/azizaka00/ober.git
    echo   Remote qo'shildi
) else (
    echo   [6/7] Remote allaqachon bor
)

REM ---- 7. Yuborish -------------------------------------------
echo.
echo   [7/7] Yuborilmoqda...
echo         GitHub login so'rashi mumkin - brauzer oynasi ochiladi.
echo.
git push -u origin main
if errorlevel 1 (
    echo.
    echo   ============================================================
    echo   YUBORILMADI
    echo   ============================================================
    echo   Ko'p uchraydigan sabablar:
    echo     - GitHub'da "ober" repo hali ochilmagan
    echo     - login bekor qilindi
    echo     - internet uzilgan
    echo.
    echo   Repo ochilganini tekshiring va skriptni qayta ishga tushiring.
    echo   Hech narsa buzilmadi - qaytadan urinsa bo'ladi.
    pause & exit /b 1
)

echo.
echo ============================================================
echo   TAYYOR
echo ============================================================
echo.
echo   Repo: https://github.com/azizaka00/ober
echo.
echo   Endi INKOGNITO oynada ochilishini tekshiring -
echo   hakam ham xuddi shunday ko'radi.
echo.
pause
start "" "https://github.com/azizaka00/ober"
