from django.db import models


class Employee(models.Model):

    # Personal Information
    id_number = models.CharField(max_length=20, null=True)

    # Social Security
    odoo_id = models.IntegerField(blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'employee'
