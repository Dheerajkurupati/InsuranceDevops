FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --default-timeout=100 --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["python", "app.py"]

