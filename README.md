# CSC-365-Project: Recipe API
Developers: Anna Rosenberg (arosen12@calpoly.edu), Michelle Tan (mtan22@calpoly.edu), Calista Kerins (crkerins@calpoly.edu)

This Recipe API returns statistics/data on common recipes. The endpoints for this API are documented in recipes.py and ingredients.py.

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

# Edge Cases

- If there are no recipes in the database matching all ingredients the user has listed, the list_recipes will return recipes that contain the most amount of ingredients that the user has listed.
- If there are multiple recipes in the database matching all ingredients the user has listed, the list_recipes will return all recipes that contain all ingredients.
- Recipes that fit into multiple meal type categories (could be made for lunch or dinner, etc.), will be allowed to be put into multiple meal type categories.
- If a user adds a recipe that contains an ingredient that is not in the ingredient database, the add_recipe enpoint will throw an error and ask users to first add the new ingredient to the database using the add_recipe endpoint.
- Our database does not have user-related identification, so all users will see everyones favoried recipes and added recipes. 
