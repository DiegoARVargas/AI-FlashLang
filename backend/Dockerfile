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

# 🔎 Inspección opcional (puedes dejarlo)
RUN ls -lR /app/staticfiles/

# 🔥 Arranca: crea superuser + gunicorn
CMD python manage.py shell -c "from users.models import CustomUser; CustomUser.objects.create_superuser('admin', 'admin@gmail.com', 'admin123456789')" && gunicorn config.wsgi:application --bind 0.0.0.0:8000
