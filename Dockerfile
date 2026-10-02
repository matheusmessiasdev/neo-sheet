# ---- Base image ----
FROM python:3.12-slim

# ---- System dependencies ----
# libpq-dev é necessário para o driver psycopg2 se comunicar com o Postgres
# build-essential é necessário para compilar alguns pacotes Python (ex: psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ---- Environment variables ----
# PYTHONDONTWRITEBYTECODE: evita arquivos .pyc desnecessários dentro do container
# PYTHONUNBUFFERED: garante que prints e logs apareçam em tempo real (importante para debug)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ---- Working directory ----
WORKDIR /app

# ---- Install Python dependencies ----
# Copiamos apenas o requirements.txt primeiro (cache de layers: se só o código mudar, não reinstala deps)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---- Copy project code ----
COPY . .

# ---- Expose port ----
# Documenta que o container usa a porta 8000 (não abre de fato — isso é papel do docker-compose)
EXPOSE 8000

# ---- Default command ----
# Para dev, isso é sobrescrito pelo docker-compose (usa runserver)
# Para produção, isso será trocado por gunicorn (Etapa 9)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]