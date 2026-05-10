# Smart Travel AI Assistant — Full RAG AI Backend

Production-ready AI travel assistant backend built with FastAPI using a Retrieval-Augmented Generation (RAG) pipeline, semantic retrieval, Redis-backed conversational memory, and Groq-hosted LLMs.

This system retrieves relevant travel data, maintains conversational context, and generates grounded, context-aware travel responses.

---

# 🧠 Core Features

## 🔍 Full Semantic RAG Pipeline

Features:

* semantic document search
* embedding-based retrieval
* ChromaDB vector persistence
* top-k contextual retrieval
* similarity-based ranking

Uses:

* SentenceTransformers
* all-MiniLM-L6-v2 embeddings
* ChromaDB

---

## 🌐 Dynamic Tour Data Ingestion

Instead of relying only on static JSON files, the backend supports ingestion from a live Django API endpoint.

Capabilities:

* fetch live travel/tour data
* transform API responses into retrieval documents
* centralized business backend architecture
* independent AI service orchestration

This creates a distributed architecture where:

* Django manages business logic and tour data
* FastAPI manages AI orchestration and retrieval
* Redis manages conversational memory

---

## 🧠 Conversational Memory (Redis-backed)

Supports:

* short-term conversational memory
* long-term summarized memory
* session persistence
* memory-efficient prompt construction

---

## ⚡ Groq LLM Integration

Supports:

* LLaMA3
* Mixtral

Features:

* ultra-fast inference
* provider abstraction
* robust retry/error handling
* scalable LLM orchestration

---

## 🎯 Strict Prompt Engineering

Prompt system designed to:

* reduce hallucinations
* force grounded answers
* prioritize retrieved context
* maintain travel-focused responses

---

## 💬 Frontend AI Chat Integration

Integrated React AI assistant includes:

* animated floating AI chat popup
* session persistence
* retrieval intelligence inspection
* responsive mobile support
* route visualization cards
* relevance scoring UI
* conversational interface memory

---

# ⚙️ Tech Stack

| Layer           | Technology                  |
| --------------- | --------------------------- |
| Backend         | FastAPI                     |
| Frontend        | React + Vite                |
| Vector Database | ChromaDB                    |
| Embeddings      | SentenceTransformers        |
| LLM Provider    | Groq API                    |
| Memory Store    | Redis                       |
| Validation      | Pydantic                    |
| Server          | Uvicorn                     |
| UI              | TailwindCSS + Framer Motion |

---

# 📂 Project Structure

```txt
app/
├─ main.py
├─ routes/
│  └─ chat.py
├─ services/
│  └─ data_ingestion.py
├─ utils/
│  ├─ embeddings.py
│  ├─ vector_db.py
│  ├─ llm_helpers.py
│  ├─ intent.py
│  └─ logger.py
├─ memory/
│  └─ chat_memory.py
```

```txt
src/
├── ai_agent/
│   └── AiAssistant.jsx
├── components/
│   └── AiChatPopup.jsx
```

---

# 🔧 Installation

```bash
git clone https://github.com/salahinmushfiq/smart_travel_ai.git
cd smart_travel_ai

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Server runs at:

```txt
http://127.0.0.1:8000/
```

---

# 🔐 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama3-8b-8192

REDIS_URL=redis://your_redis_url

DJANGO_API_URL=https://your-django-api.com/api/tours/public/
```

---

# 📡 API

## POST `/chat/`

```json
{
  "question": "Tell me about hills in Bangladesh",
  "session_id": "optional",
  "top_k": 3
}
```

---

# 📦 Example Response

```json
{
  "status": "success",
  "session_id": "uuid",
  "answer": "...",
  "retrieved_docs": [...],
  "history_length": 4,
  "intent": "conversation"
}
```

---

# 🧠 Memory Architecture

## Short-Term Memory

* Recent conversational turns stored in Redis
* Injected dynamically into prompts

## Long-Term Memory

* Older messages summarized using LLMs
* Stored separately for token efficiency

## Benefits

* prevents prompt overflow
* enables long-running sessions
* maintains contextual continuity
* improves response relevance

---

# 🔄 System Flow (FULL RAG)

```mermaid
flowchart TD

A[User Question] --> B[FastAPI /chat]

B --> C{Session Exists?}
C -->|Yes| D[Load History + Summary from Redis]
C -->|No| E[Create New Session]

D --> F[Check Memory Size]
F -->|Too Large| G[Summarize Old Messages via LLM → Store in Redis]
F -->|OK| H

E --> H

H --> I[Fetch External Tour Data]

I --> J[Embed Query]
J --> K[ChromaDB Semantic Search]
K --> L[Retrieve Top-K Docs]

L --> M[Build Prompt]
M --> N[Groq LLM API]

N --> O[Generate Answer]

O --> P[Store New Messages in Redis]
P --> Q[Return Structured Response]
```

---

# 🌐 Distributed Architecture

```mermaid
flowchart LR

A[React Frontend] --> B[FastAPI AI Backend]

B --> C[Redis Cloud]

B --> D[Groq API]

B --> E[Django Tour Backend API]
```

---

# 🧩 Architecture Principles

* LLM layer is stateless and replaceable
* RAG is data-source independent
* memory is externalized through Redis
* services are loosely coupled
* frontend and backend remain independently scalable

---

# 🚀 Future Roadmap

* hybrid semantic + keyword retrieval
* reranking pipelines
* pgvector migration
* Pinecone integration
* Tavily / SerpAPI web search
* Celery background ingestion
* personalized itinerary generation
* travel preference learning

---

# 📌 Current Status

✅ Groq API integration complete
✅ Semantic RAG pipeline operational
✅ Redis memory system active
✅ Dynamic API ingestion working
✅ Chat sessions functioning
✅ Frontend AI assistant integrated
✅ Retrieval intelligence UI deployed
🚀 Production-ready architecture established

---

# ⚠️ Known Limitations

* free-tier infrastructure may struggle with embedding-heavy deployments
* semantic retrieval increases RAM usage
* no real-time external search augmentation yet
* ingestion currently depends on public backend endpoints

---

# 🧠 What This Project Demonstrates

This project demonstrates:

* end-to-end RAG system engineering
* semantic retrieval architecture
* production AI orchestration
* conversational memory systems
* distributed backend integration
* frontend AI UX engineering
* scalable AI service architecture
* deployment-aware system design
* real-world LLM integration
* modular AI backend engineering
