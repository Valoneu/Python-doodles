import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# This sets the width and height of the square
WIDTH = 20
HEIGHT = 20

# Set the center of the square
center_x = WIDTH / 2
center_y = HEIGHT / 2

# Create a black square
square = pygame.Surface((WIDTH, HEIGHT))
square.fill(BLACK)

# Initialize pygame
pygame.init()

# Set the height and width of the screen
WINDOW_SIZE = [255, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Rotating Square")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Current angle of rotation
angle = 0
mouse_buttons = pygame.mouse.get_pressed()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
         # Get the state of the mouse buttons
          mouse_buttons = pygame.mouse.get_pressed()

    # Rotate the square if the left mouse button is pressed
        if mouse_buttons[0]:
          angle += 10

    # Set the screen background
    screen.fill(WHITE)

# Get the bounding rectangle of the square
    rect = square.get_rect()

# Set the center of rotation to the center of the square
    rect.center = (WIDTH/2, HEIGHT/2)

# Create a rotated copy of the square
    rotated_square = pygame.transform.rotate(square, angle)

    # Get the bounding rectangle of the rotated square
    rect = rotated_square.get_rect()

    # Center the rotated square on the screen
    rect.center = (center_x, center_y)

    # Draw the rotated square to the screen
    screen.blit(rotated_square, rect)

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
