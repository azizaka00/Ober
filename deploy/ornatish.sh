#!/usr/bin/env bash
# OBER — serverga o'rnatish. Ubuntu 22.04 / 24.04 / 26.04 uchun.
#
# ISHLATISH (serverga root bo'lib kirgach):
#
#   bash ornatish.sh                 -- domensiz: http://SERVER_IP da ochiladi
#   bash ornatish.sh ober.uz         -- domen bilan: HTTPS avtomatik
#
# Domen hali yo'q bo'lsa birinchi shaklni ishlating. Domen olganingizda
# skriptni domen bilan qayta yurgizasiz — hech narsa buzilmaydi.
#
# Nima qiladi:
#   1. `ober` foydalanuvchisini yaratadi (root ostida ishlatmaymiz)
#   2. Python va Caddy o'rnatadi
#   3. Ikkita xizmatni yoqadi: server va yangilik sikli
#   4. HTTPS ni sozlaydi
#
# Kod O'ZI ko'chirilmaydi — uni siz yuklaysiz (pastda yozilgan).

set -euo pipefail

ISHCHI=ober
UY=/home/$ISHCHI
LOYIHA=$UY/ober
DOMEN="${1:-}"

echo "=============================================="
echo "  OBER — serverga o'rnatish"
echo "=============================================="

if [ "$(id -u)" -ne 0 ]; then
  echo "  Root kerak:  sudo bash ornatish.sh"
  exit 1
fi

echo
echo "[1/7] Tizim yangilanmoqda..."
apt-get update -qq
apt-get install -y -qq python3 python3-venv ca-certificates curl \
  debian-keyring debian-archive-keyring apt-transport-https \
  fail2ban ufw

echo "[2/7] SSH himoyasi..."
# SSH kaliti o'rniga parol ishlatilyapti. Internetdagi botlar SSH portini
# tinmay urib turadi — kuniga minglab urinish, bu normal holat.
# fail2ban 5 marta xato parol kiritgan IP'ni 1 soatga bloklaydi.
cat >/etc/fail2ban/jail.local <<'EOF'
[sshd]
enabled  = true
maxretry = 5
findtime = 600
bantime  = 3600
EOF
systemctl enable --now fail2ban >/dev/null 2>&1 || true

# Faqat kerakli portlar ochiq: SSH, HTTP, HTTPS. Boshqasi yopiq.
ufw --force reset >/dev/null 2>&1 || true
ufw default deny incoming >/dev/null
ufw default allow outgoing >/dev/null
ufw allow 22/tcp  >/dev/null
ufw allow 80/tcp  >/dev/null
ufw allow 443/tcp >/dev/null
ufw --force enable >/dev/null

echo "[3/7] Foydalanuvchi: $ISHCHI"
if ! id "$ISHCHI" >/dev/null 2>&1; then
  adduser --system --group --home "$UY" --shell /bin/bash "$ISHCHI"
fi
mkdir -p "$LOYIHA/data" "$LOYIHA/app" "$LOYIHA/web"
chown -R "$ISHCHI:$ISHCHI" "$UY"

echo "[4/7] Caddy (HTTPS) o'rnatilmoqda..."
if ! command -v caddy >/dev/null 2>&1; then
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' \
    | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
    | tee /etc/apt/sources.list.d/caddy-stable.list >/dev/null
  apt-get update -qq
  apt-get install -y -qq caddy
fi
mkdir -p /var/log/caddy
chown -R caddy:caddy /var/log/caddy

