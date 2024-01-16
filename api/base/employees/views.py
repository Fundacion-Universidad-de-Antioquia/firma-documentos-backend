from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from .models import Employee
from .serializers import EmployeeSerializer

class EmployeesView(APIView):
    parser_classes = (MultiPartParser, JSONParser)
    # add permission to check if user is authenticated
    # TODO: Check permissions of employee role
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Employee.objects.all()

    def post(self, request, format=None):
        # Get the user from the request
        this_user = request.user
        

        # First save data as employee, then as HR
        if this_user.groups.filter(name='employee').exists():
            # Save data as employee
            ...
        elif this_user.groups.filter(name='hr').exists():
            # Save data as HR
            ...
        else:
            return Response({"message": "No tiene permisos para realizar esta acción"}, status=status.HTTP_403_FORBIDDEN)
        
        employees_serializer = EmployeeSerializer(data=request.data)
        
        if employees_serializer.is_valid():
            new_employee = employees_serializer.save()

            return Response({"message": "Empleado registrado"}, status=status.HTTP_200_OK)
        
    def get(self, request):

        # Get employee from request data (id_document)
        employee = request.data.get('id_document')

        # Serialize the data
        employee_serialized = EmployeeSerializer(employee)
        return Response(employee.data, status=status.HTTP_200_OK)
