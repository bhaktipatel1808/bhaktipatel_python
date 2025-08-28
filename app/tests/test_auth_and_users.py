import pytest
from fastapi.testclient import TestClient
import asyncio

from app.main import app
from app.db.session import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    asyncio.get_event_loop().run_until_complete(init_db())
    yield

client = TestClient(app)

def register_user(name, email, password):
    return client.post("/users", json={"name": name, "email": email, "password": password})

def login(email, password):
    return client.post("/login", json={"email": email, "password": password})

def auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def test_registration_and_login_and_me():
    r = register_user("Alice", "alice@example.com", "StrongPass123!")
    assert r.status_code == 201
    l = login("alice@example.com", "StrongPass123!")
    assert l.status_code == 200
    token = l.json()["access_token"]
    m = client.get("/me", headers=auth_header(token))
    assert m.status_code == 200
    assert m.json()["email"] == "alice@example.com"
