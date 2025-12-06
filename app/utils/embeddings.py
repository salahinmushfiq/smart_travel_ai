from sentence_transformers import SentenceTransformer, util
import torch

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')


# [number_of_docs] x [embedding_dimension]
# 5 documents → shape = 5 × 384
# Model	Embedding Dimension
# all-MiniLM-L6-v2	384
# all-MiniLM-L12-v2	768
# mpnet-base-v2	768
# bge-base-en	768
# bge-large-en	1024
# text-embedding-3-small (OpenAI)	1536
# text-embedding-3-large (OpenAI)	3072
# model decides embedding_dimension
# Precompute embeddings for your documents
# in this case [number_of_docs] x 384 for all-MiniLM-L6-v2
def embed_documents(doc_texts: list):
    return model.encode(doc_texts, convert_to_tensor=True)


def get_most_similar(doc_embeddings, doc_texts, user_question: str):
    question_embedding = model.encode(user_question, convert_to_tensor=True)   #user question becomes a 384-dim vector.
    similarities = util.cos_sim(question_embedding, doc_embeddings)  # tensor([[0.89, 0.12, 0.44, 0.03, 0.78]])
    print("similarities")
    print(similarities)
    best_idx = torch.argmax(similarities)  # Higher value = more semantically related function returns the idx.
    print("best_idx")
    print(best_idx)      # Higher value = more semantically related get value from best idx.
    return doc_texts[best_idx]
