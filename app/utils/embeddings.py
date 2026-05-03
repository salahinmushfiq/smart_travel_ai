# app/utils/embeddings.py

_model = None
util = None
torch = None


def get_model():
    global _model, util, torch

    if _model is None:
        from sentence_transformers import SentenceTransformer, util as st_util
        import torch as torch_lib

        util = st_util
        torch = torch_lib

        _model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"
        )

    return _model


def embed_documents(doc_texts: list):
    model = get_model()

    with torch.no_grad():
        return model.encode(doc_texts, convert_to_tensor=True, device="cpu")

def get_most_similar(doc_embeddings, doc_texts, user_question: str):
    model = get_model()
    question_embedding = model.encode(user_question, convert_to_tensor=True)  # user question becomes a 384-dim vector.
    similarities = util.cos_sim(question_embedding, doc_embeddings)  # tensor([[0.89, 0.12, 0.44, 0.03, 0.78]])
    print("similarities")
    print(similarities)
    best_idx = torch.argmax(similarities)  # Higher value = more semantically related function returns the idx.
    print("best_idx")
    print(best_idx)  # Higher value = more semantically related get value from best idx.
    return doc_texts[best_idx]
