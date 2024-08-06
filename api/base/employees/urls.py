from django.urls import path, include
from django.contrib import admin

from . import views

admin.autodiscover()


# /api/employees
urlpatterns = [
    path('', views.EmployeesView.as_view()),

    # Create path for getting employee data status from view
    path('data_status/', views.employee_data_policies),
    path('image_profile/', views.image_profile),
    path('list_options/', views.list_options),
    path('sign_documents/', views.sign_documents),
    path('employee_sons/', views.employee_sons),
    path('academics/', views.employee_academic),
    
    
    # path('employee_files/', views.employee_files)
]