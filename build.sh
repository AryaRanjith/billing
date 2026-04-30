#!/bin/bash
set -o errexit

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Running Django checks ==="
python manage.py check

echo "=== Running migrations ==="
python manage.py migrate --verbose

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput --verbosity 2

echo "=== Build complete ==="
