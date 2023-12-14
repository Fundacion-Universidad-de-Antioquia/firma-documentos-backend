from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from .models import Files, ZipFile
from .serializers import FilesSerializer, ZipFileSerializer
from .tasks import send_contract_sign_task, send_zip_file_task

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
class ZipFileView(APIView):

    parser_classes = (MultiPartParser, JSONParser)
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = ZipFile.objects.all()

    def get(self, request):
        '''
        Get the list of tasks:
        N° | Date | Number of sent | Status
        '''
        # Query to get the list of SignTasks: just 10
        # Get the last 10 tasks from database
        #tasks = SignTask.objects.all().last(10)
        tasks = SignTask.objects.all().order_by('zip_file_id')[:10]

        
        # Serialize the data
        serializer = SignTaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        #return Response ({"message": "Lista de tareas"}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        '''
        Get the zip file and unzip it in media folder
        Get the xls file and save it in media folder too
        Create new Celery Task
        '''

        file_serializer = ZipFileSerializer(data=request.data)

        if file_serializer.is_valid(raise_exception=True):

            # Get the data and save to database, define the model with fields
            new_file = file_serializer.save()

            # Unzip the zip file
            # zip_file = request.FILES['zip_file']
            # xlsx_file = request.FILES['xlsx_file']
            # company_sign = request.data['signs_number']

            zip_file = file_serializer.validated_data['zip_file']
            xlsx_file = file_serializer.validated_data['xlsx_file']
            company_sign = file_serializer.validated_data['signs_number']

            # Save in database
            new_zip_task = file_serializer.save()
            zip_id = new_zip_task.id
            
            # Create Task, pass the ID of the new_zip_file (model)
            send_zip_file_task.delay(zip_id)

            return Response ({"message": "Archivos recibidos"}, status=status.HTTP_200_OK)
        
        else:
            return Response ({"message": "No se ha seleccionado un archivo"}, status=status.HTTP_400_BAD_REQUEST)
