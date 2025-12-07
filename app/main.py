from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat
import os
import uvicorn

app = FastAPI(title="Smart Travel AI Assistant")

# Allow your frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:5173/", "http://localhost:5173/"],  # Allow all origins for live deployment
    allow_credentials=True,
    allow_methods=["*"],  # Allow POST, GET, etc.
    allow_headers=["*"],  # Allow all headers
)

# Include chat routes
app.include_router(chat.router)


@app.get("/")
def root():
    return {"message": "Hello! Smart Travel AI Assistant backend is running."}


@app.get("/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}! Welcome to your AI assistant."}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001)) # avoid conflict with Django
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
