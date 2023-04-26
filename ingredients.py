from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query

router = APIRouter()

@router.get("/ingredients/{ingr_id}", tags=["ingredients"])
def get_ingredient(ingr_id: int):
    """
    This endpoint returns a single ingredient by its identifier. For each ingredient
    it returns:
    * `ingredient_id`: the internal id of the ingredient. Can be used to query the
      `/ingredients/{id}` endpoint.
    * `ingredient_name`: The name of the ingredient and the amount that is needed to make the recipe.
    * `recipes`: A list of the recipes that contain the ingredient.
    """
    
    ingredient = db.get_ingredient(ingr_id)
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


class IngredientJson(BaseModel):
    ingredient_name: string
    ingredient_cost: int


@router.post("/ingredients/", tags=["ingredients"])
def add_ingredient(ingredient: IngredientJson):
    """
    This endpoint adds a single ingredient. A new ingredient is represented by its name,
    and its cost. When added, its num_recipies attribute will be intialized to 0, as no can recipes
    contain this ingreient yet because it is new. 
    
    
    This endpoint will return the new id of the ingredient created. 
    """
    
    
    return {"ingredient_id": ingredient_id}
    
    

