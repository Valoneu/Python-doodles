import pygame
import math
import sys

pygame.init()
WIDTH, HEIGHT = 960, 540
AREA = WIDTH * HEIGHT
DELTASIZE = AREA / 518400
WIN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 0, 0, 1 )
pygame.display.set_caption("Pong")

COLOR_BACKGROUND = (33, 29, 38)

FONT = pygame.font.SysFont("Seeds", 20)
clock = pygame.time.Clock()

score1 = 0
score2 = 0

player_pos = pygame.Vector2(WIN.get_width() / 50, WIN.get_height() / 2)
player_pos2 = pygame.Vector2(WIN.get_width() - (WIN.get_width() / 50), WIN.get_height() / 2)
ball_pos = pygame.Vector2(WIN.get_width() / 2, WIN.get_height() / 2)

player_width = AREA / 100000
player_height = AREA / 12500
ball_size = AREA / 75000

#pygame.mouse.set_visible(False)

def main():

    while True:
        deltaTime = clock.tick(75) / 1000
        WIN.fill(COLOR_BACKGROUND)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        pygame.draw.rect(WIN, "black", (WIDTH / 2 - AREA / 200000, 0, AREA / 100000, HEIGHT))
        pygame.draw.rect(WIN, "white", (0, 0, AREA / 50000, HEIGHT))
        pygame.draw.rect(WIN, "white", (WIDTH - AREA / 50000, 0, AREA / 50000, HEIGHT))
           
        pygame.draw.rect(WIN, "green", (player_pos.x, player_pos.y - player_height / 2, AREA / 100000, AREA / 12500))
        pygame.draw.rect(WIN, "red", (player_pos2.x, player_pos2.y - player_height / 2, AREA / 100000, AREA / 12500))
        pygame.draw.circle(WIN, "gray", (ball_pos.x, ball_pos.y), ball_size)
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            if (player_pos.y > 0 + ((AREA / 12500)) / 2):
                player_pos.y -= 200 * deltaTime * DELTASIZE
        if keys[pygame.K_s]:
            if (player_pos.y < HEIGHT - ((AREA / 12500)) / 2):
                player_pos.y += 200 * deltaTime * DELTASIZE

        pygame.display.update()
    
main()