#!/bin/bash
set -e

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Seed demo data
echo "Seeding demo data..."
python manage.py seed_data

# Start gunicorn
echo "Starting gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}

