import pygame
import math
import sys
import collections

# --- SETUP & INITIALIZATION ---
pygame.init()

WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Planet Simulation")

# --- COLORS & FONT ---
COLOR_BACKGROUND = (15, 15, 15)
COLOR_SUN = (255, 204, 0)
COLOR_TEXT = (255, 255, 255)
COLOR_UI_BG = (40, 40, 40)
COLOR_UI_BG_HOVER = (70, 70, 70)

# Use a standard system font like Consolas. Pygame handles fallbacks.
FONT = pygame.font.SysFont("Consolas", 18)
FONT_UI = pygame.font.SysFont("Consolas", 16)
FONT_FPS = pygame.font.SysFont("Consolas", 20)

# --- SIMULATION CONSTANTS ---
G = 6.67428e-11
AU = 149.6e6 * 1000
BASE_TIMESTEP = 3600 * 24
INITIAL_SCALE = 60 / AU
FOCUS_SCALE = INITIAL_SCALE * 30
LERP_FACTOR = 0.05

# --- PLANET DATA ---
PLANET_DATA = [
    {"name": "Mercury", "color": (255, 204, 153), "mass": 0.33e24, "radius": 2439, "dist_au": 0.4, "y_vel": 47.4},
    {"name": "Venus", "color": (255, 153, 153), "mass": 4.87e24, "radius": 6051, "dist_au": 0.7, "y_vel": 35.0},
    {"name": "Earth", "color": (0, 102, 255), "mass": 5.97e24, "radius": 6371, "dist_au": 1.0, "y_vel": 29.8},
    {"name": "Mars", "color": (255, 102, 0), "mass": 0.642e24, "radius": 3389, "dist_au": 1.5, "y_vel": 24.0},
    {"name": "Jupiter", "color": (204, 153, 0), "mass": 1898e24, "radius": 69911, "dist_au": 5.2, "y_vel": 13.1},
    {"name": "Saturn", "color": (255, 255, 204), "mass": 568e24, "radius": 58232, "dist_au": 9.5, "y_vel": 9.7},
    {"name": "Uranus", "color": (0, 153, 255), "mass": 86.8e24, "radius": 25362, "dist_au": 19.8, "y_vel": 6.8},
    {"name": "Neptune", "color": (102, 153, 255), "mass": 102e24, "radius": 24622, "dist_au": 30.0, "y_vel": 5.4},
]

# --- HELPER FUNCTION ---
def dim_color(color, factor=0.4):
    return tuple(max(0, int(c * factor)) for c in color)

class Planet:
    def __init__(self, x, y, radius, color, mass, name, y_vel=0):
        self.x = x
        self.y = y
        self.radius_real = radius * 1000
        self.color = color
        self.dimmed_color = dim_color(color)
        self.mass = mass
        self.name = name

        self.orbit_trail = collections.deque(maxlen=400)
        self.full_orbit = []

        self.is_sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = y_vel
        self.ax = self.ay = 0

    def draw(self, win, scale, camera_x, camera_y, show_info):
        screen_x = (self.x - camera_x) * scale + WIDTH / 2
        screen_y = (self.y - camera_y) * scale + HEIGHT / 2
        planet_radius_scaled = max(self.radius_real * scale, 2)

        if len(self.full_orbit) > 2:
            orbit_points = [
                ((p[0] - camera_x) * scale + WIDTH / 2, (p[1] - camera_y) * scale + HEIGHT / 2)
                for p in self.full_orbit
            ]
            pygame.draw.lines(win, self.dimmed_color, False, orbit_points, 1)

        if len(self.orbit_trail) > 2:
            trail_points = [
                ((p[0] - camera_x) * scale + WIDTH / 2, (p[1] - camera_y) * scale + HEIGHT / 2)
                for p in self.orbit_trail
            ]
            pygame.draw.lines(win, self.color, False, trail_points, 2)
        
        pygame.draw.circle(win, self.color, (screen_x, screen_y), planet_radius_scaled)

        if not self.is_sun and show_info:
            name_text = FONT.render(self.name, 1, COLOR_TEXT)
            dist_text = FONT.render(f"{self.distance_to_sun / AU:.2f} AU", 1, COLOR_TEXT)
            name_pos_y = screen_y - planet_radius_scaled - name_text.get_height() - 5
            dist_pos_y = screen_y + planet_radius_scaled + 5
            win.blit(name_text, (screen_x - name_text.get_width() / 2, name_pos_y))
            win.blit(dist_text, (screen_x - dist_text.get_width() / 2, dist_pos_y))

    def calculate_forces(self, planets):
        total_fx = total_fy = 0
        for other in planets:
            if self == other: continue
            dx, dy = other.x - self.x, other.y - self.y
            dist = math.sqrt(dx**2 + dy**2)
            if other.is_sun: self.distance_to_sun = dist
            force = G * self.mass * other.mass / dist**2
            theta = math.atan2(dy, dx)
            total_fx += math.cos(theta) * force
            total_fy += math.sin(theta) * force
        self.ax, self.ay = total_fx / self.mass, total_fy / self.mass

    def update_position_verlet(self, timestep, frame_count):
        self.x += self.x_vel * timestep + 0.5 * self.ax * timestep**2
        self.y += self.y_vel * timestep + 0.5 * self.ay * timestep**2
        self.orbit_trail.append((self.x, self.y))
        
        if frame_count % 15 == 0:
            self.full_orbit.append((self.x, self.y))

