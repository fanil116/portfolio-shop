#!/bin/sh
# Basic-auth для /admin/: значение берётся из ADMIN_HTPASSWD (формат user:{PLAIN}password).
set -e
echo "$ADMIN_HTPASSWD" > /etc/nginx/conf.d/admin_htpasswd
