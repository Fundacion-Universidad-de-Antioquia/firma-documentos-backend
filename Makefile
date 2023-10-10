install:
	# Instala dependencias
	python3 -m venv antenv
	. antenv/bin/activate
	pip install --upgrade pip
	pip install --target="./.python_packages/lib/site-packages" -r requirements.txt

lint:
	pylint --disable=R,C *.py

test:
	python manage.py test api.base.documents.tests --settings=firma.settings.staging

database:
	python3 manage.py migrate --settings=firma.settings.staging
