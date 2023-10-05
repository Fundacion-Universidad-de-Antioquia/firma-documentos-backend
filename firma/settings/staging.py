import os
from pathlib import Path

from firma.settings.base import *

AZURE_ACCOUNT_NAME = "storageaccountfirma"
AZURE_STORAGE_KEY = "Rjl41EFt/rSmPdAmEtyyuX//KAf2TT3c1PkBjpF5f+KoBt/pdpc1QcI414swgOgwrV30L8YnRWb/+ASth4gG0A=="
AZURE_STORAGE_CONTAINER = "docs"

# Create azure-test database connection for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB1', 'db_firmas_staging'),
        'USER': os.getenv('POSTGRES_USER1', 'prueba_dbf'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD1', '42HOxdl.2W`i:G~@,|VM'),
        'HOST': os.getenv('POSTGRES_HOST1', 'db-firmas-pg.postgres.database.azure.com'),
        'PORT': os.getenv('POSTGRES_PORT1', '5432'),
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
AZURE_ACCOUNT_NAME = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME', 'storageaccountfirma')
AZURE_STORAGE_KEY = os.environ.get('AZURE_SECRET_KEY', 'Rjl41EFt/rSmPdAmEtyyuX//KAf2TT3c1PkBjpF5f+KoBt/pdpc1QcI414swgOgwrV30L8YnRWb/+ASth4gG0A==')
AZURE_STORAGE_CONTAINER = os.environ.get('AZURE_STORAGE_CONTAINER_NAME', 'docs')
AZURE_STORAGE_URL = os.environ.get('AZURE_STORAGE_URL', 'https://storageaccountfirma.blob.core.windows.net/')
AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING', 'DefaultEndpointsProtocol=https;AccountName=' + AZURE_ACCOUNT_NAME +';AccountKey=' + AZURE_STORAGE_KEY + ';BlobEndpoint=' + AZURE_STORAGE_URL)


# TODO: Add settings for celery broker in staging environment
# Celery confs
# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_BACKEND", "redis://127.0.0.1:6379/0")
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Bogota'
