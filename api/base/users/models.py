from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    login = models.CharField(max_length=100, unique=True, default="gertic@fudea.co")

    # Create an relation with employee model one by one
    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text=('Grupos a los que pertenece el usuario.'),
        related_name="custom_user_set",  # Set a custom related_name
        related_query_name="user",
        verbose_name=('groups')
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text=('Permisos para este usuario.'),
        related_name="custom_user_set",  # Set a custom related_name
        related_query_name="user",
        verbose_name=('user permissions')
    )

    def __str__(self):
        return self.name
    
    # define class method to get an user by login field
    @classmethod
    def get_user_by_login(cls, login):
        return cls.objects.using('auth_db').get(login=login)
    
    class Meta:
        managed = True
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
        if app_label == 'users':
            return db == 'auth_db'
        
        return None
