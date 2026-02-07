import requests
import random
import json
import time
import pygame
import io

# Constants
FILTER_URL = "https://www.themealdb.com/api/json/v1/1/filter.php?c=Dessert"
LOOKUP_URL = "https://www.themealdb.com/api/json/v1/1/lookup.php?i="
COOKBOOK_FILE = "my_bakery_cookbook.txt"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CREAM = (255, 253, 208)
BROWN = (101, 67, 33)
PASTEL_PINK = (255, 209, 220)
PASTEL_BLUE = (174, 198, 207)
PASTEL_GREEN = (193, 225, 193)
SOFT_RED = (255, 105, 97)
GRAY = (180, 180, 180)

# Pygame Setup
WIN_WIDTH, WIN_HEIGHT = 1000, 700
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("The Great Python Bake-Off")
clock = pygame.time.Clock()

# Fonts
TITLE_FONT = pygame.font.SysFont("Georgia", 54, bold=True)
UI_FONT = pygame.font.SysFont("Georgia", 26)
COOKBOOK_FONT = pygame.font.SysFont("Times New Roman", 20, italic=True)
SMALL_FONT = pygame.font.SysFont("Arial", 18)

class GameState:
    MENU = 0
    LOADING = 1
    PLAYING = 2
    RESULT = 3

