"""Testes dos endpoints da API e do front-end estático."""

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


def test_chat_mock_endpoint():
    """Valida o fluxo inicial da rota /api/chat."""
    response = client.post("/api/chat", json={"message": "Quais guitarras em promoção?"})
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert len(data["products"]) > 0
