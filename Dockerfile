# Usar una imagen de Python ligera pero completa
FROM python:3.11-slim

# Evitar que Python genere archivos .pyc y permitir logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema para WeasyPrint, PostgreSQL y compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libffi-dev \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido de tu proyecto al contenedor
COPY . .

# Exponer el puerto que usa Railway por defecto
EXPOSE 8080

# Comando para arrancar la aplicación usando gunicorn
# Se usa 0.0.0.0 para que sea accesible externamente y el puerto 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]