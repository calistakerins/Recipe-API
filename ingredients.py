from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query

router = APIRouter()

@router.get("/ingredients/{ingr_id}", tags=["ingredients"])
def get_ingredients(ingr_id: int):
    """
    This endpoint returns a single ingredient by its identifier. For each ingredient
    it returns:
    * `ingredient_id`: the internal id of the ingredient. Can be used to query the
      `/ingredients/{id}` endpoint.
    * `ingredient`: The name of the ingredient and the amount that is needed to make the recipe.
    * `recipes`: A list of the recipes that contain the ingredient.
    """
    
    ingredient = db.get_ingredient(ingr_id)
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient

