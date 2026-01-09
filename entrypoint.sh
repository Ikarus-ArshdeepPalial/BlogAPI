#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Wait for DB to be ready (optional but recommended, usually handled by depends_on healthchecks or wait scripts)
# for now we rely on docker-compose depends_on

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Check if we are in development or production
if [ "$DEBUG" = "1" ] || [ "$DEBUG" = "True" ]; then
    echo "Starting Development Server..."
    exec python manage.py runserver 0.0.0.0:8000
else
    echo "Starting Gunicorn Server..."
    # 4 workers is a standard starting point
    exec gunicorn Project.wsgi:application --bind 0.0.0.0:8000 --workers 4
fi
