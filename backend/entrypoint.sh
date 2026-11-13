#!/bin/sh
set -e
python wait-for
uv run python manage.py migrate --noinput
exec "$@"
