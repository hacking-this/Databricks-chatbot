import chromadb
from sentence_transformers import SentenceTransformer
import subprocess
import os


os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Initialize the embedding model and ChromaDB model
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="chroma")
collection = client.get_or_create_collection("databricks-docs")

# Loop to keep chatting
while True:
    user_question = input("\n🧠 Ask your Databricks question (or type 'exit'): \n> ")
    if user_question.lower() in ("exit","quit"):
        break

    # Step 1: Embed user question
    query_embedding = model.encode([user_question])[0]

    # Step 2: Query the top 5 most relevant chunks
    results = collection.query(
        query_embeddings = [query_embedding],
        n_results = 5,
        include = ["documents"]
    )

    retrieved_chunks = results["documents"][0]
    context = "\n\n".join(retrieved_chunks)


    # Step 3: Create prompt for LLM
    prompt = f"""
    You are a concise and context-aware assistant specialized in Databricks.
    Use the documentation below only if it is directly relevant to the user's question.

    Instructions:
    - If the question is a greeting like "thanks", "okay", or "hi", just reply politely without technical content.
    - If the question is "What is Databricks?" or similar, give only the relevant information — no extra detail.
    - Do not answer beyond what was asked.
    - Only include SQL or PySpark if the user asks for code.
    - Avoid giving extra information not asked for.

    Documentation:
    {context}

    Question: {user_question}

    Answer:
"""


    # Step 4: Send to LLaMA 3 via Ollama
    result = subprocess.run(
        ["ollama","run","llama3"],
        input = prompt,
        text = True,
        capture_output = True
    )

    print("\n💬 Answer:\n")
    print(result.stdout.strip())