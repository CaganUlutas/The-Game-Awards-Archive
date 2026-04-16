#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing requirements..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Migrating database..."
python manage.py migrate

echo "Loading historic SQLite dump into PostgreSQL..."
python manage.py loaddata awards/fixtures/all_data.json
