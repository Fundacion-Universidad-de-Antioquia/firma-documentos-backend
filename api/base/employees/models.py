from django.db import models


class Employee(models.Model):
    full_name = models.CharField(max_length=255, blank=True, null=False)

    # TODO: Validar formato de fecha en Odoo: YYYY-MM-DD
    birth_date = models.DateField(blank=True, null=False)

    birth_place = models.CharField(max_length=255, blank=True, null=True)

    document_type= models.CharField(max_length=10, blank=True, null=False)
    id_document = models.CharField(max_length=50, blank=True, unique=True, null=False)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    military_document = models.CharField(max_length=255, blank=True, null=True)

    # Military class: Primera, Segunda, Tercera, Cuarta, Excento
    military_document_class = models.CharField(max_length=20, blank=True, null=True)
    military_document_district = models.CharField(max_length=255, blank=True, null=True)

    bank_account_number = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    bank_code = models.CharField(max_length=255, blank=True, null=True)

    # Blood Type: A+, A-, B+, B-, AB+, AB-, O+, O-
    blood_type = models.CharField(max_length=5, blank=True, null=True)

    # Home address data
    home_address = models.CharField(max_length=255, blank=True, null=True)
    home_neighborhood = models.CharField(max_length=255, blank=True, null=True)
    home_city = models.CharField(max_length=255, blank=True, null=True)
    telephone1 = models.CharField(max_length=255, blank=True, null=True)
    telephone2 = models.CharField(max_length=255, blank=True, null=True)
    cellphone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=False, null=True)

    # Social Security    

    odoo_id = models.IntegerField(blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'employee'
