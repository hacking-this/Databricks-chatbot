# 🧠 Databricks Documentation Chatbot

A local, privacy-respecting chatbot that answers questions about Databricks by referencing scraped official documentation. Built with Python, Streamlit, Ollama (LLaMA models), SentenceTransformers, and ChromaDB.

## 🚀 Features

- Ask any Databricks-related question and get precise, context-aware answers.
- Conversational memory within sessions.
- Sidebar to switch between current and previous chats.
- Easy-to-use web interface via Streamlit.
- Local LLM inference with Ollama (no OpenAI key needed).
- Can be extended into an API or chatbot for WhatsApp, Slack, etc.

## 🛠 Setup Instructions

1. **Clone the repository**

```
git clone https://github.com/your-username/databricks-chatbot.git
cd databricks-chatbot
```

2. **Install dependencies**
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Install Ollama and Pull Model**
   *Download and install Ollama: https://ollama.com/download*
   *Then pull the LLaMA model:*
```
ollama pull llama3
```

4. **Run the app**
```
streamlit run app.py
```

📁 **Folder Structure**
```
databricks-chatbot/
├── .gitignore
├── README.md
├── requirements.txt
├── app.py                  # Streamlit web app
├── chatbot.py              # Core logic for handling queries and context
├── api.py                  # (Optional) FastAPI endpoint file
├── data/
│   └── databricks_docs.txt # Raw Databricks documentation text
├── db/
│   └── chroma/             # Vector store for embeddings
├── scripts/
│   ├── scrape_docs.py      # Script to scrape Databricks docs
│   ├── extract_code.py     # Extract code snippets
│   ├── embed_docs.py       # Chunk + embed docs into ChromaDB
│   └── test.py             # CLI testing of chatbot
└── venv/                   # Virtual environment (excluded via .gitignore)
```

