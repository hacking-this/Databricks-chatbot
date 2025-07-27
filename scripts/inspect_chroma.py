import chromadb

client = chromadb.PersistentClient(path="chroma")
collection = client.get_or_create_collection("databricks-docs")

# Get all stored documents (example: first 5)
results = collection.get(include=["documents", "metadatas"], limit=5)

for i, doc in enumerate(results["documents"]):
    print(f"\n🔹 Chunk #{i+1}")
    print("📄 Content:", doc[:300])  # preview first 300 chars
    print("📁 Metadata:", results["metadatas"][i])
