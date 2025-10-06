# مرحله ۱: انتخاب بیس ایمیج
FROM python:3.12-slim

# مرحله ۲: تنظیم متغیرهای محیطی
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# مرحله ۳: ایجاد دایرکتوری برای اپ
WORKDIR /app

# مرحله ۴: نصب وابستگی‌ها
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# مرحله ۵: کپی کل پروژه داخل کانتینر
COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
