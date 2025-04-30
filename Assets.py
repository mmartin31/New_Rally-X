import pygame
import Settings as gs

class Assets(object):
    """
    Class to manage and load game assets such as spritesheets and individual sprites.

    Attributes:
        spritesheet1 (pygame.Surface): The first sprite sheet containing game assets.
        player_car (dict): A dictionary of player car sprites, categorized by animations or directions.
        objects (dict): A dictionary of object sprites used in the game.
        boundary_blocks (dict): A dictionary of boundary block sprites for the maze.
        maze1_blocks (dict): A dictionary of sprites for the first maze layout.
        maze2_blocks (dict): A dictionary of sprites for the second maze layout.
        enemy_car (dict): A dictionary of enemy car sprites, categorized by animations or directions.
    """

    def __init__(self):
        """
        Initialize the Assets object and load all necessary assets.

        Attributes:

        """
        self.spritesheet1 = self.load_sprite_sheet("images", "spritesheet.png", 336 * 4, 496 * 4)
        self.player_car = self.load_sprite_range(gs.player_Car, self.spritesheet1)
        self.objects = self.load_sprite_range(gs.objects, self.spritesheet1)
        self.boundary_blocks = self.load_sprite_range(gs.boundary_blocks, self.spritesheet1)
        self.maze1_blocks = self.load_sprite_range(gs.maze1_blocks, self.spritesheet1)
        self.maze2_blocks = self.load_sprite_range(gs.maze2_blocks, self.spritesheet1)
        self.enemy_car = self.load_sprite_range(gs.enemy_Car, self.spritesheet1)

    def load_sprite_sheet(self, path, filename, width, height):
        """
        Load a sprite sheet image and resize it.

        :param path: The path to the directory containing the sprite sheet.
        :param filename: The name of the sprite sheet file.
        :param width: The width to resize the sprite sheet to.
        :param height: The height to resize the sprite sheet to.
        :return: The loaded and resized sprite sheet image.
        """
        image = pygame.image.load(f"{path}/{filename}").convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        return image

    def load_sprite(self, spritesheet, xcoord, ycoord, width, height):
        """
        Load an individual sprite image from a sprite sheet.

        :param spritesheet: The sprite sheet image.
        :param xcoord: The x-coordinate of the sprite on the sprite sheet.
        :param ycoord: The y-coordinate of the sprite on the sprite sheet.
        :param width: The width of the sprite.
        :param height: The height of the sprite.
        :return: The loaded sprite image.
        """
        # Create an empty surface with transparency
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        # Blit the sprite onto the new surface
        image.blit(spritesheet, (0, 0), (xcoord, ycoord, width, height))
        return image

    def load_sprite_range(self, image_dict, spritesheet, row=gs.SIZE, col=gs.SIZE, width=gs.SIZE, height=gs.SIZE, resize=False):
        """
        Load a range of sprites from a sprite sheet based on a dictionary of coordinates.

        :param image_dict: A dictionary containing lists of coordinates for the sprites.
        :param spritesheet: The sprite sheet image.
        :param row: The row size of each sprite.
        :param col: The column size of each sprite.
        :param width: The width of each sprite.
        :param height: The height of each sprite.
        :param resize: Whether to resize the sprites to 32x32.
        :return: A dictionary containing lists of loaded sprite images.
        """
        animation_images = {}
        for animation in image_dict.keys():
            animation_images[animation] = []
            for coord in image_dict[animation]:
                image = self.load_sprite(spritesheet, coord[1] * col, coord[0] * row, width, height)
                if resize:
                    image = pygame.transform.scale(image, (32, 32))
                animation_images[animation].append(image)
        return animation_images

    def rotate_images_in_list(self, image_list, rotation):
        """
        Rotate each image in a list of images by a given angle.

        :param image_list: The list of images to rotate.
        :param rotation: The angle to rotate the images by.
        """
        for ind, image in enumerate(image_list):
            image = pygame.transform.rotate(image, rotation)
            image_list[ind] = image
