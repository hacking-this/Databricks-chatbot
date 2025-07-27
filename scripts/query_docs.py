import chromadb
from sentence_transformers import SentenceTransformer

# 1. Load the same model used for embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Load the ChromaDB where we stored chunks
client = chromadb.PersistentClient(path="chroma")
collection = client.get_or_create_collection("databricks-docs")

# 3. Ask a question
question = input("🔍 Ask a Databricks question:\n> ")

# 4. Embed the question
quer_embedding = model.encode([question])[0]

# 5. Query the top 5 most relevant chunks
results = collection.query(
    query_embeddings = [quer_embedding],
    n_results = 5,
    include=["documents"]
)

# 6. Show results
print("\n📄 Top matching documentation chunks:\n")
for i, doc in enumerate(results["documents"][0]):
    print(f"--- Chunk {i+1} ---\n{doc}\n")
