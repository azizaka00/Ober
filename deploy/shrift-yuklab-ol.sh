#!/bin/bash
# ONEST SHRIFTINI GOOGLE'DAN BIR MARTA YUKLAB OLISH.
#
# `web/shrift/*.woff2` fayllari ikkilik (binary) — ular loyiha papkasida
# saqlanmaydi. Yangi serverga chiqqanda yoki fayllar yo'qolsa, shu
# skript ularni qaytadan tiklaydi.
#
# Ishlatish:  bash shrift-yuklab-ol.sh
#
# Onest o'zgaruvchan shrift: har alifbo uchun BITTA fayl 400-800
# qalinlikni qoplaydi. Google CSS'i har qalinlik uchun alohida URL
# beradi, lekin ular bir xil faylga qaraydi — shuning uchun faqat
# birinchisini olamiz. (2026-08-04 da md5sum bilan tekshirilgan.)

set -eu

SHR="${1:-/home/ober/ober/web/shrift}"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
URL="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;800&display=swap"

mkdir -p "$SHR"
curl -sf -A "$UA" "$URL" -o /tmp/onest-google.css

python3 - "$SHR" <<'PY'
import os, re, sys, urllib.request

shr = sys.argv[1]
css = open('/tmp/onest-google.css', encoding='utf-8').read()
kerak = ('latin', 'latin-ext', 'cyrillic', 'cyrillic-ext')
korilgan = set()

for blok in re.split(r'(?=/\*)', css):
    nom = re.search(r'/\*\s*([a-z-]+)\s*\*/', blok)
    url = re.search(r'url\((https://[^)]+\.woff2)\)', blok)
    if not (nom and url):
        continue
    alifbo = nom.group(1)
    if alifbo not in kerak or alifbo in korilgan:
        continue
    korilgan.add(alifbo)
    yol = os.path.join(shr, f'onest-{alifbo}.woff2')
    urllib.request.urlretrieve(url.group(1), yol)
    print(f'  onest-{alifbo}.woff2  {os.path.getsize(yol) // 1024} KB')

yoq = set(kerak) - korilgan
if yoq:
    raise SystemExit(f'XATO: olinmadi -> {", ".join(sorted(yoq))}')
PY

# Fayllarni server foydalanuvchisiga bering, aks holda 403 chiqadi.
if id ober >/dev/null 2>&1; then
    chown -R ober:ober "$SHR"
fi

echo "Tayyor: $SHR"
