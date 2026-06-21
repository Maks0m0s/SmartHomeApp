#!/bin/bash
set -e

# ============================================
# SmartHomeApp - Raspberry Pi Setup Script
# ============================================

APP_DIR="/home/pi/SmartHomeApp"
DOMAIN="yourdomain.duckdns.org"
PI_USER="pi"

echo "=== Updating system ==="
sudo apt update && sudo apt upgrade -y

echo "=== Installing system dependencies ==="
sudo apt install -y python3-pip python3-venv git curl

echo "=== Installing Caddy ==="
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update && sudo apt install -y caddy

echo "=== Setting up Python venv ==="
cd "$APP_DIR"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Running build ==="
bash build.sh

echo "=== Setting up systemd service ==="
sudo cp "$APP_DIR/deploy/gunicorn.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn

echo "=== Configuring Caddy ==="
sudo cp "$APP_DIR/Caddyfile" /etc/caddy/Caddyfile
sudo systemctl enable caddy
sudo systemctl restart caddy

echo "=== Setting up DuckDNS cron job ==="
chmod +x "$APP_DIR/deploy/duckdns.sh"
(crontab -l 2>/dev/null; echo "*/5 * * * * $APP_DIR/deploy/duckdns.sh") | crontab -

echo "=== Setup complete! ==="
echo "Before running, edit the .env file and deploy/duckdns.sh with your domain and tokens."
echo "Then run: sudo systemctl restart gunicorn && sudo systemctl restart caddy"
