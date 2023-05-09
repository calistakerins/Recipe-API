from fastapi import FastAPI
from src.api import ingredients, recipes, pkg_util

description = """
Recipes API returns important information related to different recipes.

## Recipes

You can:
* **retrieve a specific recipe by id.**
* **list recipes with sorting and filtering options.**
* **add a recipe to the database**
* **modify an existing recipe**
* **favorite a recipe**
* **view your favorited recipes**

## Ingriedients

You can:
* **list ingredients with sorting and filtering options.**
* **retrieve a specific ingredient by id**

"""
tags_metadata = [
    {
        "name": "recipes",
        "description": "Access information on recipes.",
    },
    {
        "name": "ingredients",
        "description": "Access information on ingredients.",
    },

]

app = FastAPI(
    title="Recipe API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Anna Rosenberg, Michelle Tan, Calista Kerins",
        "email": "arosen12@calpoly.edu, mtan22@calpoly.edu, crkerins@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)
app.include_router(ingredients.router)
app.include_router(recipes.router)
app.include_router(pkg_util.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Recipe API. See /docs for more information."}
