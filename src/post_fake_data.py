import os
import io
import dotenv
from sqlalchemy import create_engine
import sqlalchemy
from faker import Faker
import numpy as np

local_database_connection_url = "postgresql://postgres:postgres@localhost:5432/postgres"

engine = sqlalchemy.create_engine(local_database_connection_url)

categories = []


fake = Faker()
num_users = 100000

with engine.begin() as conn:
    print("Creating tables...")
    conn.execute(sqlalchemy.text("""
    DROP TABLE IF EXISTS recipe_cuisine_types CASCADE;
    DROP TABLE IF EXISTS recipe_meal_types CASCADE;
    DROP TABLE IF EXISTS favorited_recipes CASCADE;
    DROP TABLE IF EXISTS users CASCADE;
    DROP TABLE IF EXISTS ingredients CASCADE;
    DROP TABLE IF EXISTS ingredient_quantities CASCADE;
    DROP TABLE IF EXISTS recipes CASCADE;
    DROP TABLE IF EXISTS cuisine_type CASCADE;
    DROP TABLE IF EXISTS meal_type CASCADE;

    

    CREATE TABLE
        recipes (
            recipe_id int generated always as identity not null PRIMARY KEY,
            recipe_name text not null,
            calories int,
            prep_time_mins int,
            recipe_instructions text,
            recipe_url text,
            number_of_favorites int not null
        );

    CREATE TABLE
        ingredients (
            ingredient_id int generated always as identity not null PRIMARY KEY,
            ingredient_name text not null
        );

    CREATE TABLE
        users (
            user_id int generated always as identity not null PRIMARY KEY,
            user_name text not null,
            password text not null
        );

    CREATE TABLE
        cuisine_type (
            cuisine_type_id int generated always as identity not null PRIMARY KEY,
            cuisine_type text not null
        );

    CREATE TABLE
        meal_type (
            meal_type_id int generated always as identity not null PRIMARY KEY,
            meal_type text not null
        );

    CREATE TABLE
        recipe_cuisine_types (
            recipe_id int not null,
            cuisine_type_id int not null,
            PRIMARY KEY (recipe_id, cuisine_type_id),
            FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id),
            FOREIGN KEY (cuisine_type_id) REFERENCES cuisine_type (cuisine_type_id)
        );

    CREATE TABLE
        recipe_meal_types (
            recipe_id int not null,
            meal_type_id int not null,
            PRIMARY KEY (recipe_id, meal_type_id),
            FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id),
            FOREIGN KEY (meal_type_id) REFERENCES meal_type (meal_type_id)
        );

    CREATE TABLE
        favorited_recipes (
            user_id int not null,
            recipe_id int not null,
            date_favorited text not null,
            PRIMARY KEY (user_id, recipe_id),
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id)
        );


    CREATE TABLE
        ingredient_quantities (
            recipe_id int not null,
            ingredient_id int not null,
            unit_type text,
            amount float,
            ingredient_price_usd float,
            PRIMARY KEY (recipe_id, ingredient_id),
            FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id),
            FOREIGN KEY (ingredient_id) REFERENCES ingredients (ingredient_id)
        );
        

    
    """))
    
    print("Tables created successfully")

    users = []
    for i in range(num_users):
             user_name = fake.user_name()
             password = fake.password()
             users.append(
                 {
                     "user_name": user_name,
                     "password": password
                 }
             )
    if users:
             conn.execute(sqlalchemy.text("""
             INSERT INTO users (user_name, password) VALUES (:user_name, :password);
             """), users)

    recipes =[]
    for i in range(100000):
        recipe_name = fake.sentence()
        calories = fake.random_int(min=0, max=1000)
        prep_time_mins = fake.random_int(min=0, max=1000)
        recipe_instructions = fake.paragraph(nb_sentences=5)
        recipe_url = fake.url()
        number_of_favorites = fake.random_int(min=0, max=1000)
        recipes.append(
            {
                "recipe_name": recipe_name,
                "calories": calories,
                "prep_time_mins": prep_time_mins,
                "recipe_instructions": recipe_instructions,
                "recipe_url": recipe_url,
                "number_of_favorites": number_of_favorites
            }
        )
    if recipes:
        conn.execute(sqlalchemy.text("""
        INSERT INTO recipes (recipe_name, calories, prep_time_mins, recipe_instructions, recipe_url, number_of_favorites) VALUES (:recipe_name, :calories, :prep_time_mins, :recipe_instructions, :recipe_url, :number_of_favorites);
        """), recipes)

    ingredients = []
    for i in range(100000):
        ingredient_name = fake.word()
        ingredients.append(
            {
                "ingredient_name": ingredient_name
            }
        )
    if ingredients:
        conn.execute(sqlalchemy.text("""
        INSERT INTO ingredients (ingredient_name) VALUES (:ingredient_name);
        """), ingredients)

    cuisine_types = []
    for i in range(500):
        cuisine_type = fake.word()
        cuisine_types.append(
            {
                "cuisine_type": cuisine_type
            }
        )
    if cuisine_types:
        conn.execute(sqlalchemy.text("""
        INSERT INTO cuisine_type (cuisine_type) VALUES (:cuisine_type);
        """), cuisine_types)

    meal_types = []
    for i in range(500):
        meal_type = fake.word()
        meal_types.append(
            {
                "meal_type": meal_type
            }
        )
    if meal_types:
        conn.execute(sqlalchemy.text("""
        INSERT INTO meal_type (meal_type) VALUES (:meal_type);
        """), meal_types)

    recipe_cuisine_types = []
    for i in range(100000):
        recipe_id = fake.random_int(min=1, max=100000)
        cuisine_type_id = fake.random_int(min=1, max=500)
        recipe_cuisine_types.append(
            {
                "recipe_id": recipe_id,
                "cuisine_type_id": cuisine_type_id
            }
        )
    if recipe_cuisine_types:
        insert_query = """
        INSERT INTO recipe_cuisine_types (recipe_id, cuisine_type_id)
        SELECT DISTINCT :recipe_id, :cuisine_type_id
        FROM (
            VALUES (:recipe_id, :cuisine_type_id)
        ) AS i(recipe_id, cuisine_type_id)
        LEFT JOIN recipe_cuisine_types rct
            ON rct.recipe_id = i.recipe_id AND rct.cuisine_type_id = i.cuisine_type_id
        WHERE rct.recipe_id IS NULL
        """
        conn.execute(sqlalchemy.text(insert_query), recipe_cuisine_types)

    recipe_meal_types = []
    for i in range(100000):
        recipe_id = fake.random_int(min=1, max=100000)
        meal_type_id = fake.random_int(min=1, max=500)
        recipe_meal_types.append(
            {
                "recipe_id": recipe_id,
                "meal_type_id": meal_type_id
            }
        )
    if recipe_meal_types:
        insert_query = """
        INSERT INTO recipe_meal_types (recipe_id, meal_type_id)
        SELECT DISTINCT :recipe_id, :meal_type_id
        FROM (
            VALUES (:recipe_id, :meal_type_id)
        ) AS i(recipe_id, meal_type_id)
        LEFT JOIN recipe_meal_types rmt
            ON rmt.recipe_id = i.recipe_id AND rmt.meal_type_id = i.meal_type_id
        WHERE rmt.recipe_id IS NULL
        """
        conn.execute(sqlalchemy.text(insert_query), recipe_meal_types)

    favorited_recipes = []
    for i in range(100000):
        user_id = fake.random_int(min=1, max=100000)
        recipe_id = fake.random_int(min=1, max=100000)
        date_favorited = fake.date()
        favorited_recipes.append(
            {
                "user_id": user_id,
                "recipe_id": recipe_id,
                "date_favorited": date_favorited
            }
        )

    if favorited_recipes:
        insert_query = """
        INSERT INTO favorited_recipes (user_id, recipe_id, date_favorited)
        SELECT DISTINCT :user_id, :recipe_id, :date_favorited
        FROM (
            VALUES (:user_id, :recipe_id, :date_favorited)
        ) AS i(user_id, recipe_id, date_favorited)
        LEFT JOIN favorited_recipes fr
            ON fr.user_id = i.user_id AND fr.recipe_id = i.recipe_id
        WHERE fr.user_id IS NULL
        """
        conn.execute(sqlalchemy.text(insert_query), favorited_recipes)

    ingredient_quantities = []
    for i in range(500000):
        recipe_id = fake.random_int(min=1, max=100000)
        ingredient_id = fake.random_int(min=1, max=100000)
        unit_type = fake.word()
        amount = fake.random_int(min=0, max=1000)
        ingredient_price_usd = fake.random_int(min=0, max=1000)
        ingredient_quantities.append(
            {
                "recipe_id": recipe_id,
                "ingredient_id": ingredient_id,
                "unit_type": unit_type,
                "amount": amount,
                "ingredient_price_usd": ingredient_price_usd
            }
        )
    if ingredient_quantities:
        insert_query = """
        INSERT INTO ingredient_quantities (recipe_id, ingredient_id, unit_type, amount, ingredient_price_usd)
        SELECT DISTINCT i.recipe_id, i.ingredient_id, i.unit_type, i.amount, i.ingredient_price_usd
        FROM (
            VALUES (:recipe_id, :ingredient_id, :unit_type, :amount, :ingredient_price_usd)
        ) AS i(recipe_id, ingredient_id, unit_type, amount, ingredient_price_usd)
        LEFT JOIN ingredient_quantities iq
            ON iq.recipe_id = i.recipe_id AND iq.ingredient_id = i.ingredient_id
        WHERE iq.recipe_id IS NULL
        """
        conn.execute(sqlalchemy.text(insert_query), ingredient_quantities)


         

    
    


    

   
    
