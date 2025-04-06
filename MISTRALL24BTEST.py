import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Hexagon parameters
hex_radius = 100
hex_center_x, hex_center_y = WIDTH // 2, HEIGHT // 2

def draw_rotated_hexagon(surface, center, radius, angle):
    vertices = []
    for i in range(6):
        x = radius * math.cos(math.radians(60 * i + angle))
        y = -radius * math.sin(math.radians(60 * i + angle))
        vertices.append((x + center[0], y + center[1]))
    pygame.draw.polygon(surface, WHITE, vertices)

def rotate_point(point, origin, angle):
    x, y = point
    ox, oy = origin
    sine, cosine = math.sin(angle), math.cos(angle)
    return (
        ox + (x - ox) * cosine - (y - oy) * sine,
        oy + (x - ox) * sine + (y - oy) * cosine
    )

# Ball parameters
ball_radius = 10
ball_pos_x, ball_pos_y = hex_center_x, hex_center_y
ball_vel_x, ball_vel_y = 5, 5

# Gravity and bounce logic
gravity = 0.1
bounce_factor = -0.8

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Update ball position with gravity
    ball_vel_y += gravity
    ball_pos_x += ball_vel_x
    ball_pos_y += ball_vel_y

    # Check for collisions with hexagon edges
    if abs(ball_pos_x - hex_center_x) > (hex_radius - ball_radius):
        ball_pos_x = min(max(ball_pos_x, 0), WIDTH)
        ball_vel_x *= bounce_factor

    if abs(ball_pos_y - hex_center_y) > (hex_radius * math.sqrt(3) / 2 - ball_radius):
        ball_pos_y = min(max(ball_pos_y, 0), HEIGHT)
        ball_vel_y *= bounce_factor

    # Draw rotating hexagon
    angle = pygame.time.get_ticks() / 50.0  # Rotate over time
    draw_rotated_hexagon(screen, (WIDTH // 2, HEIGHT // 2), hex_radius, angle)

    # Draw ball
    pygame.draw.circle(screen, WHITE, (int(ball_pos_x), int(ball_pos_y)), ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()