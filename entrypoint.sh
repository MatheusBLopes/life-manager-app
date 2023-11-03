#!/bin/bash

# Collect static files
python life-manager-app/manage.py collectstatic --no-input

# Start App
gunicorn -c gunicorn_config.py life_manager_app.wsgi:application
