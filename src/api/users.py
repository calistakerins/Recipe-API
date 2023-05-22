import os
from typing import List
from fastapi import APIRouter, HTTPException
import sqlalchemy
import hashlib
import datetime

from src import database as db
from api import recipes

from fastapi.params import Query


router = APIRouter()


@router.post("/users/", tags=["add_user"])
def add_user(username: str, password: str):
    """
    This endpoint will allow users to create a new user. The user must provide a username
    and password. This endpoint check to make sure no duplicate usernames can be used.
    All passwords will be stored as hashes to protect user privacy.
    """

    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-16'), salt, 100000)
    hashed_password = salt + key

    stmt = sqlalchemy.select(db.users.c.user_id).where(db.users.c.user_name == username)
    with db.engine.begin() as conn:
      check_valid = conn.execute(stmt)
      if check_valid .rowcount > 0:
        raise HTTPException(status_code=404, detail="username already exists")
      
      # Encode hashed password using base64 
      encoded_password = base64.b64encode(hashed_password).decode('utf-8')

      conn.execute(
              sqlalchemy.insert(db.users),
              [
                  {"user_name": username,
                  "password": encoded_password },
              ],
            
      )

      stmt = sqlalchemy.select(db.users.c.user_id, db.users.c.password).where(db.users.c.user_name == username)
      result = conn.execute(stmt)
      for row in result:
         user_id = row.user_id
         hashed_password = row.password

    return user_id, hashed_password


@router.get("/users/", tags=["validate_user"])
def validate_user_login(username: str, password: str):
   """
    This endpoint will allow users to check if their password is valid. This endpoint 
    will throw an error if the user does not exist, or if the passowrd is incorrect.
    """

   stmt = sqlalchemy.select(db.users.c.password).where(db.users.c.user_name == username)
   with db.engine.begin() as conn:
      result = conn.execute(stmt)
      if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="user not found")
      for row in result:
         hashed_password = row.password

    # Decode hashed password from base64
   hashed_password = base64.b64decode(hashed_password.encode('utf-8'))

   salt =hashed_password[:32]
   key = hashed_password[32:]
   check_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-16'), salt, 100000)

   if key == check_key:
        return {"message": "Password is correct"}
   else:
        return {"message": "Password is incorrect"}
      

def get_user_id(username: str):
    stmt = sqlalchemy.select(db.users.c.user_id).where(db.users.c.user_name == username)

    user_id = -1

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            user_id = row.user_id

    if user_id == -1:
        raise HTTPException(status_code=404, detail="user not found")
    return user_id


#add username to parameters
@router.put("users/{username}/favorited_recipes/{recipe_id}", tags=["favorited_recipes"])
def favorite_recipe(username: str, recipe_id: int
    ):
    """
    This endpoint will allow users to add existing recipes to their favorites list. 
    For testing purposes, use the username 'lpierce'.
    """
    user_id = get_user_id(username)

    find_recipe_stmt = sqlalchemy.select(db.recipes.c.recipe_id).where(db.recipes.c.recipe_id == recipe_id)

    with db.engine.begin() as conn:
        find_recipe_result = conn.execute(find_recipe_stmt)

        if find_recipe_result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Recipe not found.")
        
        conn.execute(
                  sqlalchemy.insert(db.favorited_recipes),
                  [
                    {"recipe_id": recipe_id,
                    "user_id": user_id,
                    "date_favorited": str(datetime.datetime.now())}
                  ]
            )

    return {"recipe_id": recipe_id,
            "user_id": user_id} 

@router.get("users/{username}/favorited_recipes/", tags=["favorited_recipes"])
def list_favorite_recipes(username: str, 
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
    sort: recipes.recipe_sort_options = recipes.recipe_sort_options.recipe
    ):
    """
    This endpoint will list all recipes in the users favorites list. For each recipe it returns:
    * `recipe_id`: the internal id of the character. Can be used to query the
      `/recipes/{recipe_id}` endpoint.
    * `recipe`: The name of the recipe.
    * `cuisine`: The cuisine that the recipe is from.
    * `meal_type`: The meal type that the recipe is from.
    * `ingredients`: The listed ingredients and amounts that are needed to make the recipe.
    * `prep_time_mins`: time needed to make the recipe.

    You can also sort the results by using the `sort` query parameter:
    * `recipe` - Sort by recipe name alphabetically.
    * `time` - Sort by cooking time.

    The `limit` and `offset` query parameters are used for pagination.
    The `limit` query parameter specifies the maximum number of results to return.
    The `offset` query parameter specifies the number of results to skip before
    """
    user_id = get_user_id(username)

    stmt = sqlalchemy.select(db.recipes.c.recipe_id, db.recipes.c.recipe_name, db.recipes.c.prep_time_mins).\
            where(db.recipes.c.recipe_id == db.favorited_recipes.c.recipe_id and db.favorited_recipes.c.user_id == user_id).\
            order_by(sort).\
            limit(limit).\
            offset(offset)

    favorited_recipes = []
    with db.engine.connect() as conn:
        favorited_results = conn.execute(stmt)
        for row in favorited_results:
            favorited_recipes.append({
                "recipe_id": row.recipe_id,
                "recipe": row.recipe_name,
                "cuisine": recipes.get_cuisine_type(row.recipe_id),
                "meal_type": recipes.get_meal_type(row.recipe_id),
                "ingredients": recipes.get_ingredients(row.recipe_id),
                "prep_time_mins": row.prep_time_mins
            })

    return favorited_recipes
