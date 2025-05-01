import pygame as py
import Settings as gs
from Assets import Assets
from Scoring import Scoring

class MainMenu:
    """
    Class representing the main menu screen of the game.

    Attributes:
        run (bool): A flag to control the main menu loop.
        assets (Assets): The game assets, including images and sounds.
        font (pygame.font.Font): The font used for rendering text in the main menu.
        window (pygame.Surface): The Pygame surface where the main menu is drawn.
        groups (dict): A dictionary of sprite groups (e.g., for the logo and flag).
        logo (pygame.sprite.Sprite): The logo sprite displayed in the main menu.
        flag_position (int): The position of the flag (used for menu selection).
        Scores (Scoring): The scoring system for managing high scores.
    """
    def __init__(self, surface):
        """
        Initialize the MainMenu object.

        :param surface: The Pygame surface where the main menu will be drawn.
        """
        py.init()  # Initialize Pygame
        self.run = True  # Flag to control the main menu loop
        self.assets = Assets()  # Load game assets
        self.font = py.font.Font(gs.font, 32)  # Set the font for text rendering
        self.window = surface  # The main game window
        self.groups = {
            'Logo': py.sprite.Group(),  # Group for the logo sprite
            'Flag': py.sprite.Group()  # Group for the flag sprite
        }

        # Load and create the logo sprite
        logo_path = 'images/New_Rally-X_logo.png'
        self.logo = self.create_logo(logo_path, 400, 300)
        self.groups['Logo'].add(self.logo)  # Add the logo to the group
        self.flag_position = 0  # Position of the flag (used for menu selection)
        self.Scores = Scoring()  # Scoring object to manage high scores

    def input(self):
        """
        Handle user input for the main menu.
        """
        for event in py.event.get():  # Iterate through all Pygame events
            if event.type == py.QUIT:  # If the user closes the window
                py.quit()  # Quit Pygame
                exit()
            if event.type == py.KEYDOWN:  # If a key is pressed
                if event.key == py.K_ESCAPE:  # If the Escape key is pressed
                    py.quit()  # Quit Pygame
                    exit()
                if event.key == py.K_RETURN:  # If the Enter key is pressed
                    self.run = False  # Exit the main menu loop

    def create_logo(self, image_path, x, y):
        """
        Create a logo sprite for the main menu.

        :param image_path: Path to the logo image file.
        :param x: The x-coordinate of the logo's center.
        :param y: The y-coordinate of the logo's center.
        :return: A Pygame sprite object representing the logo.
        """
        logo = py.sprite.Sprite()  # Create a new sprite
        logo.image = py.image.load(image_path).convert_alpha()  # Load the logo image
        logo.rect = logo.image.get_rect()  # Get the rectangle of the image
        logo.rect.center = (x, y)  # Set the position of the logo
        return logo

    def draw(self):
        """
        Draw the main menu elements on the screen.
        """
        self.window.fill(gs.BLACK)  # Fill the screen with a black background

        # Render and position the high score text
        HI_SCORE_TEXT = self.font.render("HI-SCORE", True, gs.RED)
        HI_SCORE_RECT = HI_SCORE_TEXT.get_rect(center=(gs.SCREEN_WIDTH / 2, 25))

        # Display the top score
        top_score = self.Scores.top_score
        HI_SCORE_DISPLAY_TEXT = self.font.render(str(top_score), True, gs.WHITE)
        HI_SCORE_DISPLAY_RECT = HI_SCORE_DISPLAY_TEXT.get_rect(center=(gs.SCREEN_WIDTH / 2, 50))

        # Render and position the 1UP and 2UP scores
        #UP1_TEXT = self.font.render("1UP", True, gs.RED)
        #UP1_RECT = UP1_TEXT.get_rect(center=(gs.SCREEN_WIDTH / 2 - 300, 25))
        #UP1_SCORE_TEXT = self.font.render(str(00), True, gs.WHITE)
        #UP1_SCORE_RECT = UP1_SCORE_TEXT.get_rect(center=(gs.SCREEN_WIDTH / 2 - 300, 50))

        #UP2_TEXT = self.font.render("2UP", True, gs.RED)
        #UP2_RECT = UP2_TEXT.get_rect(center=(gs.SCREEN_WIDTH / 2 + 300, 25))
        #UP2_SCORE_TEXT = self.font.render(str(00), True, gs.WHITE)
        #UP2_SCORE_RECT = UP2_SCORE_TEXT.get_rect(center=(gs.SCREEN_WIDTH / 2 + 300, 50))

        # Render and position other menu elements
        PLAYER_NUM_1 = self.font.render('1 PLAYER', True, gs.WHITE)
        PLAYER_NUM_1_RECT = PLAYER_NUM_1.get_rect(center=(gs.SCREEN_WIDTH / 2, 500))

        ENTER = self.font.render('Press enter to continue', True, gs.WHITE)
        ENTER_RECT = ENTER.get_rect(center=(gs.SCREEN_WIDTH / 2, 500))

        COMPANY = self.font.render('namco', True, gs.RED)
        COMPANY_RECT = COMPANY.get_rect(center=(gs.SCREEN_WIDTH / 2, 600))

        RIGHTS = self.font.render('1982 1986 namco ltd.', True, gs.WHITE)
        RIGHTS_RECT = RIGHTS.get_rect(center=(gs.SCREEN_WIDTH / 2, 675))

        RESERVED = self.font.render('ALL RIGHTS RESERVED', True, gs.WHITE)
        RESERVED_RECT = RESERVED.get_rect(center=(gs.SCREEN_WIDTH / 2, 725))

        # Render and position the flag sprite
        flag = self.assets.objects['Flags'][0]
        scaled_flag = py.transform.scale(flag, (50, 50))
        if self.flag_position == 0:
            flag_rect = scaled_flag.get_rect(center=(gs.SCREEN_WIDTH / 2 - 150, 500))
        else:
            flag_rect = scaled_flag.get_rect(center=(gs.SCREEN_WIDTH / 2 - 150, 550))

        # Draw the logo
        for logo in self.groups['Logo']:
            logo_x = gs.SCREEN_WIDTH / 2 - logo.rect.width / 2
            logo_y = gs.SCREEN_HEIGHT / 3 - logo.rect.height / 2
            self.window.blit(logo.image, (logo_x, logo_y))

        # Draw all menu elements on the screen
        self.window.blit(HI_SCORE_TEXT, HI_SCORE_RECT)
        self.window.blit(HI_SCORE_DISPLAY_TEXT, HI_SCORE_DISPLAY_RECT)
        #self.window.blit(UP1_TEXT, UP1_RECT)
        #self.window.blit(UP1_SCORE_TEXT, UP1_SCORE_RECT)
        #self.window.blit(UP2_TEXT, UP2_RECT)
        #self.window.blit(UP2_SCORE_TEXT, UP2_SCORE_RECT)
        #self.window.blit(PLAYER_NUM_1, PLAYER_NUM_1_RECT)
        self.window.blit(ENTER, ENTER_RECT)
        self.window.blit(COMPANY, COMPANY_RECT)
        self.window.blit(RIGHTS, RIGHTS_RECT)
        self.window.blit(RESERVED, RESERVED_RECT)
        #self.window.blit(scaled_flag, flag_rect)

        py.display.flip()  # Update the display

    def update(self):
        """
        Update the main menu state.

        This method is currently a placeholder for future updates.
        """
        pass

    def runscreen(self):
        """
        Run the main menu screen.

        This method handles the main menu loop, including input handling and drawing.
        """
        while self.run:  # Run the loop while the menu is active
            self.input()  # Handle user input
            self.draw()  # Draw the menu elements