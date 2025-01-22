import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()

# --- Global Variables ---

# Modifiable Screen Dimensions
SCREEN_SCALE_FACTOR = 1 # Adjust this for overall scaling (0.5, 0.75, 1.0, etc.)
BASE_WIDTH = 1920
BASE_HEIGHT = 1080
WIDTH = int(BASE_WIDTH * SCREEN_SCALE_FACTOR)
HEIGHT = int(BASE_HEIGHT * SCREEN_SCALE_FACTOR)

# Target FPS and timing
FPS = 300  # Target frames per second
dt = 1 / FPS  # Delta time (time per frame) used for calculations

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# --- Game Constants ---

# Paddle constants
PADDLE_WIDTH = WIDTH / 80  # Adjust divisor for paddle width relative to screen width
INITIAL_PADDLE_HEIGHT = HEIGHT / 5 # Adjust divisor for initial paddle height relative to screen height
PADDLE_HEIGHT_LIMIT = 0.25  # Minimum paddle height (25% of initial height)
PADDLE_SPEED = HEIGHT * 1.66 * dt # Initial paddle speed. Adjust multiplier as needed
PADDLE_SPEED_CAP = PADDLE_SPEED * 4  # Maximum paddle speed after ramp-up (4 times the initial speed)

# Ball constants
BALL_RADIUS = WIDTH / 120  # Adjust divisor for ball radius relative to screen width
BALL_SPEED_X = WIDTH * 1 * dt  # Initial horizontal ball speed. Adjust multiplier as needed
BALL_SPEED_Y = HEIGHT * 1 * dt # Initial vertical ball speed. Adjust multiplier as needed
MAXBALLMULT = 3 # Maximum ball speed multiplier

# Maximum deflection angle
MAX_DEFLECTION = 0.66  # (Approximately 30 degrees)

# Font setup for score display
font = pygame.font.Font(None, int(WIDTH / 40))

# --- Functions ---

def calculate_speed(base_speed):
    """Calculates speed based on delta time to maintain consistency across frame rates."""
    return base_speed * dt

# --- Classes ---

class Paddle:
    def __init__(self, x, is_ai=False):
        self.width = PADDLE_WIDTH
        self.height = INITIAL_PADDLE_HEIGHT
        self.x = x
        self.y = HEIGHT // 2 - self.height // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_ai = is_ai
        self.speed = PADDLE_SPEED

    def move(self, dy):
        # Apply speed cap
        dy = max(-self.speed, min(dy, self.speed))
        self.y += dy
        # Keep paddle within screen bounds
        self.y = max(0, min(self.y, HEIGHT - self.height))
        self.rect.y = self.y

    def ai_move(self, ball):
        # More intelligent AI: Consider paddle height for better positioning
        target_y = ball.y - self.height / 2
        target_y += random.uniform(-self.height / 4, self.height / 4)

        if abs(target_y - self.y) > self.speed:
            if target_y < self.y:
                self.move(-self.speed)
            else:
                self.move(self.speed)
        else:
            self.move(target_y - self.y)

    def update_size(self):
        # Limit paddle size reduction
        self.height = max(self.height, INITIAL_PADDLE_HEIGHT * PADDLE_HEIGHT_LIMIT)
        self.rect.height = self.height
        # Keep the paddle centered when it shrinks
        self.rect.y = self.y

class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS
        self.num_hits = 0
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.num_hits = 0
        # Random initial direction
        self.speed_x = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
        self.speed_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

    def deflect(self, paddle):
        speed = math.fabs(self.speed_x) * math.fabs(self.speed_y)
        maxballspeed = BALL_SPEED_X * BALL_SPEED_Y * MAXBALLMULT
        # Calculate the relative position of the ball to the paddle's center
        relative_y = (self.y - (paddle.y + paddle.height / 2)) / (paddle.height / 2)
        relative_y = max(-1, min(1, relative_y))

        # Calculate the deflection angle based on the relative position
        deflection_angle = relative_y * MAX_DEFLECTION

        # Reverse the ball's x-direction and increase speed (with a cap)
        if speed >= maxballspeed:
            self.speed_x *= -1
        else:
            self.speed_x *= -1.05 # -self.speed_x * ((20 + self.num_hits) / 20)

        # Adjust the ball's y-speed based on the deflection angle
        self.speed_y += deflection_angle

        # Prevent sticking
        if self.speed_x > 0:
            self.x = paddle.rect.right + self.radius
        else:
            self.x = paddle.rect.left - self.radius

        self.num_hits += 1

        # Increase paddle speed and decrease size after a hit (with caps)
        paddle.speed = min(paddle.speed * 1.1, PADDLE_SPEED_CAP)
        paddle.height *= 0.95
        paddle.update_size()

