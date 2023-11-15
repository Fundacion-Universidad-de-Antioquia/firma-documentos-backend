from __future__ import absolute_import, unicode_literals

import os
import zipfile
import datetime
from celery import shared_task
from django.conf import settings
from django.conf import settings
from firma.celery import app
from openpyxl import load_workbook
from celery.utils.log import get_task_logger
from azure.core.exceptions import ResourceExistsError

from .models import Files, ContractDocument, ZipFile
from utils import document
from utils.odoo_client import OdooClient
from utils.azure_services import connect_to_azure_storage

logger = get_task_logger(__name__)


@app.task(name="send_contract_sign_task")
def send_contract_sign_task(files_id):
    logger.info("Start sending odoo contracts")

    # get files from database
    files = Files.objects.filter(id=files_id).first()

    '''
    contract_path = os.path.join(
        settings.MEDIA_ROOT+'/docs/', files.contract_name)
    employees_data_path = os.path.join(
       settings.MEDIA_ROOT+'/docs/', files.employees_data_name)
    '''

    # Send contract to odoo
    document.create_pdfs(files.contract_template , files.employees_data)
    logger.info("Odoo contracts sent")
    pass


@app.task(name="send_zip_file_task")
def send_zip_file_task(zip_task_id):
    '''
    Create a folder with the date inside media
    Extract Zip file with all the pdf files
    Open xls file with the data
    Iterate:
      Get the employee data from xls file: name, email, file name
      Get employee ID from Odoo, if not found, create new employee
      Send pdf file to Odoo
      Update PDF file with sign fields
      Tell Odoo to send the document via email to sign

    :param zip_file: Zip file with all the pdf files
    :param xls_file: XLS file with the data
    :param company_sign: True if the company sign is required
    '''
    print("Entré ya")
    logger.info("Starting task to send pdf files")

    # Get the files from database
    # Update the upload path from this documents
    # TOFIX: Add docs path as a variable, i.e, media/docs
    zip_task = ZipFile.objects.filter(id=zip_task_id).first()
    zip_file = f'media/{zip_task.zip_file}'
    xls_file = f'media/{zip_task.xlsx_file}'
    company_sign = zip_task.signs_number


    # Get system date and create a folder inside media folder with the date
    folder_name = 'contracts_' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    blob_service_client = connect_to_azure_storage()

    try:
        os.mkdir('media/docs/' + folder_name)
    except FileExistsError as fError:
        logger.info(fError)


    with zipfile.ZipFile(zip_file, 'r') as zObject:
        file_list = zObject.infolist()
        zObject.extractall(path = 'media/docs/' + folder_name)
    
    # Get the first file in the list to get the path
    generated_dir = file_list[0].filename.split('/')[0]

    for contract_file in file_list:
        # TODO: Quita acentos en nombre del archivo: i.e. 'Álvaro' -> 'Alvaro', eso genera problema con Azure Storage
        # TODO: Maneja esto con exceptions para que no se caiga el proceso
        file_path = 'media/docs/' + folder_name + '/' + contract_file.filename

        # Enter if the file exists and is not a directory
        if os.path.exists(file_path) and not os.path.isdir(file_path):
            try:
                blob_client = blob_service_client.get_blob_client(container=settings.AZURE_STORAGE_CONTAINER, blob=file_path)
                with open(file_path, 'rb') as data:
                    blob_client.upload_blob(data)
                logger.info("File uploaded to Azure: " + contract_file.filename)
            except ResourceExistsError as rError:
                logger.info(rError)
        else:
            blob_service_client.close()
            return {"error": "No se envió archivos"}
    
    # Close connection to Azure
    blob_service_client.close()

    xls = load_workbook(filename=xls_file, read_only=True, keep_vba=True, data_only=True)

    # get first sheet
    data_sheet = xls.worksheets[0]
        
    # Get column names
    column_names = [c.value for c in data_sheet[1] if c.value is not None]

    # Connect to Odoo
    odoo = OdooClient()
     
    # Iterate to get the data
    for row in data_sheet.iter_rows(min_row=2, values_only=True):
        # TODO: Maneja esto con exceptions para que no caiga el proceso
        # Get employee data from XLSX File
        employee_data = {column_names[i]: row[i] for i in range(len(column_names))}

        # Get employee ID from Odoo
        employee_email = employee_data['CORREO'].strip()
        
        print('Correo empleado: '+employee_email)

        employee_odoo_id = odoo.search_employee(employee_email)
        # TODO: Pasar correo a minúsculas para evitar duplicados en Odoo
        if employee_odoo_id is None:
            employee_name = employee_data['NOMBRES Y APELLIDOS'].strip()
            print ('Creando empleado: ' + employee_name)
            employee_odoo_id = odoo.create_employee(employee_name, employee_email)

        # Get company signer ID from Odoo
        # TOFIX: Get company email from Odoo and search by email, maybe get directly the ID
        print(f'Firma Companía?: {company_sign}')
        # directorejectivo@fundacionudea.co
        # TODO: Cambiar el correo de la firma de la Fundación UdeA por una variable que llegue desde el form del frontend
        company_id = odoo.search_employee('directorejecutivo@fundacionudea.co') if company_sign == 2 else None
        
        # Transform PDF to base64, get number of pages to add sign fields in the last page
        nombre_archivo = employee_data['NOMBRE_ARCHIVO']

        # Full path to the file
        full_contract_path = 'media/docs/' + folder_name + '/' +  generated_dir + '/'+ nombre_archivo + '.pdf'
        try:
            document_64, numpages = document.convert_pdf_to_base64(full_contract_path)
        except FileNotFoundError as fError:
            # Continua al siguiente archivo
            logger.info(fError)
            continue

        # Upload PDF file
        pdf_id = odoo.upload_new_contract_sign(nombre_archivo, document_64)

        # Update PDF with sign fields
        second_field = True if company_sign == 2 else False
        sign_id = odoo.update_contract_sign(template_id=pdf_id, numpage=numpages, second_field=second_field)
        
        # Send document to sign
        odoo.send_sign_contract(pdf_id, nombre_archivo, employee_odoo_id, company_id)

        print('Documento enviado a firmar '+nombre_archivo)

        # Create new ContractDocument database record
        # contract_document = ContractDocument.objects.create(
        #                            name=employee_data['NOMBRES Y APELLIDOS'],
        #                            path=str(nombre_archivo + ".pdf"),
        #                            sign_id=sign_id,
        #                            employee_id=employee_odoo_id)
        # contract_document.save()
    return {"message": "Archivos enviados"}
