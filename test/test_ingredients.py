from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)

def test_get_ingredient():
    response = client.get("/ingredients/0")
    assert response.status_code == 200

    with open("test/ingredients/0.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_ingredient2():
    response = client.get("/ingredients/1000")
    assert response.status_code == 404

def test_add_ingredient():
    test = {
        "ingredient_name": "butter",
        "ingredient_cost_usd": 0,
    }
    response = client.post("/ingredients/", json=test)
    assert response.status_code == 404

def test_add_ingredient2():
    test = {
        "ingredient_name": 5,
        "ingredient_cost_usd": "string",
    }
    response = client.post("/ingredients/", json=test)
    assert response.status_code == 422