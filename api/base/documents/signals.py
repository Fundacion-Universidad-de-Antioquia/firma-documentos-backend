from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.conf import settings
from api.base.documents.tasks import create_pdf


@receiver(post_save)
def approval():
    pass
