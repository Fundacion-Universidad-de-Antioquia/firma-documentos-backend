from django.db import models
from django.conf import settings
from api.base.employees.models import Employee


# Path and name of uploaded files
def upload_to(instance, filename):
    # Return the docs path from settings
    return f'docs/{filename}'

class Files(models.Model):
    contract_name = models.CharField(max_length=255, blank=True, null=False)
    contract_template = models.FileField(
        upload_to=upload_to, blank=True, null=False)
    employees_data_name = models.CharField(
        max_length=255, blank=True, null=False)
    employees_data = models.FileField(
        upload_to=upload_to, blank=True, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'files'

class ContractDocument(models.Model):
    '''
    PDF Document (Contract) Model assigned to each employee
    Has name, upload_to path, SignTask id (from Odoo), employee id (relation)
    '''
    name = models.CharField(max_length=255, blank=True, null=False)
    path = models.FileField(upload_to=upload_to, blank=True, null=False)
    sign_id = models.IntegerField(blank=True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(blank=True, null=True)

    # relation with employee many to One
    # related_name='contract_document' for reverse search from employee: Employee.contract_document.all()
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='contract_document')


    class Meta:
        managed = True
        db_table = 'contract_document'

class ZipFile(models.Model):
    '''
    ZipFile Model to store the zip file with all the PDFs and xlsx file
    '''
    name = models.CharField(max_length=255, blank=True, null=True)
    zip_file = models.FileField(upload_to=upload_to, blank=True, null=False)
    xlsx_file = models.FileField(upload_to=upload_to, blank=True, null=False)
    signs_number = models.IntegerField(blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'zip_file'


class SignTask(models.Model):
    '''
    Tasks to create PDF and send the sign request to Odoo
    Each task is managed by Celery / Redis
    Does not relate with App models
    '''

    DIGITAL_SIGNATURE = 'DSIG'

    # Operation options to Celery
    EQUATIONS = ((DIGITAL_SIGNATURE, 'Signature'),)

    # Statuses
    STATUS_PENDING = 'PENDING'
    STATUS_ERROR = 'ERROR'
    STATUS_SUCCESS = 'SUCCESS'
    STATUSES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_ERROR, 'Error'),
        (STATUS_SUCCESS, 'Success'),
    )

    input = models.IntegerField()
    output = models.IntegerField(blank=True, null=True)

    files = models.OneToOneField(
        Files, on_delete=models.CASCADE,
        primary_key=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=8, choices=STATUSES)
    message = models.CharField(max_length=110, blank=True)
