from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser

from .models import Files
from .serializers import FilesSerializer
from .tasks import send_contract_sign_task


class FilesAPIView(APIView):
    queryset = Files.objects.order_by('created_by')
    parser_classes = (MultiPartParser, JSONParser)
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

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


files_list_upload_view = FilesAPIView.as_view()
