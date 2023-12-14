from azure.storage.blob import BlobServiceClient
from django.conf import settings
from firma.settings.development import AZURE_STORAGE_CONNECTION_STRING, AZURE_STORAGE_CONTAINER

# Create a function con connect to azure blob storage, the credentials are in settings.py
def connect_to_azure_storage():
    blob_client = BlobServiceClient.from_connection_string(conn_str=settings.AZURE_STORAGE_CONNECTION_STRING)
    print(f'Connection string: {settings.AZURE_STORAGE_CONNECTION_STRING}')
    return blob_client

# Create function to open connecton to Azure Storage
def open_storage_container(blob_client):

    container_service = blob_client.get_container_client(AZURE_STORAGE_CONTAINER)

    return container_service
