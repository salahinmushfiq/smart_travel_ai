# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
#
# router = APIRouter(prefix="/chat", tags=["chat"])
#
#
# # Request body model
# class ChatRequest(BaseModel):
#     question: str
#
#
# # Fake chatbot response (for now)
# @router.post("/")
# def chat_endpoint(request: ChatRequest):
#     user_question = request.question
#     # For Day-1, just echo message + simple reply
#     if user_question in "cox's bazar":
#         answer = "Cox's Bazar is famous for its long beach. Cheapest tours start around $50/day."
#
#     elif user_question in "bandarban":
#         answer = "Bandarban is beautiful for hills. Tours start around $60/day."
#     else:
#         answer = "Sorry, I don't have info on that yet."
#     # response = f"You said: {user_question}. I am learning FastAPI + LLM!"
#     return f"You said reply: {user_question} Answer: {answer}"
#
#
#
#
# # @router.get("/")
# # def chat_endpoint():
# #     # For Day-1, just echo message + simple reply
# #     response = f"Hello! Smart Travel AI Assistant backend is running."
# #     return {"message": response}

from fastapi import APIRouter
from pydantic import BaseModel
import json
from app.utils.embeddings import embed_documents, get_most_similar

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    question: str


# Load sample travel documents
with open("app/data/travel_docs.json", "r", encoding="utf-8") as f:
    travel_docs = json.load(f)

doc_texts = [doc["content"] for doc in travel_docs]


doc_embeddings = embed_documents(doc_texts)


@router.post("/")
def chat_endpoint(request: ChatRequest):
    user_question = request.question
    answer = get_most_similar(doc_embeddings, doc_texts, user_question)

    return {"answer": answer}
