from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.Serializer):

    # Campos relacionados con Odoo pasa con x_name
    name = serializers.CharField()
    genero = serializers.CharField(required=False)
    fecha_nacimiento = serializers.DateField(required=False)
    lugar_nacimiento = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    work_email = serializers.CharField(required=False)
    address_home_id = serializers.CharField(required=False)
    home_neighborhood = serializers.CharField(required=False)
    home_city = serializers.CharField(required=False)
    telephone1 = serializers.CharField(required=False)
    cellphone = serializers.CharField(required=False)
    project = serializers.CharField(required=False)
    job_title = serializers.CharField(required=False)
    identification_id = serializers.CharField()
    centro_costos = serializers.CharField(required=False)
    numero_cuenta_bancaria = serializers.CharField(required=False)
    banco = serializers.CharField(required=False)
    codigo_banco = serializers.CharField(required=False)
    blood_type = serializers.CharField(required=False)
    zona = serializers.CharField(required=False)
    eps = serializers.CharField(required=False)
    pension = serializers.CharField(required=False)
    severance = serializers.CharField(required=False)
    pant_size = serializers.IntegerField(required=False)
    shirt_size = serializers.IntegerField(required=False)
    shoes_size = serializers.IntegerField(required=False)
    dress_style = serializers.CharField(required=False)
    nivel_riesgo = serializers.CharField(required=False)
    salario = serializers.FloatField(required=False)
    fecha_de_ingreso = serializers.DateField(required=False)
    actualiza_datos_generales = serializers.BooleanField(required=False)
    politica_datos_generales = serializers.BooleanField(required=False)

    def create(self, validated_data):
        return Employee.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.genero = validated_data.get('genero', instance.genero)
        instance.fecha_nacimiento = validated_data.get('fecha_nacimiento', instance.fecha_nacimiento)
        instance.lugar_nacimiento = validated_data.get('lugar_nacimiento', instance.lugar_nacimiento)
        instance.email = validated_data.get('email', instance.email)
        instance.work_email = validated_data.get('work_email', instance.work_email)
        instance.address_home_id = validated_data.get('address_home_id', instance.address_home_id)
        instance.home_neighborhood = validated_data.get('home_neighborhood', instance.home_neighborhood)
        instance.home_city = validated_data.get('home_city', instance.home_city)
        instance.telephone1 = validated_data.get('telephone1', instance.telephone1)
        instance.cellphone = validated_data.get('cellphone', instance.cellphone)
        instance.project = validated_data.get('project', instance.project)
        instance.job_title = validated_data.get('job_title', instance.job_title)
        instance.identification_id = validated_data.get('identification_id', instance.identification_id)
        instance.work_phone = validated_data.get('work_phone', instance.work_phone)
        instance.centro_costos = validated_data.get('centro_costos', instance.centro_costos)
        instance.numero_cuenta_bancaria = validated_data.get('numero_cuenta_bancaria', instance.numero_cuenta_bancaria)
        instance.banco = validated_data.get('banco', instance.banco)
        instance.codigo_banco = validated_data.get('codigo_banco', instance.codigo_banco)
        instance.blood_type = validated_data.get('blood_type', instance.blood_type)
        instance.zona = validated_data.get('zona', instance.zona)
        instance.eps = validated_data.get('eps', instance.eps)
        instance.pension = validated_data.get('pension', instance.pension)
        instance.severance = validated_data.get('severance', instance.severance)
        instance.pant_size = validated_data.get('pant_size', instance.pant_size)
        instance.shirt_size = validated_data.get('shirt_size', instance.shirt_size)
        instance.shoes_size = validated_data.get('shoes_size', instance.shoes_size)
        instance.dress_style = validated_data.get('dress_style', instance.dress_style)
        instance.nivel_riesgo = validated_data.get('nivel_riesgo', instance.nivel_riesgo)
        instance.salario = validated_data.get('salario', instance.salario)
        instance.fecha_de_ingreso = validated_data.get('fecha_de_ingreso', instance.fecha_de_ingreso)
        instance.actualiza_datos_generales = validated_data.get('actualiza_datos_generales', instance.actualiza_datos_generales)
        instance.politica_datos_generales = validated_data.get('politica_datos_generales', instance.politica_datos_generales)
        instance.save()
        return instance


class EmployeeDataPoliciesSerializer(serializers.Serializer):
    data_treatment = serializers.BooleanField(required=True)
    data_policy = serializers.BooleanField(required=True)

    def validate(self, attrs):
        for attr in ['data_treatment', 'data_policy']:
            if attr not in attrs or not isinstance(attrs[attr], bool):
                raise serializers.ValidationError(f"{attr} Debe ser Verdadero o Falso.")

        return attrs
