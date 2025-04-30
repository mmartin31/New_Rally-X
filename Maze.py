import pygame
import Settings as gs

class Maze:
    """
    Class representing the maze in the game.

    Attributes:
        group (pygame.sprite.Group): The sprite group for managing maze blocks.
        assets (Assets): The game assets, including images for maze blocks.
        maze_matrix (list): A 2D list representing the layout of the maze.
        num (str): The ID of the maze layout (e.g., '1' or '2').
    """
    def __init__(self, group, assets, maze, num):
        """
        Initialize the Maze object.

        :param group: The sprite group for the maze blocks.
        :param assets: The assets containing the maze block images.
        :param maze: The matrix representing the maze layout.
        :param num: The num ID for the maze layout
        """
        self.group = group
        self.assets = assets
        self.maze_matrix = [list(row) for row in maze]
        self.num = str(num)

    def set_matrix(self, maze):
        self.maze_matrix = [list(row) for row in maze]

    def build_maze(self):
        """
        Build the maze by placing blocks according to the maze matrix.
        """
        for r, row in enumerate(self.maze_matrix):
            for c, cell in enumerate(row):
                x = c * gs.MAZE_SIZE
                y = r * gs.MAZE_SIZE
                if cell == '#':
                    block = BoundaryBlock(self.group, self.assets,self.num, x, y)
                elif cell == 'X':
                    block = self.create_maze_block(r, c, x, y)
                else:
                    continue
                self.group.add(block)

    def destroy_maze(self):
        """
        Destroy all maze sprites by removing them from the group.
        """
        for sprite in self.group:
            sprite.kill()  # Remove the sprite from all groups

    def create_maze_block(self, r, c, x, y):
        """
        Create a maze block based on its position and surrounding cells.

        :param r: The row index of the block.
        :param c: The column index of the block.
        :param x: The x-coordinate of the block.
        :param y: The y-coordinate of the block.
        :return: The created maze block.
        """
        if (self.maze_matrix[r - 1][c] != 'X' and self.maze_matrix[r][c - 1] != 'X' and
                self.maze_matrix[r + 1][c] == 'X' and self.maze_matrix[r][c + 1] == 'X'):
            return MazeBlock(self.group, self.assets, self.num, x, y, 'Top_Left')
        elif (self.maze_matrix[r - 1][c] != 'X' and self.maze_matrix[r][c - 1] == 'X' and
              self.maze_matrix[r + 1][c] == 'X' and self.maze_matrix[r][c + 1] == 'X'):
            return MazeBlock(self.group, self.assets, self.num, x, y, 'Top_Middle')
        elif (self.maze_matrix[r - 1][c] != 'X' and self.maze_matrix[r][c - 1] == 'X' and
              self.maze_matrix[r + 1][c] == 'X' and self.maze_matrix[r][c + 1] != 'X'):
            return MazeBlock(self.group, self.assets, self.num, x, y, 'Top_Right')
        elif (self.maze_matrix[r - 1][c] == 'X' and self.maze_matrix[r][c - 1] != 'X' and
              self.maze_matrix[r + 1][c] == 'X' and self.maze_matrix[r][c + 1] == 'X'):
            return MazeBlock(self.group, self.assets, self.num, x, y, 'Middle_Left')
        elif (self.maze_matrix[r - 1][c] == 'X' and self.maze_matrix[r][c - 1] == 'X' and
              self.maze_matrix[r + 1][c] == 'X' and self.maze_matrix[r][c + 1] == 'X'):
            return MazeBlock(self.group, self.assets, self.num, x, y, 'Middle')
        elif (self.maze_matrix[r - 1][c] == 'X' and self.maze_matrix[r][c - 1] == 'X' and
              self.maze_matrix[r + 1][c] == 'X' and self.maze_matrix[r][c + 1] != 'X'):
            return MazeBlock(self.group, self.assets, self.num, x, y, 'Middle_Right')
        elif (self.maze_matrix[r - 1][c] == 'X' and self.maze_matrix[r][c - 1] != 'X' and
              self.maze_matrix[r + 1][c] != 'X' and self.maze_matrix[r][c + 1] == 'X'):
            return MazeBlock(self.group, self.assets, self.num, x, y, 'Bottom_Left')
        elif (self.maze_matrix[r - 1][c] == 'X' and self.maze_matrix[r][c - 1] == 'X' and
              self.maze_matrix[r + 1][c] != 'X' and self.maze_matrix[r][c + 1] == 'X'):
            return MazeBlock(self.group, self.assets, self.num, x, y, 'Bottom_Middle')
        elif (self.maze_matrix[r - 1][c] == 'X' and self.maze_matrix[r][c - 1] == 'X' and
              self.maze_matrix[r + 1][c] != 'X' and self.maze_matrix[r][c + 1] != 'X'):
            return MazeBlock(self.group, self.assets,self.num, x, y, 'Bottom_Right')
        elif (self.maze_matrix[r - 1][c] != 'X' and self.maze_matrix[r][c - 1] != 'X' and
              self.maze_matrix[r + 1][c] == 'X' and self.maze_matrix[r][c + 1] != 'X'):
            return MazeBlock(self.group, self.assets,self.num, x, y, 'Penn_UP')
        elif (self.maze_matrix[r - 1][c] != 'X' and self.maze_matrix[r][c - 1] != 'X' and
              self.maze_matrix[r + 1][c] != 'X' and self.maze_matrix[r][c + 1] == 'X'):
            return MazeBlock(self.group, self.assets,self.num, x, y, 'Penn_Left')
        elif (self.maze_matrix[r - 1][c] != 'X' and self.maze_matrix[r][c - 1] == 'X' and
              self.maze_matrix[r + 1][c] != 'X' and self.maze_matrix[r][c + 1] != 'X'):
            return MazeBlock(self.group, self.assets, self.num, x, y, 'Penn_Right')
        elif (self.maze_matrix[r - 1][c] == 'X' and self.maze_matrix[r][c - 1] != 'X' and
              self.maze_matrix[r + 1][c] != 'X' and self.maze_matrix[r][c + 1] != 'X'):
            return MazeBlock(self.group, self.assets, self.num, x, y, 'Penn_Down')
        elif (self.maze_matrix[r - 1][c] != 'X' and self.maze_matrix[r][c - 1] == 'X' and
              self.maze_matrix[r + 1][c] != 'X' and self.maze_matrix[r][c + 1] == 'X'):
            return MazeBlock(self.group, self.assets,self.num, x, y, 'Bridge_H')
        elif (self.maze_matrix[r - 1][c] == 'X' and self.maze_matrix[r][c - 1] != 'X' and
              self.maze_matrix[r + 1][c] == 'X' and self.maze_matrix[r][c + 1] != 'X'):
            return MazeBlock(self.group, self.assets,self.num, x, y, 'Bridge_V')
        else:
            return MazeBlock(self.group, self.assets,self.num, x, y)

