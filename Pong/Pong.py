import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 960
HEIGHT = 540
WINDOW_SIZE = (WIDTH, HEIGHT)
FPS = 75
# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the paddle properties
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
PADDLE_SPEED = 5

# Set up the ball properties
BALL_RADIUS = 10
BALL_SPEED_X = 3
BALL_SPEED_Y = 3

# Create the game window
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Create the paddles
paddle1 = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create the ball
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS, BALL_RADIUS)
ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y

# Create the score variables
score1 = 0
score2 = 0
font = pygame.font.SysFont("Seeds", 50)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_w] and paddle1.y > 0:
        paddle1.y -= PADDLE_SPEED * deltaTime
    if keys[K_s] and paddle1.y < HEIGHT - PADDLE_HEIGHT:
        paddle1.y += PADDLE_SPEED * deltaTime
    if keys[K_UP] and paddle2.y > 0:
        paddle2.y -= PADDLE_SPEED * deltaTime
    if keys[K_DOWN] and paddle2.y < HEIGHT - PADDLE_HEIGHT:
        paddle2.y += PADDLE_SPEED * deltaTime
    
    deltaTime = clock.get_fps() / 20000
    # Move the ball
    ball.x += ball_speed_x * deltaTime
    ball.y += ball_speed_y * deltaTime

    # Ball collision with paddles
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_speed_x *= -1

    # Ball collision with walls
    if ball.y < 0 or ball.y > HEIGHT - BALL_RADIUS:
        ball_speed_y *= -1

    # Scoring
    if ball.x < 0:
        score2 += 1
        ball_speed_x = BALL_SPEED_X
        ball_speed_y = BALL_SPEED_Y
        ball.x = WIDTH // 2 - BALL_RADIUS // 2
        ball.y = HEIGHT // 2 - BALL_RADIUS // 2
    elif ball.x > WIDTH - BALL_RADIUS:
        score1 += 1
        ball_speed_x = -BALL_SPEED_X
        ball_speed_y = -BALL_SPEED_Y
        ball.x = WIDTH // 2 - BALL_RADIUS // 2
        ball.y = HEIGHT // 2 - BALL_RADIUS // 2

    # Clear the window
    window.fill(BLACK)

    # Draw the paddles, ball, and scores
    pygame.draw.rect(window, WHITE, paddle1)
    pygame.draw.rect(window, WHITE, paddle2)
    pygame.draw.ellipse(window, WHITE, ball)
    score_text = font.render(str(score1) + " - " + str(score2), True, WHITE)
    window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick()

# Quit the game
pygame.quit()