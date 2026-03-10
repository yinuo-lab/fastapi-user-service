from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_login_me():
    username = "testuser_ps"
    password = "12345678"

    # register (重复跑允许 201 或 409)
    r = client.post("/auth/register", json={"username": username, "password": password, "age": 20})
    assert r.status_code in (201, 409)

    # login (OAuth2 form)
    r = client.post("/auth/token", data={"username": username, "password": password})
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token

    # me
    r = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["username"] == username