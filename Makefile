install:
	# Instala dependencias
	pip install --upgrade pip &&\
		pip install -r requirements.txt

install-azure:
	pip install --upgrade pip &&\
		pip install -r requirements-azure.txt

lint:
	pylint --disable=R,C *.py

test:
	python manage.py test api.base.documents.tests --settings=firma.settings.staging