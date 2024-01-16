from django.urls import path, include
from django.contrib import admin
from .views import EmployeesView
admin.autodiscover()


# /api/documents
urlpatterns = [
    path('employees/', EmployeesView.as_view()),
]