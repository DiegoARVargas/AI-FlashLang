# Usa una imagen ligera de Python
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copia los requerimientos primero para aprovechar la caché
COPY requirements.txt .

# Instala los paquetes de Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Expone el puerto que usará Gunicorn
EXPOSE 8000

# Ejecuta collectstatic
RUN python manage.py collectstatic --noinput

# 🔎 Agrega este comando temporal para inspeccionar
RUN ls -lR /app/staticfiles/

# Arranca Gunicorn
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Comando por defecto al iniciar el contenedor:
# 1. Ejecuta collectstatic (para cargar archivos estáticos).
# 2. Inicia Gunicorn para servir la aplicación.
#CMD python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000
