import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions

# === CARGA DE VARIABLES DE ENTORNO ===
load_dotenv()  # Carga las variables desde el archivo .env

# === CONFIGURACIÓN ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("La variable de entorno OPENAI_API_KEY no está definida")

CHROMA_DIR = "./chroma_storage"
COLLECTION_NAME = "indicadores_colombia"

# === CLIENTES ===
client_openai = OpenAI(api_key=OPENAI_API_KEY)

embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)

chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_fn
)

# === FUNCIÓN PRINCIPAL DE RESPUESTA ===
def responder_pregunta(question: str) -> str:
    results = collection.query(
        query_texts=[question],
        n_results=5
    )

    context = "\n\n".join(results["documents"][0])

    completion = client_openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """
                            Eres un asistente especializado en indicadores de desarrollo de Colombia. Tu tarea es responder preguntas exclusivamente basándote en la información que se te proporciona en el 'Contexto'.

                            Si la respuesta a la pregunta no se encuentra explícitamente en el contexto proporcionado, indica que no dispones de esa información en los datos disponibles para la consulta.

                            Mantén un tono técnico y profesional, y responde de forma concisa, clara y siempre en español.
                            """
            },
            {
                "role": "user",
                "content": f"Contexto:\n{context}\n\nPregunta: {question}"
            }
        ],
        temperature=0.3
    )

    return completion.choices[0].message.content