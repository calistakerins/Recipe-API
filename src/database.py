import csv
import os
import io
from supabase import Client, create_client
import dotenv
from sqlalchemy import create_engine
import sqlalchemy

# # DO NOT CHANGE THIS TO BE HARDCODED. ONLY PULL FROM ENVIRONMENT VARIABLES.
dotenv.load_dotenv()
supabase_api_key = os.environ.get("SUPABASE_API_KEY")
supabase_url = os.environ.get("SUPABASE_URL")

if supabase_api_key is None or supabase_url is None:
    raise Exception(
        "You must set the SUPABASE_API_KEY and SUPABASE_URL environment variables."
    )

supabase: Client = create_client(supabase_url, supabase_api_key)

sess = supabase.auth.get_session()

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
users = sqlalchemy.Table("user", metadata_obj, autoload_with=engine)
