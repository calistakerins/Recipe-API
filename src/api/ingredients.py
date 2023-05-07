from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
import sqlalchemy


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
    
    stmt = (
        sqlalchemy.select(
            db.ingredients.ingredient_id,
            db.ingredients.ingredient_name,
            db.ingredients.ingredient_cost,
            #sqlalchemy.func.array_agg(db.ingredients_quantities.recipe_id).label("recipes"),
        )
    )

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="ingredient not found")
        json = {
            "ingredient_id": result.ingredient_id,
            "ingredient": result.ingredient_name,
            "ingredient_cost": result.ingredients_cost,
        }


    return json
