from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)

def test_get_recipe():
    response = client.get("/recipes/1")
    assert response.status_code == 200

    with open("test/recipes/1.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_recipe2():
    response = client.get("/recipes/1000")
    assert response.status_code == 404

def test_list_recipes():
    response = client.get("/recipes/?recipe=Chorizo%20Street%20Tacos&limit=50&offset=0&sort=recipe")
    assert response.status_code == 200

    with open("test/recipes/list.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_list_recipes2():
    response = client.get("recipes/?recipe=chicken&limit=50&offset=0&sort=recipe")
    assert response.status_code == 404
