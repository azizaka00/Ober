@echo off
rem FAQAT ASCII! Maxsus belgi bo'lmasin.
rem
rem OBER - GIT YUKLASH. Bir marta bosiladi, hammasini o'zi qiladi.
rem
rem NEGA KERAK (2026-08-22): Claude git'ni yugurta olmaydi. Bog'langan
rem papka orqali git vaqtinchalik fayllarni o'chira olmaydi
rem ("unable to unlink .git/objects/.../tmp_obj_..."), shuning uchun
rem `git add` yarim yo'lda yiqiladi. Push uchun esa GitHub kaliti
rem kerak va uni Claude'ga bermaslik kerak.
rem
rem Shuning uchun ish shunday bo'lindi: commit MATNLARINI va
rem TARTIBINI Claude yozadi, bajarishni bu skript qiladi.
rem
rem XAVFSIZ: hech narsa o'chirilmaydi (`_to_delete` dan tashqari - u
rem Claude qoldirgan bo'sh qulf fayllari). Har commit alohida
rem tekshiriladi; qo'shiladigan narsa bo'lmasa o'tkazib yuboriladi.

chcp 65001 >nul
cd /d "%~dp0"

echo ============================================================
echo   OBER - GIT YUKLASH
echo ============================================================
echo.

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
  echo   XATO: bu papka git repo emas.
  pause
  exit /b 1
)

rem ---- 1. GITIGNORE ----
echo [1/7] gitignore tekshirilmoqda...
findstr /c:"_to_delete/" .gitignore >nul 2>&1
if errorlevel 1 (
  echo.>> .gitignore
  echo # Vaqtinchalik axlat va tashqi zaxira ^(2026-08-22^)>> .gitignore
  echo _to_delete/>> .gitignore
  echo   qo'shildi: _to_delete/
)
findstr /c:"zaxira-tashqi/*.sql.gz" .gitignore >nul 2>&1
if errorlevel 1 (
  echo zaxira-tashqi/*.sql.gz>> .gitignore
  echo   qo'shildi: zaxira-tashqi/*.sql.gz
)

rem ---- 2. AXLATNI OLIB TASHLASH ----
if exist "_to_delete" (
  rmdir /s /q "_to_delete"
  echo   _to_delete o'chirildi
)

echo.
echo [2/7] gitignore commit...
call :commit ".gitignore" "gitignore: vaqtinchalik axlat va zaxira fayllari"

echo [3/7] MCP serveri...
call :commit "AGENT-REJA.md app\mcp_server.py app\mcp_sinov.py" "MCP serveri: qidir + sorov_yubor + javoblar, 95 sinov"

echo [4/7] Xato holatlari...
call :commit "web\takliflar.html web\kategoriyalar.html web\sotuvchi.html app\web_sinov.py app\xato_xabar.py app\xato_sinov.py" "Xato holatlari yolgon gapirmasin: 401 tarmoq xatosi emas"

echo [5/7] Nazorat va zaxira...
call :commit "app\havola_nazorat.py app\havola_sinov.py app\zaxira_shaxsiy.py app\manba_qorovul.py app\manba_sinov.py" "Havola nazorati, tashqi zaxira va manba qorovuli"

echo [6/7] Qolgan hammasi...
git add -A
git diff --cached --quiet
if errorlevel 1 (
  git commit -m "Kesh isitgichi, mmap, assetlinks, saboqlar va hisobotlar"
  echo   commit qilindi
) else (
  echo   yangi narsa yo'q
)

rem assetlinks nuqtali papkada - ba'zi qoidalar uni chetlaydi.
if exist "web\.well-known\assetlinks.json" (
  git ls-files --error-unmatch "web/.well-known/assetlinks.json" >nul 2>&1
  if errorlevel 1 (
    git add -f "web\.well-known\assetlinks.json"
    git commit -m "assetlinks.json: TWA toliq ekran uchun"
    echo   assetlinks majburan qo'shildi
  )
)

echo.
echo [7/7] GitHub'ga yuborilmoqda...
git push
if errorlevel 1 (
  echo.
  echo   PUSH O'TMADI.
  echo   Agar parol so'ragan bo'lsa - GitHub parolni qabul qilmaydi,
  echo   Personal Access Token kerak. Claude'ga ayting.
) else (
  echo   Yuborildi.
)

echo.
echo ============================================================
git log --oneline -8
echo ============================================================
echo.
echo   Yakuniy holat:
git status --short
echo.
pause
exit /b 0

rem ---- commit yordamchisi: %1 fayllar, %2 xabar ----
:commit
git add %~1 2>nul
git diff --cached --quiet
if errorlevel 1 (
  git commit -m "%~2" >nul
  echo   commit qilindi
) else (
  echo   yangi narsa yo'q, o'tkazildi
)
exit /b 0
