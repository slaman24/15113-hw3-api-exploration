# 15113-hw3-api-exploration

This is my hw3 Explore an API assignment.

Steps

Initialize Project

Create bake_off.py (or similar) in the root.
Import requests, random, and json.
Define the base URL constants for the API endpoints.
Implement get_dessert()

Call the filter endpoint (/filter.php?c=Dessert) to get the full list of desserts.
Randomly select one idMeal from the response.
Call the lookup endpoint (/lookup.php?i=[MEAL_ID]) to get the full recipe details.
Return the detailed meal object.
Implement Ingredient Parsing Logic

Create a helper function to iterate from 1 to 20 for strIngredientX and strMeasureX.
Filter out any values that are None, empty strings, or just whitespace.
Combine them into a clean string list (e.g., ["2 cups Flour", "3 Large Eggs"]).
Implement save_recipe(meal_data, ingredients)

Format the recipe into a readable block including the Name, Ingredients, and Instructions.
Append this block to my_bakery_cookbook.txt using the a (append) mode to preserve previous "Star Baker" successes.
Implement play_round(score)

Call get_dessert() to fetch a challenge.
Display the "Kitchen" ASCII art and the list of ingredients to the user.
Enter a while loop for user input:
If input is "hint", print instructions[:50].
If input matches the dessert name (case-insensitive), increment score, call save_recipe(), and return the updated score.
If input is incorrect, reveal the name and return the current score.
Implement main() Loop

Initialize star_baker_points = 0.
Run a while True loop that calls play_round().
After each round, ask the user if they want to "Bake another?" or "Quit".
Display the final "Star Baker" tally upon exit.
