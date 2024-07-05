from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.Serializer):

    # Campos relacionados con Odoo pasa con x_name
    full_name = serializers.CharField()
    gender = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    birth_place = serializers.CharField(required=False)
    birth_country = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    marital_status = serializers.CharField(required=False)
    emergency_contact_name = serializers.CharField(required=False)
    emergency_contact_relationship = serializers.CharField(required=False)
    emergency_contact_number = serializers.CharField(required=False)
    race = serializers.CharField(required=False)
    scholarship = serializers.CharField(required=False)
    email_work = serializers.CharField(required=False)
    address_home_id = serializers.CharField(required=False)
    home_neighborhood = serializers.CharField(required=False)
    home_city = serializers.CharField(required=False)
    home_city_name = serializers.CharField(required=False)
    telephone1 = serializers.CharField(required=False)
    cellphone = serializers.CharField(required=False)
    employee_project = serializers.CharField(required=False)
    employee_rol = serializers.CharField(required=False)
    id_document = serializers.CharField()
    cost_center = serializers.CharField(required=False)
    bank_account_number = serializers.CharField(required=False)
    bank_account_type = serializers.CharField(required=False)
    bank_name = serializers.CharField(required=False)
    codigo_banco = serializers.CharField(required=False)
    blood_type = serializers.CharField(required=False)
    employee_zone = serializers.CharField(required=False)
    eps = serializers.CharField(required=False)
    pension = serializers.CharField(required=False)
    severance = serializers.CharField(required=False)
    pant_size = serializers.IntegerField(required=False)
    shirt_size = serializers.CharField(required=False)
    shoes_size = serializers.IntegerField(required=False)
    dress_style = serializers.CharField(required=False)
    level_risk = serializers.CharField(required=False)
    salary = serializers.FloatField(required=False)
    entry_date = serializers.DateField(required=False)
    employee_code = serializers.CharField(required=False)
    employee_status = serializers.CharField(required=False)
    actualiza_datos_generales = serializers.BooleanField(required=False)
    politica_datos_generales = serializers.BooleanField(required=False)

    def create(self, validated_data):
        return Employee.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # update data according attributes

        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.birth_place = validated_data.get('birth_place', instance.birth_place)
        instance.birth_country = validated_data.get('birth_country', instance.birth_country)
        instance.email = validated_data.get('email', instance.email)
        instance.email_work = validated_data.get('email_work', instance.email_work)
        instance.address_home_id = validated_data.get('address_home_id', instance.address_home_id)
        instance.home_neighborhood = validated_data.get('home_neighborhood', instance.home_neighborhood)
        instance.home_city = validated_data.get('home_city', instance.home_city)
        instance.home_city_name = validated_data.get('home_city_name', instance.home_city_name)
        instance.telephone1 = validated_data.get('telephone1', instance.telephone1)
        instance.cellphone = validated_data.get('cellphone', instance.cellphone)
        instance.employee_project = validated_data.get('employee_project', instance.employee_project)
        instance.employee_rol = validated_data.get('employee_rol', instance.employee_rol)
        instance.id_document = validated_data.get('id_document', instance.id_document)
        instance.cost_center = validated_data.get('cost_center', instance.cost_center)
        instance.bank_account_number = validated_data.get('bank_account_number', instance.bank_account_number)
        instance.bank_name = validated_data.get('bank_name', instance.bank_name)
        instance.codigo_banco = validated_data.get('codigo_banco', instance.codigo_banco)
        instance.blood_type = validated_data.get('blood_type', instance.blood_type)
        instance.employee_zone = validated_data.get('employee_zone', instance.employee_zone)
        instance.eps = validated_data.get('eps', instance.eps)
        instance.pension = validated_data.get('pension', instance.pension)
        instance.severance = validated_data.get('severance', instance.severance)
        instance.pant_size = validated_data.get('pant_size', instance.pant_size)
        instance.shirt_size = validated_data.get('shirt_size', instance.shirt_size)
        instance.shoes_size = validated_data.get('shoes_size', instance.shoes_size)
        instance.dress_style = validated_data.get('dress_style', instance.dress_style)
        instance.level_risk = validated_data.get('level_risk', instance.level_risk)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.entry_date = validated_data.get('entry_date', instance.entry_date)
        instance.employee_code = validated_data.get('employee_code', instance.employee_code)
        instance.employee_status = validated_data.get('employee_status', instance.employee_status)
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

class EmployeeImageProfileSerializer(serializers.Serializer):
    image_profile = serializers.CharField(required=True)

    def validate(self, attrs):
        if 'image_profile' not in attrs:
            raise serializers.ValidationError("image_profile es requerido")
        return attrs

class EmployeeDocumentsSerializer(serializers.Serializer):

    # Base Documents
    bank_certification = serializers.CharField(required=False)
    curriculum_vitae = serializers.CharField(required=False)
    id_file = serializers.CharField(required=False)
    judicial_background = serializers.CharField(required=False)

    # Academic Documents
    bachelor_certification = serializers.CharField(required=False)
    high_school_certification = serializers.CharField(required=False)
    master_certification = serializers.CharField(required=False)
    postgraduate_certification = serializers.CharField(required=False)

    # Work Documents
    working_letter_1 = serializers.CharField(required=False)
    working_letter_2 = serializers.CharField(required=False)
    working_letter_3 = serializers.CharField(required=False)

    # Social Security Documents
    eps_certification = serializers.CharField(required=False)
    pension_certification = serializers.CharField(required=False)
    severance_certification = serializers.CharField(required=False)

    # Other Documents
    sworn_declaration_comfama = serializers.CharField(required=False)