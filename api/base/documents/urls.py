from django.urls import path, include
from rest_framework import routers
from .views import ZipFileView, FilesAPIView


# /api/documents
urlpatterns = [
    path('', FilesAPIView.as_view()),
    path('upload_zip', ZipFileView.as_view()),
]
