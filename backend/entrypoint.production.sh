#!/bin/sh
set -e
python wait-for
uv run --no-sync python manage.py migrate --noinput
uv run --no-sync python manage.py collectstatic --noinput
exec "$@"
