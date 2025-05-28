import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from orchestrator.main import app

client = TestClient(app)

def test_orchestrator_index_and_retrieve():
    # Index orchestrator-related documents
    docs = ["Orchestrator test", "Main pipeline", "Agent orchestration"]
    index_response = client.post("/retriever/index", json={"texts": docs})
    assert index_response.status_code == 200
    assert index_response.json()["status"] == "indexed"
    # Retrieve
    retrieve_response = client.get("/retriever/retrieve", params={"query": "orchestrator", "k": 2})
    assert retrieve_response.status_code == 200
    results = retrieve_response.json()["results"]
    assert any("orchestrator" in r.lower() or "pipeline" in r.lower() for r in results)
