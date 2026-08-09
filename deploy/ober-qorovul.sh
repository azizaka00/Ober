#!/bin/bash
# OBER qorovuli — sayt javob bermasa serverni qayta yoqadi.
#
# NEGA KERAK (2026-08-04):
# Sayt 14 soat davomida 502 berib turdi va HECH KIM BILMADI. systemd
# uchun xizmat "active (running)" edi — jarayon tirik, lekin ulanish
# navbatini qabul qilmayotgan edi. `Restart=always` bunday holatda
# yordam bermaydi: o'lmagan narsani qayta yoqmaydi.
#
# Shuning uchun tiriklikni JARAYON emas, JAVOB bilan o'lchaymiz.
#
# 2 marta ketma-ket javob bermasa qayta yoqiladi. Bir marta yetarli
# emas: yig'uvchi og'ir sikl bajarayotganda bitta so'rov kechikishi
# mumkin, bu nosozlik emas.

set -u

MANZIL="http://127.0.0.1:8800/"
BELGI="/tmp/ober-qorovul-xato"
KUTISH=10

kod=$(curl -s -o /dev/null -w "%{http_code}" --max-time "$KUTISH" "$MANZIL" || echo 000)

if [ "$kod" = "200" ]; then
    rm -f "$BELGI"
    exit 0
fi

xato=$(( $(cat "$BELGI" 2>/dev/null || echo 0) + 1 ))
echo "$xato" > "$BELGI"
logger -t ober-qorovul "javob $kod (ketma-ket $xato)"

if [ "$xato" -ge 2 ]; then
    logger -t ober-qorovul "QAYTA YOQILDI"
    systemctl restart ober-server
    rm -f "$BELGI"
fi
