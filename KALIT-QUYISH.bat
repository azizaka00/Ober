@echo off
rem FAQAT ASCII! Maxsus belgi bo'lmasin.
rem
rem OBER - serverga PAROLSIZ ulanishni sozlash.
rem Bir marta bajariladi. Undan keyin YUKLASH.bat parol so'ramaydi.
chcp 65001 >nul
setlocal
set SERVER=root@77.42.123.90

echo ============================================================
echo   OBER - parolsiz ulanishni sozlash
echo.
echo   Bu bir martalik ish. Parolni OXIRGI MARTA kiritasiz,
echo   keyin yuklash bir bosishda bo'ladi.
echo ============================================================
echo.

if exist "%USERPROFILE%\.ssh\id_ed25519.pub" (
  echo   [1/2] SSH kaliti allaqachon bor - yangisi yaratilmaydi.
) else (
  echo   [1/2] SSH kaliti yaratilmoqda...
  if not exist "%USERPROFILE%\.ssh" mkdir "%USERPROFILE%\.ssh"
  ssh-keygen -t ed25519 -N "" -C "ober-deploy" -f "%USERPROFILE%\.ssh\id_ed25519"
  if errorlevel 1 (
    echo   Kalit yaratilmadi. Windowsda OpenSSH yoqilganini tekshiring.
    pause
    exit /b 1
  )
)

echo.
echo   [2/2] Kalit serverga qo'yilmoqda.
echo   ENDI PAROL SO'RALADI - oxirgi marta.
echo.

type "%USERPROFILE%\.ssh\id_ed25519.pub" | ssh %SERVER% "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && echo QUYILDI"

if errorlevel 1 (
  echo.
  echo   Xato. Parol to'g'ri kiritilganini tekshiring.
  pause
  exit /b 1
)

echo.
echo   Tekshirilmoqda (parol SO'RALMASLIGI kerak)...
ssh -o BatchMode=yes %SERVER% "echo '  OK - parolsiz ulanish ishlayapti'"
if errorlevel 1 (
  echo   Parolsiz ulanish ishlamadi. Qayta urinib ko'ring.
  pause
  exit /b 1
)

echo.
echo ============================================================
echo   TAYYOR. Endi YUKLASH.bat ni bosish yetarli.
echo ============================================================
pause
