from django.urls import path, include
from django.contrib import admin
from .views import ZipFileView
admin.autodiscover()


# /api/documents
urlpatterns = [
    # path('', FilesAPIView.as_view()),
    path('zipfiles/', ZipFileView.as_view()),
]
