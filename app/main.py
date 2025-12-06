from fastapi import FastAPI
from app.routes import chat

app = FastAPI(title="Smart Travel AI Assistant")

# Include chat routes
app.include_router(chat.router)


@app.get("/")
def root():
    return {"message": "Hello! Smart Travel AI Assistant backend is running."}


@app.get("/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}! Welcome to your AI assistant."}
