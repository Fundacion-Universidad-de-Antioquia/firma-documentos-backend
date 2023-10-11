#!/bin/bash -v 
# pip install -r requirements.txt

# export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex())')

# Install dependencies
# sudo apt-get  install libpq-dev python-dev libpq-dev python3-dev -y

# Start Celery worker
# set -o errexit
# set -o nounset

# Create database tables
# python manage.py migrate --settings=firma.settings.development

# Start with runserver
python3 manage.py runserver 127.0.0.1:8000 --settings=firma.settings.staging &
echo "Firmas app is running"
