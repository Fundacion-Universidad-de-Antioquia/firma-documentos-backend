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
            print(f"Conexión con Odoo => {e}")


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

    def update_contract_sign(self, template_id=0, numpage=1, second_field=1):
        '''
        Actualiza el contrato previamente creado con el campo de firma
        model = sign.template
        Item Type: Signature
        :param str doc_name: proyecto_cc.pdf
        :param str document_id: xxxx
            document_id: positivo: sign.template id en base de datos (ya debe estar en la BD)
        :param numpage
        :param second_field: 2 si se agrega el campo de firma de la Fundación
        :return: item_id_company, item_id_employee (tuple)
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
            
        item_id_employee = sign_item.create(sign_field_employee)
        item_id_company = sign_item.create(sign_field_company) if second_field == 2 else None

        return (item_id_company, item_id_employee)

    def send_sign_contract(self, template_id=0, document_name="", employee_id="", company_id=""):
        '''
        Send email with document request
        :param str document_name: proyecto_cc.pdf
        :param str employee_id: ID del empleado en Odoo
        :param str template_id: ID del documento a firmar en Odoo
        :param str company_id: Id del firmante de la fundación
        '''

        print(f"ID De la compañía: {company_id}")

        # role_id para empleado es 3
        signers = [[0, 'virtual_37', {'role_id': 3, 'partner_id': employee_id}]]
        signers_count = 1

        # Agrega la firma de la fundación si es solicitado
        if company_id is not None and company_id != "":
            # role_id para compañía es 2
            print("Agrega firma de la fundación")
            signers.append([0, 'virtual_25', {'role_id': 2, 'partner_id': company_id}])
            signers_count = 2

        # FIXME: Agregar company_id como firmante cuando sea necesario
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

        # Prepare email request
        sign_email = self.odoo.env['sign.send.request']
        email_id = sign_email.create(request_fields)

        request_sign = sign_email.send_request(email_id)

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

    def search_employee_by_identification(self, employee_identification):
        '''
        Search contact and return Identification number
        In case the contact doesn't exist, return None
        '''

        odoo_context = self.odoo.env['hr.employee']
     
        # Employee identification is Interger
        odoo_employee_id = odoo_context.search([('name', '=', employee_identification)])
        if not odoo_employee_id:
            return None
        
        odoo_employee = odoo_context.browse(odoo_employee_id)
        employee = {
            "name": odoo_employee.identification_id if odoo_employee.identification_id else 'N/A',
            "genero": odoo_employee.gender if odoo_employee else 'N/A',
            "fecha_nacimiento": odoo_employee.birthday if odoo_employee.birthday else 'N/A',
            "lugar_nacimiento": odoo_employee.x_studio_lugar_de_nacimiento.x_name if odoo_employee.x_studio_lugar_de_nacimiento.x_name else 'N/A',
            "email": odoo_employee.x_studio_correo_electrnico_personal if odoo_employee.x_studio_correo_electrnico_personal else 'N/A',
            "work_email": odoo_employee.work_email if odoo_employee.work_email else 'N/A',
            "address_home_id": odoo_employee.address_home_id.name if odoo_employee.address_home_id.name else 'N/A',
            "home_neighborhood": odoo_employee.x_studio_barrio if odoo_employee.x_studio_barrio else 'N/A',
            "home_city": odoo_employee.x_studio_municipio.x_name if odoo_employee.x_studio_municipio.x_name else 'N/A',
            "telephone1": odoo_employee.work_phone if odoo_employee.work_phone else 'N/A',
            "cellphone": odoo_employee.mobile_phone if odoo_employee.mobile_phone else 'N/A',
            "project": odoo_employee.company_id.name if odoo_employee.company_id.name else 'N/A',
            "job_title": odoo_employee.job_title if odoo_employee.job_title else 'N/A',
            "identification_id": odoo_employee.name if odoo_employee.name else 'N/A',
            "centro_costos": odoo_employee.x_studio_centro_de_costos if odoo_employee.x_studio_centro_de_costos else 'N/A',
            "numero_cuenta_bancaria": odoo_employee.x_studio_nmero_de_cuenta_bancaria if odoo_employee.x_studio_nmero_de_cuenta_bancaria else 'N/A',
            "banco": odoo_employee.x_studio_many2one_field_p7Ucx.x_name if odoo_employee.x_studio_many2one_field_p7Ucx.x_name else 'N/A',
            "codigo_banco": odoo_employee.x_studio_cdigo_banco if odoo_employee.x_studio_cdigo_banco else 'N/A',
            "blood_type": odoo_employee.x_studio_rh if odoo_employee.x_studio_rh else 'N/A',
            "zona": odoo_employee.x_studio_zona_proyecto_aseo if odoo_employee.x_studio_zona_proyecto_aseo else 'N/A',
            "eps": odoo_employee.x_studio_many2one_field_qIGM2.x_name if odoo_employee.x_studio_many2one_field_qIGM2.x_name else 'N/A',
            "pension": odoo_employee.x_studio_many2one_field_GtifE.x_name if odoo_employee.x_studio_many2one_field_GtifE.x_name else 'N/A',
            "severance": odoo_employee.x_studio_many2one_field_arquY.x_name if odoo_employee.x_studio_many2one_field_arquY.x_name else 'N/A',
            "pant_size": odoo_employee.x_studio_many2one_field_ZfzC2.x_name if odoo_employee.x_studio_many2one_field_ZfzC2.x_name else 'N/A',
            "shirt_size": odoo_employee.x_studio_many2one_field_WqjQH.x_name if odoo_employee.x_studio_many2one_field_WqjQH.x_name else 'N/A',
            "shoes_size": odoo_employee.x_studio_many2one_field_rv1KK.x_name if odoo_employee.x_studio_many2one_field_rv1KK.x_name else 'N/A',
            "dress_style": odoo_employee.x_studio_estilo if odoo_employee.x_studio_estilo else 'N/A',
            "nivel_riesgo": odoo_employee.x_studio_nivel_de_riesgo_1 if odoo_employee.x_studio_nivel_de_riesgo_1 else 'N/A',
            "salario": odoo_employee.x_studio_salario_empleado_actual if odoo_employee.x_studio_salario_empleado_actual else 'N/A',
            "fecha_de_ingreso": odoo_employee.x_studio_fecha_de_ingreso_1 if odoo_employee.x_studio_fecha_de_ingreso_1 else 'N/A',
            "actualiza_datos_generales": odoo_employee.x_studio_requiere_actualiza_datos_generales,
            "politica_datos_generales": odoo_employee.x_studio_poltica_tratamiento_datos
        }

        return employee
    
    '''
    Function that search in Odoo by ID number and return odoo_employee.x_studio_requiere_actualiza_datos_generales and odoo_employee.x_studio_poltica_tratamiento_datos
    '''
    def get_employee_data_status(self, employee_identification):
        odoo_context = self.odoo.env['hr.employee']
     
        # Employee identification is Interger
        odoo_employee_id = odoo_context.search([('name', '=', employee_identification)])
        if not odoo_employee_id:
            return None
        
        odoo_employee = odoo_context.browse(odoo_employee_id)
        employee_data = {
            "is_data_updated": odoo_employee.x_studio_requiere_actualiza_datos_generales,
            "is_data_accepted": odoo_employee.x_studio_poltica_tratamiento_datos
        }

        return employee_data
    
    def update_employee_data_policies(self, employee_identification, data_policy, data_treatment):
        odoo_context = self.odoo.env['hr.employee']
     
        # Employee identification is Interger
        odoo_employee_id = odoo_context.search([('name', '=', employee_identification)])
        if not odoo_employee_id:
            return None
        
        odoo_employee = odoo_context.browse(odoo_employee_id)
        employee_data = {
            "x_studio_requiere_actualiza_datos_generales": '1' if data_policy else '0',
            "x_studio_poltica_tratamiento_datos": '1' if data_treatment else '0'
        }

        odoo_employee.write(employee_data)

        return employee_data

    
    def create__or_update_employee(self, employee_name="", employee_email=""):
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
    

    # Get states from Colombia
    '''
    def get_states(self):
        states = self.odoo.env['res.country.state'].search_read(
            [], ['id', 'name', 'code'])
        return states
    '''

    def get_employee_data(self, employee_odoo_id):
        '''
        También recibe un campo de empleado desde Odoo que indica que los campos generales están completos
        '''

    def update_employee_data(self, data):
        '''
        Update data from employee in Odoo
        get employee_id (identification number) and data to update
        '''
        # Obtiene el empleado a partir del employee_id
        employee_identification = data['id_document']
        
        employee = self.search_employee_by_identification(employee_identification)

        # Crear datos para actualizar en Odoo a partir de parámetro data
        employee_data = {}

        employee_data['birthday'] = data['birth_date']
        employee_data['x_studio_lugar_de_nacimiento'] = data['birth_place']
        employee_data['name'] = data['id_document']
        employee_data['x_studio_nmero_de_cuenta_bancaria'] = data['bank_account_number']
        employee_data['x_studio_many2one_field_p7Ucx'] = data['bank_name']
        employee_data['gender'] = data['gender']

        employee_data['address_home_id'] = data['home_address']
        employee_data['x_studio_barrio'] = data['home_neighborhood']
        employee_data['x_studio_municipio'] = data['home_city']
        employee_data['work_home'] = data['telephone1']
        employee_data['mobile_phone'] = data['cellphone']
        employee_data['x_studio_correo_electrnico_personal'] = data['email']

        # Campo para validar que los datos estén completos
        employee_data['x_studio_requiere_actualiza_datos_generales'] = data['is_data_updated']
        
        # Campo de autorización de tratamiento de datos personales
        data['is_data_treatment_accepted ']

        # Actualiza los datos del empleado en Odoo
        employee.write(employee_data)

        # Actualiza los datos del empleado



'''
user_count = api.execute_kw(database, uid, password,
                            "res.users", "search_count", [[]])
print(f"User count is: {user_count}")

companies = api.execute_kw(database, uid, password, "res.users", "read", [
                           uid, ["login", "name", "company_id"]])
print("User companies: ")
print(companies)
'''
