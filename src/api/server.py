from fastapi import FastAPI
from src.api import ingredients, recipes, pkg_util

description = """
Movie API returns dialog statistics on top hollywood movies from decades past.

## Characters

You can:
* **list characters with sorting and filtering options.**
* **retrieve a specific character by id**

## Movies

You can:
* **list movies with sorting and filtering options.**
* **retrieve a specific movie by id**
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
    title="Movie API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Anna Rosenberg, Mechelle Tan, Calista Kerins",
        "email": "arosen12@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)
app.include_router(ingredients.router)
app.include_router(recipes.router)
app.include_router(pkg_util.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Movie API. See /docs for more information."}
