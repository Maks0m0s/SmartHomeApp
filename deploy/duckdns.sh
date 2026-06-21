#!/bin/bash
# DuckDNS auto-update script
# Add to crontab: */5 * * * * /home/pi/SmartHomeApp/deploy/duckdns.sh

DOMAIN="shomeapp"
TOKEN="faa0e007-1f2d-4f85-af31-1c8478de1707"

curl -s "https://www.duckdns.org/update?domains=$DOMAIN&token=$TOKEN&ip="
