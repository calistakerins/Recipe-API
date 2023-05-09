import datetime
from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
import sqlalchemy
from sqlalchemy import desc, func, select
from typing import List
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import Integer, String

class Ingreds(BaseModel):
    ingrd: str
    ingrd_cost: float
    unit_type: str
    amount: int

class IngredientsJson(BaseModel):
    ingredients: List[Ingreds]

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
    Returns the recipe id of the new recipe.
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



@router.post("/recipes/", tags=["recipes"])
def add_recipe(recipe: str,
    cuisine: str,
    meal_type: str,
    time: int, ingredJson: IngredientsJson):
    """
    This endpoint will allow users to add their own recipes to the API. To add a recipe, the
    user must provide:
    * `recipe`: The name of the recipe.
    * `cuisine`: The cuisine that the recipe is from.
    * `meal_type`: The meal type that the recipe is from.
    * `ingredients`: The list that contains the ingredients and amounts
      that are needed to make the recipe.
    * `time`: The total time it takes to make the recipe.
    """
    with db.engine.connect() as conn:
      recipe_id = conn.execute(sqlalchemy.select(db.recipes.c.recipe_id)
                                  .where(db.recipes.c.recipe_name == recipe)).scalar()
      max_recipe_id = conn.execute(sqlalchemy.select(sqlalchemy.func.max(db.recipes.c.recipe_id))).scalar()
      if recipe_id:
        raise HTTPException(404, "recipe already in database.")
      if max_recipe_id is None:
          recipe_id = 0
      else:
          recipe_id = max_recipe_id + 1
      recipe_data = {"recipe_id": recipe_id, "recipe_name": recipe, "calories": 0, "prep_time_mins": time, "recipe_instructions": "", "recipe_url": ""}
      conn.execute(db.recipes.insert().values(**recipe_data))

      cuisine_type_id = conn.execute(sqlalchemy.select(db.cuisine_type.c.cuisine_type_id)
                                  .where(db.cuisine_type.c.cuisine_type == cuisine)).scalar()
      max_cuisine_type_id = conn.execute(sqlalchemy.select(sqlalchemy.func.max(db.cuisine_type.c.cuisine_type_id))).scalar()
      if cuisine_type_id is None and max_cuisine_type_id is None:
          cuisine_type_id = 0
      if cuisine_type_id is None and max_cuisine_type_id!= None:
        cuisine_type_id = max_cuisine_type_id+1
      cuisine_type_data = {"cuisine_type_id": cuisine_type_id, "recipe_id": recipe_id, "cuisine_type": cuisine}
      conn.execute(db.cuisine_type.insert().values(**cuisine_type_data))

      meal_type_id = conn.execute(sqlalchemy.select(db.meal_type.c.meal_type_id)
                                .where(db.meal_type.c.meal_type == meal_type)).scalar()
      max_meal_type_id = conn.execute(sqlalchemy.select(sqlalchemy.func.max(db.meal_type.c.meal_type_id))).scalar()

      if meal_type_id is None and max_meal_type_id is None:
          meal_type_id = 0
      if meal_type_id is None and max_meal_type_id != None:
          meal_type_id = max_meal_type_id+1
      meal_type_data = {"meal_type_id": 0, "meal_type": meal_type, "recipe_id": recipe_id}
      conn.execute(db.meal_type.insert().values(**meal_type_data))
      for ingredient in ingredJson.ingredients:
        ingredient_unit_type = ingredient.unit_type
        ingredient_amount = ingredient.amount
        ingredient_name = ingredient.ingrd
        ingredient_id = conn.execute(
            sqlalchemy.select(db.ingredients.c.ingredient_id)
            .where(db.ingredients.c.ingredient_name == ingredient_name)
        ).scalar()
        if ingredient_id is None:
            ingredient_id = conn.execute(
                sqlalchemy.select(sqlalchemy.func.max(db.ingredients.c.ingredient_id))
            ).scalar()
            ingredient_id += 1
            ingredient_cost_usd = ingredient.ingrd_cost
            ingredient_data = {
                "ingredient_id": ingredient_id,
                "ingredient_name": ingredient_name,
                "ingredient_cost_usd": ingredient_cost_usd,
            }
            conn.execute(db.ingredients.insert().values(**ingredient_data))

        quantity_data = {
            "recipe_id": recipe_id,
            "ingredient_id": ingredient_id,
            "unit_type": ingredient_unit_type,
            "amount": ingredient_amount,
        }
        conn.execute(db.ingredient_quantities.insert().values(**quantity_data))
      return recipe_id

