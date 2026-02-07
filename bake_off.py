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
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
GREEN = (34, 139, 34)
RED = (178, 34, 34)

# Pygame Setup
WIN_WIDTH, WIN_HEIGHT = 1000, 700
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("The Great Python Bake-Off")
clock = pygame.time.Clock()

# Fonts
TITLE_FONT = pygame.font.SysFont("Arial", 48, bold=True)
UI_FONT = pygame.font.SysFont("Arial", 24)
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
        self.secret_message = "?"
        self.hint_count = 0
        self.result_message = ""
        self.is_winner = False

    def get_dessert(self):
        try:
            response = requests.get(FILTER_URL)
            data = response.json()
            meals = data['meals']
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
        self.display_ingredients = list(self.ingredients)
        self.secret_message = "?"
        
        if self.difficulty == "easy":
            self.pixel_size = 12 # Very light pixelation
        elif self.difficulty == "medium":
            self.pixel_size = 32 # Medium blocky
        elif self.difficulty == "hard":
            self.pixel_size = 64 # Very blocky
            # Hidden ingredients
            count = max(3, len(self.ingredients) // 2)
            self.display_ingredients = random.sample(self.ingredients, count)

    def apply_pixelation(self, surface, size):
        if size <= 1: return surface
        width, height = surface.get_size()
        # Scale down to small size, then back up to create blocks
        # We use size as the "block size"
        small_w = max(1, width // size)
        small_h = max(1, height // size)
        small = pygame.transform.scale(surface, (small_w, small_h))
        return pygame.transform.scale(small, (width, height))

    def handle_hint(self):
        self.hint_count += 1
        name = self.current_meal['strMeal']
        
        if self.difficulty == "easy":
            # Reveal next letter + reduce pixelation
            reveal_len = min(len(name), self.hint_count)
            self.secret_message = name[:reveal_len] + "?" if reveal_len < len(name) else name
            self.pixel_size = max(1, self.pixel_size - 4)
        elif self.difficulty == "medium":
            # Just reveal next letter, NO pixelation change
            reveal_len = min(len(name), self.hint_count)
            self.secret_message = name[:reveal_len] + "?" if reveal_len < len(name) else name
        elif self.difficulty == "hard":
            # Hard mode: Secret message stays cryptic longer? 
            # Let's say it just shows the letter count
            self.secret_message = "?" * len(name)

    def check_guess(self):
        guess = self.input_text.strip().lower()
        if guess == "hint":
            self.handle_hint()
            self.input_text = ""
            return

        name = self.current_meal['strMeal'].lower()
        if guess == name:
            self.is_winner = True
            self.score += 1
            self.result_message = "STAR BAKER! Correct Answer!"
            self.save_recipe()
            self.state = GameState.RESULT
        else:
            self.is_winner = False
            self.result_message = f"Wrong! It was {self.current_meal['strMeal']}"
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
        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
        pygame.draw.rect(screen, BLACK, (x, y, w, h), 2, border_radius=10)
        txt = UI_FONT.render(text, True, WHITE if color != LIGHT_BLUE else BLACK)
        screen.blit(txt, (x + (w - txt.get_width()) // 2, y + (h - txt.get_height()) // 2))
        return pygame.Rect(x, y, w, h)

    def draw(self):
        screen.fill(WHITE)
        
        if self.state == GameState.MENU:
            title = TITLE_FONT.render("The Great Python Bake-Off", True, DARK_BLUE)
            screen.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 100))
            
            self.btn_easy = self.draw_button("EASY", 400, 250, 200, 50, GREEN)
            self.btn_medium = self.draw_button("MEDIUM", 400, 330, 200, 50, LIGHT_BLUE)
            self.btn_hard = self.draw_button("HARD", 400, 410, 200, 50, RED)

        elif self.state == GameState.LOADING:
            txt = TITLE_FONT.render("Preheating the oven...", True, BLACK)
            screen.blit(txt, (WIN_WIDTH // 2 - txt.get_width() // 2, WIN_HEIGHT // 2))

        elif self.state == GameState.PLAYING:
            # Draw Image
            p_img = self.apply_pixelation(self.image, self.pixel_size)
            screen.blit(p_img, (50, 50))
            pygame.draw.rect(screen, BLACK, (50, 50, 450, 450), 2)
            
            # Draw Ingredients
            ing_header = UI_FONT.render("Ingredients List:", True, BLACK)
            screen.blit(ing_header, (550, 50))
            for i, ing in enumerate(self.display_ingredients[:20]):
                txt = SMALL_FONT.render(f"• {ing}", True, BLACK)
                screen.blit(txt, (550, 90 + i * 22))
            
            # Secret Message
            sm_txt = UI_FONT.render(f"Secret Message: {self.secret_message}", True, DARK_BLUE)
            screen.blit(sm_txt, (50, 520))
            
            # Input Box
            pygame.draw.rect(screen, GRAY, (50, 580, 600, 50), border_radius=5)
            pygame.draw.rect(screen, BLACK, (50, 580, 600, 50), 2, border_radius=5)
            input_surface = UI_FONT.render(self.input_text + "|", True, BLACK)
            screen.blit(input_surface, (60, 590))
            
            hint_txt = SMALL_FONT.render("Type your guess and press ENTER (or type 'hint')", True, BLACK)
            screen.blit(hint_txt, (50, 640))
            
            score_txt = UI_FONT.render(f"Score: {self.score}", True, GREEN)
            screen.blit(score_txt, (850, 20))

        elif self.state == GameState.RESULT:
            screen.blit(self.image, (50, 50))
            pygame.draw.rect(screen, BLACK, (50, 50, 450, 450), 2)
            
            color = GREEN if self.is_winner else RED
            res_txt = UI_FONT.render(self.result_message, True, color)
            screen.blit(res_txt, (550, 150))
            
            self.btn_next = self.draw_button("Bake Another!", 600, 300, 200, 50, DARK_BLUE)
            self.btn_quit = self.draw_button("Exit Game", 600, 380, 200, 50, GRAY)

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
