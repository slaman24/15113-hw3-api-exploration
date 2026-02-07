# 15113-hw3-api-exploration

This is my hw3 Explore an API assignment.

Star image credit: https://www.shutterstock.com/search/cartoon-star

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
