import pygame


# Initialize pygame
pygame.init()

# Use 2d vectors
vector = pygame.math.Vector2

# Set display surface
# (tile size is 32*32 so 960/32 = 30 tiles wide, 640/32 = 20 tiles high)
WIDTH = 960
HEIGHT = 640
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Making a tile map!')

# Set clock and FPS
FPS = 60
clock = pygame.time.Clock()

# Create sprite sub and main groups
main_tile_group = pygame.sprite.Group()
grass_tile_group = pygame.sprite.Group()
water_tile_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()


# Define classes
class Tile(pygame.sprite.Sprite):
    """A class to read and create individual tiles and place them in the display"""

    def __init__(self, x, y, image_int, main_group, sub_group=''):
        super().__init__()
        # Load in the correct image and add it to the correct groups
        if image_int == 1:
            self.image = pygame.image.load('assets/dirt.png')
        elif image_int == 2:
            self.image = pygame.image.load('assets/grass.png')
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.image.load('assets/water.png')
            sub_group.add(self)

        # Add every tile to the main tile group
        main_group.add(self)

        # Get the rect of the image and position within the grid
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Player(pygame.sprite.Sprite):
    """A player class the user can control"""

    def __init__(self, x, y, grass_tiles, water_tiles):
        super().__init__()
        self.image = pygame.image.load('assets/knight.png')
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        # Player's default starting position
        self.starting_x = x
        self.starting_y = y

        self.grass_tiles = grass_tiles
        self.water_tiles = water_tiles

        # Kinematics vectors (first value is the x, second value is the y)
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        # Kinematic constants
        self.HORIZONTAL_ACCELERATION = 2
        self.HORIZONTAL_FRICTION = 0.15
        # Gravity
        self.VERTICAL_ACCELERATION = 0.5
        # Determine how high we can jump
        self.VERTICAL_JUMP_SPEED = 15


    def update(self):
        self.move()
        self.check_collisions()


    def move(self):
        # Set the acceleration vector to (0, 0) so there is initially no acceleration
        # If there is no force (no key presses) acting on the player then acceleration should be 0
        # Vertical acceleration (gravity) is always present regardless of key-presses
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        # If the user is pressing a key, set the x-component of the acceleration vector to a non-zero value.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION * -1

        if keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION

        # Calculate new kinematics values i.e((2, 5) + (1, 6) = (3, 11))
        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + (0.5 * self.acceleration)

        # Update new rect based on kinematic calculations and add wrap-around motion
        if self.position.x < -64:
            self.position.x = WIDTH
        elif self.position.x > WIDTH:
            self.position.x = 0

        self.rect.bottomleft = self.position


    def check_collisions(self):
        # Check for collision with the grass tiles
        collided_platforms = pygame.sprite.spritecollide(self, self.grass_tiles, False)
        if collided_platforms:
            # Only move to the platform if the player is falling down
            if self.velocity.y >= 0:
                self.position.y = collided_platforms[0].rect.top
                self.velocity.y = 0

        # Check for collision with the water tiles
        if pygame.sprite.spritecollide(self, self.water_tiles, False):
            print('YOU CANT SWIM')
            self.position = vector(self.starting_x, self.starting_y)
            self.velocity = vector(0, 0)


    def jump(self):
        # Only jump if on a grass tile
        if pygame.sprite.spritecollide(self, self.grass_tiles, False):
            self.velocity.y = self.VERTICAL_JUMP_SPEED * -1



# Create the tile map: (0 -> no tile), (1 -> dirt), (2 -> grass), (3 -> water), (4 -> player)
# (20 rows and 30 columns)
tile_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1]
]

# Create individual Tile objects from the tile map
# Loop through the 20 lists in tile_map (i moves us down the map)
for i in range(len(tile_map)):
    # Loop through the 30 elements in a given list (j moves us across the map)
    for j in range(len(tile_map[i])):
        if tile_map[i][j] == 1:
            Tile(j * 32, i * 32, 1, main_tile_group)
        elif tile_map[i][j] == 2:
            Tile(j * 32, i * 32, 2, main_tile_group, grass_tile_group)
        elif tile_map[i][j] == 3:
            Tile(j * 32, i * 32, 3, main_tile_group, water_tile_group)
        elif tile_map[i][j] == 4:
            my_player = Player(j * 32, i * 32 + 32, grass_tile_group, water_tile_group)
            my_player_group.add(my_player)

# Load in the background image
background_image = pygame.image.load('assets/background.png')
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # User wants to jump
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.jump()

    # Blit the background
    display_surface.blit(background_image, background_rect)

    # Draw tiles
    main_tile_group.draw(display_surface)

    # Draw the player
    my_player_group.draw(display_surface)
    my_player_group.update()

    # Update the screen and tick the clock
    pygame.display.flip()
    clock.tick(FPS)

# End game
pygame.quit()