echo "[5/7] Xizmatlar sozlanmoqda..."
if [ -f "$LOYIHA/deploy/ober-server.service" ]; then
  cp "$LOYIHA/deploy/ober-server.service"   /etc/systemd/system/
  cp "$LOYIHA/deploy/ober-yangilik.service" /etc/systemd/system/
  cp "$LOYIHA/deploy/ober-toliq.service"    /etc/systemd/system/

  if [ -n "$DOMEN" ]; then
    # Domen bor — Caddy sertifikatni o'zi oladi va HTTPS'ga o'tkazadi.
    sed "s/ober\.uz/$DOMEN/g" "$LOYIHA/deploy/Caddyfile" >/etc/caddy/Caddyfile
    MANZIL="https://$DOMEN"
  else
    # Domen yo'q — IP orqali oddiy HTTP. Sayt bugunoq ishlaydi, HTTPS esa
    # domen olingach qo'shiladi. Sertifikat IP manzilga berilmaydi,
    # shuning uchun bu bosqichda HTTPS texnik jihatdan mumkin emas.
    IP=$(hostname -I | awk '{print $1}')
    cat >/etc/caddy/Caddyfile <<EOF
:80 {
	encode gzip zstd
	reverse_proxy 127.0.0.1:8800
	request_body {
		max_size 6MB
	}
	header {
		X-Content-Type-Options nosniff
		-Server
	}
}
EOF
    MANZIL="http://$IP"
  fi
else
  echo
  echo "  DIQQAT: $LOYIHA hali bo'sh."
  echo "  Kodni yuklang, keyin shu skriptni qayta ishga tushiring:"
  echo
  echo "    Windows'dagi kompyuteringizdan:"
  echo "      scp -r D:\\SUNIYAGENT\\ober\\app  root@SERVER_IP:$LOYIHA/"
  echo "      scp -r D:\\SUNIYAGENT\\ober\\web  root@SERVER_IP:$LOYIHA/"
  echo "      scp -r D:\\SUNIYAGENT\\ober\\deploy root@SERVER_IP:$LOYIHA/"
  echo "      scp D:\\SUNIYAGENT\\ober\\data\\*.txt root@SERVER_IP:$LOYIHA/data/"
  echo
  echo "  Bazani ham ko'chirsangiz (115 000 e'lon tayyor keladi):"
  echo "      scp D:\\SUNIYAGENT\\ober\\data\\ober.db root@SERVER_IP:$LOYIHA/data/"
  echo
  exit 0
fi

systemctl daemon-reload
systemctl enable --now ober-server.service
systemctl enable --now ober-yangilik.service
systemctl enable --now ober-toliq.service
systemctl reload caddy || systemctl restart caddy

echo "[6/7] Kunlik zaxira nusxa..."
cat >/etc/cron.daily/ober-zaxira <<'EOF'
#!/bin/sh
# Baza — butun boyligimiz. Kuniga bir marta nusxa, 7 kunlik tarix.
D=/home/ober/ober/data
mkdir -p "$D/zaxira"
/usr/bin/sqlite3 "$D/ober.db" ".backup '$D/zaxira/ober-$(date +%u).db'" 2>/dev/null \
  || cp "$D/ober.db" "$D/zaxira/ober-$(date +%u).db"
EOF
chmod +x /etc/cron.daily/ober-zaxira
apt-get install -y -qq sqlite3

echo "[7/7] Tekshiruv..."
sleep 3
systemctl --no-pager --lines=5 status ober-server.service || true

echo
echo "=============================================="
echo "  TAYYOR"
echo
echo "  SAYT:  ${MANZIL:-http://SERVER_IP}"
echo
echo "  Holat:      systemctl status ober-server"
echo "  Jurnal:     journalctl -u ober-server -f"
echo "  Yangilik:   journalctl -u ober-yangilik -f"
echo "  To'liq:     journalctl -u ober-toliq -f"
echo "  Qayta:      systemctl restart ober-server"
echo
if [ -z "$DOMEN" ]; then
  echo "  Domen olganingizda shuni bajaring (HTTPS o'zi qo'shiladi):"
  echo "    bash $LOYIHA/deploy/ornatish.sh ober.uz"
  echo "  Undan oldin DNS: ober.uz -> shu serverning IP manzili"
fi
echo "=============================================="
