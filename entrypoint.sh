#!/bin/sh

echo "📡 Checking if Postgres is ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "✅ Postgres is ready!"

echo "🚀 Running migrations..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# اجرای Gunicorn
echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -

#echo "🌍 Starting Django server..."
#python manage.py runserver 0.0.0.0:8000