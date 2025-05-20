import os
import importlib.util
from types import SimpleNamespace
import pytest


def load_app_module():
    """Load the Flask app module from the Llama-Chat file."""
    repo_root = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(repo_root, "Llama-Chat")
    spec = importlib.util.spec_from_file_location("llama_chat", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.app.config["TESTING"] = True
    return module


@pytest.fixture()
def app_module():
    return load_app_module()


@pytest.fixture()
def client(app_module):
    with app_module.app.test_client() as client:
        yield client


def test_chat_route_returns_messages(client, app_module, monkeypatch):
    def fake_chat_with_model(client_arg, messages, model="llama"):
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="ok"))])

    monkeypatch.setattr(app_module, "chat_with_model", fake_chat_with_model)

    response = client.post("/chat", json={"messages": [{"role": "user", "content": "Hi"}]})
    assert response.status_code == 200
    data = response.get_json()
    assert "messages" in data
    assert isinstance(data["messages"], list)


def test_transcribe_without_file_returns_400(client):
    response = client.post("/transcribe")
    assert response.status_code == 400
