FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    chown -R appuser:appuser /app

USER appuser

ENTRYPOINT ["sh", "/app/entrypoint.sh"]

# ---- Default command ----
# Para dev, isso é sobrescrito pelo docker-compose (usa runserver)
# Para produção, isso será trocado por gunicorn (Etapa 9)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000