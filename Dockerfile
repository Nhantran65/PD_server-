FROM python:3.10-slim

# Tạo thư mục làm việc
WORKDIR /app

# Copy source code
COPY . /app

# Cài đặt thư viện
RUN pip install --no-cache-dir -r requirements.txt

# Mở port FastAPI chạy
EXPOSE 8000

# Lệnh chạy uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
