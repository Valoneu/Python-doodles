import pygame
import sys
import math
from pygame.locals import *

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Rotating Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Ball properties
ball_radius = 15
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [0, 0]
gravity = 1
elasticity = 1  # Ball bounces back with 80% of its velocity

# Hexagon properties
hex_radius = 300
hex_rotation = 0
rotation_speed = 0.01

# Calculate hexagon vertices (6 points)
def get_hexagon_vertices(center_x, center_y, radius, rotation):
    vertices = []
    for i in range(6):
        angle = rotation + (math.pi / 3) * i  # 60 degrees = pi/3 radians
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        vertices.append((x, y))
    return vertices

# Check if point is inside a polygon
def point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside

# Find closest edge to a point
def closest_edge(point, polygon):
    x, y = point
    n = len(polygon)
    min_dist = float('inf')
    closest_line = None
    normal = None
    
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        
        # Line segment vector
        line_vec = (p2[0] - p1[0], p2[1] - p1[1])
        line_len = math.sqrt(line_vec[0]**2 + line_vec[1]**2)
        
        # Normalize
        if line_len > 0:
            norm_line = (line_vec[0] / line_len, line_vec[1] / line_len)
        else:
            continue
        
        # Vector from p1 to point
        point_vec = (x - p1[0], y - p1[1])
        
        # Project point_vec onto norm_line
        projection = (point_vec[0] * norm_line[0] + point_vec[1] * norm_line[1])
        projection = max(0, min(line_len, projection))
        
        # Find closest point on line
        closest_point = (
            p1[0] + norm_line[0] * projection,
            p1[1] + norm_line[1] * projection
        )
        
        # Calculate distance
        dist = math.sqrt((x - closest_point[0])**2 + (y - closest_point[1])**2)
        
        if dist < min_dist:
            min_dist = dist
            closest_line = (p1, p2)
            # Find normal vector (perpendicular to line)
            normal = (-norm_line[1], norm_line[0])
    
    return min_dist, closest_line, normal

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    # Clear the screen
    screen.fill(BLACK)
    
    # Update hexagon rotation
    hex_rotation += rotation_speed
    hexagon = get_hexagon_vertices(WIDTH // 2, HEIGHT // 2, hex_radius, hex_rotation)
    
    # Draw hexagon
    pygame.draw.polygon(screen, BLUE, hexagon, 2)
    
    # Apply gravity
    ball_vel[1] += gravity
    
    # Update ball position
    new_pos = [ball_pos[0] + ball_vel[0], ball_pos[1] + ball_vel[1]]
    
    # Check for collision with hexagon
    if not point_in_polygon(new_pos, hexagon):
        dist, line, normal = closest_edge(ball_pos, hexagon)
        
        if dist <= ball_radius:
            # Calculate reflection
            dot_product = ball_vel[0] * normal[0] + ball_vel[1] * normal[1]
            ball_vel[0] = ball_vel[0] - 2 * dot_product * normal[0]
            ball_vel[1] = ball_vel[1] - 2 * dot_product * normal[1]
            
            # Apply elasticity
            ball_vel[0] *= elasticity
            ball_vel[1] *= elasticity
    
    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # Keep ball inside the hexagon
    if not point_in_polygon(ball_pos, hexagon):
        # If somehow the ball gets outside, adjust its position
        dist, _, normal = closest_edge(ball_pos, hexagon)
        adjustment = ball_radius - dist
        if adjustment > 0:
            ball_pos[0] += normal[0] * adjustment
            ball_pos[1] += normal[1] * adjustment
    
    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(75)

# Quit pygame
pygame.quit()
sys.exit()