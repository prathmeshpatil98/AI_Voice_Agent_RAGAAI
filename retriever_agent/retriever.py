from fastapi import APIRouter
from sentence_transformers import SentenceTransformer
import redis
import os
import numpy as np
from redis.commands.search.field import VectorField, TextField
from pydantic import BaseModel

router = APIRouter()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.Redis.from_url(REDIS_URL)

model = SentenceTransformer("all-MiniLM-L6-v2")
INDEX_NAME = "finance_index"

def create_redis_index():
    try:
        redis_client.ft(INDEX_NAME).info()
    except:
        schema = [
            VectorField("embedding", "FLAT", {
                "TYPE": "FLOAT32",
                "DIM": 384,
                "DISTANCE_METRIC": "COSINE"
            }),
            TextField("text")
        ]
        redis_client.ft(INDEX_NAME).create_index(schema)

create_redis_index()

class TextsRequest(BaseModel):
    texts: list[str]

@router.post("/index")
def index_documents(request: TextsRequest):
    texts = request.texts
    pipe = redis_client.pipeline()
    for i, doc in enumerate(texts):
        emb = model.encode(doc).astype(np.float32).tobytes()
        doc_id = f"doc:{i}"
        pipe.hset(doc_id, mapping={"embedding": emb, "text": doc})
    pipe.execute()
    return {"status": "indexed", "documents_added": len(texts)}

@router.get("/retrieve")
def retrieve_top_k(query: str, k: int = 3):
    q_emb = model.encode(query).astype(np.float32).tobytes()
    query_string = f'*=>[KNN {k} @embedding $vec_param AS vector_score]'
    results = redis_client.ft(INDEX_NAME).search(query_string, query_params={"vec_param": q_emb})
    hits = [doc.text for doc in results.docs]
    return {"results": hits}
