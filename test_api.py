import pytest
from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage

import main
from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def agente_fake(monkeypatch):
    """Substitui o agente real para que a suíte rode offline e sem custo de API."""

    class _AgenteFake:
        async def ainvoke(self, _payload):
            return {"messages": [AIMessage(content="Resposta simulada.")]}

    monkeypatch.setattr(main, "agente_corporativo", _AgenteFake())


def test_index_retorna_html(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


def test_agent_query_estrutura(client, agente_fake):
    resp = client.post("/agent/query", json={"question": "Qual foi a produtividade em fevereiro?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert isinstance(data["tools_used"], list)


def test_agent_query_requer_campo_question(client):
    resp = client.post("/agent/query", json={})
    assert resp.status_code == 422
