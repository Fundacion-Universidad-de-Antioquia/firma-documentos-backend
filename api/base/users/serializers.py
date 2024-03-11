from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):

    identification_number = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ['identification_number', 'password']

class ObtainTokenSerializer(serializers.Serializer):
    identification_number = serializers.CharField()
    password = serializers.CharField()
