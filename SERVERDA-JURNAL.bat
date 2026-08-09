@echo off
rem FAQAT ASCII! Maxsus belgi bo'lmasin.
rem OBER - server jurnalini faylga tushiradi: data\jurnal.txt
chcp 65001 >nul
set SERVER=root@77.42.123.90
set LOG=%~dp0data\jurnal.txt

echo OBER jurnal - %DATE% %TIME% > "%LOG%"
echo ==================== SERVER ==================== >> "%LOG%"
ssh -o BatchMode=yes %SERVER% journalctl -u ober-server -n 20 --no-pager >> "%LOG%" 2>&1
echo. >> "%LOG%"
echo ==================== YANGILIK ==================== >> "%LOG%"
ssh -o BatchMode=yes %SERVER% journalctl -u ober-yangilik -n 40 --no-pager >> "%LOG%" 2>&1
echo. >> "%LOG%"
echo ---- TUGADI ---- >> "%LOG%"
exit
