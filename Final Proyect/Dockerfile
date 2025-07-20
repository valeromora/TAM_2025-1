# Dockerfile actualizado
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Asegurarse de que el storage existe en el contenedor
RUN mkdir -p /app/chroma_storage

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
