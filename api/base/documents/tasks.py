from __future__ import absolute_import, unicode_literals

import os
from firma.celery    import app
from celery.utils.log import get_task_logger
from django.conf import settings
from .models import Files
from utils import document

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
