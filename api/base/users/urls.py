from django.urls import path, include
from django.contrib import admin
from api.base.users.views import Login
from api.base.users.views import venga_entre
admin.autodiscover()

# /api/documents
urlpatterns = [
    # Create login and logout urls
    path('token/', Login.as_view(), name='token'),
    # path('venga_entre/', venga_entre, name='venga_entre'),
]
