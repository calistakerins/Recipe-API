from fastapi import APIRouter, HTTPException
from enum import Enum
import sqlalchemy
from sqlalchemy import desc, func, select

from src import database as db
from fastapi.params import Query


router = APIRouter()

def list_recipes_with_ingredient(ingr_id: int):
    """
    This endpoint returns a list of the recipes that contain a certain ingredient. For each recipe it returns:
    * `recipe_name`: the name of the recipe. Can be used to query the
    """
    stmt = sqlalchemy.select(
            db.recipes.c.recipe_name,
        ).select_from(
            db.recipes.join(
                db.ingredient_quantities,
                db.ingredient_quantities.c.recipe_id == db.recipes.c.recipe_id and
                db.ingredient_quantities.c.ingredient_id == ingr_id
 
            )
        ).where(db.ingredient_quantities.c.ingredient_id == ingr_id).distinct()
    
    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="ingredient not found")
        json = []
        for row in result:
          json.append(row.recipe_name)
        return json

@router.get("/ingredients/{ingredient_id}", tags=["ingredients"])
def get_ingredients(ingr_id: int):
    """
    This endpoint returns a single ingredient by its identifier. For each ingredient
    it returns:
    * `ingredient_id`: the internal id of the ingredient. Can be used to query the
      `/ingredients/{id}` endpoint.
    * `ingredient`: The name of the ingredient 
    * `ingredient_cost`: The cost of the ingredient 
    * `recipes`: A list of the recipes that contain the ingredient.

    """
    stmt = sqlalchemy.select(
            db.ingredients.c.ingredient_id,
            db.ingredients.c.ingredient_name,
            db.ingredients.c.ingredient_cost_usd,
        ).where(db.ingredients.c.ingredient_id == ingr_id)
    

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="ingredient not found")
        json = []
        for row in result:
          json.append({
              "ingredient_id": row.ingredient_id,
              "ingredient_name": row.ingredient_name,
              "ingredient_cost_usd": "$" + str(row.ingredient_cost_usd),
              "recipes": list_recipes_with_ingredient(ingr_id)

          })


    return json
