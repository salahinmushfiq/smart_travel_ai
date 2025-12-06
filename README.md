# Smart Travel AI Assistant - FastAPI Backend

This is the **semantic search backend** for the Smart Travel AI Assistant.  
It uses **SentenceTransformers embeddings** to find the most relevant travel document for a user question.

---

## Features 

- Load travel documents from JSON
- Compute **document embeddings** using `all-MiniLM-L6-v2`
- Precompute embeddings at startup for faster requests
- Compute **cosine similarity** to find the most relevant document
- FastAPI endpoint `/chat/` for semantic search

---

## Tech Stack

- Python 3.11+
- [FastAPI](https://fastapi.tiangolo.com/)
- [SentenceTransformers](https://www.sbert.net/)
- [PyTorch](https://pytorch.org/)
- Pydantic (for request validation)

---

## Project Structure

app/
├─ main.py
├─ init.py
├─ routes/
│ ├─ chat.py
├─ utils/
│ ├─ embeddings.py
└─ data/
├─ travel_docs.json

yaml
Copy code

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/salahinmushfiq/smart_travel_ai.git
cd smart-travel-ai-backend
Create virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Running the Server
bash
Copy code
uvicorn app.main:app --reload
Open your browser at http://127.0.0.1:8000/ → basic health check

POST to /chat/ with JSON:

json
Copy code
{
  "question": "Tell me about beaches in Bangladesh"
}
Response:

json
Copy code
{
  "answer": "Cox's Bazar is famous for long beaches."
}