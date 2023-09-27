from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from .views import ZipFileView, FilesAPIView
admin.autodiscover()


# /api/documents
urlpatterns = [
    # path('', FilesAPIView.as_view()),
    path('zipfiles/', ZipFileView.as_view()),
]
