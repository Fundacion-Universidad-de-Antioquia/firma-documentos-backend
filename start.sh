#!/bin/bash -v 
# pip install -r requirements.txt

# export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex())')

# Start Celery worker
set -o errexit
set -o nounset

# Create database tables
# python manage.py migrate --settings=firma.settings.development

# Start with runserver
python3 manage.py runserver --settings=firma.settings.staging &&
python3 -m celery -A firma worker
