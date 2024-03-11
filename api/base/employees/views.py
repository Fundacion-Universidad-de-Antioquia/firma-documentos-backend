import hashlib
from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from utils.odoo_client import OdooClient

from .models import Employee
from .serializers import EmployeeSerializer

class EmployeesView(APIView):
    parser_classes = (MultiPartParser, JSONParser)
    # add permission to check if user is authenticated
    # TODO: Check permissions of employee role
    # permission_classes = [IsAuthenticated]

    queryset = Employee.objects.all()    

    def get(self, request):
        employee = Employee.objects.get(employee_identification=request.data.get('employee_identification'))

        if employee is None:
            return Response('Empleado no encontrado', status=status.HTTP_404_NOT_FOUND)

        return Response(employee, status=status.HTTP_200_OK)
    
    # Post function to get employee data and use odoo_client to upload it
    def post(self, request):

        print("Post request received")

        employee_serializer = EmployeeSerializer(data=request.data or None)

        if employee_serializer.is_valid(raise_exception=True):
            print("Employee serializer is valid")

            # Get username from request

            odoo_client = OdooClient()

            employee_id = odoo_client.update_employee_data(employee_serializer.data)

            if employee_id:
                return Response('Datos de empleado creados', status=status.HTTP_201_CREATED)
            
            return Response('Error al crear datos de empleado', status=status.HTTP_400_BAD_REQUEST)

        return Response({employee_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# Create function view called authenticate
'''
https://backend-employees.azuresites.net/employees/login/

Llega del formulario de login en React
'''
        


# Conectar a Odoo para obtener datos de empleado según la cédula de la intranet.

# Enviar datos a Odoo
        