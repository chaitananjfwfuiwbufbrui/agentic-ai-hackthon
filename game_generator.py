import pygame
import random

def generate_game_code(context):
    """
    Generates the Python code for a 2D game based on the given context.
    For this example, we'll create a "waste sorting" game.
    """
    game_code = f"""
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Waste Management Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game variables
score = 0
font = pygame.font.Font(None, 36)

# Waste items
waste_items = [
    {{"name": "Apple Core", "type": "Organic", "color": GREEN}},
    {{"name": "Plastic Bottle", "type": "Recyclable", "color": BLUE}},
    {{"name": "Newspaper", "type": "Recyclable", "color": BLUE}},
    {{"name": "Battery", "type": "Hazardous", "color": RED}},
    {{"name": "Old Lightbulb", "type": "Hazardous", "color": RED}},
    {{"name": "Banana Peel", "type": "Organic", "color": GREEN}},
]

# Bins
bins = [
    {{"name": "Recyclable", "rect": pygame.Rect(100, 450, 150, 100), "color": BLUE}},
    {{"name": "Organic", "rect": pygame.Rect(325, 450, 150, 100), "color": GREEN}},
    {{"name": "Hazardous", "rect": pygame.Rect(550, 450, 150, 100), "color": RED}},
]

# Current waste item
current_waste = random.choice(waste_items)
waste_rect = pygame.Rect(SCREEN_WIDTH // 2 - 25, 100, 50, 50)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main():
    global current_waste, waste_rect, score
    running = True
    dragging = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if waste_rect.collidepoint(event.pos):
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                for bin_info in bins:
                    if waste_rect.colliderect(bin_info["rect"]):
                        if current_waste["type"] == bin_info["name"]:
                            score += 10
                        else:
                            score -= 5
                        current_waste = random.choice(waste_items)
                        waste_rect.topleft = (SCREEN_WIDTH // 2 - 25, 100)
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    waste_rect.move_ip(event.rel)

        screen.fill(WHITE)

        # Draw bins
        for bin_info in bins:
            pygame.draw.rect(screen, bin_info["color"], bin_info["rect"])
            draw_text(bin_info["name"], font, BLACK, screen, bin_info["rect"].x + 10, bin_info["rect"].y + 10)

        # Draw waste item
        pygame.draw.rect(screen, current_waste["color"], waste_rect)
        draw_text(current_waste["name"], font, BLACK, screen, waste_rect.x, waste_rect.y - 30)

        # Draw score
        draw_text(f"Score: {{score}}", font, BLACK, screen, 10, 10)

        pygame.display.flip()

if __name__ == "__main__":
    main()
"""
    return game_code
