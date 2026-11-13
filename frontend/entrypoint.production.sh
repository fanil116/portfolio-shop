#!/bin/sh
set -e
# Клиентские ассеты отдаёт nginx из общего volume
cp -rf .output/public/_nuxt/. nuxt_volume/
exec "$@"
