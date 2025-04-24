import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# 📁 Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 🔄 Cargar variables de entorno desde el archivo .env activo
load_dotenv(os.path.join(BASE_DIR, ".env"))

# 🔐 Configuración de seguridad
# ⚠️ Elimina el valor por defecto para forzar que siempre se defina un SECRET_KEY en producción
SECRET_KEY = os.getenv("SECRET_KEY")

# 🔐 DEBUG debe estar en False por defecto para prevenir fugas de información
DEBUG = os.getenv("DEBUG", "False") == "True"

# 🔐 ALLOWED_HOSTS se define por entorno, sin valores por defecto
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# ✅ Aplicaciones instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",   # Habilita Django REST Framework (DRF) para crear APIs
    "rest_framework_simplejwt", # Permite manejar autenticación con JWT.
    "api_vocabulary",  # Aplicación principal
    "users",  # Aplicación para gestionar usuarios
    "django_extensions", # Herramientas adicionales para desarrollo
]

# ⚙️ Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",  # ⚠️ Necesario para el admin
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # ⚠️ Necesario para autenticación
    "django.contrib.messages.middleware.MessageMiddleware",  # ⚠️ Necesario para mensajes en el admin
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 🌐 Configuración de URLs raíz
ROOT_URLCONF = "config.urls"

# 🧱 Configuración de templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # ⚠️ Usa BASE_DIR correctamente
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ⚙️ Configuración WSGI
WSGI_APPLICATION = "config.wsgi.application"

# ✅ Configuración de PostgreSQL desde variables de entorno
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "ai_flashlang_db"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# 🔐 Configuración de JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ✅ Modelo de usuario personalizado
AUTH_USER_MODEL = "users.CustomUser"

# ✅ Archivos estáticos y multimedia
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# 🔐 Seguridad para producción (sobrescrito en settings.production.py)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# SECURE_SSL_REDIRECT = True  # ✅ Descomenta en producción con HTTPS

# 🌐 CORS (para cuando integre el frontend)
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",  # Desarrollo local (Vite)
#     "https://flashlang.app",  # Producción
# ]