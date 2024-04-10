import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser

from utils.odoo_client import OdooClient

from .models import Employee
from .serializers import EmployeeSerializer

class EmployeesView(APIView):
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = EmployeeSerializer
    # add permission to check if user is authenticated
    # TODO: Check permissions of employee role

    queryset = Employee.objects.all()

    def get(self, request):

        # Get user id from token
        user_login = request.user['login']
        # Response error with when user is not authenticated
        if user_login is None:
            return Response({"error": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get employee data from Odoo
        odoo_client = OdooClient()

        if odoo_client == None:
            return Response({"error": "Error al conectar con el ERP"}, status=status.HTTP_400_BAD_REQUEST)

        # El empleado ya viene en formato JSON, por eso no hay que serializarlo
        employee = odoo_client.search_employee_by_identification(user_login)

        if employee is None:
            print("Employee not found in ERP")
            return Response({"error": "Empleado no encontrado en el ERP"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(data=employee)

        if serializer.is_valid():
            response_data = serializer.data
        else:
            response_data = serializer.errors

        print("Empleado encontrado en el ERP ", employee)
        print("Employee serializer en GET: ", response_data)
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    
    # Post function to get employee data and use odoo_client to upload it
    def post(self, request):

        employee_serializer = EmployeeSerializer(data=request.data or None)

        print(f"Employee serializer en POST: {employee_serializer}")

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

'''
Solicita estado de política de datos y actualización de datos
'''

@api_view(['GET', 'POST'])
def employee_data_policies(request):
    if request.method == 'GET':
        employee_id_number = request.user['login']
        odoo_client = OdooClient()
        employee_status = odoo_client.get_employee_data_status(employee_id_number)

        if employee_status is None:
            return Response({"error": "Empleado no encontrado en el ERP"}, status=status.HTTP_404_NOT_FOUND)

        return Response(employee_status, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        employee_id_number = request.user['login']
        odoo_client = OdooClient()

        # from request get data status
        data_policy = request.data.get('data_policy')
        data_treatment = request.data.get('data_treatment')

        employee_status = odoo_client.update_employee_data_policies(employee_id_number, data_policy, data_treatment)

        if employee_status is None:
            return Response({"error": "Empleado no encontrado en el ERP"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "datos de empleado actualizados"}, status=status.HTTP_200_OK)
