import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from orchestrator.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert "ok" in response.text.lower()

def test_index_and_retrieve():
    # Index some documents
    docs = ["Hello world", "AI voice agent test", "Finance news"]
    index_response = client.post("/retriever/index", json={"texts": docs})
    assert index_response.status_code == 200
    assert index_response.json()["status"] == "indexed"
    # Retrieve
    retrieve_response = client.get("/retriever/retrieve", params={"query": "voice agent", "k": 2})
    assert retrieve_response.status_code == 200
    results = retrieve_response.json()["results"]
    assert any("voice agent" in r.lower() or "ai" in r.lower() for r in results)
