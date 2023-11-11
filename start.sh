#!/bin/bash -v 
# . antenv/bin/activate
# pip install -r requirements.txt

# export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex())')

# Install dependencies
# sudo apt-get  install libpq-dev python-dev libpq-dev python3-dev -y

# Start Celery worker
# set -o errexit
# set -o nounset

echo "Collect static"
python manage.py collectstatic --noinput

# Create database tables
echo "------------------------->Start migratons"
python3 manage.py makemigrations --settings=firma.settings.staging --noinput 1>&2
python3 manage.py migrate --settings=firma.settings.staging 1>&2

# Start with runserver
echo "---------------------> Starting Firmas app"
python3 -m celery -A firma worker 1>&2 &
python3 manage.py runserver 0.0.0.0:8000 --settings=firma.settings.staging 1>&2
