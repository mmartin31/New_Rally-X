import pygame as py
import Settings as gs

class Character(py.sprite.Sprite):
    """
    Base class for a character in the game.

    This class provides common functionality for movement, direction changes,
    collision detection, and animation.

    Attributes:
        speed (int): The movement speed of the character.
        direction (str): The current direction of the character ('UP', 'DOWN', 'LEFT', 'RIGHT').
        anim_time_set (int): The timestamp for the last animation frame update.
        anim_time (int): The time interval (in milliseconds) between animation frames.
        anim_index (int): The current index of the animation frame.
        animating (bool): Indicates if the character is currently animating.
        anim_actions (list): A list of animation actions for direction changes.
        is_crashed (bool): Indicates if the character has crashed.
        rect (pygame.Rect): The rectangle defining the character's position and size.
        image (pygame.Surface): The current image representing the character.
    """
    def __init__(self, group, x, y):
        """
        Initialize a Character object.

        :param group: The sprite group the character belongs to.
        :param x: The x-coordinate of the character.
        :param y: The y-coordinate of the character.
        """
        super().__init__(group)
        self.speed = 0  # Movement speed of the character
        self.direction = 'RIGHT'  # Initial direction of the character
        self.anim_time_set = py.time.get_ticks()  # Time tracker for animation
        self.anim_time = 50  # Time interval for animation frames
        self.anim_index = 0  # Current animation frame index
        self.animating = False  # Flag to indicate if animation is active
        self.anim_actions = []  # List of animation actions
        self.is_crashed = False  # Flag to indicate if the character has crashed

    def auto_move(self, matrix, group):
        """
        Automatically move the character forward and handle collisions.

        :param matrix: The matrix representing the maze layout.
        :param group: The sprite group containing the blocks in the maze.
        """
        self.move()  # Move the character in the current direction
        self.detect_maze_collision(matrix, group)  # Check for collisions

    def change_direction(self, direction):
        """
        Change the direction of the character.

        :param direction: The new direction of the character.
        """
        horizontal = ['RIGHT', 'LEFT']
        vertical = ['UP', 'DOWN']
        if self.direction != direction:
            # Snap to grid when changing between horizontal and vertical directions
            if self.direction in horizontal and direction not in horizontal:
                self.snap_to_grid()
            elif self.direction in vertical and direction not in vertical:
                self.snap_to_grid()
            # Set up animation for the direction change
            self.anim_actions = [self.direction + "_TO_" + direction, direction]
            self.animating = True
            self.anim_index = 0
            self.anim_time_set = py.time.get_ticks()
            self.direction = direction

    def snap_to_grid(self):
        """
        Snap the character to the nearest grid position.
        """
        grid_size = gs.MAZE_SIZE
        offset = (grid_size // 5)
        self.rect.x = (round(self.rect.x / grid_size) * grid_size) + offset
        self.rect.y = (round(self.rect.y / grid_size) * grid_size) + offset

    def move(self):
        """
        Move the character in the current direction.
        """
        if self.is_crashed:
            return  # Stop movement if the character has crashed
        if self.direction == 'LEFT':
            self.rect.x -= self.speed
        elif self.direction == 'RIGHT':
            self.rect.x += self.speed
        elif self.direction == 'DOWN':
            self.rect.y += self.speed
        elif self.direction == 'UP':
            self.rect.y -= self.speed

    def detect_maze_collision(self, matrix, group):
        """
        Detect and handle collisions with the maze and blocks.

        :param matrix: The matrix representing the maze layout.
        :param group: The sprite group containing the blocks in the maze.
        """
        player_x = self.rect.x // gs.MAZE_SIZE
        player_y = self.rect.y // gs.MAZE_SIZE
        max_x = len(matrix[0]) - 1
        max_y = len(matrix) - 1

        # Check for collisions and adjust direction accordingly
        if self.will_collide(self.direction, group):
            if self.direction == 'RIGHT':
                if player_x + 1 <= max_x and matrix[player_y][player_x + 1] in ['X', '#']:
                    if player_y + 1 <= max_y and matrix[player_y + 1][player_x] not in ['X', '#']:
                        self.change_direction('DOWN')
                    elif player_y - 1 >= 0 and matrix[player_y - 1][player_x] not in ['X', '#']:
                        self.change_direction('UP')
            elif self.direction == 'LEFT':
                if player_x - 1 >= 0 and matrix[player_y][player_x - 1] in ['X', '#']:
                    if player_y - 1 >= 0 and matrix[player_y - 1][player_x] not in ['X', '#']:
                        self.change_direction('UP')
                    elif player_y + 1 <= max_y and matrix[player_y + 1][player_x] not in ['X', '#']:
                        self.change_direction('DOWN')
            elif self.direction == 'DOWN':
                if player_y + 1 <= max_y and matrix[player_y + 1][player_x] in ['X', '#']:
                    if player_x - 1 >= 0 and matrix[player_y][player_x - 1] not in ['X', '#']:
                        self.change_direction('LEFT')
                    elif player_x + 1 <= max_x and matrix[player_y][player_x + 1] not in ['X', '#']:
                        self.change_direction('RIGHT')
            elif self.direction == 'UP':
                if player_y - 1 >= 0 and matrix[player_y - 1][player_x] in ['X', '#']:
                    if player_x + 1 <= max_x and matrix[player_y][player_x + 1] not in ['X', '#']:
                        self.change_direction('RIGHT')
                    elif player_x - 1 >= 0 and matrix[player_y][player_x - 1] not in ['X', '#']:
                        self.change_direction('LEFT')

    def will_collide(self, direction, group):
        """
        Check if the character will collide with a block in the given direction.

        :param direction: The direction of movement.
        :param group: The sprite group containing the blocks in the maze.
        :return: True if a collision will occur, False otherwise.
        """
        offset = gs.MAZE_SIZE // 5
        future_rect = self.rect.copy()
        if direction == 'LEFT':
            future_rect.x -= (self.speed + offset)
        elif direction == 'RIGHT':
            future_rect.x += (self.speed + offset)
        elif direction == 'DOWN':
            future_rect.y += (self.speed + offset)
        elif direction == 'UP':
            future_rect.y -= (self.speed + offset)

        # Check for collision with any block in the group
        for block in group:
            if future_rect.colliderect(block.rect):
                return True

        return False

    def animate_turn(self):
        """
        Animate the character's turn by switching between images.
        """
        if self.animating:
            if py.time.get_ticks() - self.anim_time_set >= self.anim_time:
                if self.anim_index < len(self.car[self.anim_actions[0]]) - 1:
                    self.anim_index += 1
                    self.image = self.car[self.anim_actions[0]][self.anim_index]
                else:
                    # Reset animation and set the new direction
                    self.anim_index = 0
                    self.animating = False
                    self.direction = self.anim_actions[1]
                    self.image = self.car[self.direction][0]
                self.anim_time_set = py.time.get_ticks()


class Player(Character):
    """
    Class representing the player in the game.

    The Player class extends the Character class and includes additional functionality
    specific to the player, such as handling input, managing score, lives, and creating
    smoke screens.

    Attributes:
        car (dict): A dictionary of player car images for different directions.
        image (pygame.Surface): The current image representing the player.
        rect (pygame.Rect): The rectangle defining the player's position and size.
        score (int): The player's current score.
        speed (int): The player's movement speed.
        lives (int): The number of lives the player has remaining.
        ID (int): The player's ID (e.g., 1 for Player 1, 2 for Player 2).
    """

    def __init__(self, group, x, y, assets, num):
        """
        Initialize a Player object.

        :param group: The sprite group the player belongs to.
        :param x: The x-coordinate of the player.
        :param y: The y-coordinate of the player.
        :param assets: The assets containing the player images.
        :param num: The player's ID (e.g., 1 for Player 1, 2 for Player 2).
        """
        super().__init__(group, x, y)
        self.car = assets.player_car  # Dictionary of player car images for different directions
        self.image = self.car["RIGHT"][0]  # Initial image facing right
        self.rect = self.image.get_rect(center=(x, y))  # Set the player's position
        self.score = 0  # Player's score
        self.speed = 8  # Player's movement speed
        self.lives = 3  # Number of lives the player starts with
        self.ID = num  # Player's ID

    def input(self, group, smoke_group, assets, maze):
        """
        Handle player input for movement and actions.

        :param group: The sprite group containing the blocks in the maze.
        :param smoke_group: The sprite group for smoke screens.
        :param assets: The assets containing the smoke screen images.
        :param maze: The matrix representing the maze layout.
        """
        keys = py.key.get_pressed()  # Get the current state of keyboard keys
        # Check for movement keys and change direction if no collision is detected
        if keys[py.K_LEFT] and not self.will_collide('LEFT', group):
            self.change_direction('LEFT')
        elif keys[py.K_RIGHT] and not self.will_collide('RIGHT', group):
            self.change_direction('RIGHT')
        elif keys[py.K_DOWN] and not self.will_collide('DOWN', group):
            self.change_direction('DOWN')
        elif keys[py.K_UP] and not self.will_collide('UP', group):
            self.change_direction('UP')
        # Uncomment the following lines to enable smoke screen creation
        # elif keys[py.K_SPACE]:
        #    self.create_smoke_screen(smoke_group, assets, maze)

    def check_flag_collision(self, flags, score_increment):
        """
        Check for collisions with flags and update the score.

        :param flags: The list of flag objects in the game.
        :param score_increment: The score increment for collecting a flag.
        """
        for flag in flags:
            # Check if the player collides with a flag and it hasn't been collected yet
            if self.rect.colliderect(flag.rect) and not flag.isCollected:
                flag.collect()  # Mark the flag as collected
                # Double the score increment if the flag is a special flag
                if flag.isSpec:
                    self.score += score_increment * 2
                else:
                    self.score += score_increment

    def create_smoke_screen(self, smoke_group, assets, maze):
        """
        Create a smoke screen at the player's current position.

        The smoke screen is only created if the target grid space is empty.

        :param smoke_group: The sprite group for smoke screens.
        :param assets: The assets containing the smoke screen images.
        :param maze: The matrix representing the maze layout.
        """
        # Determine the target position based on the player's direction
        target_x, target_y = self.rect.centerx, self.rect.centery
        if self.direction == 'RIGHT':
            target_x -= gs.MAZE_SIZE
        elif self.direction == 'DOWN':
            target_y -= gs.MAZE_SIZE
        elif self.direction == 'LEFT':
            target_x += gs.MAZE_SIZE
        elif self.direction == 'UP':
            target_y += gs.MAZE_SIZE

        # Snap the target position to the grid
        grid_x = (target_x // gs.MAZE_SIZE) * gs.MAZE_SIZE + 48
        grid_y = (target_y // gs.MAZE_SIZE) * gs.MAZE_SIZE + 48

        # Check if the target grid space is empty
        if maze[grid_y // gs.MAZE_SIZE][grid_x // gs.MAZE_SIZE] == ' ':
            # Create and add a smoke screen to the smoke group
            smoke_screen = Smoke_Screen(smoke_group, grid_x, grid_y, assets)
            smoke_group.add(smoke_screen)



class Smoke_Screen(py.sprite.Sprite):
    """
    Class representing a smoke screen in the game.

    The smoke screen is a temporary object created by the player to obscure
    the view of opponents or block their path.

    Attributes:
        assets (Assets): The game assets containing smoke screen images.
        image (pygame.Surface): The final image representing the smoke screen.
        rect (pygame.Rect): The rectangle defining the smoke screen's position and size.
        block_size (int): The size of the smoke screen block.
        image1 (pygame.Surface): The top-left image of the smoke screen.
        image2 (pygame.Surface): The top-right image of the smoke screen.
        image3 (pygame.Surface): The bottom-left image of the smoke screen.
        image4 (pygame.Surface): The bottom-right image of the smoke screen.
        start_time (int): The timestamp when the smoke screen was created.
        duration (int): The duration for which the smoke screen is displayed (in milliseconds).
    """

    def __init__(self, group, x, y, assets):
        """
        Initialize a Smoke_Screen object.

        :param group: The sprite group the smoke screen belongs to.
        :param x: The x-coordinate of the smoke screen's position.
        :param y: The y-coordinate of the smoke screen's position.
        :param assets: The assets containing the smoke screen images.
        """
        super().__init__(group)
        self.assets = assets  # Game assets for the smoke screen
        self.image = None  # Placeholder for the smoke screen image
        self.rect = None  # Placeholder for the smoke screen's rectangle
        self.block_size = gs.SIZE  # Size of the smoke screen block
        self.load_images()  # Load the smoke screen images
        self.create_image()  # Create the final smoke screen image
        self.set_position(x, y)  # Set the position of the smoke screen
        self.start_time = py.time.get_ticks()  # Record the time the smoke screen was created
        self.duration = 3000  # Duration (in milliseconds) the smoke screen will last

    def set_position(self, x, y):
        """
        Set the position of the smoke screen.

        :param x: The x-coordinate of the smoke screen.
        :param y: The y-coordinate of the smoke screen.
        """
        if self.image:  # Ensure the image is loaded before setting the position
            self.rect = self.image.get_rect(center=(x, y))

    def load_images(self):
        """
        Load the images for the smoke screen.

        The smoke screen consists of four images that will be merged to create
        the final appearance.
        """
        self.image1 = self.assets.objects['Smoke'][0]  # Top-left image
        self.image2 = self.assets.objects['Smoke'][1]  # Top-right image
        self.image3 = self.assets.objects['Smoke'][2]  # Bottom-left image
        self.image4 = self.assets.objects['Smoke'][3]  # Bottom-right image

    def create_image(self):
        """
        Create the final image for the smoke screen by merging individual images.

        The images are combined into a single surface, and a specific portion
        is cropped to create the final appearance of the smoke screen.
        """
        # Create a surface to merge the images
        merged_image = py.Surface((self.block_size * 2, self.block_size * 2), py.SRCALPHA)
        merged_image.blit(self.image1, (0, 0))  # Place top-left image
        merged_image.blit(self.image2, (self.block_size, 0))  # Place top-right image
        merged_image.blit(self.image3, (0, self.block_size))  # Place bottom-left image
        merged_image.blit(self.image4, (self.block_size, self.block_size))  # Place bottom-right image
        crop_rect = py.Rect(32, 0, 96, 96)  # Define the cropping rectangle
        self.image = merged_image.subsurface(crop_rect)  # Crop the merged image

    def update(self):
        """
        Update the smoke screen's state.

        This method checks if the smoke screen's duration has expired and removes
        it from the game if necessary.
        """
        current_time = py.time.get_ticks()  # Get the current time
        if current_time - self.start_time > self.duration:  # Check if the duration has passed
            self.kill()  # Remove the smoke screen from the game