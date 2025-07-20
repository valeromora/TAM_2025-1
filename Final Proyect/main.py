from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import responder_pregunta

app = FastAPI(
    title="Chatbot de Indicadores Colombia",
    description="API para consultar indicadores preprocesados con ChromaDB y responder usando OpenAI",
    version="2.0.0"
)

class Query(BaseModel):
    question: str

@app.post("/chat")
async def chat(query: Query):
    try:
        answer = responder_pregunta(query.question)
        return {
            "question": query.question,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))