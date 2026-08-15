@echo off
rem FAQAT ASCII! Maxsus belgi bo'lmasin.
rem
rem OBER - Digital Asset Links faylini yozadi.
rem Butun mantiq app\assetlinks_kirit.py da. Bu fayl ishga tushirgich.
rem
rem Usiz TWA ilova ochilganda tepada brauzer manzil satri turadi.
rem Xato xabari chiqmaydi - shunchaki ilovaga o'xshamaydi.
chcp 65001 >nul
python "%~dp0app\assetlinks_kirit.py"
pause
