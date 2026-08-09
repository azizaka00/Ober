#!/usr/bin/env bash
# OBER — Telegram yozuvlarini tozalab, qaytadan yig'ish.
#
# NEGA ALOHIDA FAYL: cmd -> ssh -> bash zanjirida tirnoq belgilari
# buzilib ketadi ("Error: in prepare, incomplete input"). Skript
# fayl bo'lib ko'chirilsa, hech qanday qochirish kerak emas.
#
# OLX ma'lumotiga TEGILMAYDI - faqat manba='telegram'.
set -uo pipefail

DB=/home/ober/ober/data/ober.db
APP=/home/ober/ober/app

echo "=== Telegram yozuvlari ==="
sqlite3 "$DB" "SELECT 'oldin: ' || COUNT(*) FROM elonlar WHERE manba='telegram';"

sqlite3 "$DB" "DELETE FROM elonlar WHERE manba='telegram';"
echo "o'chirildi"

cd "$APP" || exit 1

echo
echo "=== Qaytadan yig'ish (6 sahifa) ==="
python3 telegram_yig.py 6

echo
echo "=== Qidiruv indeksi qayta qurilmoqda ==="
python3 fts_qur.py

echo
sqlite3 "$DB" "SELECT 'keyin: ' || COUNT(*) FROM elonlar WHERE manba='telegram';"
sqlite3 "$DB" "SELECT 'eng arzon: ' || MIN(narx_som) || '  eng qimmat: ' || MAX(narx_som) FROM elonlar WHERE manba='telegram' AND narx_som > 0;"
