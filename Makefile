install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

install-azure:
	pip install --upgrade pip &&\
		pip install -r requirements-azure.txt

lint:
	pylint --disable=R,C *.py

format:
	black *.py

test:
	python manage.py test