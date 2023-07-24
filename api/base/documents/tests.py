from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User

from api.base.documents.models import ZipFile

# Create tests for ZipFile class
class ZipFileTestCase(APITestCase):

    def setUp(self):
        print("Testing API Start")
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testapi', password='testapi')
        self.client.force_authenticate(user=self.user)
        self.good_zip = "/home/juanpa/FudeA/firma_digital/firma/media/good_docs.zip"
        self.bad_zip = "/home/juanpa/FudeA/firma_digital/firma/media/bad_docs.zip"

    # Create a test to upload a good ZipFile
    def test_upload_good_zip_file(self):
        data = {
            "path": self.good_zip
        }

        print("Testing good Zip")

        user = User.objects.get(username='testapi')
        client = APIClient()
        client.force_authenticate(user=user, token='zeMiK2nPYPKpgRjOSqo7Z6Jz0gzWSh')

        request = client.post("/api/documents/upload_zip", data, format='multipart')

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    # Create a test to upload a bad ZipFile
    def test_upload_bad_zip_file(self):
        data = {
            "path": self.bad_zip
        }
        print("Testing bad Zip")
        user = User.objects.get(username='testapi', token='zeMiK2nPYPKpgRjOSqo7Z6Jz0gzWSh')
        client = APIClient()
        client.force_authenticate(user=user)

        request = client.post("/api/documents/upload_zip", data, format='multipart')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
