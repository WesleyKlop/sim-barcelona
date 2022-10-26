#!/usr/bin/env bash

set -euo pipefail

xset s noblank
xset s off
xset -dpms

unclutter -root &

exec /usr/bin/chromium-browser \
	--noerrdialogs \
	--disable-infobars \
	--disable-features=Translate \
	--kiosk \
	"http://localhost"
