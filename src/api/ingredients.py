from fastapi import APIRouter, HTTPException
from enum import Enum
import sqlalchemy
from sqlalchemy import desc, func, select
from pydantic import BaseModel
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

@router.get("/ingredients/{ingr_id}", tags=["ingredients"])
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
    
    stmt = sqlalchemy.select(
        db.ingredients.c.ingredient_name).where(db.ingredients.c.ingredient_name == ingredient.ingredient_name.upper())

    with db.engine.begin() as conn:
      check_valid = conn.execute(stmt)
      if check_valid .rowcount > 0:
        raise HTTPException(status_code=404, detail="ingredient already exists")


        json ={}
        for row in result:
          json["ingredient_id"] = row.ingredient_id
          json["ingredient_name"] = row.ingredient_name
          json["ingredient_cost_usd"] = "$" + str(row.ingredient_cost_usd)
          json["recipes"] = list_recipes_with_ingredient(ingr_id)


    return json

class IngredientJson(BaseModel):
    ingredient_name: str
    ingredient_cost_usd: int


@router.post("/ingredients/", tags=["ingredients"])
def add_ingredient(ingredient: IngredientJson):
    """
    This endpoint adds a single ingredient. A new ingredient is represented by its name,
    and its cost. 
    
    This endpoint will return the new id of the ingredient created. 
    """


    with db.engine.begin() as conn:
      ingredient_num_ids = conn.execute(sqlalchemy.select(func.max(db.ingredients.c.ingredient_id)))
      for row in ingredient_num_ids:
        ingredient_id = row[0] + 1

      conn.execute(
              sqlalchemy.insert(db.ingredients),
              [
                  {"ingredient_id": ingredient_id,
                  "ingredient_name": ingredient.ingredient_name,
                  "ingredient_cost_usd": ingredient.ingredient_cost_usd},
              ],
          
      )

    return {"ingredient_id": ingredient_id} 
