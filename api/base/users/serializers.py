from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):

    login = serializers.CharField()
    contrasena = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ['login', 'contrasena']

class ObtainTokenSerializer(serializers.Serializer):
    login = serializers.CharField()
    contrasena = serializers.CharField()
