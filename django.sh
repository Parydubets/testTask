#!/bin/bash
echo "Creating Migrations..."
python manage.py makemigrations djangoapp
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================


pytest testTask

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000
