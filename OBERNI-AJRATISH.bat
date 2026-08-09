@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ============================================================
REM  OBER'ni NAIZA papkasidan AJRATIB CHIQARISH
REM
REM  HOZIRGI HOLAT
REM    D:\SUNIYAGENT          <- NAIZA git repositoriysi
REM      └─ ober\             <- OBER shu yerda, NAIZA ichida
REM
REM  MUAMMOSI
REM    1) OBER fayllari NAIZA repositoriysiga tushib ketadi
REM    2) Ildizdagi .gitignore OBER papkalarini qamramaydi ->
REM       bot kaliti va sessiya tokenlari himoyasiz
REM    3) Arizaga havola bersak, hakam NAIZA kodini ham ko'radi
REM
REM  BUNDAN KEYIN
REM    D:\OBER                <- mustaqil loyiha, o'z git'i
REM    D:\SUNIYAGENT          <- faqat NAIZA
REM
REM  BU SKRIPT HECH NARSANI O'CHIRMAYDI.
REM  Faqat NUSXA ko'chiradi va tekshiradi. Eski papkani o'zingiz,
REM  yangisi ishlashiga ishonch hosil qilgandan keyin o'chirasiz.
REM ============================================================

set MANBA=%~dp0
if "%~1"=="" (set MANZIL=D:\OBER) else (set MANZIL=%~1)

echo.
echo ============================================================
echo   OBER ajratilmoqda
echo ============================================================
echo   Qayerdan : %MANBA%
echo   Qayerga  : %MANZIL%
echo.

if exist "%MANZIL%" (
    echo   DIQQAT: "%MANZIL%" allaqachon mavjud.
    echo   Ichidagi bir xil nomli fayllar ustiga yoziladi.
    echo.
    choice /c YN /m "   Davom etaymi"
    if errorlevel 2 exit /b 1
    echo.
)

echo   Ko'chirilmoqda... ^(baza katta, biroz kutasiz^)
echo.

REM /E   - bo'sh papkalar bilan birga hammasi
REM /XD  - vaqtinchalik va qayta yaratiladigan papkalar olinmaydi
robocopy "%MANBA%." "%MANZIL%" /E /R:1 /W:1 ^
    /XD "__pycache__" ".pytest_cache" "tmp" ^
    /XF "*.pyc" "buyruq.txt" "javob.txt" ^
    /NFL /NDL /NJH /NJS /NC /NS

set RC=%ERRORLEVEL%
if %RC% GEQ 8 (
    echo.
    echo   XATO: ko'chirish tugallanmadi ^(robocopy kodi %RC%^).
    echo   Eski papka JOYIDA QOLDI - hech narsa yo'qolmadi.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   TEKSHIRUV
echo ============================================================
echo.

REM Muhim fayllar yetib kelganini tasdiqlaymiz
set YETMADI=0
for %%f in (
    "app\server.py"
    "app\baza.py"
    "app\qidiruv.py"
    "web\index.html"
    "web\sotuvchi.html"
    "web\takliflar.html"
    ".gitignore"
    "OBER-DIZAYN-QOIDALARI.md"
    "NAVBATCHI.bat"
) do (
    if not exist "%MANZIL%\%%~f" (
        echo   [YO'Q]  %%~f
        set YETMADI=1
    )
)

if "!YETMADI!"=="1" (
    echo.
    echo   ^>^>^> Ba'zi fayllar ko'chmadi. Eski papkani O'CHIRMANG.
    pause
    exit /b 1
)

echo   [OK] Asosiy kod fayllari joyida

if exist "%MANZIL%\data\ober.db" (
    for %%A in ("%MANZIL%\data\ober.db") do set /a MB=%%~zA/1048576
    echo   [OK] Baza ko'chdi ^(!MB! MB^)
) else (
    echo   [!]  data\ober.db ko'chmadi - lokal sinov uchun kerak edi.
    echo        Productionga ta'sir qilmaydi, u serverda alohida turadi.
)

echo.
echo ============================================================
echo   TAYYOR
echo ============================================================
echo.
echo   Yangi joy: %MANZIL%
echo.
echo   KEYINGI QADAMLAR - shu tartibda:
echo.
echo   1^) YANGI papkani sinab ko'ring:
echo        %MANZIL%\NAVBATCHI.bat  ni oching, ishlashini tekshiring.
echo.
echo   2^) Cowork'da papkani almashtiring:
echo        Claude'ga D:\SUNIYAGENT emas, %MANZIL% ni tanlab bering.
echo        Aks holda men eski nusxani tahrirlab yuraman.
echo.
echo   3^) Ishonch hosil qilgach, ESKI papkani o'chiring:
echo        %MANBA%
echo        ^(shoshilmang - bir-ikki kun tursin^)
echo.
echo   4^) NAIZA repositoriysidan OBER'ni chiqaring:
echo        cd /d D:\SUNIYAGENT
echo        git rm -r --cached ober
echo        echo ober/ ^>^> .gitignore
echo        git commit -m "OBER alohida loyihaga ajratildi"
echo        git push
echo.
echo      DIQQAT: bu OBER'ni kelajakdagi commitlardan chiqaradi,
echo      lekin ESKI commitlardan O'CHIRMAYDI. Agar bot kaliti
echo      allaqachon tushgan bo'lsa, u tarixda qoladi -
echo      shuning uchun @BotFather orqali kalitni almashtiring.
echo.
echo   5^) Yangi joyda o'z git'ini boshlang:
echo        cd /d %MANZIL%
echo        git init
echo        git add .
echo        git status        ^<-- ro'yxatni KO'Z BILAN o'qing
echo        git commit -m "OBER - teskari marketplace MVP"
echo.
pause
