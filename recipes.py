from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query

router = APIRouter()


@router.get("/recipes/{recipe_id}", tags=["recipes"])
def get_recipe(recipe_id: int):
    """
    This endpoint returns a single recipe by its identifier. For each recipe
    it returns:
    * `recipe_id`: the internal id of the recipe. Can be used to query the
      `/recipes/{id}` endpoint.
    * `cuisine`: The cuisine that the recipe is from.
    * `meal_type`: The meal type that the recipe is from (breakfast, lunch, dinner, ect).
    * `ingredients`: The listed ingredients and amounts that are needed to make the recipe.
    * `time`: The total time it takes to make the recipe.
    """

    recipe = db.get_recipe(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

class recipe_sort_options(str, Enum):
    movie_title = "recipe"
    character = "time"

@router.get("/recipes/", tags=["recipes"])
def list_recipe(recipe: str = "",
    cuisine: str = "",
    meal_type: str = "",
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
    sort: recipe_sort_options = recipe_sort_options.recipe):
    """
    This endpoint returns a list of recipes. For each recipe it returns:
    * `recipe_id`: the internal id of the character. Can be used to query the
      `/recipes/{recipe_id}` endpoint.
    * `recipe`: The name of the recipe.
    * `cuisine`: The cuisine that the recipe is from.
    * `meal_type`: The meal type that the recipe is from.
    * `ingredients`: The listed ingredients and amounts that are needed to make the recipe.

    You can filter for recipes whose name contains a string by using the
    `recipe` query parameter. You can filter for recipes by cuisine by using the
    `cuisine` query parameter. You can filter for recipes by meal-type by using the
    `type` query parameter. 

    You can also sort the results by using the `sort` query parameter:
    * `recipe` - Sort by recipe name alphabetically.
    * `time` - Sort by cooking time.

    The `limit` and `offset` query parameters are used for pagination.
    The `limit` query parameter specifies the maximum number of results to return.
    The `offset` query parameter specifies the number of results to skip before
    returning results.
    """
    return


def add_recipe(recipe: str,
    cuisine: str,
    meal_type: str,
    ingredients: str,
    time: int):
    """
    This endpoint will allow users to add their own recipes to the API. A recipie will consist of:
    * `recipe`: The name of the recipe.
    * `cuisine`: The cuisine that the recipe is from.
    * `meal_type`: The meal type that the recipe is from.
    * `ingredients`: The listed ingredients and amounts that are needed to make the recipe.
    * `time`: The total time it takes to make the recipe.
    """
    return 

def modify_recipe(recipe_id: int,
    old_ingredient: str = "",
    new_ingredient: str = "",
    new_amount: str = "",
    ):
    """
    This endpoint will allow users to modify an ingredient in an existing recipe. 
    The user will be able to change the name of an ingredient or the amount of an ingredient.
    If the string of an old ingredient matches an ingredient in the recipe,
    the ingredient will be changed to the new ingredient. The user can also change the
    amount of an ingredient used in the recipe with the new_amount parameter. 
    """
    return
