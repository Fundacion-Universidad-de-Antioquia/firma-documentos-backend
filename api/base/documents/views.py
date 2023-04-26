import zipfile
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser

from .models import Files
from .serializers import FilesSerializer
from .tasks import send_contract_sign_task

# List http methods
# POST
# GET
# PUT
# DELETE
# PATCH

class FilesAPIView(APIView):
    queryset = Files.objects.order_by('created_by')
    parser_classes = (MultiPartParser, JSONParser)
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]


    '''
    Upload documents (docx, xlsx)
    Process the documents
    Send the documents to Odoo
    '''
    def post(self, request, format=None):
        '''
        request.data.get('contract_name')
        request.data.get('employee_data')
        request.data.get('contract_name')
        '''
        file_serializer = FilesSerializer(data=request.data or None)

        # Get the files (docx, xlsx)
        # create the record on database

        print("Request data all: ", request.data)
        if file_serializer.is_valid(raise_exception=True):

            new_file = file_serializer.save()

            # add task to celery
            print(f"Tipo new file{type(new_file)}")
            print(f"Contract: {new_file.contract_template}")
            print(f"Data: {new_file.employees_data}")
            send_contract_sign_task.delay(new_file.id)

            return Response(file_serializer.data, status=status.HTTP_201_CREATED)

        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Queryset
        id_file = request.data.get('id')
        print(f'Request: {id_file}')
        # files = Files.objects.filter(id=request.data['id']).first()
        files = Files.objects.all()

        # Validation
        if files:
            files_serializer = FilesSerializer(files, many=True)

            # Create new celery task
            return Response(files_serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'No existe registro de archivos con ese id'}, status=status.HTTP_400_BAD_REQUEST)

# Create a view to upload zip file and extract it
class UploadZipFile(APIView):
    parser_classes = (MultiPartParser, JSONParser)

    '''
    def post(self, request, format=None):
        file_serializer = FilesSerializer(data=request.data or None)

        if file_serializer.is_valid(raise_exception=True):
            new_file = file_serializer.save()

            # add task to celery
            print(f"Tipo new file{type(new_file)}")
            print(f"Contract: {new_file.contract_template}")
            print(f"Data: {new_file.employees_data}")

            # Extract zip file
            # zip_ref = zipfile.ZipFile(new_file.contract_template, 'r')
            # zip_ref.extractall('media/zip_files')
            # zip_ref.close()

            # send_contract_sign_task.delay(new_file.id)


            return Response(file_serializer.data, status=status.HTTP_201_CREATED)

        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    '''

    # create post method and return response "Hola Angie"
    def post(self, request, format=None):
        return Response ({"message": "Archivos recividos"}, status=status.HTTP_200_OK)
    
    # create get method and return response "Hola Angie"
    def get(self, request):
        return Response ({"message": "Este es tu dato: CORRECTO"}, status=status.HTTP_200_OK)

# Create serializer to upload zip file
'''
class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ('id', 'contract_template', 'employees_data', 'created_by')

    # Validate input
    def validate(self, data):
        # Validate contract template
        contract_template = data.get('contract_template')
        if not contract_template:
            raise serializers.ValidationError('No se ha seleccionado un archivo de contrato')

        # Validate employees data
        employees_data = data.get('employees_data')
        if not employees_data:
            raise serializers.ValidationError('No se ha seleccionado un archivo de datos de empleados')

        # Validate created_by
        created_by = data.get('created_by')
        if not created_by:
            raise serializers.ValidationError('No se ha seleccionado un usuario')

        return data
'''