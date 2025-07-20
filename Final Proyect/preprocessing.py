import pandas as pd
import chardet
from pathlib import Path
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
import os
import tiktoken

# === CONFIGURACIÓN GENERAL ===
OPENAI_API_KEY = "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"  # tu clave
CHROMA_DIR = "chroma_storage"
COLLECTION_NAME = "indicadores_colombia"
DATA_DIR = Path("Dataset")
MAX_TOKENS = 500

# === EMBEDDING FUNCTION ===
client_openai = OpenAI(api_key=OPENAI_API_KEY)
embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)

# === INICIALIZACIÓN DE CHROMA ===
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_fn
)

# === FUNCIONES AUXILIARES ===
def read_csv(path):
    with open(path, "rb") as f:
        enc = chardet.detect(f.read())["encoding"]
    return pd.read_csv(path, encoding=enc)

def chunk_text(text, max_tokens=MAX_TOKENS):
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    return [enc.decode(tokens[i:i+max_tokens]) for i in range(0, len(tokens), max_tokens)]

def process_folder(folder: Path):
    name = folder.name
    print(f"📁 Procesando: {name}")

    metadata, dictionary, codelist, enriched = "", {}, {}, []

    for f in folder.iterdir():
        fname = f.name.lower()

        if "metadata" in fname:
            metadata = read_csv(f).to_string(index=False)
        elif "dictionary" in fname:
            df = read_csv(f)
            for _, row in df.iterrows():
                dictionary[str(row.get("Column", "")).strip()] = str(row.get("Description", "")).strip()
        elif "code list" in fname:
            df = read_csv(f)
            for _, row in df.iterrows():
                field = str(row.get("Field", "")).strip()
                val = str(row.get("Value", "")).strip()
                desc = str(row.get("Description", "")).strip()
                if field and val:
                    codelist.setdefault(field, {})[val] = desc
        elif "dataset" in fname:
            df = read_csv(f)
            for _, row in df.iterrows():
                linea = []
                for col in df.columns:
                    val = str(row[col])
                    desc = codelist.get(col, {}).get(val, val)
                    var_name = dictionary.get(col, col)
                    linea.append(f"{var_name}: {desc}")
                enriched.append(" | ".join(linea))
            break  # solo un dataset por carpeta

    base_text = f"Indicador: {name}\n\nMETADATA:\n{metadata}\n\nDATOS:\n" + "\n".join(enriched[:50])
    return base_text, name

# === PROCESAMIENTO PRINCIPAL ===
doc_id = 0
for folder in DATA_DIR.iterdir():
    if not folder.is_dir():
        continue
    content, name = process_folder(folder)
    chunks = chunk_text(content)
    ids = [f"{name}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": name, "chunk": i} for i in range(len(chunks))]
    collection.add(documents=chunks, ids=ids, metadatas=metadatas)
    print(f"✅ {name}: {len(chunks)} chunks cargados.")
