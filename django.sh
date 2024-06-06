#!/bin/bash

echo "Creating Migrations..."
python manage.py makemigrations app
echo ====================================

echo "Starting Migrations..."
python manage.py migrate app
echo ====================================

python manage.py populate

pytest testTask --create-db


echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000
