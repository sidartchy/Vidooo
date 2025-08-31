from __future__ import annotations
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from typing import List
import os


def embed_texts(texts: List[str], language: str = 'en') -> List[List[float]]:
    """
    Generate embeddings of texts from chunks. 
    Args:
        texts (List[str]) : List of texts to be embedded.
        language (str): Language of the texts (default: 'en' for English).
    Returns:
        embeddings (List[float]): List of embeddings of texts.
    """
    load_dotenv()
    embedding_model = os.getenv("EMBEDDING_MODEL")
    if not embedding_model:
        raise Exception("Embedding model not loaded")
    if not embedding_model.startswith("models/"):
        embedding_model = f'models/{embedding_model}'
    
    # Google's text-embedding-004 is multilingual, but we can add language context
    emb = GoogleGenerativeAIEmbeddings(
        model=embedding_model,
        # You can add task_type for better language-specific embeddings
        task_type="retrieval_query" if language == 'en' else "retrieval_document"
    )
    return emb.embed_documents(texts)

