from django.urls import path, include
from rest_framework import routers
from . import views


# /api/documents
urlpatterns = [
    # path('', views.files_list_upload_view),
    path('', views.UploadZipFile.as_view()),
]
