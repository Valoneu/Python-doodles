from abc import update_abstractmethods
from operator import ne
from re import U
import pygame
import math

pygame.init()
WIDTH, HEIGHT = 1000, 1000    
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

COLOR_BACKGROUND = (15, 15, 15)
COLOR_SUN = (255, 204, 0)
COLOR_MERCURY = (255, 204, 153)
COLOR_VENUS = (255, 153, 153)
COLOR_EARTH = (0, 102, 255)
COLOR_MARS = (255, 102, 0)
COLOR_JUPITER = (204, 153, 0)
COLOR_SATURN = (255, 255, 204)
COLOR_URANUS = (0, 153, 255)
COLOR_NEPTUNE = (102, 153, 255)

FONT = pygame.font.SysFont("JetBrains Mono", 26)

class Planet:
    AU = 149.6e6 * 1000 # AU in meters
    G = 6.67428e-11 # Gravitaion
    SCALE = 100 / AU # 1AU = 40 pixels
    TIMESTEP = 3600 * 24 # 1 day in seconds

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

                while len(updated_points) > 250:
                    del updated_points[0]
        
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000000000, 1)}GM", 1, (255,255,255))
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_width() / 2))

        pygame.draw.circle(win, self.color, (x, y), self.radius)
    
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()
    zoom = 1
    FITSIZE = 0.1

    sun = Planet(0, 0, 696 * zoom * FITSIZE / 4, COLOR_SUN, 1.98892 * 10**30)
    sun.sun = True

    mercury = Planet(-0.4 * Planet.AU * zoom, 0, 4 * zoom, COLOR_MERCURY, 0.33 * 10**24)
    mercury.y_vel = 47.4 * 1000
    venus = Planet(-0.7 * Planet.AU * zoom, 0, 9 * zoom, COLOR_VENUS, 4.87 * 10**24)
    venus.y_vel = 35 * 1000
    earth = Planet(-1 * Planet.AU * zoom, 0, 12 * zoom, COLOR_EARTH, 5.97 * 10**24)
    earth.y_vel = 29.8 * 1000
    mars = Planet(-1.5 * Planet.AU, 0, 6 * zoom, COLOR_MARS, 0.642 * 10**24)
    mars.y_vel = 24 * 1000
    jupiter = Planet(-5.2 * Planet.AU * zoom, 0, 140 * zoom * FITSIZE, COLOR_JUPITER, 1898 * 10**24)
    jupiter.y_vel = 13.1 * 1000
    saturn = Planet(-9.5 * Planet.AU * zoom, 0, 120 * zoom * FITSIZE, COLOR_SATURN, 568 * 10**24)
    saturn.y_vel = 9.7 * 1000
    uranus = Planet(-19.8 * Planet.AU * zoom, 0, 51 * zoom * FITSIZE, COLOR_URANUS, 86.8 * 10**24)
    uranus.y_vel = 6.8 * 1000
    neptune = Planet(-30 * Planet.AU * zoom, 0, 49 * zoom * FITSIZE, COLOR_NEPTUNE, 102 * 10**24)
    neptune.y_vel = 5.4 * 1000


    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        WIN.fill(COLOR_BACKGROUND)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        
        pygame.display.update()
    
    pygame.QUIT()

main()