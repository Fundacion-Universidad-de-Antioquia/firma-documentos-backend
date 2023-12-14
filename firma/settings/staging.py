import os
from pathlib import Path

from firma.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["webapp-firma-backend.azurewebsites.net", "*"]
CSRF_TRUSTED_ORIGINS = ["https://webapp-firma-backend.azurewebsites.net"]
CSRF_ALLOWED_ORIGINS = ["https://webapp-firma-backend.azurewebsites.net"]
CORS_ORIGINS_WHITELIST = ["https://webapp-firma-backend.azurewebsites.net"]
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


# Create blob endpoint connection to azure storage for media files
# Create azurite connetion for Django
AZURE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
AZURE_STORAGE_KEY = os.getenv('AZURE_SECRET_KEY')
AZURE_STORAGE_CONTAINER = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
AZURE_STORAGE_URL = os.getenv('AZURE_STORAGE_URL')
AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING', 'DefaultEndpointsProtocol=https;AccountName=' + AZURE_ACCOUNT_NAME +';AccountKey=' + AZURE_STORAGE_KEY + ';BlobEndpoint=' + AZURE_STORAGE_URL)


# TODO: Add settings for celery broker in staging environment
# Celery confs
# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_BROKER_URL = os.getenv("CELERY_BROKER")
CELERY_RESULT_BACKEND = os.getenv("CELERY_BACKEND")
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Bogota'
