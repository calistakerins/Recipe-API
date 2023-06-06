import datetime
from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
import sqlalchemy
from sqlalchemy import desc, func, select
from sqlalchemy import*
from fastapi import HTTPException, Body
from typing import Optional
from typing import List
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import Integer, String
from psycopg2.errors import UniqueViolation


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
    * `meal_type`: The meal type that the recipe is from (breakfast, lunch, dinner, etc).
    * `ingredients`: The listed ingredients and amounts that are needed to make the recipe.
    * `prep_time_mins`: The total time needed to prep the recipe in minutes.
    * `instructions`: The instructions needed to make the recipe.
    * `number_of_favorites`: The number of users that have favorited the recipe.

    """
    with db.engine.connect() as conn:
        recipe_stmt = (
        sqlalchemy.select(
            db.recipes.c.recipe_id,
            db.recipes.c.recipe_name,
            db.recipes.c.prep_time_mins,
            db.recipes.c.recipe_instructions,
            db.recipes.c.number_of_favorites,
            sqlalchemy.func.ARRAY_AGG(sqlalchemy.distinct(db.meal_type.c.meal_type)).label("meal_types"),
            sqlalchemy.func.ARRAY_AGG(sqlalchemy.distinct(db.cuisine_type.c.cuisine_type)).label("cuisine_types"),
            sqlalchemy.func.ARRAY_AGG(sqlalchemy.distinct(db.ingredients.c.ingredient_name)).label("ingredients"),
        )
        .select_from(
            db.recipes
            .outerjoin(
                db.recipe_meal_types,
                db.recipes.c.recipe_id == db.recipe_meal_types.c.recipe_id
            )
            .outerjoin(
                db.recipe_cuisine_types,
                db.recipes.c.recipe_id == db.recipe_cuisine_types.c.recipe_id
            )
            .outerjoin(
                db.meal_type,
                db.meal_type.c.meal_type_id == db.recipe_meal_types.c.meal_type_id
            )
            .outerjoin(
                db.cuisine_type,
                db.cuisine_type.c.cuisine_type_id == db.recipe_cuisine_types.c.cuisine_type_id
            )
            .outerjoin(
                db.ingredient_quantities,
                db.recipes.c.recipe_id == db.ingredient_quantities.c.recipe_id
            )
            .outerjoin(
                db.ingredients,
                db.ingredients.c.ingredient_id == db.ingredient_quantities.c.ingredient_id
            )
        )
        .where(db.recipes.c.recipe_id == recipe_id)
        .group_by(
            db.recipes.c.recipe_id,
            db.recipes.c.recipe_name,
            db.recipes.c.prep_time_mins,
            db.recipes.c.recipe_instructions,
            db.recipes.c.number_of_favorites
        )
        )
        result = conn.execute(recipe_stmt)
        row = result.fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="Recipe not found.")

        json = {
            "recipe_id": row.recipe_id,
            "recipe_name": row.recipe_name,
            "cuisine_type": row.cuisine_types,
            "meal_type": row.meal_types,
            "prep_time_mins": row.prep_time_mins,
            "instructions": row.recipe_instructions,
            "ingredients": row.ingredients,
            "number_of_favorites": row.number_of_favorites,
        }

    return json




class recipe_sort_options(str, Enum):
    recipe = "recipe"
    time = "time"
    number_of_favorites = "number_of_favorites"

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
    * `time`: time needed to make the recipe.
    * `instructions`: instrustion to make the recipe.
    * `number_of_favorites`: number of users who have favorited recipe.


    You can filter for recipes whose name contains a string by using the
    `recipe` query parameter. You can filter for recipes by cuisine by using the
    `cuisine` query parameter. You can filter for recipes by meal-type by using the
    `type` query parameter. 

    You can also sort the results by using the `sort` query parameter:
    * `recipe` - Sort by recipe name alphabetically.
    * `time` - Sort by cooking time.
    * `number_of_favorites` - Sort by number of users who have favorited recipe.


    The `limit` and `offset` query parameters are used for pagination.
    The `limit` query parameter specifies the maximum number of results to return.
    The `offset` query parameter specifies the number of results to skip before
    returning results.
    """
    if sort is recipe_sort_options.recipe:
        sort_by = db.recipes.c.recipe_name
    elif sort is recipe_sort_options.time:
        sort_by = db.recipes.c.prep_time_mins
    elif sort is recipe_sort_options.number_of_favorites:
        sort_by = db.recipes.c.number_of_favorites.desc()
    else:
        raise HTTPException(status_code=400, detail="Invalid sort option")

    stmt = (
        sqlalchemy.select(
            db.recipes.c.recipe_id,
            db.recipes.c.recipe_name,
            db.recipes.c.prep_time_mins,
            db.recipes.c.recipe_instructions,
            db.recipes.c.number_of_favorites,
            sqlalchemy.func.ARRAY_AGG(sqlalchemy.distinct(db.meal_type.c.meal_type)).label("meal_types"),
            sqlalchemy.func.ARRAY_AGG(sqlalchemy.distinct(db.cuisine_type.c.cuisine_type)).label("cuisine_types")
        )
        .select_from(
            db.recipes
            .outerjoin(
                db.recipe_meal_types,
                db.recipes.c.recipe_id == db.recipe_meal_types.c.recipe_id
            )
            .outerjoin(
                db.recipe_cuisine_types,
                db.recipes.c.recipe_id == db.recipe_cuisine_types.c.recipe_id
            )
            .outerjoin(
                db.meal_type,
                db.meal_type.c.meal_type_id == db.recipe_meal_types.c.meal_type_id
            )
            .outerjoin(
                db.cuisine_type,
                db.cuisine_type.c.cuisine_type_id == db.recipe_cuisine_types.c.cuisine_type_id
            )
        )
        .group_by(
            db.recipes.c.recipe_id,
            db.recipes.c.recipe_name,
            db.recipes.c.prep_time_mins,
            db.recipes.c.recipe_instructions,
            db.recipes.c.number_of_favorites
        ).order_by(sort_by).limit(limit).offset(offset).distinct()
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
            json["recipes"].append({"recipe_id": row[0], "recipe_name": row[1], "cuisine": row[6],
                                     "meal_type": row[5], "prep_time_mins": str(row[2]) + " minutes",
                                       "instructions": row[3], "number_of_favorites": row[4]})
        return json





class IngredientsJson(BaseModel):
    ingredient_id: int
    unit_type: Optional[str]
    amount: Optional[int]
    ingredient_price_usd: Optional[float]


class recipeJson(BaseModel):
    recipe: str
    cuisine_type_id: Optional[List[int]]
    meal_type_id: Optional[List[int]]
    calories: Optional[int]
    time: Optional[int]
    recipe_instructions: Optional[str]
    url: Optional[str]
    ingredients: Optional[List[IngredientsJson]]


# all parameters are optional except the recipe name
# all parameters are passed in from the request body now
# complex transaction function since it uses commit(), rollback(), implements data validation, performs multiple database operations
@router.post("/recipes/", tags=["recipes"])
def add_recipe(recipe: recipeJson):
    """
    This endpoint will allow users to add their own recipes to the API.
    To add a recipe, the user must provide:
    * `recipe`: The name of the recipe.
    * `cuisine_type_id`: The cuisine id(s) for the recipe cuisine(s).
    * `meal_type_id`: The meal type id(s) for the recipe meal type(s).
    * `calories`: Total calories in one serving of the recipe.
    * `time`: The total time it takes to make the recipe.
    * `recipe_instructions`: The instructions to make the recipe.
    * `url`: The url to the recipe.
    * `ingredients`: The list that contains the ingredients and amounts
      that are needed to make the recipe.
    """
    check_valid_recipe_stmt = sqlalchemy.select(db.recipes.c.recipe_id).where(db.recipes.c.recipe_name == recipe.recipe)
    with db.engine.begin() as conn:
        result = conn.execute(check_valid_recipe_stmt)
        if result.rowcount != 0:
            raise HTTPException(status_code=409, detail="recipe already exists")
        stmt = sqlalchemy.insert(db.recipes).values(recipe_name=recipe.recipe, calories=recipe.calories,
                                                    prep_time_mins=recipe.time, recipe_instructions=recipe.recipe_instructions,
                                                    recipe_url=recipe.url, number_of_favorites=0)
        result = conn.execute(stmt)
        recipe_id = result.inserted_primary_key[0]
        print(recipe.cuisine_type_id, recipe.meal_type_id)
        if recipe.cuisine_type_id is not None:
            for cuisine_type in recipe.cuisine_type_id:
                check_valid_cuisine_stmt = sqlalchemy.select(db.cuisine_type.c.cuisine_type).where(db.cuisine_type.c.cuisine_type_id == cuisine_type)
                check_valid_result = conn.execute(check_valid_cuisine_stmt)
                if check_valid_result.rowcount == 0:
                    conn.rollback()
                    raise HTTPException(status_code=400, detail="invalid cuisine id")
                stmt = sqlalchemy.insert(db.recipe_cuisine_types).values(recipe_id=recipe_id, cuisine_type_id=cuisine_type)
                conn.execute(stmt)
        if recipe.meal_type_id is not None:
            for meal_type in recipe.meal_type_id:
                check_valid_meal_type_stmt = sqlalchemy.select(db.meal_type.c.meal_type).where(db.meal_type.c.meal_type_id == meal_type)
                check_valid_result = conn.execute(check_valid_meal_type_stmt)
                if check_valid_result.rowcount == 0:
                    conn.rollback()
                    raise HTTPException(status_code=400, detail="invalid meal type id")
                stmt = sqlalchemy.insert(db.recipe_meal_types).values(recipe_id=recipe_id, meal_type_id=meal_type)
                conn.execute(stmt)
        if recipe.ingredients is not None:
            for ingredient in recipe.ingredients:
                check_valid_ingredient_stmt = sqlalchemy.select(db.ingredients.c.ingredient_name).where(db.ingredients.c.ingredient_id == ingredient.ingredient_id)
                check_valid_result = conn.execute(check_valid_ingredient_stmt)
                if check_valid_result.rowcount == 0:
                    conn.rollback()
                    raise HTTPException(status_code=400, detail="invalid ingredient id")
                stmt = sqlalchemy.insert(db.ingredient_quantities).values(recipe_id=recipe_id, ingredient_id= ingredient.ingredient_id,
                                                                            unit_type=ingredient.unit_type, amount=ingredient.amount, ingredient_price_usd=ingredient.ingredient_price_usd)
                conn.execute(stmt)
            
        return {"recipe_id": recipe_id}

# replaced post call with put call
# parameters include ids instead of names so the function wouldn't have to look up the names and match them
# made fields such as new_ingredient_cost, new_amount, and new_unit_type optional
@router.put("/recipes/{recipe_id}/", tags=["recipes"])
def modify_recipe(
    recipe_id: int,
    old_ingredient_id: int,
    new_ingredient_name: str,
    new_unit_type: Optional[str] = None,
    new_amount: Optional[str] = None,
    new_ingredient_cost: Optional[float] = None,
):
    with db.engine.connect() as conn:
        if old_ingredient_id and new_ingredient_name:
            ingredient_update_query = update(db.ingredients).where(
                db.ingredients.c.ingredient_id == old_ingredient_id
            ).values(
                ingredient_name=new_ingredient_name
            )
            conn.execute(ingredient_update_query)
            ingredient_quantity_update_query = update(db.ingredient_quantities).where(
                (db.ingredient_quantities.c.recipe_id == recipe_id)
                & (db.ingredient_quantities.c.ingredient_id == old_ingredient_id)
            )
            if new_unit_type is not None:
                ingredient_quantity_update_query = ingredient_quantity_update_query.values(
                    unit_type=new_unit_type
                )
            if new_amount is not None:
                ingredient_quantity_update_query = ingredient_quantity_update_query.values(
                    amount=new_amount
                )
            if new_ingredient_cost is not None:
                ingredient_quantity_update_query = ingredient_quantity_update_query.values(
                    ingredient_price_usd=new_ingredient_cost
                )
            
            if new_unit_type is not None or new_amount is not None or new_ingredient_cost is not None:
                conn.execute(ingredient_quantity_update_query)
                conn.commit()
            
            return f"Ingredient with ID {old_ingredient_id} updated to '{new_ingredient_name}' and ingredient information updated in recipe with ID {recipe_id}"
        else:
            return "Please provide both old ingredient ID and new ingredient name"



#add username to parameters
@router.put("/favorited_recipes/", tags=["favorited_recipes"])
def favorite_recipe(user_id: int, recipe_id: int
    ):
    """
    This endpoint will allow users to add existing recipes to their favorites list. 
    The user must provide their username to favorite a recipe.
    """
    #check user exists
    find_user_stmt = sqlalchemy.select(db.users.c.user_id).where(db.users.c.user_id == user_id)
    
   
    find_recipe_stmt = sqlalchemy.select(db.recipes.c.recipe_id).where(db.recipes.c.recipe_id == recipe_id)

    with db.engine.connect() as conn:
        transaction = conn.begin()

        find_user_result = conn.execute(find_user_stmt)
        if find_user_result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found.")
        find_recipe_result = conn.execute(find_recipe_stmt)
        if find_recipe_result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Recipe not found.")
        
        try:
            conn.execute(
                    sqlalchemy.insert(db.favorited_recipes),
                    [
                        {"recipe_id": recipe_id,
                        "user_id": user_id,
                        "date_favorited": str(datetime.datetime.now())}
                    ]
                )
                #exception will occur here if the recipe is already in the favorites list
            transaction.commit()
            #updates the number of favorites for the recipe if it is not already in the favorited by the user
            update_num_favs_stmt = sqlalchemy.update(db.recipes).where(db.recipes.c.recipe_id == recipe_id).values(number_of_favorites = db.recipes.c.number_of_favorites + 1)
            conn.execute(update_num_favs_stmt)
            conn.commit()
        #if the recipe is already in the favorites list, updates the date_favorited
        except sqlalchemy.exc.IntegrityError: 
            transaction.rollback()
            update_favorite_stmt = sqlalchemy.update(db.favorited_recipes).where(db.favorited_recipes.c.recipe_id == recipe_id and db.favorited_recipes.c.user_id == user_id).values(date_favorited = str(datetime.datetime.now()))
            conn.execute(update_favorite_stmt)

    return {"recipe_id": recipe_id,
            "user_id": user_id} 

@router.delete("/favorited_recipes/", tags=["favorited_recipes"])
def unfavorite_recipe(user_id: str, recipe_id: int
    ):
    """
    This endpoint will allow users to remove existing recipes from their favorites list. 
   
    """
    find_user_stmt = sqlalchemy.select(db.users.c.user_id).where(db.users.c.user_id == user_id)

    find_recipe_stmt = sqlalchemy.select(db.recipes.c.recipe_id).where(db.recipes.c.recipe_id == recipe_id)

    delete_favorite_stmt = sqlalchemy.delete(db.favorited_recipes).where(db.favorited_recipes.c.recipe_id == recipe_id and db.favorited_recipes.c.user_id == user_id)

    check_if_favorited_stmt = sqlalchemy.select(db.favorited_recipes.c.recipe_id).where(db.favorited_recipes.c.recipe_id == recipe_id and db.favorited_recipes.c.user_id == user_id)

    decrement_num_favs_stmt = sqlalchemy.update(db.recipes).where(db.recipes.c.recipe_id == recipe_id).values(number_of_favorites = db.recipes.c.number_of_favorites - 1)

    with db.engine.connect() as conn:
        transaction = conn.begin()
        find_user_result = conn.execute(find_user_stmt)
        if find_user_result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found.")
        find_recipe_result = conn.execute(find_recipe_stmt)
        if find_recipe_result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Recipe not found.")
        check_if_favorited_result = conn.execute(check_if_favorited_stmt)
        if check_if_favorited_result.rowcount == 0:
            return {"recipe_id": recipe_id,
                    "user_id": user_id} 
        
        try:
            conn.execute(delete_favorite_stmt)
            transaction.commit()
            conn.execute(decrement_num_favs_stmt)
            conn.commit()
        except sqlalchemy.exc.IntegrityError:
            transaction.rollback()
    
    return {"recipe_id": recipe_id,
            "user_id": user_id} 

@router.get("/favorited_recipes/", tags=["favorited_recipes"])
def list_favorite_recipes(user_id: int, 
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
    ):
    """
    This endpoint will list all recipes in the users favorites list. For each recipe it returns:
    * `recipe_id`: the internal id of the character. Can be used to query the
      `/recipes/{recipe_id}` endpoint.
    * `recipe`: The name of the recipe.
    * `cuisine`: The cuisine that the recipe is from.
    * `meal_type`: The meal type that the recipe is from.
    * `prep_time_mins`: The time needed to make the recipe.
    * `instructions`: The instructions for making the recipe.
    * `ingredients`: The listed ingredients and amounts that are needed to make the recipe.
    * `prep_time_mins`: time needed to make the recipe.

    The `limit` and `offset` query parameters are used for pagination.
    The `limit` query parameter specifies the maximum number of results to return.
    The `offset` query parameter specifies the number of results to skip before
    """
    

    recipe_stmt = (
        sqlalchemy.select(
            db.recipes.c.recipe_id,
            db.recipes.c.recipe_name,
            db.recipes.c.prep_time_mins,
            db.recipes.c.recipe_instructions,
            sqlalchemy.func.ARRAY_AGG(sqlalchemy.distinct(db.meal_type.c.meal_type)).label("meal_types"),
            sqlalchemy.func.ARRAY_AGG(sqlalchemy.distinct(db.cuisine_type.c.cuisine_type)).label("cuisine_types"),
            sqlalchemy.func.ARRAY_AGG(sqlalchemy.distinct(db.ingredients.c.ingredient_name)).label("ingredients"),
        )
        .select_from(
            db.recipes
            .outerjoin(
                db.recipe_meal_types,
                db.recipes.c.recipe_id == db.recipe_meal_types.c.recipe_id
            )
            .outerjoin(
                db.recipe_cuisine_types,
                db.recipes.c.recipe_id == db.recipe_cuisine_types.c.recipe_id
            )
            .outerjoin(
                db.meal_type,
                db.meal_type.c.meal_type_id == db.recipe_meal_types.c.meal_type_id
            )
            .outerjoin(
                db.cuisine_type,
                db.cuisine_type.c.cuisine_type_id == db.recipe_cuisine_types.c.cuisine_type_id
            )
            .outerjoin(
                db.ingredient_quantities,
                db.recipes.c.recipe_id == db.ingredient_quantities.c.recipe_id
            )
            .outerjoin(
                db.ingredients,
                db.ingredients.c.ingredient_id == db.ingredient_quantities.c.ingredient_id
            )
            .join(
                db.favorited_recipes,
                db.recipes.c.recipe_id == db.favorited_recipes.c.recipe_id
            )
        )
        .where(db.favorited_recipes.c.user_id == user_id)
        .group_by(
            db.recipes.c.recipe_id,
            db.recipes.c.recipe_name,
            db.recipes.c.prep_time_mins,
            db.recipes.c.recipe_instructions        ).order_by(db.recipes.c.recipe_name).limit(limit).offset(offset).distinct()
        )

    with db.engine.connect() as conn:
        favorited_results = conn.execute(recipe_stmt)
        if favorited_results.rowcount == 0:
            raise HTTPException(status_code=404, detail="no recipes favorited")
        json = {}
        json["recipes"] = []
        for row in favorited_results:
            json["recipes"].append({"recipe_id": row[0], "recipe_name": row[1], "cuisine": row[6],
                                     "meal_type": row[5], "prep_time_mins": str(row[2]) + " minutes",
                                       "instructions": row[3], "number_of_favorites": row[4]})
        return json


