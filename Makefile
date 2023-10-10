install:
	# Instala dependencias
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint --disable=R,C *.py

test:
	python manage.py test api.base.documents.tests --settings=firma.settings.staging

database:
	python3 manage.py migrate --settings=firma.settings.staging
