import sys
from firma.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# Create SECRET_KEY VARIABLE with the secret key value
SECRET_KEY = '1c153c54d3b21a8ad94a766e4fb2427e816a5092990957923c27c4335f198cdb'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    },
}

if 'test' in sys.argv or 'test\_coverage' in sys.argv: #Covers regular testing and django-coverage
 DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
 DATABASES['default']['NAME'] = ':memory:'

# Create azurite connetion for Django
AZURE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
AZURE_SECRET_KEY = os.getenv('AZURE_SECRET_KEY')
AZURE_STORAGE_CONTAINER = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
AZURE_STORAGE_URL = os.getenv('AZURE_STORAGE_URL')
AZURE_STORAGE_CONNECTION_STRING = ('DefaultEndpointsProtocol=https;AccountName='
    f'{AZURE_ACCOUNT_NAME};'+
    f'AccountKey={AZURE_SECRET_KEY};'
    f'BlobEndpoint={AZURE_STORAGE_URL}')


# Celery confs
# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_BROKER_URL = os.getenv('CELERY_BROKER')
CELERY_RESULT_BACKEND = os.getenv('CELERY_BACKEND')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Bogota'
