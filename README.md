# 15113-hw3-api-exploration

This is my hw3 Explore an API assignment.

Star image credit: https://www.shutterstock.com/search/cartoon-star

My Python app, The Great Python Bake-Off, uses the requests Python librray to query TheMealDB API, filtering for dessert recipes. The API returns the data in a JSON format, and the app iterates through numbered keys (in the form strIngredient1, strIngredient2, etc.) to extract the ingredient and measurment details in the recipe. The app also retrieves an image of the recipe using io.BytesIO. This allows the app to process the images in memory without having to save the files to a disk, which can take up a lot of space.
