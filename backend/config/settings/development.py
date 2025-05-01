from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] += (
    "rest_framework.authentication.SessionAuthentication",
) # Para usar el login de DRF en desarrollo local