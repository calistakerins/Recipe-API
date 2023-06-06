from fastapi import APIRouter, HTTPException
from enum import Enum
import sqlalchemy
from sqlalchemy import desc, func, select
from pydantic import BaseModel
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
    * `ingredient`: The name of the ingredient 
    * `recipes`: A list of the recipes that contain the ingredient.

    """
    stmt = (
        sqlalchemy.select(
            db.ingredients.c.ingredient_id,
            db.ingredients.c.ingredient_name,
            db.recipes.c.recipe_id,
            db.recipes.c.recipe_name
        )
        .select_from(
            db.ingredients
            .outerjoin(
                db.ingredient_quantities,
                db.ingredients.c.ingredient_id == db.ingredient_quantities.c.ingredient_id
            )
            .outerjoin(
                db.recipes,
                db.recipes.c.recipe_id == db.ingredient_quantities.c.recipe_id
            )
        )
        .where(db.ingredients.c.ingredient_id == ingr_id)
    )

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        
        ingredient_data = {}
        recipe_list = []
        for row in result:
            if "ingredient_id" not in ingredient_data:
                ingredient_data["ingredient_id"] = row.ingredient_id
                ingredient_data["ingredient_name"] = row.ingredient_name
            
            recipe_list.append({"recipe_id": row.recipe_id, "recipe_name": row.recipe_name})
        
        ingredient_data["recipes"] = recipe_list

    return ingredient_data


class IngredientJson(BaseModel):
    ingredient_name: str


@router.post("/ingredients/", tags=["ingredients"])
def add_ingredient(ingredient: IngredientJson):
    """
    This endpoint adds a single ingredient. A new ingredient is represented by its name.
    
    This endpoint will return the new id of the ingredient created. 
    """
    stmt = sqlalchemy.select(
        db.ingredients.c.ingredient_id).where(db.ingredients.c.ingredient_name == ingredient.ingredient_name)

    with db.engine.begin() as conn:
      check_valid = conn.execute(stmt)
      if check_valid .rowcount > 0:
        for row in check_valid:
            ingredient_id = row.ingredient_id
        return {"ingredient_id": ingredient_id} 


      conn.execute(
              sqlalchemy.insert(db.ingredients),
              [
                  {"ingredient_name": ingredient.ingredient_name}
              ],
      )

      stmt = sqlalchemy.select(db.ingredients.c.ingredient_id).where(db.ingredients.c.ingredient_name == ingredient.ingredient_name)
      result = conn.execute(stmt)
      for row in result:
         ingredient_id = row.ingredient_id

    return {"ingredient_id": ingredient_id} 
