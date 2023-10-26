import os
from pathlib import Path

from firma.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_COOKIE_DOMAIN = '.azurewebsites.net'
CSRF_COOKIE_SECURE = True

# Create azure-test database connection for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    },
}

# Create blob endpoint to azurite storage for media files
AZURITE_DOCUMENTS_STORAGE = {
    'ACCOUNT_NAME': os.getenv('AZURITE_ACCOUNT_NAME', 'devstoreaccount1'),
    'ACCOUNT_KEY': os.getenv('AZURITE_ACCOUNT_KEY', 'Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=='),
    'ENDPOINT': os.getenv('AZURITE_ENDPOINT', 'http://127.0.0.1:10000/devstoreaccount1'),
    'CONTAINER': os.getenv('AZURITE_CONTAINER', 'media'),
    'URL': 'http://127.0.0.1:10000/devstoreaccount1/media-test/docs',
}

# Create blob endpoint connection to azure storage for media files
# Create azurite connetion for Django
AZURE_ACCOUNT_NAME = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME')
AZURE_STORAGE_KEY = os.environ.get('AZURE_SECRET_KEY')
AZURE_STORAGE_CONTAINER = os.environ.get('AZURE_STORAGE_CONTAINER_NAME')
AZURE_STORAGE_URL = os.environ.get('AZURE_STORAGE_URL')
AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING', 'DefaultEndpointsProtocol=https;AccountName=' + AZURE_ACCOUNT_NAME +';AccountKey=' + AZURE_STORAGE_KEY + ';BlobEndpoint=' + AZURE_STORAGE_URL)


# TODO: Add settings for celery broker in staging environment
# Celery confs
# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND")
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Bogota'
