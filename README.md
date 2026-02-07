# 15113-hw3-api-exploration

This is my hw3 Explore an API assignment.

Star image credit: https://www.shutterstock.com/search/cartoon-star

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

1. The Ingredients: TheMealDB API
   We are using TheMealDB API, an open-source database.

Step A (The Menu): First, we call a "filter" endpoint. This gives us a massive list of every dessert in their database, but only includes the names and IDs.
Step B (The Recipe): Once you pick a difficulty, the game picks a random ID and calls the "lookup" endpoint. This returns a massive JSON object containing everything: the name, full instructions, a link to the photo, and 20 separate slots for ingredients. 2. Extractions: Ingredients & Measures
Extracting the recipe is tricky because the API doesn't use a list; it uses separate keys like strIngredient1, strIngredient2, etc.

Our code uses a for loop that counts from 1 to 20.
In each step, it constructs a string (e.g., f"strIngredient{i}") to "knock on the door" of that data slot.
If someone is "home" (the ingredient isn't empty), it grabs the matching strMeasure for that same number, cleans up any weird whitespace, and adds it to your cookbook list. 3. Visuals: Remote Images to Pygame
This is the coolest part! Since we don't want to fill your computer with hundreds of dessert photos, we do everything in "live memory":

Downloading: We use the requests library to go to the strMealThumb URL and download the raw image data as a stream of bytes.
Virtual Files: Pygame usually likes loading files from a disk. To bypass this, we use io.BytesIO. This acts like a "virtual file" in your computer's RAM.
Loading: Pygame reads from this virtual file, and we scale it to fit our window—allowing us to show high-def photos of delicious desserts instantly.

No, it does not cost any money, and you don't need to worry about an API key!

Here is how that works:

The "1" Key: TheMealDB provides a public "test" API key which is the digit 1. I have built your script to use this key automatically in the URLs (e.g., .../v1/1/lookup.php).
Free for Developers: This public key is specifically designed for students and developers to explore the API, build apps, and learn without any sign-up process or financial commitment.
Limitations: Because it is free, it is technically limited to a "reasonable" number of requests, but for a single player in a CLI game, you will never hit any limits or be charged anything.

prompt log:
Context: I am building a standalone Python CLI game called "The Great Python Bake-Off" for my coding class. The game uses the TheMealDB API to fetch random recipes and challenges the user to guess the dessert name based on its ingredients.

Goal: Create a script that:

Fetches Data: Uses the requests library to call https://www.themealdb.com/api/json/v1/1/filter.php?c=Dessert. This will get a list of all desserts.

Selection: Randomly selects one dessert ID from that list and then fetches the full details for that specific meal using https://www.themealdb.com/api/json/v1/1/lookup.php?i=[MEAL_ID].

Game Logic: > - Display only the list of Ingredients and Measurements to the user (e.g., "2 cups Flour", "3 Eggs").

Hide the name of the dessert and the instructions.

Ask the user to guess the name of the dessert.

Scoring & Interaction: > - If the user is stuck, allow them to type "hint" to see the first 50 characters of the instructions.

If they guess correctly, award them a "Star Baker" point and save the full recipe (Name, Ingredients, and Instructions) into a local file named my_bakery_cookbook.txt.

If they guess incorrectly, show them the correct answer with a "Better luck next time" message.

Formatting: Use clear print statements, some simple ASCII art for a "Kitchen" feel, and a loop so the user can play multiple rounds or "Quit" the game.

Constraints: Do not use any API keys. Use the json and random libraries. Keep the code organized into functions (e.g., get_dessert(), play_round(), save_recipe()).

Plan Mode Task: Please outline the step-by-step logic for this script, including how to handle the JSON response and how to format the ingredient list cleanly.

Could we have graphics pop into a new window? Possibly using pygame or something like that? I want to expand outside the terminal and make it feel more like an app or game.

I absolutely love the incorporation of an image! Here is what I am thinking: Get rid of the terminal input all together. Can you expand the size of the window so you display the image of the desert pixelated with the list of ingredients next to it? I feel like the terminal input makes the game feel disjointed. What if there was a welcome screen to start that said Welcome to the Great Python Bake-Off! and then the user has to click on either the word easy, medium, or hard to select a game mode. If the user picks easy, the image of the dessert is pixelated (but not that much, so it is still pretty easy to identify what is in the image). There is also the words Secret Message: ? at the bottom of the screen, and a text box. If the user types hint in the text box, the image becomes even more unpixelated, and the ? in Secret Message: ? is replaced with the next letter of the secret desert. If the user picks medium, the image does not get more unpixelated, and if they pick hard, only half of the ingredients are shown.

I love this! A few things I want to add:

What are the UI/UX capabilities of pygame. Can we make the overall look more aesthetically pleasing, adding a cutsey dessert theme. It would be great if you could stylze the buttons more, and write the ingredients in a way that gives it a vintage cookbook style. I want the game to look fun and cute and transport the user!
For all modes, I think it would be helpful to adjust the scoring to be abit more fair. For example, if the desert was "Mini bundt cakes", the guess should be case insensative and the user should also be able to guess something like "bundt cake" and still get the points, or maybe if the secret dessert was "Walnut, honey banana bread, the user should be able to guess "banana bread" and get the points
For all modes, there should be a letter count for the secret dessert displayed (maybe right under "Secret Message: ?). That count should go down when the user uses hint to reveal a new letter, the ? should disappear, and the cursor should jump, indicating that there is a space in the secret dessert title
Because of my modications listed in 3, I'm thinking of slightly adjusting hard mode and having the only reasons that it is hard is that half of the ingredients are listed. You can maybe indicate that there are other ingredients, but just put a ? in their place

This is really great! I absolutely love what you did! I have a few more changes:

I think the starting level of pixelation is great for each mode. I do think that for each mode, the picture should become less pixeltated when the user types hint
I don't think I want a letter count anymore. Instead, could there be a button that reads Reveal Word, that will reveal te next unrevealed word in the secret dessert. If the user reveals the last letter or clicking this button reveals the last word, the user should be taken immediately to the losing screen
Sometimes, the secret message dashed extend into the cookbook box. Is there a way to make the cookbook box not as long (and if there are more ingrediants, just decreasing the font to have them fit)
In the losing screen, the message goes off the canvas, could you fix this bug?
The only other issue is that this game is nearly impossible! I don't seem to know any of these desserts! How are they filtered in the api? Is there a way to retrieve easier ones or at least ones that are more commonly known?

That all looks really great! I think for all modes, could you maybe limit the secret dessert to only be three words max? Also on the winning and losing screens, the message is currently being drawn on the upper right side of the canvas. Instead, on these screens, can you center the image of the dessert and then below it (centered) either have the message "Darn! The secret dessert was..." or "Star Baker!" with images of stars on either side? The star emoji doesn't seem to be working so I have added in a star image you can use called star_sprite.png

Perfect! Some final adjustments:

The buttons "Bake Another" and "Close Shop" are off screen. Maybe could you make the image of the dessert slightly smaller so they can fit on the canvas, otherwise, I really like the structure of the winning and losing pages!
On the winning screen, could you make the images of the two stars bigger, they are kind of hard to see
Finally, can you explain to me how you are using the api and extracting the recipe ingredients? How are you getting the corresponding images as well? I'm curious to learn how this is all working behind the scenes!
