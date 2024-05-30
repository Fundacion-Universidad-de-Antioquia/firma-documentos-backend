import base64
import odoorpc
from xmlrpc.client import Binary

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

        # en Odoo identification_id es el nombre del empleado
        employee = {
            "full_name": odoo_employee.identification_id if odoo_employee.identification_id else 'N/A',
            "gender": odoo_employee.gender if odoo_employee else 'N/A',
            "birth_date": odoo_employee.birthday if odoo_employee.birthday else 'N/A',
            "birth_place": odoo_employee.x_studio_lugar_de_nacimiento.x_name if odoo_employee.x_studio_lugar_de_nacimiento.x_name else 'N/A',
            "birth_country": odoo_employee.country_of_birth.name if odoo_employee.country_of_birth.name else 'N/A',
            "email": odoo_employee.x_studio_correo_electrnico_personal if odoo_employee.x_studio_correo_electrnico_personal else 'N/A',
            "email_work": odoo_employee.work_email if odoo_employee.work_email else 'N/A',
            "address_home_id": odoo_employee.address_home_id.name if odoo_employee.address_home_id.name else 'N/A',
            "home_neighborhood": odoo_employee.x_studio_barrio if odoo_employee.x_studio_barrio else 'N/A',
            "home_city": odoo_employee.x_studio_municipio.x_studio_cdigo_municipio_1 if odoo_employee.x_studio_municipio.x_studio_cdigo_municipio_1 else 'N/A',
            "telephone1": odoo_employee.work_phone if odoo_employee.work_phone else 'N/A',
            "cellphone": odoo_employee.mobile_phone if odoo_employee.mobile_phone else 'N/A',
            "employee_project": odoo_employee.company_id.name if odoo_employee.company_id.name else 'N/A',
            "employee_rol": odoo_employee.job_title if odoo_employee.job_title else 'N/A',
            "id_document": odoo_employee.name if odoo_employee.name else 'N/A',
            "cost_center": odoo_employee.x_studio_centro_de_costos if odoo_employee.x_studio_centro_de_costos else 'N/A',
            "bank_account_number": odoo_employee.x_studio_nmero_de_cuenta_bancaria if odoo_employee.x_studio_nmero_de_cuenta_bancaria else 'N/A',
            "bank_name": odoo_employee.x_studio_many2one_field_p7Ucx.x_name if odoo_employee.x_studio_many2one_field_p7Ucx.x_name else 'N/A',
            "blood_type": odoo_employee.x_studio_rh if odoo_employee.x_studio_rh else 'N/A',
            "employee_zone": odoo_employee.x_studio_zona_proyecto_aseo if odoo_employee.x_studio_zona_proyecto_aseo else 'N/A',
            "eps": odoo_employee.x_studio_many2one_field_qIGM2.x_name if odoo_employee.x_studio_many2one_field_qIGM2.x_name else 'N/A',
            "pension": odoo_employee.x_studio_many2one_field_GtifE.x_name if odoo_employee.x_studio_many2one_field_GtifE.x_name else 'N/A',
            "severance": odoo_employee.x_studio_many2one_field_arquY.x_name if odoo_employee.x_studio_many2one_field_arquY.x_name else 'N/A',
            "pant_size": odoo_employee.x_studio_many2one_field_ZfzC2.x_name if odoo_employee.x_studio_many2one_field_ZfzC2.x_name else 'N/A',
            "shirt_size": odoo_employee.x_studio_many2one_field_WqjQH.x_name if odoo_employee.x_studio_many2one_field_WqjQH.x_name else 'N/A',
            "shoes_size": odoo_employee.x_studio_many2one_field_rv1KK.x_name if odoo_employee.x_studio_many2one_field_rv1KK.x_name else 'N/A',
            "dress_style": odoo_employee.x_studio_estilo if odoo_employee.x_studio_estilo else 'N/A',
            "level_risk": odoo_employee.x_studio_nivel_de_riesgo_1 if odoo_employee.x_studio_nivel_de_riesgo_1 else 'N/A',
            "salary": odoo_employee.x_studio_salario_empleado_actual if odoo_employee.x_studio_salario_empleado_actual else 'N/A',
            "entry_date": odoo_employee.x_studio_fecha_de_ingreso_1 if odoo_employee.x_studio_fecha_de_ingreso_1 else 'N/A',
            "employee_code": odoo_employee.x_studio_codigo if odoo_employee.x_studio_codigo else 'N/A',
            "employee_status": odoo_employee.x_studio_estado_empleado if odoo_employee.x_studio_estado_empleado else 'N/A'
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
            "is_data_updated": True if odoo_employee.x_studio_requiere_actualiza_datos_generales == "Si" else False,
            "is_data_accepted": True if odoo_employee.x_studio_poltica_tratamiento_datos == "Si" else False
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
            "x_studio_requiere_actualiza_datos_generales": 'Si' if data_policy else 'No',
            "x_studio_poltica_tratamiento_datos": 'Si' if data_treatment else 'No'
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

    def update_employee_data(self, employee_identification, data):
        '''
        Update data from employee in Odoo
        get employee_id (identification number) and data to update
        '''
        # Obtiene el empleado a partir del employee_id
        # employee_identification = data['id_document']
        
        # employee = self.search_employee_by_identification(employee_identification)
        odoo_context = self.odoo.env['hr.employee']

        # Get list[] from employee with name = employee_identification
        employee = odoo_context.search([('name', '=', employee_identification)])
        employee = odoo_context.browse(employee[0])
        # Crear datos para actualizar en Odoo a partir de parámetro data
        employee_data = {}

        gender_mapping = {"masculino": "male", "femenino": "female", "otro": "other"}

        try:
            if data.get('id_document') and data.get('id_document') != 'N/A':
                employee_data['name'] = data.get('id_document')
            
            if data.get('full_name') and data.get('full_name') != 'N/A':
                employee_data['identification_id'] = data.get('full_name')

            if data.get('birth_date') and data.get('birth_date') != 'N/A':
                employee_data['birthday'] = data.get('birth_date')

            if data.get('bank_account_number') and data.get('bank_account_number') != 'N/A':
                employee_data['x_studio_nmero_de_cuenta_bancaria'] = data.get('bank_account_number')
            
            if data.get('gender') and data.get('gender') != 'N/A':
                gender_spanish = data.get('gender')
                employee_data['gender'] = gender_mapping.get(gender_spanish.lower(), None)
            
            if data.get('blood_type') and data.get('blood_type') != 'N/A':
                employee_data['x_studio_rh'] = data.get('blood_type')
   
            if data.get('home_neighborhood') and data.get('home_neighborhood') != 'N/A':
                employee_data['x_studio_barrio'] = data.get('home_neighborhood')
            
            if data.get('telephone1') and data.get('telephone1') != 'N/A':
                employee_data['work_phone'] = data.get('telephone1')
            
            if data.get('cellphone') and data.get('cellphone') != 'N/A':
                employee_data['mobile_phone'] = data.get('cellphone')
            
            if data.get('email') and data.get('email') != 'N/A':
                employee_data['x_studio_correo_electrnico_personal'] = data.get('email')
            
            if data.get('dress_style') and data.get('dress_style') != 'N/A':
                employee_data['x_studio_estilo'] = data.get('dress_style')


            # Actualizar con relaciones con Otros modelos

            if data.get('address_home_id') and data.get('address_home_id') != 'N/A':
                context = self.odoo.env['res.partner']
                address_id = context.search([('name', '=', data.get('address_home_id'))])
                if not address_id:
                    address_id = context.create({'name': data.get('address_home_id')})
                address = context.browse(address_id)
                employee.address_home_id = address

            if  data.get('bank') and data.get('bank_name') != 'N/A':
                context = self.odoo.env['x_banco']  
                bank_id = context.search([('x_name', '=', data.get('bank_name'))])
                bank = context.browse(bank_id)
                employee.x_studio_many2one_field_p7Ucx  = bank
            
            if data.get('eps') and data.get('eps') != 'N/A':
                context = self.odoo.env['x_eps']
                eps_id = context.search([('x_name', '=', data.get('eps'))])
                eps = context.browse(eps_id)
                employee.x_studio_many2one_field_qIGM2 = eps

            if data.get('home_city') and data.get('home_city') != 'N/A':
                context = self.odoo.env['x_bancos']
                city_id = context.search([('x_studio_cdigo_municipio_1', '=', data.get('home_city'))])
                city = context.browse(city_id)
                employee.x_studio_municipio = city
            
            if data.get('birth_place') and data.get('birth_place') != 'N/A':
                context = self.odoo.env['x_municipios']
                city_id = context.search([('x_studio_cdigo_municipio_1', '=', data.get('birth_place'))])
                city = context.browse(city_id)
                employee.x_studio_lugar_de_nacimiento = city
            
            if data.get('birth_country') and data.get('birth_country') != 'N/A':
                context = self.odoo.env['res.country']
                country_id = context.search([('name', '=', data.get('birth_country'))])
                country = context.browse(country_id)
                employee.x_studio_pais_de_nacimiento = country

            if data.get('pension') and data.get('pension') != 'N/A':
                context = self.odoo.env['x_afp']
                pension_id = context.search([('x_name', '=', data.get('pension'))])
                pension = context.browse(pension_id)
                employee.x_studio_many2one_field_GtifE = pension
            
      
            if data.get('shirt_size') and data.get('shirt_size') != 'N/A':
                context = self.odoo.env['x_talla_camisa']
                shirt_id = context.search([('x_name', '=', data.get('shirt_size'))])
                shirt = context.browse(shirt_id)
                employee.x_studio_many2one_field_WqjQH = shirt

            if data.get('pant_size') and data.get('pant_size') != 'N/A':
                context = self.odoo.env['x_talla_pantalon']
                pant_id = context.search([('x_name', '=', data.get('pant_size'))])
                pant = context.browse(pant_id)
                employee.x_studio_many2one_field_ZfzC2 = pant

            if data.get('shoes_size') and data.get('shoes_size') != 'N/A':
                context = self.odoo.env['x_talla_calzado']
                shoe_id = context.search([('x_name', '=', data.get('shoes_size'))])
                shoe = context.browse(shoe_id)
                employee.x_studio_many2one_field_rv1KK = shoe

            # Actualiza los datos del empleado en Odoo
            employee.write(employee_data)
            return employee.id
        except Exception as e:
            print(f"Error al actualizar datos de empleado: {e}, Causa: {e.__cause__}")
            return False
    
    def get_employee_profile_image(self, identification_number):
        '''
        Get the profile image of an employee in Odoo
        '''
        odoo_context = self.odoo.env['hr.employee']
        employee = odoo_context.search([('name', '=', identification_number)])
        if employee:
            employee = odoo_context.browse(employee[0])
            profile_image = employee.image_1920 if employee.image_1920 else None
            return profile_image
        else:
            return None
    
    def update_employee_image(self, identification_number, image_base64):
        '''
        Update the profile image of an employee in Odoo
        '''
        odoo_context = self.odoo.env['hr.employee']
        employee = odoo_context.search([('name', '=', identification_number)])
        if employee:
            employee = odoo_context.browse(employee[0])
            employee_data = {}

            # Remove the "data:image/png;base64," part from the base64 string
            image_base64 = image_base64.split(",")[1]
             # Convert the base64 string to binary data
            image_binary = base64.b64decode(image_base64)

            employee_data['image_1920'] = image_base64
            employee.write(employee_data)
            return True
        else:
            return False
    
    def get_list_options(self):
        '''
        Obtiene lista de opciones de los campos de Odoo para el formulario de registro
        '''
        list_options = {}

        # Agrega EPS
        odoo_context = self.odoo.env['x_eps']
        eps_ids = odoo_context.search([])
        eps_dict = {}
        for eps in odoo_context.browse(eps_ids):
            # Add eps name and eps code to the list
            eps_dict[eps.id] = {"name": eps.x_name, "code": eps.x_studio_cdigo}        
        list_options["eps"] = eps_dict

        odoo_context = self.odoo.env['x_banco']
        banks_ids = odoo_context.search([])
        banks_dict = {}
        for bank in odoo_context.browse(banks_ids):
            banks_dict[bank.id] = {"name": bank.x_name, "code": bank.x_studio_cdigo_banco}
        list_options["banks"] = banks_dict

        odoo_context = self.odoo.env['x_afp']
        pension_ids = odoo_context.search([])
        pension_dict = {}
        for pension in odoo_context.browse(pension_ids):
            pension_dict[pension.id] = {"name": pension.x_name, "code": pension.x_studio_cdigo}
        list_options["afp"] = pension_dict


        odoo_context = self.odoo.env['x_cesantias']
        severance_ids = odoo_context.search([])
        severance_dict = {}
        for severance in odoo_context.browse(severance_ids):
            severance_dict[severance.id] = {"name": severance.x_name, "code": severance.x_studio_cdigo_nmina_1}
        list_options["severance"] = severance_dict

        # Tallajes
        odoo_context = self.odoo.env['x_talla_camisa']
        shirt_ids = odoo_context.search([])
        shirt_dict = {}
        for shirt in odoo_context.browse(shirt_ids):
            shirt_dict[shirt.id] = {"name": shirt.x_name, "code": shirt.x_name}
        list_options["shirt_size"] = shirt_dict

        odoo_context = self.odoo.env['x_talla_pantalon']
        pant_ids = odoo_context.search([])
        pant_dict = {}
        for pant in odoo_context.browse(pant_ids):
            pant_dict[pant.id] = {"name": pant.x_name, "code": pant.x_name}
        list_options["pant_size"] = pant_dict

        odoo_context = self.odoo.env['x_talla_calzado']
        shoe_ids = odoo_context.search([])
        shoe_dict = {}
        for shoe in odoo_context.browse(shoe_ids):
            shoe_dict[shoe.id] = {"name": shoe.x_name, "code": shoe.x_name}
        list_options["shoes_size"] = shoe_dict

        # Ubicaciones
        odoo_context = self.odoo.env['x_bancos']
        cities_ids = odoo_context.search([])
        cities_dict = {}
        for city in odoo_context.browse(cities_ids):
            cities_dict[city.id] = {"name": str(city.x_name)+'-'+str(city.x_studio_departamento), 
                                   "code": city.x_studio_cdigo_municipio_1}
        list_options["cities"] = cities_dict

        odoo_context = self.odoo.env['res.country']
        countries_ids = odoo_context.search([])
        countries_dict = {}
        for country in odoo_context.browse(countries_ids):
            countries_dict[country.id] = {"name": country.name, "code": country.code}
        
        list_options["countries"] = countries_dict

        return list_options
        




'''
user_count = api.execute_kw(database, uid, password,
                            "res.users", "search_count", [[]])
print(f"User count is: {user_count}")

companies = api.execute_kw(database, uid, password, "res.users", "read", [
                           uid, ["login", "name", "company_id"]])
print("User companies: ")
print(companies)
'''
