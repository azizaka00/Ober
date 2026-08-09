#!/bin/bash
# BAZADAGI ISH E'LONLARIDAN NARXNI OLIB TASHLASH.
#
# 2026-08-04: `telegram_manba.py` ga `ishmi()` qo'shildi — endi yangi
# ish e'lonlari narxsiz keladi. Lekin bazada allaqachon yig'ilganlari
# maosh bilan turibdi va bosh sahifadagi vitrinaga chiqyapti.
#
# Bu skript o'shalarni tuzatadi. Ish e'loni O'CHIRILMAYDI — u indeksda
# qoladi va qidiruvda topiladi. Faqat narxi olib tashlanadi, chunki
# maosh narx emas.
#
# Ishlatish:  bash ish-narxini-tozala.sh
set -eu

DB=/home/ober/ober/data/ober.db

echo "=== OLDIN ==="
sudo -u ober sqlite3 -header -column "$DB" "
SELECT substr(nom,1,40) nom, narx_som
FROM elonlar
WHERE manba='telegram' AND faol=1 AND narx_som>0
  AND (nom LIKE '%ISHGA TAKLIF%' OR nom LIKE '%kerak%' OR nom LIKE '%КЕРАК%'
       OR nom LIKE '%ВАКАНСИЯ%' OR nom LIKE '%Требует%' OR tavsif LIKE '%вакансия%'
       OR tavsif LIKE '%ishga taklif%' OR tavsif LIKE '%иш таклиф%')
ORDER BY narx_som DESC LIMIT 12;
"

sudo -u ober sqlite3 "$DB" "
UPDATE elonlar SET narx_som = NULL
WHERE manba='telegram' AND narx_som IS NOT NULL
  AND (
    tavsif LIKE '%ishga taklif%' OR tavsif LIKE '%иш таклиф%'
    OR tavsif LIKE '%вакансия%'  OR tavsif LIKE '%vakansiya%'
    OR tavsif LIKE '%требует%'   OR tavsif LIKE '%xodim kerak%'
    OR tavsif LIKE '%ходим керак%' OR tavsif LIKE '%ishchi kerak%'
    OR tavsif LIKE '%зарплата%'  OR tavsif LIKE '%oylik maosh%'
    OR tavsif LIKE '%ойлик маош%' OR tavsif LIKE '%резюме%'
    OR nom LIKE '%ISHGA TAKLIF%' OR nom LIKE '%ВАКАНСИЯ%'
    OR nom LIKE '%Требуется%'    OR nom LIKE '%КЕРАК%'
  );
SELECT 'narxi olib tashlandi: ' || changes();
"

# Savolga o'xshagan sarlavhalar — e'lon emas, kanaldagi oddiy xabar.
sudo -u ober sqlite3 "$DB" "
UPDATE elonlar SET faol = 0
WHERE manba='telegram' AND faol=1 AND (nom LIKE '%?' OR nom LIKE '%？');
SELECT 'savol-sarlavha o''chirildi: ' || changes();
"

echo
echo "=== KEYIN: vitrinaga nima tushadi ==="
sudo -u ober sqlite3 -header -column "$DB" "
SELECT substr(nom,1,38) nom, narx_som, manba
FROM elonlar
WHERE faol=1 AND rasm IS NOT NULL AND rasm<>'' AND narx_som>0
ORDER BY olindi DESC LIMIT 12;
"
