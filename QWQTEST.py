import pygame
import math

pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Hexagon parameters
center = (400, 300)
hex_radius = 200
rotation_angle = 0
rotation_speed = 2  # degrees per frame

# Ball parameters
ball_radius = 20
ball_pos = [400.0, 300.0]
ball_vel = [5.0, 4.0]
gravity = 0.5  # New gravity constant

def closest_point_on_segment(a, b, p):
    ax, ay = a
    bx, by = b
    px, py = p

    abx = bx - ax
    aby = by - ay
    apx = px - ax
    apy = py - ay

    len_sq = abx**2 + aby**2
    t = (apx * abx + apy * aby) / len_sq if len_sq != 0 else 0
    t = max(0.0, min(1.0, t))

    return (ax + t * abx, ay + t * aby)

def get_rotated_hexagon(center, radius, angle):
    vertices = []
    for i in range(6):
        current_angle = math.radians(angle + i * 60)
        x = center[0] + radius * math.cos(current_angle)
        y = center[1] + radius * math.sin(current_angle)
        vertices.append((x, y))
    return vertices

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update rotation angle
    rotation_angle += rotation_speed
    if rotation_angle >= 360:
        rotation_angle -= 360

    # Get hexagon vertices
    hexagon = get_rotated_hexagon(center, hex_radius, rotation_angle)

    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Check collisions with each edge
    for i in range(len(hexagon)):
        a = hexagon[i]
        b = hexagon[(i + 1) % 6]

        closest = closest_point_on_segment(a, b, ball_pos)
        dx = ball_pos[0] - closest[0]
        dy = ball_pos[1] - closest[1]
        distance_sq = dx**2 + dy**2

        if distance_sq < ball_radius**2:
            # Calculate edge normal
            edge_v = (b[0] - a[0], b[1] - a[1])
            normal = (-edge_v[1], edge_v[0])
            length = math.hypot(*normal)
            if length == 0:
                continue
            normal = (normal[0]/length, normal[1]/length)

            # Verify normal direction points inward
            dir_to_center = (center[0] - closest[0], center[1] - closest[1])
            if (normal[0] * dir_to_center[0] + normal[1] * dir_to_center[1]) < 0:
                normal = (-normal[0], -normal[1])

            # Resolve collision
            penetration = ball_radius - math.sqrt(distance_sq)
            ball_pos[0] += normal[0] * penetration
            ball_pos[1] += normal[1] * penetration

            # Reflect velocity
            vel_dot = ball_vel[0] * normal[0] + ball_vel[1] * normal[1]
            ball_vel[0] = ball_vel[0] - 2 * vel_dot * normal[0]
            ball_vel[1] = ball_vel[1] - 2 * vel_dot * normal[1]

    # Apply gravity after collision resolution
    ball_vel[1] += gravity

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.polygon(screen, (255, 255, 255), hexagon, 2)
    pygame.draw.circle(screen, (255, 0, 0), (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()