import zipfile
from rest_framework import serializers
from api.base.documents.models import Files, ZipFile


'''
OJOOO, DEBE HACER UN SERIALIZER PARA LOS DOS ARCHIVOS POR REQUEST
'''

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = [
                  'contract_template',
                  'employees_data',
                  ]


# Create Class ZipFileSerializer and validate the zip file that have just pdf files inside
class ZipFileSerializer(serializers.ModelSerializer):
    '''
    The data that we are going to receive is a zip file, 
    a XLSX File and a number (1, 2, the number of sign fields)
    '''
    class Meta:
        model = ZipFile
        fields = ['zip_file', 'xlsx_file', 'sign_number']

    # Validate input
    def validate(self, data):

        # Validate that send a zip file, xlsx file and number

        if not data.get('zip_file'):
            raise serializers.ValidationError('Falta archivo comprimido')
        if not data.get('xlsx_file'):
            raise serializers.ValidationError('Falta archivo de Excel')
        if not data.get('sign_number'):
            raise serializers.ValidationError('Falta cantidad de firmas')
                
        # Get the file as Zip file
        zip_file = zipfile.ZipFile(data.get('zip_file'))
        
        # Validate that the files inside zip file are pdf with list comprehension
        if not all(file.endswith('.pdf') for file in zip_file.namelist()):
            raise serializers.ValidationError('El archivo comprimido contiene archivos no válidos (PDF)')
        
        # Validate that the other file is xlsx
        xlsx_file = data.get('xlsx_file')
        if not xlsx_file.name.endswith('.xlsx'):
            raise serializers.ValidationError('No envía archivo xlsx')
        
        # Validate that the number is 1 or 2
        number = data.get('number')
        if number != 1 and number != 2:
            raise serializers.ValidationError('El número de firmas debe ser 1 o 2')        

        return data