class UI:
    def __init__(self, planets):
        self.buttons = []
        self.panel_width = 200
        self.panel_x = WIDTH - self.panel_width - 10
        y_offset = 10
        for planet in planets:
            if planet.is_sun: continue
            rect = pygame.Rect(self.panel_x, y_offset, self.panel_width, 30)
            self.buttons.append({"rect": rect, "planet": planet, "text": planet.name})
            y_offset += 35

    def draw(self, win):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            bg_color = COLOR_UI_BG_HOVER if button["rect"].collidepoint(mouse_pos) else COLOR_UI_BG
            pygame.draw.rect(win, bg_color, button["rect"], border_radius=5)
            text_surf = FONT_UI.render(button["text"], 1, COLOR_TEXT)
            text_rect = text_surf.get_rect(center=button["rect"].center)
            win.blit(text_surf, text_rect)

    def handle_click(self, pos):
        for button in self.buttons:
            if button["rect"].collidepoint(pos):
                return button["planet"]
        return None

def main():
    run = True
    clock = pygame.time.Clock()
    frame_count = 0

    scale = INITIAL_SCALE
    time_multiplier = 1.0
    show_info = True
    camera_x, camera_y = 0, 0
    camera_target = None
    CAMERA_SPEED = 20

    sun = Planet(0, 0, 696340, COLOR_SUN, 1.98892 * 10**30, "Sun")
    sun.is_sun = True
    planets = [sun]
    for data in PLANET_DATA:
        planets.append(Planet(x=-data["dist_au"] * AU, y=0, radius=data["radius"], color=data["color"],
                              mass=data["mass"], name=data["name"], y_vel=data["y_vel"] * 1000))

    ui = UI(planets)

    for planet in planets:
        if planet.is_sun: continue
        planet.calculate_forces(planets)

    while run:
        clock.tick(150)
        timestep = BASE_TIMESTEP * time_multiplier
        frame_count += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_planet = ui.handle_click(event.pos)
                    if clicked_planet: camera_target = clicked_planet
            if event.type == pygame.KEYDOWN:
                user_interrupted = True
                if event.key == pygame.K_ESCAPE: run = False
                elif event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS: scale *= 1.5
                elif event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS: scale /= 1.5
                elif event.key == pygame.K_UP: time_multiplier *= 1.5
                elif event.key == pygame.K_DOWN: time_multiplier = max(0.1, time_multiplier / 1.5)
                elif event.key == pygame.K_i: show_info = not show_info
                elif event.key == pygame.K_r: camera_x, camera_y, scale = 0, 0, INITIAL_SCALE
                else: user_interrupted = False
                if user_interrupted: camera_target = None

        keys = pygame.key.get_pressed()
        camera_move_amount = CAMERA_SPEED / scale
        user_moved = False
        if keys[pygame.K_w]: camera_y -= camera_move_amount; user_moved = True
        if keys[pygame.K_s]: camera_y += camera_move_amount; user_moved = True
        if keys[pygame.K_a]: camera_x -= camera_move_amount; user_moved = True
        if keys[pygame.K_d]: camera_x += camera_move_amount; user_moved = True
        if user_moved: camera_target = None

        if camera_target:
            target_x, target_y = camera_target.x, camera_target.y
            target_scale = FOCUS_SCALE
            camera_x += (target_x - camera_x) * LERP_FACTOR
            camera_y += (target_y - camera_y) * LERP_FACTOR
            scale += (target_scale - scale) * LERP_FACTOR
            if abs(camera_x - target_x) < 1e6 and abs(scale - target_scale) < 1e-12:
                camera_target = None

        old_accelerations = {}
        for planet in planets:
            if planet.is_sun: continue
            old_accelerations[planet.name] = (planet.ax, planet.ay)
            planet.update_position_verlet(timestep, frame_count)
        
        for planet in planets:
            if planet.is_sun: continue
            planet.calculate_forces(planets)

        for planet in planets:
            if planet.is_sun: continue
            old_ax, old_ay = old_accelerations[planet.name]
            planet.x_vel += 0.5 * (old_ax + planet.ax) * timestep
            planet.y_vel += 0.5 * (old_ay + planet.ay) * timestep

        WIN.fill(COLOR_BACKGROUND)
        for planet in planets:
            planet.draw(WIN, scale, camera_x, camera_y, show_info)
        ui.draw(WIN)

        info_text_y = 10
        controls_text = [
            f"Zoom: {scale/INITIAL_SCALE:.1f}x  | +/- to change",
            f"Time: {time_multiplier:.1f}x | UP/DOWN to change",
            f"Info: {'ON' if show_info else 'OFF'} | Press 'I' to toggle",
            f"Move: WASD | Reset: R | Focus: Click list"
        ]
        for line in controls_text:
            text_surf = FONT.render(line, 1, COLOR_TEXT)
            WIN.blit(text_surf, (10, info_text_y))
            info_text_y += text_surf.get_height() + 4
            
        # --- FPS COUNTER DRAWING ---
        fps_text = FONT_FPS.render(f"FPS: {int(clock.get_fps())}", 1, COLOR_TEXT)
        WIN.blit(fps_text, (WIDTH - fps_text.get_width() - 10, HEIGHT - fps_text.get_height() - 10))

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()