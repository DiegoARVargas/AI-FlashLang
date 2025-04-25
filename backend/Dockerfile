# Usa una imagen ligera de Python
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias (como PostgreSQL)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copia los requerimientos primero para aprovechar la caché
COPY requirements.txt .

# Instala los paquetes de Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Ejecuta collectstatic
RUN python manage.py collectstatic --noinput

# ✅ Copia archivos estáticos recolectados a carpeta pública de Render
RUN mkdir -p /public && cp -r /app/staticfiles/* /public/

# Expone el puerto para Gunicorn
EXPOSE 8000

# Comando por defecto al iniciar el contenedor
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
