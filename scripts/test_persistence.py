from rag_pipeline.vector_store import get_collection_count, init_chroma_db, add_documents, persist_collection, query_documents, delete_documents
from dotenv import load_dotenv
import os

def main()-> None:
    load_dotenv()
    collection_name:str = os.getenv("COLLECTION_NAME", "")
    persist_directory:str = os.getenv("PERSIST_DIR", "")
    if not collection_name or not persist_directory:
        raise ValueError("COLLECTION_NAME and PERSIST_DIR must be set in the .env file.")
    db = init_chroma_db(collection_name=collection_name, persist_directory=persist_directory)

    print(f"Collection has {get_collection_count(db)} documents.")

if __name__ == "__main__":
    main()