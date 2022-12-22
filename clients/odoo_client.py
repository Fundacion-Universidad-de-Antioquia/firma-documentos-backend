from xmlrpc import client

from django.conf import settings


class OdooClient():

    def __init__(self):
        self.url = settings.ODOO_API['URL']
        self.username = settings.ODOO_API['USERNAME']
        self.api_key = settings.ODOO_API['API_KEY']
        self.database = settings.ODOO_API['DATABASE']

        # Establish the Connection
        common = client.ServerProxy("%s/xmlrpc/2/common" % self.url)

        self.uid = common.authenticate(
            self.database, self.username, self.api_key, {})

        self.api = client.ServerProxy("%s/xmlrpc/2/object" % self.url)

    '''
        Obtener la lista de proyectos de Odoo
        Se hace la consulta en Odoo de los departamentos, modelo hr.department
    '''

    def get_projects(self, project_id=False):
        # Projects are Employee Departments in Odoo (hr.department)
        domain = [("hr.department", "=", project_id)] if project_id else []
        fields = ["id", "name"]
        projects = self.api.execute_kw(self.database, self.uid, self.api_key,
                                       "hr.department", "search_read", [domain, fields])

        return projects

    '''
        Obtener la lista de empleados de un proyecto desde Odoo
        Se hace la consulta en Odoo de los empleados, modelo hr.employee
        Se pide los empleados que pertenecen al departamento identificado con project_id
    '''

    def get_employees(self, project_id):
        domain = [("department_id", "=", project_id)]
        fields = ["name", "work_email", "identification_id", "work_phone",
                  "job_title", "x_studio_fecha_de_ingreso", "x_studio_salario_empleado_1", "x_studio_tipo_de_contrato", "x_studio_banco", "x_studio_tipo_de_cuenta", "x_studio_nmero_de_cuenta_bancaria", "x_studio_arl", "x_studio_descripcin_cambios"]
        employees = self.api.execute_kw(self.database, self.uid, self.api_key,
                                        "hr.employee", "search_read", [domain, fields])

        return employees

    def send_new_contract_sign(self, name, document_64):
        '''
        Crea nuevo registro de contrato con el PDF generado
        Recibe el documento PDF en base64
        :param str name: proyecto_cc.pdf
        :param base64 document_64:
        :return: ID del documento creado
        '''
        doc_id = self.api.execute_kw(self.database, self.uid, self.api_key,
                                     "sign.template", "create",
                                     [{'name': name, 'datas': document_64}])
        return doc_id

    def update_contract_sign(self, doc_name, document_id):
        '''
        Actualiza el contrato previamente creado con el campo de firma
        model = sign.template
        Item Type: Signature
        :param str doc_name: proyecto_cc.pdf
        :param str document_id: xxxx
            document_id: positivo: sign.template id en base de datos (ya debe estar en la BD)
        :return: Booleano True si agregó la firma
        '''
        sign_items = {
            '0':
                {
                    'type_id': 1,
                    'required': True,
                    'name': 'Firma',
                    'responsible_id': 3,
                    'page': '2',
                    'posX': 0.065,
                    'posY': 0.811,
                    'width': 0.319,
                    'height': 0.051},
                '-1':
                    {
                    'type_id': 1,
                    'required': True,
                    'option_ids': [],
                    'responsible_id': 3,
                    'page': '2',
                    'posX': 0.659,
                    'posY': 0.813,
                    'width': 0.2,
                    'height': 0.05
                },
                'name': doc_name
        }

        # Create sign ITEM
        domain = [("sign.template")]

        place_sign = self.api.execute_kw(self.database, self.uid, self.api_key, "sign.template",
                                         "update_from_pdfviewer()",
                                         [[document_id], sign_items])

        if (place_sign):
            print("Documento con firma")

    def send_sign_contract(self, document_id, email):
        pass


'''
user_count = api.execute_kw(database, uid, password,
                            "res.users", "search_count", [[]])
print(f"User count is: {user_count}")

companies = api.execute_kw(database, uid, password, "res.users", "read", [
                           uid, ["login", "name", "company_id"]])
print("User companies: ")
print(companies)
'''
