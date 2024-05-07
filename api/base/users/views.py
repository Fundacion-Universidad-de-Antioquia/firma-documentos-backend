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
from utils.odoo_client import OdooClient


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

        with connections['auth_db'].cursor() as cursor:
            cursor.execute("SELECT id, login, contrasena FROM INTRANET_EMPLEADOS_USUARIOS WHERE login = %s", [identification_number])
            user = cursor.fetchone()

            # Usuario es lista, se convierte a diccionario
            user = dict(zip(['id', 'login', 'contrasena'], user))    

        if user is None or not self.check_md5_password(password, user["contrasena"]):
            return Response({'error': 'Nombre de usuario o contraseña incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)
        
         # Generate JWT Token
        access_token = CustomUserModelBackend.generate_access_token(user)

        return Response({"access_token": access_token, "is_data_treatment_accepted": True, "is_data_updated": True}, status=status.HTTP_200_OK)

        # GEt user data from Odoo
        # odoo_client = OdooClient()
        #employee_status = odoo_client.get_employee_data_status(identification_number)
        #if employee_status is None:
        #    return Response({'error': 'No existe datos de empleado'}, status=status.HTTP_404_NOT_FOUND)

        #return Response({"access_token": access_token, 
        #                 "is_data_treatment_accepted": employee_status['is_data_accepted'],
        #                 "is_data_updated": employee_status['is_data_updated']}, 
        #                 status=status.HTTP_200_OK)
        
    
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
@permission_classes([IsAuthenticated])
def venga_entre(request):
    print(f'Datos de request: {request.data}')
    return Response({'message': 'Venga entre'}, status=HTTP_200_OK)
