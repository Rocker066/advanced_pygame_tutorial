import pygame
import pygame.math as math

# Initialize Pygame
pygame.init()

# Create vectors for position, velocity, and acceleration
position = math.Vector2(100, 100)  # Starting position
velocity = math.Vector2(0, 0)       # Initial velocity
acceleration = math.Vector2(0, 0)   # Initial acceleration

screen = pygame.display.set_mode((500, 500))

keys = pygame.key.get_pressed()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if keys[pygame.K_LEFT]:
        acceleration.x = -1  # Move left
    elif keys[pygame.K_RIGHT]:
        acceleration.x = 1  # Move right
    else:
        acceleration.x = 0  # No horizontal movement

    if keys[pygame.K_UP]:
        acceleration.y = -1  # Move up
    elif keys[pygame.K_DOWN]:
        acceleration.y = 1  # Move down
    else:
        acceleration.y = 0  # No vertical movement

    # Example: Apply constant acceleration (e.g., gravity)
    acceleration.y = 0.5  # Simulating gravity

    # Update velocity based on acceleration
    velocity += acceleration

    # Update position based on velocity
    position += velocity

    # Clear screen and draw the object at the new position (e.g., a circle)
    screen.fill((0, 0, 0))  # Clear screen with black
    pygame.draw.circle(screen, (255, 0, 0), (int(position.x), int(position.y)), 15)  # Draw player

    pygame.display.flip()  # Update display

pygame.quit()