class Blocks(pygame.sprite.Sprite):
    """
    Base class for blocks in the maze.

    Attributes:
        group (pygame.sprite.Group): The sprite group the block belongs to.
        assets (Assets): The game assets containing block images.
        block_size (int): The size of the block.
        num (str): The ID of the maze layout the block belongs to.
        image (pygame.Surface): The image representing the block.
        rect (pygame.Rect): The rectangle defining the block's position and size.
    """
    def __init__(self, group, assets, num, x=0, y=0):
        """
        Initialize a Blocks object.

        :param group: The sprite group the block belongs to.
        :param assets: The assets containing the block images.
        :param num: The num ID for the maze layout.
        :param x: The x-coordinate of the block.
        :param y: The y-coordinate of the block.
        """
        super().__init__(group)
        self.assets = assets
        self.block_size = gs.SIZE
        self.num = num
        self.image = None
        self.rect = None
        self.set_position(x, y)

    def set_position(self, x, y):
        """
        Set the position of the block.

        :param x: The x-coordinate of the block.
        :param y: The y-coordinate of the block.
        """
        if self.image:
            self.rect = self.image.get_rect(topleft=(x, y))

class BoundaryBlock(Blocks):
    """
    Class representing a boundary block in the maze.

    Attributes:
        image1 (pygame.Surface): The top-left part of the boundary block image.
        image2 (pygame.Surface): The top-right part of the boundary block image.
        image3 (pygame.Surface): The bottom-left part of the boundary block image.
        image4 (pygame.Surface): The bottom-right part of the boundary block image.
    """
    def __init__(self, group, assets, num,  x=0, y=0):
        """
        Initialize a BoundaryBlock object.

        :param group: The sprite group the block belongs to.
        :param assets: The assets containing the block images.
        :param num: The num ID for the maze layout.
        :param x: The x-coordinate of the block.
        :param y: The y-coordinate of the block.
        """
        super().__init__(group, assets, num, x, y)
        self.load_images()
        self.create_image()
        self.set_position(x, y)

    def load_images(self):
        """
        Load the images for the boundary block.
        """
        self.image1 = self.assets.boundary_blocks['Maze' + str(self.num)][0]
        self.image2 = self.assets.boundary_blocks['Maze' + str(self.num)][1]
        self.image3 = self.assets.boundary_blocks['Maze' + str(self.num)][2]
        self.image4 = self.assets.boundary_blocks['Maze' + str(self.num)][3]

    def create_image(self):
        """
        Create the final image for the boundary block by merging individual images.
        """
        merged_image = pygame.Surface((self.block_size * 2, self.block_size * 2), pygame.SRCALPHA)
        merged_image.blit(self.image1, (0, 0))
        merged_image.blit(self.image2, (self.block_size, 0))
        merged_image.blit(self.image3, (0, self.block_size))
        merged_image.blit(self.image4, (self.block_size, self.block_size))
        crop_rect = pygame.Rect(32, 32, 96, 96)
        self.image = merged_image.subsurface(crop_rect)