# def modify_recipe(recipe_id: int,
#     old_ingredient: str = "",
#     new_ingredient: str = "",
#     new_amount: str = "",
#     ):
#     """
#     This endpoint will allow users to modify an ingredient in an existing recipe. 
#     The user will be able to change the name of an ingredient or the amount of an ingredient.
#     If the string of an old ingredient matches an ingredient in the recipe,
#     the ingredient will be changed to the new ingredient. The user can also change the
#     amount of an ingredient used in the recipe with the new_amount parameter. 
#     """
#     with db.engine.connect() as conn:
#       if old_ingredient:
#           ingredient_id_query = select(db.ingredients.c.ingredient_id).where(db.ingredients.c.ingredient_name == old_ingredient)
#           result = conn.execute(ingredient_id_query).fetchone()
#           if result is None:
#               return f"Ingredient '{old_ingredient}' not found in recipe with ID {recipe_id}"
#           old_ingredient_id = result[0]
          
#           update_query = update(db.ingredient_quantities).where(
#               (db.ingredient_quantities.c.recipe_id == recipe_id) & 
#               (db.ingredient_quantities.c.ingredient_id == old_ingredient_id)
#           )
#           if new_ingredient:
#               ingredient_id_query = select(db.ingredients.c.ingredient_id).where(db.ingredients.c.ingredient_name == new_ingredient)
#               result = conn.execute(ingredient_id_query).fetchone()
#               if result is None:
#                   return f"Ingredient '{new_ingredient}' not found in ingredients table"
#               new_ingredient_id = result[0]
#               update_query = update_query.values(ingredient_id=new_ingredient_id)
#           if new_amount:
#               update_query = update_query.values(amount=new_amount)
#           conn.execute(update_query)
#           return f"Ingredient '{old_ingredient}' updated to '{new_ingredient}' and amount updated to '{new_amount}' in recipe with ID {recipe_id}"
#       else:
#           return "Please provide an old ingredient name to update"


def get_user_id(username: str):
    stmt = sqlalchemy.select(db.users.c.user_id).where(db.users.c.user_name == username)

    user_id = -1

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            user_id = row.user_id
    
    return user_id


#add username to parameters
@router.get("/users/{username}/recipes/{recipe_id}", tags=["recipes"])
def favorite_recipe(username: str, 
    recipe_id: int
    ):
    """
    This endpoint will allow users to add existing recipes to their favorites list. 
    It will write the recipe_id to the favorite_recipes database.
    """
    #check if recipe exists
    #check if recipe is already in favorites
    #add recipe to favorites

    user_id = get_user_id(username)

    stmt = sqlalchemy.select(db.recipes.c.recipe_id).where(db.recipes.c.recipe_id == recipe_id)

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Recipe not found.")
        
    stmt = sqlalchemy.select(db.favorited_recipes.c.recipe_id).where(db.favorited_recipes.c.recipe_id == recipe_id and db.favorited_recipes.c.user_id == user_id)
    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        if result.rowcount != 0:
            raise HTTPException(status_code=422, detail="Recipe already favorited.")
        
    json = {"recipe_id": recipe_id,
            "user_id": user_id,
            "date_favorited": str(datetime.datetime.now())
    }

    stmt = sqlalchemy.insert(db.favorited_recipes)
    with db.engine.connect() as conn:
        result = conn.execute(stmt, json)
    

    return result

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
