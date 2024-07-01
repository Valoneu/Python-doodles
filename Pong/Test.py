import pygame
import random

# Initialize Pygame
pygame.init()

# Set the width and height of the screen [width, height]
size = (1920,1080)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Snake Game")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Snake position and size
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

# Food position
food_pos = [random.randrange(1, (size[0]//10)) * 10,
            random.randrange(1, (size[1]//10)) * 10]
food_spawn = True

# Snake movement direction
direction = 'RIGHT'
change_to = direction

# Snake speed
snake_speed = 30

# Frame rate
clock = pygame.time.Clock()

# Game over function
def gameOver():
    # Set the background color to black
    screen.fill(black)
    
    # Write game over message in white color
    font = pygame.font.SysFont('arial', 72)
    text = font.render('Game Over', True, white)
    screen.blit(text, [size[0] // 6, size[1] // 3])
    
    # Update the display
    pygame.display.flip()
    
    # Wait for 3 seconds and restart the game
    pygame.time.wait(3000)
    pygame.quit()
    quit()

# Main game loop
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
    
    # Update the direction
    direction = change_to

    # Update the snake position
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        food_spawn = False
    else:
        snake_body.pop()
    
    if not food_spawn:
        food_pos = [random.randrange(1, (size[0]//10)) * 10,
                    random.randrange(1, (size[1]//10)) * 10]
    food_spawn = True

    # Fill the screen with black color
    screen.fill(black)

    # Draw the snake and food
    for pos in snake_body:
        pygame.draw.rect(screen, white, [pos[0], pos[1], 10, 10])
    
    pygame.draw.rect(screen, red, [food_pos[0], food_pos[1], 10, 10])

    # Check for collisions with the borders
    if snake_pos[0] < 0 or snake_pos[0] > size[0] - 10 or snake_pos[1] < 0 or snake_pos[1] > size[1] - 10:
        gameOver()

    # Check for collisions with itself
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            gameOver()

    # Update the display
    pygame.display.flip()
    
    # Set the game speed
    clock.tick(snake_speed)

pygame.quit()