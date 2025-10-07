# Imagen base oficial de Python
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Puerto por defecto para Azure Container Apps
EXPOSE 8080

CMD ["python", "app.py"]
