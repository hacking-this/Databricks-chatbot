import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from ollama import Client

# Load once
client = chromadb.PersistentClient(path="chroma")
collection = client.get_or_create_collection(name="databricks-docs")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
ollama_client = Client(host="http://localhost:11434")  # Default for Ollama

def get_response(query: str, chat_history=None) -> str:
    history_prompt = ""
    if chat_history:
        for role, msg in chat_history:
            prefix = "User" if role=="User" else "Assistant"
            history_prompt += f"{prefix}: {msg}\n"
    # Embed user query
    embedded_query = embedding_model.encode(query).tolist()

    # Search ChromaDB
    results = collection.query(query_embeddings=[embedded_query], n_results=5)
    context_chunks = [doc for doc in results["documents"][0]]
    context = "\n\n".join(context_chunks)

    # Build prompt
    prompt = f"""
You are a specialized in Databricks.
Use the documentation below only if it is directly relevant to the user's question.

Instructions:
- If the question is a greeting like "thanks", "okay", or "hi", just reply politely without technical content.
- If the question is "What is Databricks?" or similar, give a short 2-3 sentence description — no extra detail and if asked for more then give more details.
- Do not answer beyond what was asked until and unless asked.
- Only include SQL or PySpark if the user asks for code.

Documentation:
{context}

Question: {query}

Answer:
"""

    # Generate answer with Ollama
    response = ollama_client.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response['message']['content']