class BakeryGame:
    def __init__(self):
        self.state = GameState.MENU
        self.difficulty = None
        self.score = 0
        self.current_meal = None
        self.ingredients = []
        self.display_ingredients = []
        self.image = None
        self.pixel_size = 1
        self.input_text = ""
        self.revealed_indices = set()
        self.hint_count = 0
        self.result_message = ""
        self.is_winner = False
        
        # Load Star Sprite
        try:
            self.star_img = pygame.image.load("star_sprite.png")
            self.star_img = pygame.transform.scale(self.star_img, (80, 80))
        except:
            self.star_img = None

    def get_dessert(self):
        try:
            response = requests.get(FILTER_URL)
            data = response.json()
            meals = data['meals']
            
            # Step 1: Filter by word count (max 3 words) for ALL modes
            meals = [m for m in meals if len(m['strMeal'].split()) <= 3]
            
            # Easy Mode Filtering
            if self.difficulty == "easy":
                keywords = ["cake", "pie", "cookie", "pudding", "brownie", "donut", "ice cream"]
                easy_meals = [m for m in meals if any(k in m['strMeal'].lower() for k in keywords)]
                if easy_meals:
                    meals = easy_meals

            meal_id = random.choice(meals)['idMeal']
            
            detail_response = requests.get(f"{LOOKUP_URL}{meal_id}")
            meal = detail_response.json()['meals'][0]
            
            # Load Image
            img_res = requests.get(meal['strMealThumb'])
            img_data = io.BytesIO(img_res.content)
            self.image = pygame.image.load(img_data)
            self.image = pygame.transform.scale(self.image, (450, 450))
            
            return meal
        except Exception as e:
            print(f"API Error: {e}")
            return None

    def start_game(self, diff):
        self.difficulty = diff
        self.state = GameState.LOADING
        self.input_text = ""
        self.hint_count = 0
        self.revealed_indices = set()
        
        meal = self.get_dessert()
        if meal:
            self.current_meal = meal
            self.ingredients = self.parse_ingredients(meal)
            self.setup_round()
            self.state = GameState.PLAYING
        else:
            self.state = GameState.MENU

    def parse_ingredients(self, meal):
        ing_list = []
        for i in range(1, 21):
            ing = meal.get(f"strIngredient{i}")
            meas = meal.get(f"strMeasure{i}")
            if ing and ing.strip():
                clean_meas = meas.strip() if meas and meas.strip() else ""
                ing_list.append(f"{clean_meas} {ing.strip()}".strip())
        return ing_list

    def setup_round(self):
        self.display_ingredients = []
        name = self.current_meal['strMeal']
        
        # Initialize revealed indices (spaces and punctuation revealed by default)
        for i, char in enumerate(name):
            if not char.isalnum():
                self.revealed_indices.add(i)
        
        if self.difficulty == "easy":
            self.pixel_size = 8 # Lightly pixelated
            self.display_ingredients = list(self.ingredients)
        elif self.difficulty == "medium":
            self.pixel_size = 24
            self.display_ingredients = list(self.ingredients)
        elif self.difficulty == "hard":
            self.pixel_size = 48
            # Show half ingredients, rest are '?'
            count = max(3, len(self.ingredients) // 2)
            indices = random.sample(range(len(self.ingredients)), count)
            for i in range(len(self.ingredients)):
                if i in indices:
                    self.display_ingredients.append(self.ingredients[i])
                else:
                    self.display_ingredients.append("??? (Hidden Ingredient)")

    def apply_pixelation(self, surface, size):
        if size <= 1: return surface
        width, height = surface.get_size()
        small_w = max(1, width // size)
        small_h = max(1, height // size)
        small = pygame.transform.scale(surface, (small_w, small_h))
        return pygame.transform.scale(small, (width, height))

    def handle_hint(self):
        name = self.current_meal['strMeal']
        # Find next unrevealed character
        new_revealed = False
        for i in range(len(name)):
            if i not in self.revealed_indices:
                self.revealed_indices.add(i)
                self.hint_count += 1
                new_revealed = True
                break
        
        # Pixelation decreases on EVERY hint for all modes
        self.pixel_size = max(1, self.pixel_size - (4 if self.difficulty == "easy" else 2))
        
        if new_revealed:
            self.check_auto_loss()

    def reveal_word(self):
        name = self.current_meal['strMeal']
        words = name.split()
        current_pos = 0
        
        for word in words:
            # Find the index range of this word in the original name
            word_start = name.find(word, current_pos)
            word_end = word_start + len(word)
            
            # Check if this word is fully revealed
            is_word_revealed = all(i in self.revealed_indices for i in range(word_start, word_end))
            
            if not is_word_revealed:
                # Reveal all characters in this word
                for i in range(word_start, word_end):
                    self.revealed_indices.add(i)
                
                # Pixelation decreases
                self.pixel_size = max(1, self.pixel_size - (8 if self.difficulty == "easy" else 4))
                self.check_auto_loss()
                return
            
            current_pos = word_end

    def check_auto_loss(self):
        name = self.current_meal['strMeal']
        # If all alphabetic characters are revealed, user loses because they didn't "guess" it
        all_revealed = all(i in self.revealed_indices for i in range(len(name)) if name[i].isalnum())
        if all_revealed:
            self.is_winner = False
            self.result_message = f"Darn! The secret dessert was {name}"
            self.state = GameState.RESULT

    def is_close_enough(self, guess, target):
        guess = guess.lower().strip()
        target = target.lower().strip()
        
        if not guess: return False
        if guess == target: return True
        
        # Check if guess is a substantial part of the target
        # e.g., "banana bread" in "Walnut, honey banana bread"
        if len(guess) > 3 and guess in target:
            return True
        
        # Check if target contains the key words of the guess
        guess_words = set(guess.split())
        target_words = set(target.replace(",", "").split())
        if guess_words.issubset(target_words) and len(guess_words) >= 2:
            return True
            
        return False

    def check_guess(self):
        guess = self.input_text.strip().lower()
        if guess == "hint":
            self.handle_hint()
            self.input_text = ""
            return

        target_name = self.current_meal['strMeal']
        if self.is_close_enough(guess, target_name):
            self.is_winner = True
            self.score += 1
            self.result_message = "Star Baker!"
            self.save_recipe()
            self.state = GameState.RESULT
        else:
            self.is_winner = False
            self.result_message = f"Darn! The secret dessert was {target_name}"
            self.state = GameState.RESULT

    def save_recipe(self):
        try:
            with open(COOKBOOK_FILE, "a") as f:
                f.write(f"--- {self.current_meal['strMeal']} ---\n")
                f.write("Ingredients:\n")
                for ing in self.ingredients:
                    f.write(f"- {ing}\n")
                f.write("\nInstructions:\n")
                f.write(f"{self.current_meal['strInstructions']}\n\n")
        except: pass

    def draw_button(self, text, x, y, w, h, color):
        shadow_offset = 4
        pygame.draw.rect(screen, BROWN, (x+shadow_offset, y+shadow_offset, w, h), border_radius=15)
        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=15)
        pygame.draw.rect(screen, BROWN, (x, y, w, h), 3, border_radius=15)
        txt = UI_FONT.render(text, True, BROWN)
        screen.blit(txt, (x + (w - txt.get_width()) // 2, y + (h - txt.get_height()) // 2))
        return pygame.Rect(x, y, w, h)

    def draw_secret_message(self, x, y):
        name = self.current_meal['strMeal']
        display_str = ""
        for i, char in enumerate(name):
            if i in self.revealed_indices:
                display_str += char + " "
            else:
                display_str += "_ "
        
        txt = UI_FONT.render(f"Secret Recipe: {display_str}", True, BROWN)
        # Scale if it's too long
        if txt.get_width() > 650:
            ratio = 650 / txt.get_width()
            txt = pygame.transform.scale(txt, (int(txt.get_width() * ratio), int(txt.get_height() * ratio)))
        screen.blit(txt, (x, y))

    def draw(self):
        # Background - Vintage Cream Parchment
        screen.fill(CREAM)
        # Decorative Border
        pygame.draw.rect(screen, PASTEL_PINK, (10, 10, WIN_WIDTH-20, WIN_HEIGHT-20), 5, border_radius=20)
        
        if self.state == GameState.MENU:
            title = TITLE_FONT.render("The Great Python Bake-Off", True, BROWN)
            screen.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 100))
            
            sub = UI_FONT.render("Choose your kitchen level:", True, BROWN)
            screen.blit(sub, (WIN_WIDTH // 2 - sub.get_width() // 2, 180))
            
            self.btn_easy = self.draw_button("Home Baker (Easy)", 350, 250, 300, 60, PASTEL_GREEN)
            self.btn_medium = self.draw_button("Pastry Chef (Med)", 350, 340, 300, 60, PASTEL_BLUE)
            self.btn_hard = self.draw_button("Master Baker (Hard)", 350, 430, 300, 60, SOFT_RED)

        elif self.state == GameState.LOADING:
            txt = TITLE_FONT.render("Folding in the flour...", True, BROWN)
            screen.blit(txt, (WIN_WIDTH // 2 - txt.get_width() // 2, WIN_HEIGHT // 2))

        elif self.state == GameState.PLAYING:
            # Draw Image
            p_img = self.apply_pixelation(self.image, self.pixel_size)
            screen.blit(p_img, (50, 50))
            pygame.draw.rect(screen, BROWN, (50, 50, 450, 450), 4)
            
            # Draw Cookbook Page for Ingredients (Narrower to avoid overlap)
            pygame.draw.rect(screen, WHITE, (530, 40, 420, 460), border_radius=5)
            pygame.draw.rect(screen, BROWN, (530, 40, 420, 460), 2, border_radius=5)
            
            ing_header = TITLE_FONT.render("Ingredients", True, BROWN)
            small_title = pygame.transform.scale(ing_header, (ing_header.get_width()//2, ing_header.get_height()//2))
            screen.blit(small_title, (550, 50))
            
            # Dynamic Font Size for Ingredients
            ing_font = COOKBOOK_FONT
            if len(self.display_ingredients) > 13:
                ing_font = pygame.font.SysFont("Times New Roman", 17, italic=True)
            if len(self.display_ingredients) > 17:
                ing_font = pygame.font.SysFont("Times New Roman", 14, italic=True)

            for i, ing in enumerate(self.display_ingredients[:20]):
                txt = ing_font.render(f"~ {ing}", True, BLACK)
                screen.blit(txt, (550, 95 + i * 18))
            
            # Buttons for Hints (Positioned below cookbook)
            self.btn_hint_letter = self.draw_button("Reveal Letter", 750, 520, 200, 40, PASTEL_PINK)
            self.btn_hint_word = self.draw_button("Reveal Word", 750, 575, 200, 40, PASTEL_BLUE)
            
            # Secret Message
            self.draw_secret_message(50, 520)
            
            # Input Box
            pygame.draw.rect(screen, WHITE, (50, 595, 600, 50), border_radius=10)
            pygame.draw.rect(screen, BROWN, (50, 595, 600, 50), 2, border_radius=10)
            input_surface = UI_FONT.render(self.input_text + "|", True, BLACK)
            screen.blit(input_surface, (65, 605))
            
            hint_txt = SMALL_FONT.render("Type guess + ENTER (or use help buttons)", True, BROWN)
            screen.blit(hint_txt, (50, 655))
            
            score_txt = TITLE_FONT.render(f"Score: {self.score}", True, BROWN)
            scaled_score = pygame.transform.scale(score_txt, (score_txt.get_width()//2, score_txt.get_height()//2))
            screen.blit(scaled_score, (850, 640))

        elif self.state == GameState.RESULT:
            # Center and scale image slightly smaller for results
            res_img_size = 350
            scaled_img = pygame.transform.scale(self.image, (res_img_size, res_img_size))
            img_x = (WIN_WIDTH - res_img_size) // 2
            img_y = 40
            screen.blit(scaled_img, (img_x, img_y))
            pygame.draw.rect(screen, BROWN, (img_x, img_y, res_img_size, res_img_size), 4)
            
            # Display result message
            res_txt = UI_FONT.render(self.result_message, True, BROWN)
            if res_txt.get_width() > 800:
                ratio = 800 / res_txt.get_width()
                res_txt = pygame.transform.scale(res_txt, (int(res_txt.get_width() * ratio), int(res_txt.get_height() * ratio)))
            
            res_x = (WIN_WIDTH - res_txt.get_width()) // 2
            res_y = img_y + res_img_size + 40
            
            if self.is_winner and self.star_img:
                # Draw stars on either side (now bigger)
                star_y = res_y + (res_txt.get_height() // 2) - 40
                screen.blit(self.star_img, (res_x - 100, star_y))
                screen.blit(self.star_img, (res_x + res_txt.get_width() + 20, star_y))
            
            screen.blit(res_txt, (res_x, res_y))
            
            self.btn_next = self.draw_button("Bake Another!", 350, res_y + 60, 300, 60, PASTEL_GREEN)
            self.btn_quit = self.draw_button("Close Shop", 350, res_y + 140, 300, 60, GRAY)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.state == GameState.MENU:
                        if self.btn_easy.collidepoint(pos): self.start_game("easy")
                        if self.btn_medium.collidepoint(pos): self.start_game("medium")
                        if self.btn_hard.collidepoint(pos): self.start_game("hard")
                    elif self.state == GameState.PLAYING:
                        if self.btn_hint_letter.collidepoint(pos):
                            self.handle_hint()
                        elif self.btn_hint_word.collidepoint(pos):
                            self.reveal_word()
                    elif self.state == GameState.RESULT:
                        if self.btn_next.collidepoint(pos): self.state = GameState.MENU
                        if self.btn_quit.collidepoint(pos): running = False
                
                if event.type == pygame.KEYDOWN and self.state == GameState.PLAYING:
                    if event.key == pygame.K_RETURN:
                        self.check_guess()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if len(self.input_text) < 30:
                            self.input_text += event.unicode

            self.draw()
            clock.tick(30)
        pygame.quit()

if __name__ == "__main__":
    game = BakeryGame()
    game.run()
