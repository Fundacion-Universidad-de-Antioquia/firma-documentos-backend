import odoorpc

# import django setings
from django.conf import settings


class OdooClient():

    def __init__(self):
        # import odoo data connection from django config
        self.url = settings.ODOO_API['ODOO_URL']
        self.username = settings.ODOO_API['ODOO_USERNAME']
        self.api_key = settings.ODOO_API['ODOO_API_KEY']
        self.database = settings.ODOO_API['ODOO_DATABASE']
        self.password = settings.ODOO_API['ODOO_PASSWORD']
        
        # Create exeception to manage the connection via internet to Odoo
        try:
            # Prepare conenction
            self.odoo = odoorpc.ODOO(
            host=self.url, port=443, protocol='jsonrpc+ssl')
            
            # Login to Odoo
            self.odoo.login(self.database, self.username, self.password)
            self.user = self.odoo.env.user
        except Exception as e:
            print(f"No se pudo conectar a Odoo {e}")

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

    def upload_new_contract_sign(self, name, document_64):
        '''
        Crea nuevo registro de contrato con el PDF generado
        Recibe el documento PDF en base64
        1- Subir PDF, registro de ir.attachment
        :param str name: proyecto_cc.pdf
        :param base64 document_64:
        :return: ID del documento creado
        '''

        attachment_vals = {
            'name': name,
            'type': 'binary',
            'mimetype': 'application/pdf',
            'store_fname': name,
            'datas': document_64
        }

        # Subir documento
        new_attachment = self.odoo.env['ir.attachment']
        attachment_id = new_attachment.create(attachment_vals)

        template_vals = {
            'attachment_id': attachment_id
        }

        # Crear documento para firmar
        sign_template = self.odoo.env['sign.template']
        template_id = sign_template.create(template_vals)

        return template_id

    def update_contract_sign(self, template_id=0, numpage=1, second_field=True):
        '''
        Actualiza el contrato previamente creado con el campo de firma
        model = sign.template
        Item Type: Signature
        :param str doc_name: proyecto_cc.pdf
        :param str document_id: xxxx
            document_id: positivo: sign.template id en base de datos (ya debe estar en la BD)
        :param numpage
        :param second_field: True si se agrega el campo de firma de la Fundación
        :return: Booleano True si agregó la firma
        '''

        # Campo de firma del Gerente es tipo Compañia
        sign_field_company = {
            'type_id': 1,
            'required': True,
            'name': 'Firma',
            'template_id': template_id,
            'responsible_id': 2,  # 1: Customer, 2: Company, 3: Employee, 4: Standard
            'page': numpage,
            'posX': 0.107,
            'posY': 0.714,
            'width': 0.373,
            'height': 0.064
        }

        # Campo de empleado tipo Empleado
        sign_field_employee = {
            'type_id': 1,
            'required': True,
            'name': 'Firma',
            'template_id': template_id,
            'responsible_id': 3,  # 1: Customer, 2: Company, 3: Employee, 4: Standard
            'page': numpage,
            'posX': 0.531,
            'posY': 0.714, 
            'width': 0.326,
            'height': 0.064
        }

        # Create sign items
        # update_from_pdfviewer(self, template_id=None, duplicate=None, sign_items=None, name=None):

        sign_template = self.odoo.env['sign.template']
        sign_item = self.odoo.env['sign.item']

        if second_field: 
            print("Envia firma de la fundación") 
            item_id_company = sign_item.create(sign_field_company)
            
        item_id_employee = sign_item.create(sign_field_employee)

        return (item_id_company, item_id_employee)

    def send_sign_contract(self, template_id=0, document_name="", employee_id="", company_id=""):
        '''
        Send email with document request
        :param str document_name: proyecto_cc.pdf
        :param str employee_id: ID del empleado en Odoo
        :param str template_id: ID del documento a firmar en Odoo
        :param str company_id: Id del firmante de la fundación
        '''

        print(f"ID Del companía: {company_id}")
        print(f"ID De empleado: {employee_id}")

        # Agrega la firma de la fundación si es necesario
        signers = []
        signers.append([0, 'virtual_37', {'role_id': 2, 'partner_id': employee_id}])
        signers_count = 1
        if company_id != None:
            signers.append([0, 'virtual_25', {'role_id': 3, 'partner_id': company_id}])
            signers_count = 2

        request_fields = {
            'template_id': template_id,
            #'signer_ids': [[0, 'virtual_25', {'role_id': 2, 'partner_id': company_id}],  # 13444 es el ID en Odoo del Director de la fundación
            #               [0, 'virtual_37', {'role_id': 3, 'partner_id': employee_id}]],
            'signer_ids': signers,
            'signer_id': False,
            'signers_count': signers_count,
            'has_default_template': True,
            'follower_ids': [[6, False, []]],
            'subject': f'Solicitud de firma {document_name}',
            'filename': document_name,
            'message_cc': '<p><br></p>',
            'attachment_ids': [[6, False, []]],
            'message': '<p>Hola.</p><p>Mensaje generado automáticamente, no responder</p>'
        }

        print("Preparar correo con firmantes: {signers}")

        # Prepare email request
        sign_email = self.odoo.env['sign.send.request']
        email_id = sign_email.create(request_fields)

        print(f'ID de plantilla de email {email_id}')

        request_sign = sign_email.send_request(email_id)

        print(f'Correo enviado código {request_sign}')

        return request_sign

    def search_employee(self, employee_email=""):
        '''
        Search contact and return ID
        In case the contact doesn't exist, return None
        '''

        partner = self.odoo.env['res.partner']
        try:
            # Partner id is Interger, but the result is type integer[], get the first
            partner_id = partner.search([('email', '=', employee_email)])[0]
        except IndexError:
            partner_id = None
        
        return partner_id
    
    def create_employee(self, employee_name="", employee_email=""):
        '''
        Create employee in Odoo
        '''
        partner = self.odoo.env['res.partner']
        
        partner_id = partner.create(
            {'is_company': False,
             'company_type': 'person',
             'type': 'contact',
             'user_ids': [],
             'name': employee_name,
             'email': employee_email
            }
        )
        
        return partner_id


'''
user_count = api.execute_kw(database, uid, password,
                            "res.users", "search_count", [[]])
print(f"User count is: {user_count}")

companies = api.execute_kw(database, uid, password, "res.users", "read", [
                           uid, ["login", "name", "company_id"]])
print("User companies: ")
print(companies)
'''
