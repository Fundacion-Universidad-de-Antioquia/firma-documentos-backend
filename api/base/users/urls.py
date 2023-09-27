from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from api.base.users import views
admin.autodiscover()

# /api/documents
urlpatterns = [
    # Create login and logout urls
    path('', views.UserList.as_view()),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('rtoken/', views.TokenRefresh.as_view, name='rtoken'),
]
