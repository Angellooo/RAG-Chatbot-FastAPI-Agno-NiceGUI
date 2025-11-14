from fastapi.testclient import TestClient
from src.backend.main import app

client = TestClient(app)


def test_chat_stream_returns_chunks():
    payload = {"prompt": "Hello world"}
    response = client.post("/chat/stream", json=payload)
    assert response.status_code == 200
    # Response is streamed, but TestClient collects it
    text = response.text
    assert "Hello" in text
    assert "world" in text


def test_chat_stream_handles_empty_prompt():
    payload = {"prompt": ""}
    response = client.post("/chat/stream", json=payload)
    assert response.status_code == 200
    assert response.text == ""  # no chunks expected


def test_chat_stream_invalid_payload():
    # Missing required field 'prompt'
    response = client.post("/chat/stream", json={})
    assert response.status_code == 422  # validation error
