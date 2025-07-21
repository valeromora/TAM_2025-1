
# 📊 Chatbot de Indicadores de Colombia

Este proyecto integra una **API en FastAPI** con un **frontend en Streamlit** para consultar y visualizar respuestas basadas en una colección embebida con ChromaDB y generadas por modelos de OpenAI. Está diseñado para responder preguntas sobre indicadores de desarrollo en Colombia.

## 🧠 Tecnologías utilizadas

- **FastAPI** – API REST para recibir preguntas y responder usando GPT.
- **Streamlit** – Interfaz gráfica interactiva.
- **OpenAI** – Generación de respuestas contextuales.
- **ChromaDB** – Almacenamiento vectorial local.
- **Python-dotenv** – Gestión de claves a través de archivo `.env`.

## 📁 Estructura del proyecto

```
├── chatbot.py          # Lógica de embeddings y respuesta con OpenAI
├── main.py             # Backend API con FastAPI
├── dash_app.py         # Interfaz con Streamlit
├── requirements.txt    # Dependencias del proyecto
├── .env                # Clave de OpenAI (no incluida en el repositorio)
```

## 🚀 Cómo ejecutar el proyecto

### 1. Clonar el repositorio y entrar al directorio

```bash
git clone https://github.com/tu_usuario/chatbot-colombia.git
cd chatbot-colombia
```

### 2. Crear el archivo `.env` con tu API key de OpenAI

```env
OPENAI_API_KEY=sk-xxxxxx...
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la API (puerto 8000)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 5. En otra terminal, ejecutar Streamlit (puerto 8501)

```bash
streamlit run dash_app.py
```

## 🌐 Acceso

- API: http://localhost:8000/docs
- Frontend: http://localhost:8501

## 📝 Licencia

MIT License
