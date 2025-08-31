"""
Utility functions for ingesting video content and updating the vector store.
"""
from rag_pipeline.loader import load_documents
from rag_pipeline.chunker import chunk_transcripts
from rag_pipeline.embeddings import embed_texts
from rag_pipeline.vector_store import init_chroma_db, add_documents, persist_collection
import logging

logging.basicConfig(level=logging.INFO)

def main() -> None:

    URL: str = "https://www.youtube.com/watch?v=QqsLTNkzvaY"

    chroma_db = init_chroma_db(collection_name="video_chunks")
    documents = load_documents(URL, language='en')  # Explicitly request English transcripts
    chunks = chunk_transcripts(documents)
    embeddings = embed_texts([chunk.page_content for chunk in chunks], language='en')
    logging.info(f"Generated {len(embeddings)} embeddings for {len(chunks)} chunks.")

    # TODO: store in vector store
    add_documents(chroma_db, [chunk.page_content for chunk in chunks], metadatas=[chunk.metadata for chunk in chunks])

if __name__ == "__main__":
    main()