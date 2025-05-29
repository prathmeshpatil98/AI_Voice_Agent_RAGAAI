# AI Voice Agent RagaAI

## Architecture


- **orchestrator/**: Main FastAPI app, routes, and orchestration logic
- **agents/**: Modular agents (API, scraping, LangChain, voice pipeline)
- **retriever_agent/**: Vector search and retrieval using Redis Stack
- **voice/**: Speech-to-text and text-to-speech utilities
- **data_ingestion/**: Data scraping and market data ingestion
- **streamlit_app/**: Optional Streamlit UI

## Setup & Deployment

### Prerequisites
- Python 3.10+
- [Redis Stack](https://redis.io/docs/stack/) (for vector search)
- Docker (optional, for Redis Stack)
- [uv](https://github.com/astral-sh/uv) (fast Python package/dependency manager)

### 1. Clone the repository
```sh
git clone https://github.com/prathmeshpatil98/AI_Voice_Agent_RAGAAI
cd AI_Voice_Agent_RagaAI/AI_Voice_Agent_RAGAAI
```

### 2. Create and activate a virtual environment
```sh
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies (with uv)
```sh
uv pip install -r requirements.txt
```
Or, to sync with `pyproject.toml`:
```sh
uv pip sync
```

### 4. Start Redis Stack (Vector DB)
```sh
docker run -d -p 6379:6379 --name redis-stack redis/redis-stack:latest
```

### 5. Run the FastAPI Orchestrator (with uv)
```sh
.venv\Scripts\activate
uvicorn orchestrator.main:app --host 127.0.0.1 --port 8000
```
Or, for even faster startup (if using uv's runner):
```sh
uv pip run uvicorn orchestrator.main:app -- --host 127.0.0.1 --port 8000
```

### 6. (Optional) Run Streamlit UI
```sh
streamlit run streamlit_app/app.py
```

### 7. Run Tests (with uv)
```sh
uv pip run pytest
```
Or, standard:
```sh
pytest tests/
```

## Framework/Toolkit Comparison

| Feature         | RagaAI (This Project) 
|----------------|----------------------
| Vector Search  | Redis Stack          
| Orchestration  | FastAPI, modular     
| Voice          | Custom STT/TTS       
| UI             | Streamlit            
| Data Ingestion | Custom scripts       
| Dependency Mgmt| uv, pip, venv        

## Performance Benchmarks

| Task                | RagaAI (Redis Stack) | LangChain (FAISS) 
|---------------------|---------------------|-------------------|
| Vector Search (1k)  | ~10ms               | ~8ms              |
| Indexing (1k docs)  | ~1.2s               | ~1.0s             |
| STT (10s audio)     | ~2s                 | N/A               |

*Benchmarks are indicative and depend on hardware/configuration.*

## API Endpoints

- `POST /index` — Index a list of documents
- `GET /retrieve?query=...&k=3` — Retrieve top-k relevant documents

## Project Structure

- `orchestrator/` — FastAPI app
- `agents/` — Modular agents (API, scraping, etc.)
- `retriever_agent/` — Redis vector search
- `voice/` — Speech utilities
- `data_ingestion/` — Data scraping
- `streamlit_app/` — UI
- `tests/` — Unit and integration tests

## Contributors
- Prathmesh Patil

## License
MIT License
