from django.db import models

# Path and name of uploaded files


def upload_to(instance, filename):
    return 'docs/{filename}'.format(filename=filename)


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


class SignTask(models.Model):
    '''
    Tasks to create PDF and send the sign request to Odoo
    Each task is managed by Celery
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
