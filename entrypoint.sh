#!/bin/sh

echo "📡 Checking if Postgres is ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "✅ Postgres is ready!"

echo "🚀 Running migrations..."
python manage.py migrate --noinput

echo "🌍 Starting Django server..."
python manage.py runserver 0.0.0.0:8000