# --- Initialize Game ---

# Create screen with vsync
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Pong Game")

# Clock to control frame rate
clock = pygame.time.Clock()

# Create paddles and ball
paddle_left = Paddle(0)
paddle_right = Paddle(WIDTH - PADDLE_WIDTH)
ball = Ball()

# Score tracking
score_left = 0
score_right = 0

# AI state (True = AI on, False = AI off)
left_ai = True
right_ai = True

# --- Game Loop ---

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                left_ai = not left_ai  # Toggle left AI
                paddle_left.is_ai = left_ai
            if event.key == pygame.K_p:
                right_ai = not right_ai  # Toggle right AI
                paddle_right.is_ai = right_ai

    # --- Paddle Movement ---
    keys = pygame.key.get_pressed()

    if not left_ai:
        # Left paddle controls (W/S)
        if keys[pygame.K_w]:
            paddle_left.move(-PADDLE_SPEED)
        if keys[pygame.K_s]:
            paddle_left.move(PADDLE_SPEED)
    else:
        paddle_left.ai_move(ball)  # Control left paddle with AI

    if not right_ai:
        # Right paddle controls (Up/Down arrows)
        if keys[pygame.K_UP]:
            paddle_right.move(-PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            paddle_right.move(PADDLE_SPEED)
    else:
        paddle_right.ai_move(ball)  # Control right paddle with AI

    # --- Ball Movement ---
    ball.move()

    # --- Collision with Top and Bottom Walls ---
    if ball.y + ball.radius > HEIGHT or ball.y - ball.radius < 0:
        ball.speed_y *= -1

    # --- Enhanced Collision Detection with Paddles ---
    # Predict the ball's next position
    next_ball_rect = pygame.Rect(
        int(ball.x + ball.speed_x - ball.radius),
        int(ball.y + ball.speed_y - ball.radius),
        2 * ball.radius,
        2 * ball.radius,
    )

    # Check for collision with the paddles at the next position
    if next_ball_rect.colliderect(paddle_right.rect):
        ball.deflect(paddle_right)
    elif next_ball_rect.colliderect(paddle_left.rect):
        ball.deflect(paddle_left)

    # --- Check for Scoring ---
    if ball.x - ball.radius < 0:
        score_right += 1
        ball.reset()
        # Reset paddle size and speed after scoring
        paddle_left.height = INITIAL_PADDLE_HEIGHT
        paddle_left.speed = PADDLE_SPEED
        paddle_left.update_size()
        paddle_right.height = INITIAL_PADDLE_HEIGHT
        paddle_right.speed = PADDLE_SPEED
        paddle_right.update_size()
        time.sleep(0.5)  # Short pause before restart

    elif ball.x + ball.radius > WIDTH:
        score_left += 1
        ball.reset()
        # Reset paddle size and speed after scoring
        paddle_left.height = INITIAL_PADDLE_HEIGHT
        paddle_left.speed = PADDLE_SPEED
        paddle_left.update_size()
        paddle_right.height = INITIAL_PADDLE_HEIGHT
        paddle_right.speed = PADDLE_SPEED
        paddle_right.update_size()
        time.sleep(0.5)

    # --- Clear Screen ---
    screen.fill(BLACK)

    # --- Draw Paddles, Ball, and Scores ---
    pygame.draw.rect(screen, WHITE, paddle_left.rect)
    pygame.draw.rect(screen, WHITE, paddle_right.rect)
    ball.draw()

    # Display scores
    score_display = font.render(f"{score_left} - {score_right}", True, WHITE)
    screen.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, 10))

    # Display AI status
    left_ai_text = "AI" if left_ai else "Manual"
    right_ai_text = "AI" if right_ai else "Manual"
    left_ai_display = font.render(f"Left: {left_ai_text}", True, WHITE)
    right_ai_display = font.render(f"Right: {right_ai_text}", True, WHITE)
    screen.blit(left_ai_display, (10, 10))
    screen.blit(right_ai_display, (WIDTH - right_ai_display.get_width() - 10, 10))

    # --- Update Display ---
    pygame.display.flip()

    # --- Control Frame Rate ---
    clock.tick(FPS)

# --- Quit Game ---
pygame.quit()