import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser

from utils.odoo_client import OdooClient
from utils.file_utils import base64_to_image, image_to_base64

from .models import Employee
from .serializers import EmployeeSerializer, EmployeeDataPoliciesSerializer, EmployeeImageProfileSerializer


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
            response_data = employee
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    
    # Post function to get employee data and use odoo_client to upload it
    def post(self, request):
        # Get user id from token
        user_login = request.user['login']
        # Response error with when user is not authenticated
        if user_login is None:
            return Response({"error": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        employee_serializer = EmployeeSerializer(data=request.data or None)

        if employee_serializer.is_valid(raise_exception=True):
            odoo_client = OdooClient()

            employee_id = odoo_client.update_employee_data(user_login, employee_serializer.data)

            if employee_id:
                return Response({"Datos de empleado actualizados"}, status=status.HTTP_201_CREATED)
            
            return Response({"error":"Error al actualizar datos de empleado"}, status=status.HTTP_400_BAD_REQUEST)

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

        employeeSerializer = EmployeeDataPoliciesSerializer(data=request.data)

        if not employeeSerializer.is_valid():
            return Response(employeeSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # from request get data status
        data_policy = employeeSerializer.data.get('data_policy')
        data_treatment = employeeSerializer.data.get('data_treatment')

        print(f"Data policy: {data_policy} - Data treatment: {data_treatment}")

        odoo_client = OdooClient()

        employee_status = odoo_client.update_employee_data_policies(employee_id_number, data_policy, data_treatment)

        if employee_status is None:
            return Response({"error": "Empleado no encontrado en el ERP"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "datos de empleado actualizados"}, status=status.HTTP_200_OK)
    
    return Response({"error": "Método no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET', 'POST'])
def image_profile(request):
    if request.method == 'GET':
        employee_id_number = request.user['login']
        print("Employee id number getting image: ", employee_id_number)
        odoo_client = OdooClient()
        image_base64 = odoo_client.get_employee_profile_image(employee_id_number)

        if image_base64 is None:
            return Response({"error": "Empleado sin imagen"}, status=status.HTTP_404_NOT_FOUND)
        
        # image_profile = base64_to_image(image_profile)
        return Response({"image_profile": image_base64}, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        employee_id_number = request.user['login']

        image_profile = request.data.get('image_profile')
        print("Image profile: ", image_profile)
        
        try:
            odoo_client = OdooClient()

            employee_status = odoo_client.update_employee_image(employee_id_number, image_profile)

            if not employee_status:
                return Response({"error": "Empleado no encontrado en el ERP"}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": "datos de empleado actualizados"}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error: ", e)
            return Response({"error": "Error al actualizar imagen de empleado"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"error": "Método no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def list_options(request):
    odoo_client = OdooClient()
    options = odoo_client.get_list_options()

    if options is None:
        return Response({"error": "Error al obtener opciones"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(options, status=status.HTTP_200_OK)

@api_view(['GET'])
def sign_documents(request):
    odoo_client = OdooClient()
    employee_identification = request.user['login']
    documents = odoo_client.get_sign_documents(employee_identification)

    if documents is None:
        return Response({"error": "No hay datos de documentos para firmar de empleado"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(documents, status=status.HTTP_200_OK)
