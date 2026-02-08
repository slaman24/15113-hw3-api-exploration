# 15113-hw3-api-exploration

This is my hw3 Explore an API assignment. Using AI (specifically Gemini 3 Flash), I have built an app called The Great Python Bake-Off, which is a dessert guesser game that challenges the user to identify a secret dessert based on an image and list of ingredients. It uses TheMealDB API.

TheMealDB API: https://www.themealdb.com/api.php

Video demo: https://drive.google.com/file/d/1oHCjM2R7hTt5wsJiI1r65pkuBd6_yNS4/view?usp=sharing

Star image credit: https://www.shutterstock.com/search/cartoon-star

My Python app uses the requests Python librray to query TheMealDB API, filtering for dessert recipes. The API returns the data in a JSON format, and the app iterates through numbered keys (in the form strIngredient1, strIngredient2, etc.) to extract the ingredient and measurment details in the recipe. The app also retrieves an image of the recipe using io.BytesIO. This allows the app to process the images in memory without having to save the files to a disk, which can take up a lot of space.
