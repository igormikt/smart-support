from fastapi.testclient import TestClient

from app.api.routes import llm_service
from app.main import app


def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ingest_with_mocked_llm(monkeypatch):
    from app.schemas.support import SupportResult

    def fake_analyze(text):
        return SupportResult(
            category="access",
            summary="Customer cannot log in.",
            priority="high",
            next_action="Check account access.",
            fields={"source": "test"},
            confidence="high",
            escalate=False,
        )

    monkeypatch.setattr(llm_service, "analyze", fake_analyze)

    with TestClient(app) as client:
        response = client.post(      
        "/ingest",
        json={"text": "I cannot log in to my account."},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "access"
    assert data["escalate"] is False
    assert data["audit_id"] > 0




