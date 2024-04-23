from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.db import connections
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed, ParseError
from jwt.exceptions import ExpiredSignatureError

from .serializers import UserSerializer

# Assign get_user_model()
User = get_user_model()

class CustomUserModelBackend(authentication.BaseAuthentication):

    serializer_class = UserSerializer

    def authenticate(self, request):
        '''
        Authenticate the user with the identification number and password
        First check the token
        Then check the user and password

        Parameters:
        request (Request): The request that the API client sends 
        '''

        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        access_token = self.get_the_token_from_header(jwt_token)

        # Decode JWT and verify signature
        try:
            # The SECRET KEY changes in every stage, keep an eye on this
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'], options={"verify_iat":False})
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except ExpiredSignatureError:
            raise AuthenticationFailed("Tiempo de sesión ha expirado")
        except jwt.exceptions.DecodeError as e:
            # print the full error
            print(f"Error: {e}")
            raise ParseError('Token no válido')
        
        # Get user from database, can be login
        login = payload.get('user_identifier')
        if login is None:
            raise AuthenticationFailed('Usuario no encontrado en el token')
        
        # TODO: Agregar Nombre de tabla desde el Settings
        with connections['auth_db'].cursor() as cursor:
            # cursor.execute("SELECT id, login FROM %s WHERE login = %s", [settings.USERS_TABLE,  login])
            cursor.execute("SELECT id, login FROM INTRANET_EMPLEADOS_USUARIOS WHERE login = %s", [login])
            user = cursor.fetchone()

            # Usuario es lista, se convierte a diccionario
            user = dict(zip(['id', 'login'], user))

        if user is None:
            raise AuthenticationFailed('Usuario no encontrado en la base de datos')
        user['is_authenticated'] = True
        return (user, payload)
    
    def authenticate_header(self, request):
        return 'Bearer'
    
    
    @classmethod
    def generate_access_token(cls, user):
        # Create payload
        payload = {
            'user_identifier': user['login'],
            'exp': int((datetime.utcnow() + timedelta(hours=settings.JWT_CONF['TOKEN_LIFETIME_HOURS'])).timestamp()),
            'iat': datetime.utcnow().timestamp()
        }

        # Encode JWT with secret key
        access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return access_token
    
    @classmethod
    def generate_refresh_token(cls, user):
        
        # Create payload
        payload = {
            'user_identifier': user['login'],
            'exp': int((datetime.utcnow() + timedelta(days=settings.JWT_CONF['REFRESH_TOKEN_LIFETIME_DAYS']))),
            'iat': datetime.utcnow()
        }

        # Encode JWT with secret key
        refresh_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return refresh_token
    
    
    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')  # clean the token
        return token


    def get_user(self, user_id):
        try:
            return User.objects.using('auth_db').get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    # for custom permissions use this link
    # https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#custom-permissions
    def has_perm(self, user_obj, perm, obj=None):
        return True


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view or edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Permissions are only granted to the owner of the object.
        return obj.owner == request.user
