# Vidooo

A RAG application that lets you chat with YouTube videos using their transcripts. Ask questions and get answers with timestamp references.

## Features

- **Transcript Processing**: Fetches YouTube transcripts with timestamps
- **Q&A System**: Ask questions about video content
- **Timestamp References**: Get specific timestamps for answers
- **Vector Storage**: ChromaDB for efficient retrieval
- **LLM Integration**: Powered by Google Gemini 2.5 Flash

## Tech Stack

- **Python 3.12+** | **LangChain** | **ChromaDB** | **Google Generative AI** | **YouTube Transcript API**

## Quick Start

1. **Install**
   ```bash
   git clone <repo>
   cd youtube-summarizer
   uv pip install -e .
   ```

2. **Configure**
   ```env
   GOOGLE_API_KEY=your_key_here
   COLLECTION_NAME=video_chunks
   EMBEDDING_MODEL=text-embedding-004
   ```

3. **Use**
   ```bash
   # Ingest video (update URL in scripts/ingest_vid.py)
   uv run python scripts/ingest_vid.py
   
   # Start chatting
   uv run python rag_pipeline/qa_chains.py
   ```

## Project Structure

```
youtube-summarizer/
├── rag_pipeline/     # Core RAG components
├── scripts/         # Utility scripts
├── chroma_db/       # Vector storage
└── pyproject.toml   # Configuration
```

## TODO / Development Tracker

### In Progress
- [ ] **Chunking Strategy**: Merge small transcript chunks for better context
- [ ] **Hallucination Reduction**: Improve prompt engineering and retrieval


### Planned Features
- [ ] **Web Extension**: Browser extension for YouTube integration
- [ ] **Backend API**: FastAPI server for web interface
- [ ] **Hybrid Embeddigs**: Try VLMs along with transcripts 
- [ ] **Caching System**: Cache embeddings to avoid re-computation
- [ ] **Error Handling**: Better error messages and recovery
- [ ] **Testing Suite**: Unit tests for all components
- [ ] **Documentation**: API docs and usage examples

### Completed
- [x] Core RAG pipeline
- [x] YouTube transcript extraction
- [x] Vector storage with ChromaDB
- [x] Q&A system with timestamps
- [x] Language-aware processing
- [x] Debug functionality
- [x] Chat history support

## Debug

Use debug mode to inspect retrieval:
```bash
# In chat interface, type: debug
# Then enter query to see retrieved documents
```

## License

MIT License

---
