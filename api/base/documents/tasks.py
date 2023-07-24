from __future__ import absolute_import, unicode_literals

import os
import zipfile
import datetime
from firma.celery    import app
from django.conf import settings
from openpyxl import load_workbook
from celery.utils.log import get_task_logger

from .models import Files, ContractDocument
from ..employees.models import Employee
from utils import document
from utils.odoo_client import OdooClient

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


@app.task(name="send_pdf_files_task")
async  def send_zip_file_task(zip_file, xls_file, company_sign=True):
    '''
    Create a folder with the date inside media
    Extract Zip file with all the pdf files
    Open xls file with the data
    Iterate:
      Get the employee data from xls file: name, email, file name
      Get employee ID from Odoo, if not found, create new employee
      Send pdf file to Odoo
      Update PDF with sign fields
      Tell Odoo to send the document via email to sign

    :param zip_file: Zip file with all the pdf files
    :param xls_file: XLS file with the data
    :param company_sign: True if the company sign is required
    '''
    logger.info("Starting task to send pdf files")

    # Get system date and create a folder inside media folder with the date
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    os.mkdir(f'media/{date}')

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(f'media/{date}')

    
    xls = load_workbook(filename=xls_file, read_only=True, keep_vba=True)

    # get first sheet
    data_sheet = xls.worksheets[0]
        
    # Get column names
    column_names = [c.value for c in data_sheet[1] if c.value is not None]

    # Connect to Odoo
    odoo = OdooClient()
    odoo.connect()
     
    # Iterate to get the data
    for row in data_sheet.iter_rows(min_row=2, values_only=True):
        # Get employee data from XLSX File
        employee_data = {column_names[i]: row[i] for i in range(len(column_names))}

        # Get employee ID from Odoo
        employee_odoo_id = await odoo.search_employee(employee_email=employee_data['email'])
        if employee_odoo_id is None:
            employee_odoo_id = await odoo.create_employee(employee_data['nombre'], employee_data['email'])

        # Get company signer ID from Odoo
        company_id = odoo.search_employee(employee_email=employee_data['email_fundacion']) if company_sign else None

        # Transform PDF to base64
        document_64, numpages = document.convert_pdf_to_base64(f'media/{date}/{employee_data["nombre_archivo"]}')

        # Upload PDF file
        pdf_id = odoo.upload_new_contract_sign(employee_data['nombre_archivo'], document_64)

        # Update PDF with sign fields
        sign_id = odoo.update_contract_sign(template_id=pdf_id, numpage=numpages, second_field=company_sign)
        
        # Send document to sign
        odoo.send_sign_contract(pdf_id, employee_odoo_id, company_id)

        # Create new ContractDocument database record
        contract_document = ContractDocument.objects.create(
                                    name=employee_data['nombre'],
                                    path=str(date),
                                    sign_id=sign_id,
                                    employee_id=employee_odoo_id
                                    )
        contract_document.save()
