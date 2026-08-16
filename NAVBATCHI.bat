@echo off
rem FAQAT ASCII! Maxsus belgi bo'lmasin.
rem
rem OBER - NAVBATCHI. Bir marta ishga tushiriladi va ochiq turadi.
rem
rem NEGA KERAK (2026-08-03): Claude terminalga yoza olmaydi. Har server
rem buyrug'i uchun alohida .bat yozib, Explorer ochib, yo'lni terib,
rem jurnalni o'qish kerak edi - har buyruq 5 qadam va 2-3 daqiqa.
rem Endi Claude faqat `data\buyruq.txt` ga yozadi, natijani
rem `data\javob.txt` dan o'qiydi. GUI umuman ishlatilmaydi.
rem
rem TO'XTATISH: shu oynani yoping yoki Ctrl+C.
chcp 65001 >nul
setlocal enabledelayedexpansion
set BUYRUQ=%~dp0data\buyruq.txt
set JAVOB=%~dp0data\javob.txt
set SERVER=root@77.42.123.90

echo ============================================================
echo   OBER NAVBATCHI - ishlayapti
echo.
echo   Bu oyna OCHIQ TURSIN.
echo   Claude buyruq bersa - shu yerda bajariladi.
echo   To'xtatish: oynani yoping.
echo ============================================================
echo.

:aylana
if exist "%BUYRUQ%" (
  echo [%TIME%] buyruq keldi
  echo OBER navbatchi - %DATE% %TIME% > "%JAVOB%"
  echo ============================================ >> "%JAVOB%"

  rem Buyruq faylining birinchi qatori - nima qilish kerakligi
  set /p AMAL=<"%BUYRUQ%"

  rem TEZKOR: FAQAT web/ - QAYTA YOQISH YO'Q. 2026-08-16.
  rem web ichidagi HTML, CSS va JS statik fayllar - server ularni
  rem diskdan o'qiydi. Ya'ni qayta yoqish umuman shart emas.
  rem To'liq yuklash ~100 soniya edi: app va web butunlay
  rem ko'chirilardi va uchta xizmat qayta yoqilardi. Frontend
  rem ishida bularning hech biri kerak emas.
  rem DIQQAT: blok ichidagi rem satrlarida qavs ishlatilmaydi.
  if "!AMAL!"=="web" (
    echo -- faqat web yuklanmoqda >> "%JAVOB%"
    scp -q -r "%~dp0web" %SERVER%:/home/ober/ober/ >> "%JAVOB%" 2>&1
    echo -- tayyor, qayta yoqilmadi >> "%JAVOB%"
  ) else if "!AMAL!"=="yuklash" (
    echo -- kod yuklanmoqda >> "%JAVOB%"
    scp -q -r "%~dp0app" %SERVER%:/home/ober/ober/ >> "%JAVOB%" 2>&1
    scp -q -r "%~dp0web" %SERVER%:/home/ober/ober/ >> "%JAVOB%" 2>&1
    scp -q "%~dp0data\telegram-kanallar.txt" %SERVER%:/home/ober/ober/data/ >> "%JAVOB%" 2>&1
    rem 2026-08-13: faqat ober-server restart qilinardi - ober-yangilik
    rem va ober-toliq eski kod bilan qolaverardi - avtoelon adapteri
    rem serverda yig'ilmagan edi. Endi uchalasi birga restart bo'ladi.
    rem IZOH: blok ichidagi rem satrlarida qavs ishlatilmaydi -
    rem muvozanatsiz qavs butun if blokini buzadi. 2026-08-13 xato.
    ssh -o BatchMode=yes %SERVER% systemctl restart ober-server ober-yangilik ober-toliq >> "%JAVOB%" 2>&1
    echo -- tayyor >> "%JAVOB%"
  ) else (
    rem Boshqa holatda: buyruq.txt ni skript deb serverda bajaramiz
    scp -q "%BUYRUQ%" %SERVER%:/tmp/ober-ish.sh >> "%JAVOB%" 2>&1
    ssh -o BatchMode=yes %SERVER% bash /tmp/ober-ish.sh >> "%JAVOB%" 2>&1
  )

  echo ---- TUGADI ---- >> "%JAVOB%"
  del "%BUYRUQ%" >nul 2>&1
  echo [%TIME%] bajarildi
)
timeout /t 3 /nobreak >nul
goto aylana
