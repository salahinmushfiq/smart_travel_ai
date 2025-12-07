# Smart Travel AI Assistant - FastAPI Backend

**Semantic search and AI-powered travel assistant backend** built with **FastAPI**.  
It retrieves the most relevant travel documents for a user question and generates **context-aware AI responses** using a local LLaMA3 model via Ollama.

---

## 🛠 Features

- Load travel documents from JSON (`travel_docs.json`)
- Compute **document embeddings** with `all-MiniLM-L6-v2` (SentenceTransformers)
- Store embeddings in **ChromaDB** for fast similarity search
- Retrieve top-K relevant documents using **cosine similarity**
- Generate AI answers with **LLaMA3 (Ollama)** using retrieved context
- **CORS-enabled** API for frontend integration
- Deployment-ready with configurable ports

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Backend | Python 3.11+ | Main programming language |
| Web Framework | FastAPI | REST API for user requests |
| Vector DB | ChromaDB | Persistent storage of embeddings |
| NLP / Embeddings | SentenceTransformers (`all-MiniLM-L6-v2`) | Convert documents & queries into vectors |
| AI Model | LLaMA3 via Ollama | Generate natural language responses |
| Request Validation | Pydantic | Ensure API request structure is correct |
| Deployment | Uvicorn | ASGI server to run FastAPI app |

---

## 📂 Project Structure

app/
├─ main.py # FastAPI entrypoint
├─ routes/
│ └─ chat.py # /chat/ endpoint
├─ utils/
│ ├─ embeddings.py # Document embedding functions
│ ├─ vector_db.py # ChromaDB integration
│ └─ llm_helpers.py # Ollama LLaMA3 interaction
├─ data/
│ └─ travel_docs.json # Source travel documents
└─ init.py
requirements.txt # Dependencies

yaml
Copy code

---

## 🔧 Installation

1. Clone the repository:

```bash
git clone https://github.com/salahinmushfiq/smart_travel_ai.git
cd smart_travel_ai
Create and activate a Python virtual environment:

bash
Copy code
python -m venv venv
# Linux / Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
🚀 Running the Server
bash
Copy code
uvicorn app.main:app --reload
Server runs at http://127.0.0.1:8000/
```
2. Health check endpoint:
```bash
GET http://127.0.0.1:8000/
Response: {"message": "Hello! Smart Travel AI Assistant backend is running."}
📡 API Endpoints
POST /chat/
Send a user question to the AI assistant.

Request JSON:

json
Copy code
{
  "question": "Tell me about beaches in Bangladesh",
  "top_k": 3
}
question: user query (string)

top_k: number of top documents to retrieve (default = 3)

Response JSON:

json
Copy code
{
  "question": "Tell me about beaches in Bangladesh",
  "retrieved_docs": [
    "Cox's Bazar is famous for long beaches.",
    "Patenga Beach is near Chittagong city.",
    "Inani Beach is known for coral stones."
  ],
  "context": "Cox's Bazar is famous for long beaches.\nPatenga Beach is near Chittagong city.\nInani Beach is known for coral stones.",
  "answer": "Cox's Bazar, Patenga, and Inani are popular beaches in Bangladesh. Cox's Bazar is the longest natural beach in the world."
}
```
Explanation of fields:

retrieved_docs → Top-K documents from ChromaDB

context → Concatenated text fed to LLaMA3

answer → AI-generated response, grounded in retrieved documents

## 🧠 How It Works (Conceptual Flow)

```mermaid
flowchart TD
    A[User Question] -->|POST /chat/| B[FastAPI Endpoint]
    B --> C[Convert Question to Embedding]
    C --> D[Query ChromaDB for Top-K Similar Docs]
    D --> E[Concatenate Top-K Docs as Context]
    E --> F[LLaMA3 Model via Ollama]
    F --> G[Generate Answer]
    G --> H[Return Response JSON]

    style A fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style B fill:#dbeafe,stroke:#3b82f6,stroke-width:2px
    style C fill:#f0fdf4,stroke:#10b981,stroke-width:2px
    style D fill:#ede9fe,stroke:#8b5cf6,stroke-width:2px
    style E fill:#fef2f2,stroke:#ef4444,stroke-width:2px
    style F fill:#e0f2fe,stroke:#0ea5e9,stroke-width:2px
    style G fill:#fef3c7,stroke:#d97706,stroke-width:2px
    style H fill:#d1fae5,stroke:#059669,stroke-width:2px

    click B href "https://fastapi.tiangolo.com/" "FastAPI Docs"
    click F href "https://ollama.com/docs" "Ollama LLaMA3 Docs"
    click D href "https://www.trychroma.com/" "ChromaDB Docs"