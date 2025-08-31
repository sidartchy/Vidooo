from vector_store import init_chroma_db

def get_retriever(collection_name: str, persist_directory: str = "./chroma_db", k: int = 8):
    db = init_chroma_db(collection_name, persist_directory)
    retriever = db.as_retriever(
                    search_kwargs={"k": k}
                    )
    return retriever


