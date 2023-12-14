Write-Host "Collect static"
python manage.py collectstatic --noinput

Write-Host "------------------------->Start migratons"
python manage.py makemigrations --settings=firma.settings.development --noinput 2>&1
python manage.py migrate --settings=firma.settings.development 2>&1


Write-Host "---------------------> Starting Firmas app"
Start-Job { python -m celery -A firma worker 2>&1 }
python manage.py runserver 0.0.0.0:8000 --settings=firma.settings.development 2>&1