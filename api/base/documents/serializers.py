from rest_framework import serializers
from api.base.documents import models


'''
OJOOO, DEBE HACER UN SERIALIZER PARA LOS DOS ARCHIVOS POR REQUEST
'''


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Files
        fields = ['id', 'created_by',
                  'contract_name',
                  'employees_data_name',
                  ]
