from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser): 
    
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    login = models.CharField(max_length=100, unique=True)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()

    is_active = models.BooleanField()
    is_staff =  models.BooleanField()
    date_joined = models.DateTimeField()
    is_admin = models.BooleanField()


    # Create an relation with employee model one by one
    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name
    
    # define class method to get an user by login field
    @classmethod
    def get_user_by_login(cls, login):

        return cls.objects.using('auth_db').get(login=login)
    
    class Meta:
        managed = False
        db_table = settings.USERS_TABLE


class UserRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'users':
            return 'auth_db'
        return None
    
    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if model is None:
            return db == 'auth_db'
        
        if db == 'auth_db':
            return model._meta.app_label == 'users'
        elif model._meta.app_label == 'users':
            return False
        return None
