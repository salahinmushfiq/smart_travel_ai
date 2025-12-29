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
- Session-based conversation memory (multi-turn chat)
- Maintains last N turns per session to control memory size
- Automatic conversation history injection into prompts
- Resume conversations using session_id
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
├─ memory/
│  └─ chat_memory.py  # Session-based chat memory
├─ data/
│ └─ travel_docs.json # Source travel documents
└─ __init__.py
requirements.txt # Dependencies


---

## 🔧 Installation

1. Clone the repository:

```bash
git clone https://github.com/salahinmushfiq/smart_travel_ai.git
cd smart_travel_ai
# Create and activate a Python virtual environment:
python -m venv venv
# Linux / Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# Server runs at http://127.0.0.1:8000/
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
  "session_id": "optional-session-id",
  "top_k": 3
}
session_id (optional): continues an existing conversation if provided; otherwise, a new session is created. 

question: user query (string)

top_k: number of top documents to retrieve (default = 3)

Response JSON:

json
Copy code
{
  "question": "Tell me about beaches in Bangladesh",
  "session_id": "generated-session-id",
  "retrieved_docs": [
    "Cox's Bazar is famous for long beaches.",
    "Patenga Beach is near Chittagong city.",
    "Inani Beach is known for coral stones."
  ],
  "answer": "Cox's Bazar, Patenga, and Inani are popular beaches in Bangladesh. Cox's Bazar is the longest natural beach in the world.",
  "history_length": 4,
  "context_docs": [
  {
    "title": "Cox's Bazar Beach",
    "content": "Cox's Bazar is famous for long beaches and is the longest natural beach in the world.",
    "source": "travel_docs.json"
  },
  {
    "title": "Patenga Beach",
    "content": "Patenga Beach is near Chittagong city and popular among tourists.",
    "source": "travel_docs.json"
  }
]
}


```
Explanation of fields:

retrieved_docs → Top-K documents retrieved from ChromaDB

answer → AI-generated response, grounded in retrieved documents

history_length → number of messages in this session (user + assistant)

context_docs → optional array of structured retrieved documents (title, content, source)
## 🧠 Conversation Memory

The backend supports multi-turn conversations using session-based memory.

- Each chat session is identified by a `session_id`
- Conversation history is stored server-side
- History is injected into the LLM prompt automatically
- Only the last N turns are kept to control context size

This enables users to pause, resume, and continue conversations naturally.

## 🧠 How It Works (Conceptual Flow)

```mermaid
flowchart TD
    A[User Question] -->|POST /chat/| B[FastAPI Endpoint]
    B --> C{Check Session ID}
    C -->|Exists| D[Retrieve conversation history]
    C -->|New| E[Create new session]
    D & E --> F[Convert Question to Embedding -> For vector DB query] 
    F --> G[Query ChromaDB for Top-K Similar Docs]
    G --> H[Build Prompt: History + Top-K Docs + Current Question]
    H --> I[LLaMA3 Model via Ollama]
    I --> J[Generate Answer]
    J --> K[Store user & assistant messages in session memory]
    K --> L[Return Response JSON with session_id, answer, retrieved_docs, history_length]

    style A fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#1e3a8a
    style B fill:#dbeafe,stroke:#3b82f6,stroke-width:2px,color:#1e3a8a
    style C fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#1e3a8a
    style D fill:#f0fdf4,stroke:#10b981,stroke-width:2px,color:#1e3a8a
    style E fill:#f0fdf4,stroke:#10b981,stroke-width:2px,color:#1e3a8a
    style F fill:#ede9fe,stroke:#8b5cf6,stroke-width:2px,color:#1e3a8a
    style G fill:#fef2f2,stroke:#ef4444,stroke-width:2px,color:#1e3a8a
    style H fill:#e0f2fe,stroke:#0ea5e9,stroke-width:2px,color:#1e3a8a
    style I fill:#e0f2fe,stroke:#0ea5e9,stroke-width:2px,color:#1e3a8a
    style J fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#1e3a8a
    style K fill:#d1fae5,stroke:#059669,stroke-width:2px,color:#1e3a8a
    style L fill:#dbeafe,stroke:#3b82f6,stroke-width:2px,color:#1e3a8a

    click B href "https://fastapi.tiangolo.com" "FastAPI Docs"
    click F href "https://ollama.com/docs" "Ollama LLaMA3 Docs"
    click D href "https://www.trychroma.com/docs" "ChromaDB Docs"