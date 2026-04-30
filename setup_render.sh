#!/bin/bash
# Diagnostic script to fix common 500 errors

echo "Running Django checks..."
python manage.py check

echo ""
echo "Checking database..."
python manage.py migrate --no-input

echo ""
echo "Creating superuser (non-interactive)..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser 'admin' created with password 'admin123'")
else:
    print("Superuser already exists")
END

echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "Diagnostic complete!"
