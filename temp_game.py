import pygame
import math
import random

# Initialize Pygame
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
BLUE = (60, 120, 220)
RED = (200, 30, 30)
PALE_YELLOW = (255, 255, 224)
PALE_BLUE = (173, 216, 230)
DEEP_BLUE = (0, 0, 139)
BROWN = (139, 69, 19)
INFO_BOX_COLOR = (20, 20, 60)
INFO_BORDER_COLOR = (150, 150, 255)

# Game settings
ROCKET_SPEED = 4
FPS = 60

# --- Setup Screen and Clock ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Planet Surface Explorer")
clock = pygame.time.Clock()

# --- Fonts ---
try:
    FONT_SMALL = pygame.font.SysFont('Arial', 16)
    FONT_MEDIUM = pygame.font.SysFont('Arial', 24)
    FONT_LARGE = pygame.font.SysFont('Arial', 48)
except pygame.error:
    FONT_SMALL = pygame.font.Font(None, 20)
    FONT_MEDIUM = pygame.font.Font(None, 30)
    FONT_LARGE = pygame.font.Font(None, 54)


# --- Helper Functions ---
def draw_text(text, font, color, surface, x, y, center=False):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    return lines

# --- Game Classes ---
class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40), pygame.SRCALPHA)
        # Draw a simple rocket shape
        pygame.draw.polygon(self.image, WHITE, [(15, 0), (0, 40), (30, 40)]) # Main body
        pygame.draw.polygon(self.image, RED, [(15, 25), (5, 40), (25, 40)]) # Flame
        self.rect = self.image.get_rect(center=(50, SCREEN_HEIGHT // 2))
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        keys = pygame.key.get_pressed()
        self.speed_x = 0
        self.speed_y = 0

        if keys[pygame.K_LEFT]:
            self.speed_x = -ROCKET_SPEED
        if keys[pygame.K_RIGHT]:
            self.speed_x = ROCKET_SPEED
        if keys[pygame.K_UP]:
            self.speed_y = -ROCKET_SPEED
        if keys[pygame.K_DOWN]:
            self.speed_y = ROCKET_SPEED
            
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Keep rocket on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Planet(pygame.sprite.Sprite):
    def __init__(self, name, color, radius, orbit_radius, orbit_speed, description):
        super().__init__()
        self.name = name
        self.color = color
        self.radius = radius
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.description = description
        
        self.angle = random.uniform(0, 2 * math.pi)
        self.image = pygame.Surface((self.radius * 2 + 10, self.radius * 2 + 10), pygame.SRCALPHA)
        self.image_center = (self.image.get_width() // 2, self.image.get_height() // 2)
        
        pygame.draw.circle(self.image, self.color, self.image_center, self.radius)
        
        if self.name == "Saturn":
            pygame.draw.ellipse(self.image, PALE_YELLOW, (0, self.image_center[1] - 5, self.image.get_width(), 10), 2)

        self.rect = self.image.get_rect()
        self.visited = False
        self.update()

    def update(self):
        self.angle += self.orbit_speed
        self.rect.centerx = int(CENTER_X + self.orbit_radius * math.cos(self.angle))
        self.rect.centery = int(CENTER_Y + self.orbit_radius * math.sin(self.angle))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.circle(surface, (50, 50, 50), (CENTER_X, CENTER_Y), self.orbit_radius, 1)
        if not self.visited:
            draw_text(self.name, FONT_SMALL, WHITE, surface, self.rect.centerx, self.rect.bottom + 5, center=True)

# --- Game State Setup ---
def game_setup():
    rocket = Rocket()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(rocket)
    
    planets_data = [
        {"name": "Mercury", "color": GRAY, "radius": 8, "orbit": 60, "speed": 0.01, "desc": "Mercury's surface is rocky and covered with craters, much like our Moon. It has no atmosphere to protect it from impacts."},
        {"name": "Venus", "color": (230, 200, 100), "radius": 12, "orbit": 90, "speed": 0.008, "desc": "Venus has a solid surface of volcanic rock. It's hidden by a thick, toxic atmosphere, making it the hottest planet."},
        {"name": "Earth", "color": BLUE, "radius": 13, "orbit": 130, "speed": 0.006, "desc": "Our home! Earth's surface is unique, with liquid water oceans, solid land continents, and ice caps. It's teeming with life."},
        {"name": "Mars", "color": RED, "radius": 10, "orbit": 170, "speed": 0.005, "desc": "The 'Red Planet'. Mars has a cold, dusty, rocky surface. It features giant volcanoes, deep canyons, and polar ice caps."},
        {"name": "Jupiter", "color": (210, 180, 140), "radius": 25, "orbit": 230, "speed": 0.003, "desc": "Jupiter is a gas giant with no solid surface to stand on! Its 'surface' is a swirling layer of colorful clouds and storms."},
        {"name": "Saturn", "color": PALE_YELLOW, "radius": 22, "orbit": 290, "speed": 0.002, "desc": "Like Jupiter, Saturn is a gas giant with no solid surface. It's famous for its beautiful rings made of ice and rock particles."},
        {"name": "Uranus", "color": PALE_BLUE, "radius": 18, "orbit": 340, "speed": 0.0015, "desc": "Uranus is an ice giant. It doesn't have a true solid surface, but a hot, dense interior of 'icy' materials like water and methane."},
        {"name": "Neptune", "color": DEEP_BLUE, "radius": 17, "orbit": 390, "speed": 0.001, "desc": "Neptune is a dark, cold ice giant. It has no solid surface and is the windiest planet, with supersonic storms."},
        {"name": "Pluto", "color": BROWN, "radius": 6, "orbit": 440, "speed": 0.0008, "desc": "This dwarf planet has a solid, icy surface with vast plains, towering mountains of water ice, and a thin atmosphere."}
    ]

    planets = pygame.sprite.Group()
    for p_data in planets_data:
        planet = Planet(p_data["name"], p_data["color"], p_data["radius"], p_data["orbit"], p_data["speed"], p_data["desc"])
        planets.add(planet)
    
    stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(200)]
    
    return rocket, all_sprites, planets, stars

# --- Main Game Loop ---
def main():
    rocket, all_sprites, planets, stars = game_setup()
    
    visited_planets_count = 0
    game_over = False
    running = True
    show_info = False
    info_text_lines = []
    info_planet_name = ""
    
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if show_info:
                    show_info = False # Close info box on any key press
                if game_over and event.key == pygame.K_r:
                    main() # Restart the game
                    return
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --- Game Logic ---
        if not show_info and not game_over:
            rocket.update()
            planets.update()

            # Collision detection
            collided_planets = pygame.sprite.spritecollide(rocket, planets, False, pygame.sprite.collide_circle)
            for planet in collided_planets:
                if not planet.visited:
                    planet.visited = True
                    visited_planets_count += 1
                    show_info = True
                    info_planet_name = planet.name
                    info_text_lines = wrap_text(planet.description, FONT_MEDIUM, SCREEN_WIDTH - 150)
                    
            if visited_planets_count >= len(planets):
                game_over = True

        # --- Drawing ---
        screen.fill(BLACK)
        for star in stars:
            pygame.draw.circle(screen, WHITE, star, 1)

        pygame.draw.circle(screen, YELLOW, (CENTER_X, CENTER_Y), 30)
        
        planets.draw(screen)
        for p in planets:
            p.draw(screen)
        screen.blit(rocket.image, rocket.rect)

        # UI
        draw_text("Planet Surface Explorer", FONT_MEDIUM, WHITE, screen, 20, 10)
        draw_text("Use Arrow Keys to fly. Visit all planets!", FONT_SMALL, WHITE, screen, 20, 40)
        draw_text(f"Planets Visited: {visited_planets_count} / {len(planets)}", FONT_MEDIUM, WHITE, screen, SCREEN_WIDTH - 250, 10)

        # Info Box Display
        if show_info:
            box_rect = pygame.Rect(50, 150, SCREEN_WIDTH - 100, 300)
            pygame.draw.rect(screen, INFO_BOX_COLOR, box_rect, border_radius=15)
            pygame.draw.rect(screen, INFO_BORDER_COLOR, box_rect, 3, border_radius=15)
            
            draw_text(info_planet_name, FONT_LARGE, YELLOW, screen, SCREEN_WIDTH / 2, 190, center=True)
            
            line_y = 250
            for line in info_text_lines:
                draw_text(line, FONT_MEDIUM, WHITE, screen, SCREEN_WIDTH / 2, line_y, center=True)
                line_y += 35
            
            draw_text("Press any key to continue exploring...", FONT_SMALL, WHITE, screen, SCREEN_WIDTH / 2, 420, center=True)

        # Game Over Screen
        if game_over:
            draw_text("Congratulations!", FONT_LARGE, YELLOW, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50, center=True)
            draw_text("You have learned about all the planets!", FONT_MEDIUM, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10, center=True)
            draw_text("Press 'R' to play again or ESC to quit.", FONT_MEDIUM, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50, center=True)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()