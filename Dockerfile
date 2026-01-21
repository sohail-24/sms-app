# ---------- Base image ----------
FROM python:3.11-slim

# ---------- Environment ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------- System dependencies ----------
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---------- Work directory ----------
WORKDIR /app

# ---------- Install Python dependencies ----------
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---------- Copy project ----------
COPY . .

# ---------- Collect static files ----------
RUN python manage.py collectstatic --noinput || true

# ---------- Expose port ----------
EXPOSE 8000

# ---------- Run with Gunicorn (PRODUCTION) ----------
CMD ["gunicorn", "SMS.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

