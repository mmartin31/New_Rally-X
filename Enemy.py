import pygame as py
from Player import Character
import Settings as gs

class Enemy(Character):
    """
    Represents an enemy car in the game, which can chase the player and interact with smoke.

    Attributes:
        car (dict): A dictionary containing enemy car images for different directions and actions.
        image (pygame.Surface): The current image representing the enemy.
        rect (pygame.Rect): The rectangle defining the enemy's position and size.
        speed (int): The current speed of the enemy.
        isSmoke (bool): A flag indicating whether the enemy is in smoke.
        anim_actions (str): The current animation action (e.g., 'SPIN', direction).
        anim_index (int): The current frame index for the animation.
        anim_time_set (int): The timestamp of the last animation frame update.
        anim_time (int): The delay between animation frames in milliseconds.
    """

    def __init__(self, group, x, y, assets):
        """
        Initialize an Enemy object.

        :param group: The sprite group the enemy belongs to.
        :param x: The x-coordinate of the enemy.
        :param y: The y-coordinate of the enemy.
        :param assets: The assets containing the enemy car images.
        """
        super().__init__(group, x, y)
        self.car = assets.enemy_car  # Enemy car images
        self.image = self.car["RIGHT"][0]  # Initial image
        self.rect = self.image.get_rect(center=(x, y))  # Position of the enemy
        self.speed = 0  # Initial speed
        self.isSmoke = False  # Flag to check if the enemy is in smoke

    def chase_player(self, player, group):
        """
        Make the enemy chase the player by changing its direction.

        :param player: The player object to chase.
        :param group: The group of sprites to check for collisions.
        """
        player_x = player.rect.x
        player_y = player.rect.y

        # Determine the direction to move based on the player's position
        if abs(player_x - self.rect.x) > abs(player_y - self.rect.y):
            if player_x - self.rect.x > 0 and not self.will_collide('RIGHT', group):
                self.change_direction('RIGHT')
            if player_x - self.rect.x < 0 and not self.will_collide('LEFT', group):
                self.change_direction('LEFT')
        else:
            if player_y - self.rect.y > 0 and not self.will_collide('DOWN', group):
                self.change_direction('DOWN')
            if player_y - self.rect.y < 0 and not self.will_collide('UP', group):
                self.change_direction('UP')

    def check_player_collision(self, player):
        """
        Check if the enemy collides with the player.

        :param player: The player object to check collision with.
        :return: True if a collision occurs, False otherwise.
        """
        return self.rect.colliderect(player.rect)

    def check_smoke_collision(self, smoke):
        """
        Check if the enemy collides with smoke and adjust its behavior.

        :param smoke: A list of smoke objects to check collision with.
        """
        self.isSmoke = False
        for object in smoke:
            if self.rect.colliderect(object.rect):
                self.isSmoke = True
                break

        # Adjust speed and animation based on smoke collision
        if self.isSmoke:
            self.speed = 0
            self.anim_actions = "SPIN"
        else:
            self.speed = 8  # Reset speed if not in smoke
            self.anim_actions = self.direction  # Reset to default animation

    def animate_turn(self):
        """
        Animate the enemy's movement or spin action.
        """
        if py.time.get_ticks() - self.anim_time_set >= self.anim_time:
            if self.anim_actions == "SPIN":
                # Loop through spin animation frames
                if self.anim_index < len(self.car[self.anim_actions]) - 1:
                    self.anim_index += 1
                else:
                    self.anim_index = 0
            else:
                # Loop through movement animation frames
                if self.anim_index < len(self.car[self.anim_actions]) - 1:
                    self.anim_index += 1
                else:
                    self.anim_index = 0

            self.image = self.car[self.anim_actions][self.anim_index]
            self.anim_time_set = py.time.get_ticks()


class Crash(py.sprite.Sprite):
    """
    Represents a crash effect in the game, displayed when a collision occurs.

    Attributes:
        assets (Assets): The game assets containing crash images.
        image (pygame.Surface): The final crash image to be displayed.
        rect (pygame.Rect): The rectangle defining the position of the crash effect.
        block_size (int): The size of each block in the crash effect.
        image1 (pygame.Surface): The top-left part of the crash image.
        image2 (pygame.Surface): The top-right part of the crash image.
        image3 (pygame.Surface): The bottom-left part of the crash image.
        image4 (pygame.Surface): The bottom-right part of the crash image.
        start_time (int): The timestamp when the crash effect started.
        duration (int): The duration of the crash effect in milliseconds.
    """

    def __init__(self, group, x, y, assets):
        """
        Initialize a Crash object.

        :param group: The sprite group the crash effect belongs to.
        :param x: The x-coordinate of the crash effect.
        :param y: The y-coordinate of the crash effect.
        :param assets: The assets containing the crash images.
        """
        super().__init__(group)
        self.assets = assets  # Game assets
        self.image = None  # Placeholder for the crash image
        self.rect = None  # Placeholder for the crash position
        self.block_size = gs.SIZE  # Size of the crash effect
        self.load_images()  # Load crash images
        self.create_image()  # Create the final crash image
        self.set_position(x, y)  # Set the position of the crash effect
        self.start_time = py.time.get_ticks()  # Start time of the crash effect
        self.duration = 3000  # Duration of the crash effect in milliseconds

    def set_position(self, x, y):
        """
        Set the position of the crash effect, snapping it to the grid.

        :param x: The x-coordinate of the crash effect.
        :param y: The y-coordinate of the crash effect.
        """
        grid_x = (x // gs.MAZE_SIZE) * gs.MAZE_SIZE + 48
        grid_y = (y // gs.MAZE_SIZE) * gs.MAZE_SIZE + 48
        self.rect = self.image.get_rect(center=(grid_x, grid_y))

    def load_images(self):
        """
        Load the images for the crash effect.
        """
        self.image1 = self.assets.objects['Crash'][0]
        self.image2 = self.assets.objects['Crash'][1]
        self.image3 = self.assets.objects['Crash'][2]
        self.image4 = self.assets.objects['Crash'][3]

    def create_image(self):
        """
        Create the final crash image by merging individual images.
        """
        merged_image = py.Surface((self.block_size * 2, self.block_size * 2), py.SRCALPHA)
        merged_image.blit(self.image1, (0, 0))
        merged_image.blit(self.image2, (self.block_size, 0))
        merged_image.blit(self.image3, (0, self.block_size))
        merged_image.blit(self.image4, (self.block_size, self.block_size))
        crop_rect = py.Rect(0, 0, 96, 96)  # Define the cropping rectangle
        self.image = merged_image.subsurface(crop_rect)

    def update(self):
        """
        Update the crash effect, removing it after its duration has elapsed.
        """
        current_time = py.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()  # Remove the crash effect from the game