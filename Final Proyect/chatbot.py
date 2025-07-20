from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
import os

# === CONFIGURACIÓN ===
OPENAI_API_KEY = "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"  # o usa dotenv
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