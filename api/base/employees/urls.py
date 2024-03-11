from django.urls import path, include
from django.contrib import admin
from . import views

admin.autodiscover()


# /api/employees
urlpatterns = [
    path('', views.EmployeesView.as_view())
]