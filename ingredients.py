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
    and its cost. When added, its num_recipes attribute will be intialized to 0, as no can recipes
    contain this ingredient yet because it is new. 
    
    
    This endpoint will return the new id of the ingredient created. 
    """
    
    
    return {"ingredient_id": ingredient_id}

class character_sort_options(str, Enum):
    ingredient = "ingredient"

@router.get("/ingredients/", tags=["ingredients"])
def list_ingredients(
    name: str = "",
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
    sort: character_sort_options = character_sort_options.character,):
    """
    This endpoint returns a list of ingredients. For each ingredient it returns:
    * `ingr_id`: the internal id of the ingredient. Can be used to query the
      `/ingredients/{ingr_id}` endpoint.
    * `ingredient_name`: The name of the ingredient.
    * `recipes`: The list of recipes that include this ingredient.

    You can filter for characters whose name contains a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `ingredient` - Sort by ingredient name alphabetically.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """
    return json
    

