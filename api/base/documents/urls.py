from django.urls import path, include
from rest_framework import routers
from . import views


# /api/documents
urlpatterns = [
    # path('', views.files_list_upload_view),
    path('', views.UploadFilesView.as_view()),
]
