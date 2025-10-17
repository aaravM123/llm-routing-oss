from fastapi.testclient import TestClient
from services.api.app.main import app

client = TestClient(app)


def test_healthz():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "LLM Router OSS API", "status": "running"}
