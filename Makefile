install:
	# Dependencies installation
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint --disable=R,C *.py

test:
	python3 manage.py test api.tests --settings=myproject.settings.staging

database:
	python3 manage.py migrate --settings=firma.settings.staging
	python manage.py makemigrations --settings=firma.settings.development