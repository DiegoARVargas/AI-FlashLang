# backend/config/storages.py

from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class MediaStorage(S3Boto3Storage):
    location = "audio"  # Carpeta base dentro del bucket
    default_acl = None  # No usaremos ACLs (obligatorio si el bucket tiene Ownership Enforced)
    file_overwrite = True  # Sobrescribe si ya existe
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN