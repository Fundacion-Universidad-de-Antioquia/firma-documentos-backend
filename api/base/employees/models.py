from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=False)
    second_name = models.CharField(max_length=255, blank=True, null=False)
    name = models.CharField(max_length=255, blank=True, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False)
    odoo_id = models.IntegerField(blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'employee'
