from django.urls import path, include
from django.contrib import admin
from . import views

admin.autodiscover()


# /api/employees
urlpatterns = [
    path('', views.EmployeesView.as_view()),

    # Create path for getting employee data status from view
    path('data_status/', views.employee_data_policies)
]