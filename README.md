# CSC-365-Project: Recipe API
Developers: Anna Rosenberg (arosen12@calpoly.edu), Michelle Tan (mtan22@calpoly.edu), Calista Kerins (crkerins@calpoly.edu)

This Recipe API returns statistics/data on common recipes. This API will contain the following endpoints: get_recipe(recipe_id: str), list_recipes(dish: str = "", limit: int, offset: int,  sort: sort_options), and add_recipe(dish: str, ingredients: list). The get_recipe endpoint will allow users to retrieve a specific recipe by using a unique recipe id. The list_recipes endpoint will allow users to view a list of recipes, and will allow them to search by dish name or by dishes that contain a specified ingredient. Users can also sort the recipes returned by list_recipes in the following ways: by dish title aplabetically, by calories in dish, by cost of total ingredients, and by number of ingredients used. The add_recipe endpoint will allow users to add their own recipes to the API. 

# User Stories / Functional Requirements

- As a user, I want to be able to access recipes with a given list of ingredients, so that I can make a meal with food I already have.
- As a user, I want to be able to filter recipes by meal type (breakfast, lunch, dinner, dessert, snack) so that I can find a recipe for the meal I am making.
- As a user, I want to be able to filter recipes by cuisine (Italian, Korean, Mexican, etc.) so that I can make whatever type of food I am craving.
- As a chef, I want to be able to add new recipes I have created to the database of existing recipes so that I can access them again.
- As a user, I want to be able to see what ingredients I am missing from a specific recipe so that I know what I need to buy.
- The system shall order recipes based on the number of matching ingredients between each recipe and the given user input, displaying recipes with the most matching ingredients at the top.
- As a user, I want to be able to see how long it will take me to make each recipe so that I can plan accordingly.
- As a user, I want to be able to filter recipes by the time they take to make so that I can search for an easy meal if I am in a rush.
- As a user, I want to be able to favorite recipes, so that I can quickly access recipes I like.
