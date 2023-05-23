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
    
def test_add_recipe1():
    response = client.post(
        "/recipes/",
        json={
            "recipe": "Chicken Parmesean",
            "cuisine": "Italian",
            "meal_type": "Dinner",
            "time": 30,
            "ingredJson": {
                "ingredients": [
                    {
                        "ingrd": "Raw Chicken",
                        "ingrd_cost": 10.99,
                        "unit_type": "g",
                        "amount": 100
                    },
                    {
                        "ingrd": "Parmesean",
                        "ingrd_cost": 2.99,
                        "unit_type": "ml",
                        "amount": 200
                    }
                ]
            }
        }
    )
    assert response.status_code == 200
    assert response.json() == 1 


def test_add_recipe2():
    response = client.post(
        "/recipes/",
        json={
            "cuisine": "Italian",
            "meal_type": "Dinner",
            "time": 30,
            "ingredJson": {
                "ingredients": [
                    {
                        "ingrd": "Ingredient 1",
                        "ingrd_cost": 1.99,
                        "unit_type": "g",
                        "amount": 100
                    },
                    {
                        "ingrd": "Ingredient 2",
                        "ingrd_cost": 2.99,
                        "unit_type": "ml",
                        "amount": 200
                    }
                ]
            }
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Recipe name is required."

def test_modify_recipe1():
    response = client.put(
        "/recipes/0/",
        json={
            "old_ingredient_id": 4,
            "new_ingredient_name": "Parsley",
            "new_unit_type": "oz",
            "new_amount": 150,
            "new_ingredient_cost": 2.49
        }
    )
    assert response.status_code == 200
    assert response.text == "Ingredient with ID 4 updated to 'parsley' and ingredient information updated in recipe with ID 0"

def test_modify_recipe2():
    response = client.put(
        "/recipes/1/",
        json={
            "new_ingredient_name": "New Ingredient 1",
            "new_unit_type": "oz",
            "new_amount": 150,
            "new_ingredient_cost": 2.49
        }
    )
    assert response.status_code == 200 
    assert response.text == "Please provide both old ingredient ID and new ingredient name"

def test_modify_recipe3():
    response = client.put(
        "/recipes/1/",
        json={
            "old_ingredient_id": 1,
            "new_unit_type": "oz",
            "new_amount": 150,
            "new_ingredient_cost": 2.49
        }
    )
    assert response.status_code == 200 
    assert response.text == "Please provide both old ingredient ID and new ingredient name"

