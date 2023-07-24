from django.test import TestCase

from .odoo_client import OdooClient
from .document import convert_pdf_to_base64

class DocumentTestCase(TestCase):
    def setUp(self):
        pass

    def test_convert_pdf_to_base64(self):
        pass

class OdooClientTestCase(TestCase):
    def setUp(self):
        self.odoo = OdooClient()

    def test_connect(self):
        '''
        Test connection with Odoo API
        '''
        self.assertIsNotNone(self.odoo.user)
        self.assertEquals(self.odoo.user.email, 'gertic@fundacionudea.co')

    def test_search_employee_exist(self):
        employee_email = 'asistentetic@fundacionudea.co'
        employee_id = self.odoo.search_employee(employee_email)
        self.assertIsNotNone(employee_id)
        self.assertEquals(employee_id, 12)

    def test_search_employee_not_exist(self):
        employee_email = 'juanpabotero@hotmail.coom'
        employee_id = self.odoo.search_employee(employee_email)
        self.assertIsNone(employee_id)

    def test_create_employee(self):
        employee_email = 'correo_test_juan@yahoo.com'
        employee_name = 'Juan Pablo Botero López'
        employee_id = self.odoo.create_employee(employee_name, employee_email)
        self.assertIsNotNone(employee_id)

    def test_upload_new_contract_sign(self):
        pdf_document = 'media/docs/Acuerdo_None.pdf'
        pdf_name = 'Acuerdo_None.pdf'
        pdf_base_64, num_pages = convert_pdf_to_base64(pdf_document)
        pdf_id = self.odoo.upload_new_contract_sign(pdf_name, pdf_base_64)
        self.assertIsNotNone(pdf_id)

    def test_update_contract_sign(self):
        pass

    def test_update_contract_one_sign(self):
        pass

    def test_send_document_to_sign(self):
        pass