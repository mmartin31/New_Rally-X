import pygame as py
import pygame.sprite
from Scoring import Scoring
import random
import Settings as gs

class Flag(py.sprite.Sprite):
    """
    Represents a flag in the game. Flags can be of different types (Normal, Special, or Lucky)
    and are collectible by the player.

    Attributes:
        group (pygame.sprite.Group): The sprite group the flag belongs to.
        flags (list): A list of flag images.
        image (pygame.Surface): The current image representing the flag.
        rect (pygame.Rect): The rectangle defining the flag's position and size.
        isNorm (bool): Indicates if the flag is a Normal flag.
        isSpec (bool): Indicates if the flag is a Special flag.
        isLucky (bool): Indicates if the flag is a Lucky flag.
        positions (tuple): The initial position of the flag (x, y).
        isCollected (bool): Indicates if the flag has been collected.
    """

    def __init__(self, group, x, y, assets):
        """
        Initialize a Flag object.

        :param group: The sprite group the flag belongs to.
        :param x: The x-coordinate of the flag.
        :param y: The y-coordinate of the flag.
        :param assets: The assets containing the flag images.
        """
        super().__init__(group)
        self.group = group
        self.flags = assets.objects['Flags']  # List of flag images
        self.image = self.flags[0]  # Default to Normal flag image
        self.rect = self.image.get_rect(center=(x, y))  # Set the flag's position
        self.isNorm = True  # Flag is Normal by default
        self.isSpec = False  # Not a Special flag by default
        self.isLucky = False  # Not a Lucky flag by default
        self.positions = (x, y)  # Store the initial position
        self.isCollected = False  # Flag is not collected initially

    def change_type(self, type):
        """
        Change the type of the flag.

        :param type: The new type of the flag ('Special' or 'Lucky').
        """
        if type == 'Special':
            self.isSpec = True
            self.isNorm = False
            self.image = self.flags[1]  # Update to Special flag image
        else:
            self.isLucky = True
            self.isNorm = False
            self.image = self.flags[2]  # Update to Lucky flag image

    def collect(self):
        """
        Mark the flag as collected and remove it from the game.
        """
        self.isCollected = True
        self.kill()  # Remove the flag from the sprite group


class Point(pygame.sprite.Sprite):
    """
    Represents a point object displayed when a flag is collected.
    The point object shows the score earned and disappears after a short duration.

    Attributes:
        assets (Assets): The game assets containing point images.
        block_size (int): The size of the point display.
        image (pygame.Surface): The final image representing the point.
        rect (pygame.Rect): The rectangle defining the point's position and size.
        flags_collected (int): The number of flags collected by the player.
        image_indexes (dict): A mapping of flags collected to image indexes.
        image_index (int): The index of the current point image.
        isSpec (bool): Indicates if the point is for a Special flag.
        image1 (pygame.Surface): The base point image.
        image2 (pygame.Surface): The secondary point image.
        image3 (pygame.Surface): The image for Special flag points.
        start_time (int): The timestamp when the point object was created.
        duration (int): The duration for which the point is displayed (in milliseconds).
    """

    def __init__(self, group, x, y, assets, flags_collected, isSpec):
        """
        Initialize a Point object.

        :param group: The sprite group the point belongs to.
        :param x: The x-coordinate of the point.
        :param y: The y-coordinate of the point.
        :param assets: The assets containing the point images.
        :param flags_collected: The number of flags collected by the player.
        :param isSpec: Whether the point is for a Special flag.
        """
        super().__init__(group)
        self.assets = assets
        self.block_size = 64  # Size of the point display
        self.image = None  # Placeholder for the point image
        self.rect = None  # Placeholder for the point position
        self.flags_collected = flags_collected  # Number of flags collected
        self.image_indexes = {1: 0, 3: 2, 5: 4, 7: 6, 9: 8}  # Mapping of flags to image indexes
        if flags_collected in self.image_indexes:
            self.image_index = self.image_indexes[flags_collected]
        elif flags_collected > 0:
            self.image_index = self.image_indexes[flags_collected - 1]
        else:
            self.image_index = 0
        self.isSpec = isSpec  # Whether the point is for a Special flag
        self.load_images()  # Load the point images
        self.create_image()  # Create the final point image
        self.set_position(x, y)  # Set the position of the point
        self.start_time = pygame.time.get_ticks()  # Record the start time
        self.duration = 1500  # Duration for which the point is displayed (in milliseconds)

    def set_position(self, x, y):
        """
        Set the position of the point object.

        :param x: The x-coordinate of the point.
        :param y: The y-coordinate of the point.
        """
        if self.image:
            self.rect = self.image.get_rect(center=(x, y))  # Center the point at the given position

    def load_images(self):
        """
        Load the images for the point object.
        """
        self.image1 = self.assets.objects['Points'][self.image_index]  # Base point image
        if self.flags_collected < 10:
            self.image2 = self.assets.objects['Points'][1]  # Image for less than 10 flags
        else:
            self.image2 = self.assets.objects['Points'][9]  # Image for 10 or more flags
        if self.isSpec:
            self.image3 = self.assets.objects['Points'][10]  # Image for Special flag points

    def create_image(self):
        """
        Create the final image for the point object by merging individual images.
        """
        merged_image = pygame.Surface((self.block_size * 3, self.block_size * 2), pygame.SRCALPHA)
        merged_image.blit(self.image1, (0, 0))  # Add the base point image
        merged_image.blit(self.image2, (self.block_size, 0))  # Add the secondary point image

        if self.isSpec:
            # Crop and add the Special flag point image
            image3_cropped = self.image3.subsurface(
                pygame.Rect(0, self.block_size // 2, self.block_size, self.block_size // 2))
            if self.flags_collected % 2 == 1:
                merged_image.blit(image3_cropped, (self.block_size * 2, 0))
            else:
                merged_image.blit(image3_cropped, (self.block_size * 2, self.block_size // 2))

        # Crop the final merged image based on the number of flags collected
        if self.flags_collected % 2 == 1:
            crop_rect = pygame.Rect(0, 0, self.block_size * 3, self.block_size // 2)
        else:
            crop_rect = pygame.Rect(0, self.block_size // 2, self.block_size * 3, self.block_size // 2)

        self.image = merged_image.subsurface(crop_rect)  # Set the final image

    def update(self):
        """
        Update the point object. Remove it after its duration has elapsed.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()  # Remove the point object from the sprite group