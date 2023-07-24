from django.urls import path, include
from rest_framework import routers
from api.base.users import views


# /api/documents
urlpatterns = [
    # Create login and logout urls
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.UserList.as_view()),
    path('rtoken/', views.TokenRefresh.as_view, name='rtoken'),
]
