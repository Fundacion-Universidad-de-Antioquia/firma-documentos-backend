from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):

    # Validate the data from request in a method called validate
    def validate(self, data):

        if not self.full_name:
            raise serializers.ValidationError('Falta nombre completo')
        
        # Complete the rest of validations from model Employee
        if not self.id_document:
            raise serializers.ValidationError('Falta documento de identidad')
        
        return data
    
    def create(self, validated_data):
        return Employee.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        ...

    class Meta:
        model = Employee
        # exclude = ['id']
        fields = '__all__'

