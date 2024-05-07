from django.test import TestCase
from employees.models import Employee

class EmployeeTestCase(TestCase):
    def setup(self):
        Employee.objects.create(
            full_name="John Doe", 
            birth_date="1990-01-01", 
            birth_place="Bogotá", 
            document_type="CC", 
            id_document="123456789", 
            photo="photo.jpg", 
            military_document="123456789", 
            military_document_class="Primera", 
            military_document_district="Bogotá", 
            bank_account_number="123456789", 
            bank_name="Bancolombia", 
            bank_code="123456789", 
            blood_type="A+", 
            home_address="Calle 123", 
            home_neighborhood="Barrio 123", 
            home_city="Bogotá", 
            telephone1="123456789", 
            telephone2="123456789", 
            cellphone="123456789",
            email="john_doe@example.com"
        )

        john = Employee.objects.get(full_name="John Doe")
        self.assertEqual(john.email, "john_doe@example.com")
        self.assertEqual(john.blood_type, "A+")

    # API TESTS, ENDPOINTS, employee
    
    def test_get_employee():
        ...

    def test_create_employee():
        ...
    
    def test_update_employee():
        ...

    # API Test with authentication by RF
    def test_get_employee_authenticated():
        ...




