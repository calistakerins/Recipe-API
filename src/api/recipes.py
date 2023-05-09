import datetime
from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
import sqlalchemy
from sqlalchemy import desc, func, select
from typing import List
from pydantic import BaseModel


router = APIRouter()


@router.get("/recipes/{recipe_id}", tags=["recipes"])
def get_recipe(recipe_id: int):
    """
    This endpoint returns a single recipe by its identifier. For each recipe
    it returns:
    * `recipe_id`: the internal id of the recipe. Can be used to query the
      `/recipes/{id}` endpoint.
    * `recipe_name`: The name of the recipe.
    * `cuisine`: The cuisine that the recipe is from.
    * `meal_type`: The meal type that the recipe is from (breakfast, lunch, dinner, ect).
    * `ingredients`: The listed ingredients and amounts that are needed to make the recipe.
    * `time`: The total time it takes to make the recipe.
    """
    json = None

    stmt = sqlalchemy.select(db.recipes.c.recipe_id, 
                db.recipes.c.recipe_name,
                db.recipes.c.calories,
                db.recipes.c.prep_time_mins,
                db.recipes.c.recipe_instructions,
                db.recipes.c.recipe_url
            ).where(db.recipes.c.recipe_id == recipe_id)

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            json = {
                "recipe_id": row.recipe_id,
                "recipe_name": row.recipe_name,
                "calories": row.calories,
                "prep_time_mins": row.prep_time_mins,
                "recipe_instructions": row.recipe_instructions,
                "recipe_url": row.recipe_url
            }

    if json is None:
            raise HTTPException(status_code=404, detail="Recipe not found.")

    return json

def ListMealTypes(recipe_id: int):
    stmt = sqlalchemy.select(
            db.meal_type.c.meal_type,
        ).where(db.meal_type.c.recipe_id == recipe_id)
    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="recipe not found")
        json = []
        for row in result:
            json.append(row.meal_type)
        return json

def ListCuisineTypes(recipe_id: int):
    stmt = sqlalchemy.select(
            db.cuisine_type.c.cuisine_type,
        ).where(db.cuisine_type.c.recipe_id == recipe_id)
    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="recipe not found")
        json = []
        for row in result:
            json.append(row.cuisine_type)
        return json
    

    

class recipe_sort_options(str, Enum):
    recipe = "recipe"
    time = "time"

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
    * `time`: time needed to make the recipe.

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
    if sort == recipe_sort_options.recipe:
        sort_by = db.recipes.c.recipe_name
    elif sort == recipe_sort_options.time:
        sort_by = db.recipes.c.prep_time_mins
    
    stmt = (
        sqlalchemy.select(db.recipes.c.recipe_id,
                          db.recipes.c.recipe_name,
                          db.recipes.c.prep_time_mins).select_from(db.recipes.join(db.cuisine_type, db.recipes.c.recipe_id == db.cuisine_type.c.recipe_id).join(db.meal_type, db.recipes.c.recipe_id == db.meal_type.c.recipe_id))
                          .order_by(sort_by).limit(limit).offset(offset).distinct()

     )
    
    if recipe != "":
        stmt = stmt.where(db.recipes.c.recipe_name.ilike(f"%{recipe}%"))

    if cuisine != "":
        stmt = stmt.where(db.cuisine_type.c.cuisine_type.ilike(f"%{cuisine}%"))

    if meal_type != "":
        stmt = stmt.where(db.meal_type.c.meal_type.ilike(f"%{meal_type}%"))

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="no recipes found")
        json = {}
        json["recipes"] = []
        for row in result:
            json["recipes"].append({"recipe_id": row[0], "recipe_name": row[1], "cuisine": ListCuisineTypes(row[0]), "meal_type": ListMealTypes(row[0]), "time": str(row[2]) + " minutes"})
        return json

class meal_typeJson(BaseModel):
    meal_type_id: int

class cuisine_typeJson(BaseModel):
    cuisine_type_id: int
    
class RecipeJson(BaseModel):
    recipe_name: str
    cusine_type: List[cuisine_typeJson]
    meal_type: List[meal_typeJson]
    calories: int
    prep_time_mins: int
    recipe_instructions: int
    recipe_url: str

class IngredientQuantityJson(BaseModel):
    ingredient_id: int
    unit_type: str
    amount: int

class QuantitiesJson(BaseModel):
    ingredientQuantities = List[IngredientQuantityJson]

def add_recipe(recipe_id: int, recipes: RecipeJson, quantities: QuantitiesJson):
    """
    This endpoint will allow users to add their own recipes to the API. 
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

#add username to parameters
def favorite_recipe(recipe_id: int, user_id: int
    ):
    """
    This endpoint will allow users to add existing recipes to their favorites list. 
    It will write the recipe_id to the favorite_recipes database.
    """
    #check if recipe exists
    #check if recipe is already in favorites
    #add recipe to favorites

    """ stmt = sqlalchemy.select(db.recipes.c.recipe_id).where(db.recipes.c.recipe_id == recipe_id)

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Recipe not found.")
        
    stmt = sqlalchemy.select(db.favorite_recipes.c.recipe_id).where(db.favorite_recipes.c.recipe_id == recipe_id)
    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        if result.rowcount != 0:
            raise HTTPException(status_code=422, detail="Recipe already favorited.")
        
    json = {"recipe_id": recipe_id,
            "user_id": user_id,
            "date_favorited": datetime.datetime.now().toString()
    }
    stmt = db.favorite_recipes.insert() """

    return None

def list_favorite_recipes(limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
    sort: recipe_sort_options = recipe_sort_options.recipe
    ):
    """
    This endpoint will list all recipes in the users favorites list. For each recipe it returns:
    * `recipe_id`: the internal id of the character. Can be used to query the
      `/recipes/{recipe_id}` endpoint.
    * `recipe`: The name of the recipe.
    * `cuisine`: The cuisine that the recipe is from.
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
