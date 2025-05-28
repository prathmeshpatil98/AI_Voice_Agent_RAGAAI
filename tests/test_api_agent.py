import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from orchestrator.main import app

client = TestClient(app)

def test_api_index_and_retrieve():
    # Index some API-related documents
    docs = ["API agent test", "API integration", "Voice API"]
    index_response = client.post("/retriever/index", json={"texts": docs})
    assert index_response.status_code == 200
    assert index_response.json()["status"] == "indexed"
    # Retrieve
    retrieve_response = client.get("/retriever/retrieve", params={"query": "API", "k": 2})
    assert retrieve_response.status_code == 200
    results = retrieve_response.json()["results"]
    assert any("api" in r.lower() for r in results)

