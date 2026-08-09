@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ============================================================
REM  OBER — President Tech Award uchun TOZA GitHub repo tayyorlash
REM
REM  NEGA ALOHIDA REPO
REM  D:\SUNIYAGENT NAIZA repositoriysi (github.com/azizaka00/naiza).
REM  OBER uning ichida. Agar shu repo havolasini arizaga bersak:
REM    1) hakam NAIZA kodini ham ko'radi (aralash, tushunarsiz)
REM    2) eski commitlarda sir qolgan bo'lishi mumkin
REM  Shuning uchun TOZA nusxa yasaymiz: tarixsiz, sirsiz.
REM
REM  Bu skript FAQAT tayyorlaydi. GitHub'ga yuborishni oxirida
REM  o'zingiz qilasiz — parol/token menga kerak emas va men uni
REM  so'ramayman.
REM ============================================================

set MANBA=%~dp0
set NUSXA=%~dp0..\ober-github

echo.
echo ============================================================
echo   OBER - toza GitHub nusxasi tayyorlanmoqda
echo ============================================================
echo.

if exist "%NUSXA%" (
    echo   Eski nusxa topildi, o'chirilmoqda...
    rmdir /s /q "%NUSXA%"
)
mkdir "%NUSXA%"

echo   Kod ko'chirilmoqda ^(faqat kerakli papkalar^)...
robocopy "%MANBA%app"    "%NUSXA%\app"    /E /NFL /NDL /NJH /NJS /NC /NS >nul
robocopy "%MANBA%web"    "%NUSXA%\web"    /E /NFL /NDL /NJH /NJS /NC /NS /XD shrift chat-uploads elon-rasmlar >nul
robocopy "%MANBA%deploy" "%NUSXA%\deploy" /E /NFL /NDL /NJH /NJS /NC /NS >nul
robocopy "%MANBA%docs"   "%NUSXA%\docs"   /E /NFL /NDL /NJH /NJS /NC /NS >nul

copy /y "%MANBA%.gitignore"                "%NUSXA%\.gitignore" >nul 2>&1
copy /y "%MANBA%OBER-DIZAYN-QOIDALARI.md"  "%NUSXA%\" >nul 2>&1

REM __pycache__ va .pyc tozalanadi
for /d /r "%NUSXA%" %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
del /s /q "%NUSXA%\*.pyc" >nul 2>&1

echo.
echo ============================================================
echo   XAVFSIZLIK TEKSHIRUVI - sir qolib ketmadimi
echo ============================================================
echo.

set XAVF=0

REM 1. Token/baza fayllari umuman ko'chmaganini tekshiramiz
for %%f in (bot-token.txt ober.db vizual_token.txt) do (
    dir /s /b "%NUSXA%\%%f" >nul 2>&1 && (
        echo   [XAVF] %%f nusxada bor!
        set XAVF=1
    )
)

REM 2. Fayllar ichida ochiq kalit qolmaganini tekshiramiz
findstr /s /i /m /c:"sk-proj" /c:"sk-svcacct" "%NUSXA%\*.py" "%NUSXA%\*.html" "%NUSXA%\*.js" >nul 2>&1 && (
    echo   [XAVF] Fayl ichida OpenAI kaliti topildi!
    set XAVF=1
)

findstr /s /i /m /r /c:"[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]*:AA" "%NUSXA%\*.py" "%NUSXA%\*.txt" >nul 2>&1 && (
    echo   [XAVF] Telegram bot kaliti topildi!
    set XAVF=1
)

if "!XAVF!"=="1" (
    echo.
    echo   ^>^>^> TO'XTANG. Yuqoridagi fayllarni olib tashlamaguningizcha
    echo   ^>^>^> GitHub'ga YUBORMANG.
    echo.
    pause
    exit /b 1
)

echo   [OK] Token fayllari yo'q
echo   [OK] Ochiq kalit topilmadi
echo.

echo ============================================================
echo   TAYYOR: %NUSXA%
echo ============================================================
echo.
echo   Endi shu uchta qadamni o'zingiz bajaring:
echo.
echo   1^) github.com/new -^> repo nomi: ober
echo      Public tanlang ^(hakam ochishi kerak^)
echo      README, .gitignore, license QO'SHMANG - bizda bor
echo.
echo   2^) Shu oynaga quyidagilarni ketma-ket yozing:
echo.
echo        cd /d "%NUSXA%"
echo        git init
echo        git add .
echo        git status
echo.
echo      ^>^>^> git status ro'yxatini KO'Z BILAN o'qing.
echo      ^>^>^> Agar token, .db yoki data/ ko'rinsa - to'xtang.
echo.
echo        git commit -m "OBER - teskari marketplace MVP"
echo        git branch -M main
echo        git remote add origin https://github.com/azizaka00/ober.git
echo        git push -u origin main
echo.
echo   3^) Brauzerda INKOGNITO oynada oching:
echo        https://github.com/azizaka00/ober
echo      Ochilsa - havolani arizaga qo'ying.
echo.
pause
