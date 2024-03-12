from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.conf import settings
from django.db import connections
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from .serializers import UserSerializer
from .auth_backends import CustomUserModelBackend


User = get_user_model()

class Login(APIView):

    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        '''
        Campos en la intranet: login y contrasena
        '''

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        identification_number = serializer.validated_data.get('login')
        password = serializer.validated_data.get('contrasena')

        print(f'Serializer: {serializer.validated_data}')

        with connections['auth_db'].cursor() as cursor:
            cursor.execute("SELECT id, login, contrasena FROM INTRANET_EMPLEADOS_USUARIOS WHERE login = %s", [identification_number])
            user = cursor.fetchone()
            # The user is a list of values, id, login, contrasena, convert to a dict
            user = dict(zip(['id', 'login', 'contrasena'], user))

            # print the contrasena from user
            print(f'Contrasena: {user["contrasena"]}')

        # user = User.objects.using('auth_db').raw("SELECT id, login, contrasena FROM INTRANET_EMPLEADOS_USUARIOS WHERE login = %s", [identification_number])

        # user = User.get_user_by_login(identification_number)
        

        if user is None or not self.check_md5_password(password, user["contrasena"]):
            return Response({'error': 'Nombre de usuario o contraseña incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)
        
         # Generate JWT Token
        access_token = CustomUserModelBackend.generate_access_token(user)

        return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        
    
    def get(self, request):
        return Response({'error': 'Método no permitido'}, status=HTTP_404_NOT_FOUND)
    
    def check_md5_password(self, request_password, user_password):
        '''
        Check the password with md5 hash

        Parameters:
        request_password (str): The password that the API client sends
        '''
        if request_password is None:
            return False
        return request_password == user_password

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@api_view(['POST'])
@permission_classes([AllowAny])
def venga_entre(request):
    print(f'Datos de request: {request.data}')
    return Response({'message': 'Venga entre'}, status=HTTP_200_OK)
