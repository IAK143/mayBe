import pytest
from fastapi.testclient import TestClient
from apps.worker.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "documents_count" in response.json()

def test_job_ingest_and_get_document():
    ingest_payload = {
        "source": "api_test",
        "url": "http://example.com/test",
        "raw_text": "Sample text for API ingestion test"
    }
    response = client.post("/jobs/ingest", json=ingest_payload)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["status"] == "COMPLETED"
    doc_id = res_data["document_id"]

    # Retrieve document
    doc_resp = client.get(f"/document/{doc_id}")
    assert doc_resp.status_code == 200
    assert doc_resp.json()["raw_text"] == "Sample text for API ingestion test"

    # Retrieve provenance
    prov_resp = client.get(f"/provenance/{doc_id}")
    assert prov_resp.status_code == 200
    assert prov_resp.json()["source"] == "api_test"
