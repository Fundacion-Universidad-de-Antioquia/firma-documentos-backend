import os
from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from azure.storage.blob import BlobServiceClient, BlobClient

from api.base.documents.models import ZipFile
from utils.azure_services import connect_to_azure_storage, open_storage_container

User = get_user_model()
# Create tests for ZipFile class
class ZipFileTestCase(APITestCase):

    def setUp(self):
        print("Setup testing environment")
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testapi', password='testapi')
        self.client.force_authenticate(user=self.user)
        self.good_zip = "/home/juanpa/FudeA/firma_digital/firma/media/good_docs.zip"
        self.bad_zip = "/home/juanpa/FudeA/firma_digital/firma/media/bad_docs.zip"
        self.blob_service_client = connect_to_azure_storage()

    # Create a test to open Azure storage connection
    def test_open_azure_connection(self):
        blob_container = self.blob_service_client.get_container_client("doc-devel")
        self.assertEqual(blob_container.container_name, "doc-devel")
        self.blob_service_client.close()

        
    # Test uploading file to Azure
    def test_upload_file_azure(self):
        blob_container = self.blob_service_client.get_container_client("doc-devel")
        blob_client = blob_container.get_blob_client("good_docs.zip")
        print("Upload Good Zip")

        with open(file=os.path.join("/home/juanpa/FudeA/firma_digital/firma/media/good_docs.zip"), mode="rb") as data:
            self.assertIsInstance(blob_client.upload_blob(data), dict, "Error uploading file to Azure")

        self.blob_service_client.close()
