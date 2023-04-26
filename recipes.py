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
    * `recipe_id`: the internal id of the character. Can be used to query the
      `/recipes/{recipe_id}` endpoint.
    * `recipe_name`: The name of the recipe.
    * `cuisine_type`: The cuisine that the recipe is from.
    * `meal_type`: The meal type that the recipe is from.
    * `calories`: total calories in the recipe
    * `prep_time`: The total time it takes to make the recipe.
    * `num_ingredients`: The total number of ingredients the recipe.
    * `ingredients`: The listed ingredients and amounts that are needed to make the recipe.
    * `recipe_cost`: The total cost of making the recipe.
    * `recipe_url`: url link to the recipe.
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
    * `recipe_name`: The name of the recipe.
    * `cuisine_type`: The cuisine that the recipe is from.
    * `meal_type`: The meal type that the recipe is from.
    * `calories`: total calories in the recipe
    * `prep_time`: The total time it takes to make the recipe.
    * `num_ingredients`: The total number of ingredients the recipe.
    * `recipe_cost`: The total cost of making the recipe.
    * `recipe_url`: url link to the recipe.

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



class RecipeJson(BaseModel):
    recipe_name: string
    cusine_type: string
    meal_type: string
    calories: int
    prep_time: int
    num_ingredients: int
    recipe_url: string
    
class IngredientJson(BaseModel):
    ingredient_id: int
    unit_type: string
    amount: int
        
class QuantitiesJson(BaseModel):
    ingredientQuantities = List[IngredientJson]


@router.post("/recipes/{recipe_id}", tags=["recipes"])
def add_recipe(recipe: RecipeJson, ingredient_quantities:QuantitiesJson):
    """
    This endpoint will allow users to add their own recipes to the API. A recipie will consist of:
    * `recipe_name`: The name of the recipe.
    * `cuisine_type`: The cuisine that the recipe is from.
    * `meal_type`: The meal type that the recipe is from.
    * `calories`: total calories in the recipe
    * `prep_time`: The total time it takes to make the recipe.
    * `num_ingredients`: The total number of ingredients the recipe.
    * `recipe_url`: url link to the recipe.
    
    This endpoint will also require users to specify the ingredient qauntities required
    to make the recipe. For each ingredient in the recipe, the user must specfiy:
     * `ingredient_id`: The id of the ingredient.
     * `unit_type`: the unit the recipe is measured in.
     * `amount`: the amount of ingredient used in recipe.

    To add a new recipe, all ingredients in the recipe must already but in the database.
    If an ingredient is not, this enpoint will throw an error and ask users to add
    the new ingredient first. 
    
    When a new recipe is added, this endpoint must also update the num_recipes atribute of the ingredients used
    in the recipe. All ingredients used in a new recipe will have their num_recipes atribute increased
    by 1. 

    This enpoint will return the id of the resulting recipe created
    """
    return 

@router.post("/recipes/{recipe_id}", tags=["recipes"])
def favorite_recipe(recipe_id: int,
    ):
    """
    This endpoint will allow users to add existing recipes to their favorites list. 
    It will write the recipe_id to the favorite_recipes database.
    
    This endpoint will return the recipe id that was added to the favorited_recipes.
    """
    return

@router.get("/favorite_recipes/", tags=["favorite_recipes"])
def list_favorite_recipes(limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
    sort: recipe_sort_options = recipe_sort_options.recipe
    ):
    """
    This endpoint will list all recipes in the users favorites list. For each recipe it returns:
    * `recipe_id`: the internal id of the character. Can be used to query the
      `/recipes/{recipe_id}` endpoint.
    * `recipe`: The name of the recipe.
    * `cuisine_type`: The cuisine that the recipe is from.
    * `meal_type`: The meal type that the recipe is from.
    * `ingredients`: The listed ingredients and amounts that are needed to make the recipe.
    * `time`: time needed to make the recipe.

    You can also sort the results by using the `sort` query parameter:
    * `recipe` - Sort by recipe name alphabetically.
    * `time` - Sort by cooking time.

    The `limit` and `offset` query parameters are used for pagination.
    The `limit` query parameter specifies the maximum number of results to return.
    The `offset` query parameter specifies the number of results to skip before
    """
    return

