"""Testes dos endpoints da API e do front-end estático."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from emporio_ozzy.api.main import app

client = TestClient(app)


def test_health_endpoint():
    """Valida o endpoint de saúde da aplicação."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "Emporio Ozzy"


def test_index_page():
    """Valida se a página principal HTML do chat é servida corretamente."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Empório da Música" in response.text
    assert "Ozzy" in response.text


def test_static_assets():
    """Valida se os arquivos estáticos (CSS, JS, imagens) são servidos sem erro 404."""
    css_res = client.get("/static/css/style.css")
    assert css_res.status_code == 200

    js_res = client.get("/static/js/chat.js")
    assert js_res.status_code == 200

    img_res = client.get("/static/images/ozzy_mascot_avatar_1793632768308.jpg")
    assert img_res.status_code == 200


def test_session_lifecycle():
    """Valida criação e reset de sessão."""
    create_res = client.post("/api/session")
    assert create_res.status_code == 200
    session_id = create_res.json()["session_id"]
    assert len(session_id) > 10

    delete_res = client.delete(f"/api/session/{session_id}")
    assert delete_res.status_code == 200
    assert delete_res.json()["cleared"] is True


def test_chat_endpoint_with_agent():
    """Valida o fluxo da rota /api/chat integrada ao agente Ozzy."""
    with patch("emporio_ozzy.api.main.get_agent") as mock_get_agent:
        mock_agent = mock_get_agent.return_value
        mock_agent.chat.return_value = {
            "reply": "Olá! Temos guitarras incríveis em promoção!",
            "handoff": False,
            "ticket_id": None,
        }

        response = client.post(
            "/api/chat",
            json={"message": "Quais guitarras em promoção?", "session_id": "sess-123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data
        assert data["session_id"] == "sess-123"
        assert "guitarras" in data["reply"]
        assert data["handoff"] is None


def test_chat_endpoint_handoff():
    """Valida quando a resposta inclui handoff com atendente humano."""
    with patch("emporio_ozzy.api.main.get_agent") as mock_get_agent:
        mock_agent = mock_get_agent.return_value
        mock_agent.chat.return_value = {
            "reply": "Chamando especialista humano para ajudar!",
            "handoff": True,
            "ticket_id": "#TK-1234",
        }

        response = client.post(
            "/api/chat",
            json={"message": "Quero falar com atendente", "session_id": "sess-456"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["handoff"] is not None
        assert data["handoff"]["ticket_id"] == "#TK-1234"
