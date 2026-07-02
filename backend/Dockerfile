FROM python:3.10-slim

WORKDIR /app

# ติดตั้ง System dependencies สำหรับ psycopg2 และคอมไพล์ฟังก์ชัน C
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# คัดลอกและติดตั้ง requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์โปรเจกต์ทั้งหมด
COPY . .

# ตั้งค่า PYTHONPATH
ENV PYTHONPATH=/app

# เปิด Port 8000
EXPOSE 8000

# รัน bootstrap ก่อนเพื่อสร้างข้อมูลตั้งต้น จากนั้นค่อยรัน uvicorn server
CMD python app/db/bootstrap.py && uvicorn app.main:app --host 0.0.0.0 --port 8000
