# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece directorio de trabajo
WORKDIR /app

# Copia archivos
COPY . /app

# Instala dependencias
RUN pip install --no-cache-dir fastapi uvicorn streamlit requests chromadb openai python-dotenv

# Expone los puertos
EXPOSE 8000 8501

# Usa un script para lanzar ambas apps en segundo plano
CMD ["bash", "-c", "\
  uvicorn main:app --host 0.0.0.0 --port 8000 & \
  streamlit run dash_app.py --server.port=8501 --server.address=0.0.0.0"]