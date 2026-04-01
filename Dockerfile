FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Forzar la ruta donde Debian Trixie/Bookworm guarda las librerías compartidas
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:/usr/lib:/usr/local/lib

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libffi-dev \
    libglib2.0-0 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libpangocairo-1.0-0 \
    libcairo2 \
    shared-mime-info \
    libpq-dev \
    gcc \
    && ldconfig \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]