class MazeBlock(Blocks):
    """
    Class representing a maze block in the maze.

    Attributes:
        blocktype (str): The type of the maze block (e.g., 'Top_Left', 'Middle').
        image1 (pygame.Surface): The top-left part of the maze block image.
        image2 (pygame.Surface): The top-right part of the maze block image.
        image3 (pygame.Surface): The bottom-left part of the maze block image.
        image4 (pygame.Surface): The bottom-right part of the maze block image.
    """
    def __init__(self, group, assets, num, x=0, y=0, blocktype='Solo'):
        """
        Initialize a MazeBlock object.

        :param group: The sprite group the block belongs to.
        :param assets: The assets containing the block images.
        :param num: The num ID for the maze layout
        :param x: The x-coordinate of the block.
        :param y: The y-coordinate of the block.
        :param blocktype: The type of the maze block.
        """
        super().__init__(group, assets, num, x, y)
        self.blocktype = blocktype
        self.load_images()
        self.create_image()
        self.set_position(x, y)

    def load_images(self):
        """
        Load the images for the maze block.
        """
        if self.num == '1':
            self.image1 = self.assets.maze1_blocks[self.blocktype][0]
            self.image2 = self.assets.maze1_blocks[self.blocktype][1]
            self.image3 = self.assets.maze1_blocks[self.blocktype][2]
            self.image4 = self.assets.maze1_blocks[self.blocktype][3]
        else:
            self.image1 = self.assets.maze2_blocks[self.blocktype][0]
            self.image2 = self.assets.maze2_blocks[self.blocktype][1]
            self.image3 = self.assets.maze2_blocks[self.blocktype][2]
            self.image4 = self.assets.maze2_blocks[self.blocktype][3]

    def create_image(self):
        """
        Create the final image for the maze block by merging individual images.
        """
        merged_image = pygame.Surface((self.block_size * 2, self.block_size * 2), pygame.SRCALPHA)
        merged_image.blit(self.image1, (0, 0))
        merged_image.blit(self.image2, (self.block_size, 0))
        merged_image.blit(self.image3, (0, self.block_size))
        merged_image.blit(self.image4, (self.block_size, self.block_size))
        if self.blocktype == 'Penn_Left' or self.blocktype == 'Penn_Right':
            crop_rect = pygame.Rect(32, 32, 96, 96)
        else:
            crop_rect = pygame.Rect(0, 0, 96, 96)
        self.image = merged_image.subsurface(crop_rect)