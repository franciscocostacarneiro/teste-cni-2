import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_index_retorna_html(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


def test_agent_query_estrutura(client):
    # O teste valida a estrutura da resposta, sem depender de chamada real ao LLM.
    # O corpo "answer" é garantido pela fixture do endpoint; tools_used é lista.
    resp = client.post("/agent/query", json={"question": "Qual foi a produtividade em fevereiro?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert isinstance(data["tools_used"], list)


def test_agent_query_requer_campo_question(client):
    resp = client.post("/agent/query", json={})
    assert resp.status_code == 422
