from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List, Optional
import os

def init_chroma_db(collection_name: str, persist_directory:str = "chroma_db") -> Chroma:
    load_dotenv()
    vector_db = Chroma(
        collection_name=collection_name,
        persist_directory=persist_directory,
        embedding_function=GoogleGenerativeAIEmbeddings(model=os.getenv('EMBEDDING_MODEL', 'text-embedding-004')),
    )
    return vector_db

def add_documents(
        vectordb: Chroma, 
        texts: list[str], 
        metadatas: Optional[List[dict]] = None, 
        ids: Optional[List[str]] = None 
        ) -> None:
    vectordb.add_texts(texts=texts, metadatas=metadatas, ids=ids)

def query_documents(vectordb: Chroma, query: str, k: int = 5):
    """
    Only for debugging and testing. Similarity search in chain will be done using retreiver.
    """
    return vectordb.similarity_search(query, k=k)


def get_collection_count(vectordb: Chroma) -> int:
    """Get the number of documents in the collection."""
    return vectordb._collection.count()

def delete_documents(vectordb: Chroma, ids: List[str]) -> None:
    """Delete documents by IDs."""
    vectordb.delete(ids=ids)

def persist_collection(vectordb: Chroma):
    vectordb.persist() #type: ignore

