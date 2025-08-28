from __future__ import annotations
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from loader import load_documents
from typing import List

def chunk_transcripts( documents: List[Document], chunk_size = 1000, chunk_overlap=100):
    chunker = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size, 
        chunk_overlap = chunk_overlap,
        separators=["\n\n" , "\n", " ", ""]
        )
    
    # chunks = []
    split_docs = chunker.split_documents(documents)
    return split_docs

