import pygame
import random

# Initialize Pygame
pygame.init()

# --- Constants ---
# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# --- Game Variables ---
game_over = False
score = 0

# --- Classes ---

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 60])  # Placeholder, replace with an image
        self.image.fill(GREEN)  # Fill with green color
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0

    def update(self):
        # Movement
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5

        self.rect.x += self.speed_x

        # Keep ship within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30])  # Replace with asteroid image
        self.image.fill(RED)  # Fill with red color
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 4)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([5, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        # Remove bullet if it goes off screen
        if self.rect.bottom < 0:
            self.kill()

# --- Create Game Objects ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Spaceship()
all_sprites.add(player)

for i in range(50):  # Create some asteroids
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

# --- Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # --- Game Logic ---
    if not game_over:
        all_sprites.update()

        # Check for bullet-asteroid collisions
        hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for hit in hits:
            score += 10
            # Create new asteroid for each collision
            asteroid = Asteroid()
            all_sprites.add(asteroid)
            asteroids.add(asteroid)

        # Check for player-asteroid collisions
        hits = pygame.sprite.spritecollide(player, asteroids, False)
        if hits:
            game_over = True

    # --- Drawing ---
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Display score (add font rendering)
    # ... (Code to display score using a font)

    # Game over message
    if game_over:
        # ... (Code to display game over message)
        font = pygame.font.Font(None, 74)  # You can use a different font
        text = font.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)

    pygame.display.flip()  # Update the display
    clock.tick(75)  # Limit to 60 frames per second

pygame.quit()