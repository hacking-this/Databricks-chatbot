import os
import glob
import uuid
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# === Config ===
DATA_DIR = "data"
CHUNK_SIZE = 500 # Number of characters per chunk
model = SentenceTransformer('all-MiniLM-L6-v2') # small, fast, good quality

# === Setup ChromaDB ===

client = chromadb.PersistentClient(path="chroma")
collection = client.get_or_create_collection(name="databricks-docs")


# === Chunking Function ===
def chunk_text(text, size=CHUNK_SIZE, overlap=100):
    chunks = []
    start=0
    while start < len(text):
        end = min(start+size, len(text))
        chunk = text[start:end].strip()
        chunks.append(chunk)
        start += size - overlap  # overlap for next chunk
    return chunks

# === Embed Files ===
for filepath in glob.glob(os.path.join(DATA_DIR, "*.txt")):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"📄 Processing: {filepath}")
    chunks = chunk_text(text)

    embeddings = model.encode(chunks).tolist()
    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"source":os.path.basename(filepath), "chunk": i} for i in range(len(chunks))]

    collection.add(ids = ids, documents = chunks, embeddings = embeddings, metadatas = metadatas)

print("✅ All documents embedded and stored in ChromaDB.")