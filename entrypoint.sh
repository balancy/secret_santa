#!/bin/sh

python manage.py migrate --no-input
gunicorn secret_santa.wsgi:application --bind 0.0.0.0:8080