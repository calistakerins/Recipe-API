import csv
import os
import io
from supabase import Client, create_client
import dotenv
from sqlalchemy import create_engine
import sqlalchemy



def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

engine = sqlalchemy.create_engine(database_connection_url())

conn = engine.connect()

metadata_obj = sqlalchemy.MetaData()

recipes = sqlalchemy.Table("recipes", metadata_obj, autoload_with=engine)
ingredients = sqlalchemy.Table("ingredients", metadata_obj, autoload_with=engine)
ingredient_quantities = sqlalchemy.Table("ingredient_quantities", metadata_obj, autoload_with=engine)
cuisine_type = sqlalchemy.Table("cuisine_type", metadata_obj, autoload_with=engine)
meal_type = sqlalchemy.Table("meal_type", metadata_obj, autoload_with=engine)
favorited_recipes = sqlalchemy.Table("favorited_recipes", metadata_obj, autoload_with=engine)
users = sqlalchemy.Table("users", metadata_obj, autoload_with=engine)
recipe_cuisine_types = sqlalchemy.Table("recipe_cuisine_types", metadata_obj, autoload_with=engine)
recipe_meal_types = sqlalchemy.Table("recipe_meal_types", metadata_obj, autoload_with=engine)
