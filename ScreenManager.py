import pygame as py

class ScreenManager:
    """
    Class to manage and switch between different screens in the game.

    This class handles the addition of screens, switching between them, and
    delegating input handling to the currently active screen.

    Attributes:
        window (pygame.Surface): The main Pygame window surface where screens are displayed.
        screens (dict): A dictionary storing screens by their names.
        current_screen (object): The currently active screen object.
    """

    def __init__(self, window):
        """
        Initialize the ScreenManager object.

        :param window: The Pygame window surface where screens will be displayed.
        """
        py.init()  # Initialize Pygame
        self.window = window  # The main game window
        self.screens = {}  # Dictionary to store screens by name
        self.current_screen = None  # The currently active screen

    def add_screen(self, name, screen):
        """
        Add a screen to the manager.

        :param name: The name of the screen (used as a key in the dictionary).
        :param screen: The screen object to be added.
        """
        self.screens[name] = screen  # Add the screen to the dictionary

    def set_screen(self, name):
        """
        Set the current screen to the specified screen.

        :param name: The name of the screen to activate.
        """
        if name in self.screens:  # Check if the screen exists
            self.current_screen = self.screens[name]  # Set the current screen
            self.current_screen.run = True  # Mark the screen as active
            self.current_screen.runscreen()  # Call the screen's main run method

    def handle_events(self):
        """
        Handle Pygame events and delegate input to the current screen.

        :return: False if the user quits the game, True otherwise.
        """
        for event in py.event.get():  # Iterate through all Pygame events
            if event.type == py.QUIT:  # Check if the user closes the window
                return False
            if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:  # Check if the Escape key is pressed
                return False
            if self.current_screen:  # If a screen is active
                self.current_screen.input()  # Delegate input handling to the current screen
        return True  # Continue running the game