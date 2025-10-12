FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# ---------- مرحله ۴: نصب وابستگی‌های سیستم ----------
# نصب ابزارهای موردنیاز برای psycopg2 (PostgreSQL) و غیره
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt


COPY . /app/

# ---------- مرحله ۷: اضافه کردن entrypoint ----------
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENV DOCKER=1
# ---------- مرحله ۸: تعیین entrypoint ----------
ENTRYPOINT ["/entrypoint.sh"]


#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
