from rest_framework import serializers
from api.base.documents.models import Files


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
