# Usar la imagen completa de Python para evitar la falta de librerías base en WeasyPrint
FROM python:3.11

# Evitar archivos .pyc y permitir logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar solo las herramientas de renderizado específicas (la imagen completa ya trae el resto)
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libpangocairo-1.0-0 \
    libcairo2 \
    shared-mime-info \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Usar shell para garantizar que la variable $PORT de Railway se asigne correctamente
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]