from __future__ import annotations
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from typing import List
import os


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings of texts from chunks. 
    Args:
        texts (List[str]) : List of texts to be embedded.
    Returns:
        embeddings (List[float]): List of embeddings of texts.
    """
    load_dotenv()
    embedding_model = os.getenv("EMBEDDING_MODEL")
    if not embedding_model:
        raise Exception("Embedding model not loaded")
    if not embedding_model.startswith("models/"):
        embedding_model = f'models/{embedding_model}'
    emb = GoogleGenerativeAIEmbeddings(model=embedding_model)
    return emb.embed_documents(texts)

