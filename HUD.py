import pygame as py
import Settings as gs

class HUD:
    """
    Represents the Heads-Up Display (HUD) in the game.

    Attributes:
        score_display_1UP (int): The score for Player 1.
        score_display_2UP (int): The score for Player 2.
        hi_score_display (int): The high score displayed on the HUD.
        radar_scale (int): The scale factor for radar objects.
        level (int): The current game level.
        lives (int): The number of lives remaining.
        number_players (int): The number of players in the game (1 or 2).
        font (pygame.font.Font): The font used for rendering text.
        life_image (pygame.Surface): The image used to represent a life icon.
        fuel_image (list): A list of images representing the fuel bar.
        fuel_percentage (float): The current fuel level as a percentage (1.00 = full).
        HUD_WIDTH (int): The width of the HUD area.
        radar_objects (list): A list of objects to display on the radar.
        start_time (int): The timestamp when the HUD was initialized.
    """

    def __init__(self, assets, players):
        """
        Initialize the HUD with game assets and player information.

        :param assets: The assets containing HUD images (e.g., life icons, fuel bar).
        :param players: The number of players in the game (1 or 2).
        """
        self.score_display_1UP = 0  # Score for Player 1
        self.score_display_2UP = 0  # Score for Player 2
        self.hi_score_display = 888888  # Default high score display
        self.radar_scale = 7  # Scale factor for radar objects
        self.level = 1  # Current game level
        self.lives = 3  # Number of lives remaining
        self.number_players = players  # Number of players
        self.font = py.font.Font(gs.font, 32)  # Font for rendering text
        self.life_image = assets.objects['Life'][0]  # Life icon image
        self.fuel_image = assets.objects['Fuel_Bar']  # Fuel bar images
        self.fuel_percentage = 1.00  # Fuel level as a percentage (1.00 = full)
        self.HUD_WIDTH = 400  # Width of the HUD area
        self.radar_objects = []  # List of objects to display on the radar
        self.start_time = py.time.get_ticks()  # Start time for HUD updates

    def update(self, surface):
        """
        Update the HUD and redraw it on the given surface.

        :param surface: The surface to draw the HUD on.
        """
        self.draw(surface)  # Redraw the HUD elements

    def update_score(self, player):
        """
        Update the score display for the specified player.

        :param player: The player object containing the updated score.
        """
        if player.ID == 1:
            self.score_display_1UP = player.score  # Update Player 1's score
        elif player.ID == 2:
            self.score_display_2UP = player.score  # Update Player 2's score
        self.get_player_lives(player)  # Update the lives display

    def get_player_lives(self, player):
        """
        Update the number of lives remaining for the given player.

        :param player: The player object containing the current lives count.
        """
        self.lives = player.lives  # Set the lives count from the player object

    def update_radar(self, objects):
        """
        Update the radar with the positions of objects (e.g., enemies, flags).

        :param objects: A list of tuples representing objects on the radar.
                        Each tuple contains (x, y, color).
        """
        self.radar_objects = objects  # Store the radar objects for rendering

    def draw(self, surface):
        """
        Draw the HUD elements on the given surface.

        :param surface: The surface to draw the HUD on.
        """
        # Draw the HUD background rectangle
        py.draw.rect(surface, gs.BLACK, (gs.SCREEN_WIDTH - self.HUD_WIDTH, 0, self.HUD_WIDTH, gs.SCREEN_HEIGHT))

        # Render and position the high score text
        HI_SCORE_TEXT = self.font.render("HI-SCORE", True, gs.RED)
        HI_SCORE_RECT = HI_SCORE_TEXT.get_rect(center=(gs.SCREEN_WIDTH - 200, 25))

        # Render and position the high score value
        HI_SCORE_DISPLAY_TEXT = self.font.render((str(self.hi_score_display)), True, gs.WHITE)
        HI_SCORE_DISPLAY_RECT = HI_SCORE_DISPLAY_TEXT.get_rect(right=gs.SCREEN_WIDTH - 20, top=50)

        # Render and position Player 1's score
        UP1_TEXT = self.font.render("1UP", True, gs.RED)
        UP1_RECT = UP1_TEXT.get_rect(center=(gs.SCREEN_WIDTH - 200, 125))
        UP1_SCORE_TEXT = self.font.render(str(self.score_display_1UP), True, gs.WHITE)
        UP1_SCORE_RECT = UP1_SCORE_TEXT.get_rect(right=gs.SCREEN_WIDTH - 20, top=150)

        # Render and position Player 2's score (if applicable)
        UP2_TEXT = self.font.render("2UP", True, gs.RED)
        UP2_RECT = UP2_TEXT.get_rect(center=(gs.SCREEN_WIDTH - 200, 225))
        UP2_SCORE_TEXT = self.font.render(str(self.score_display_2UP), True, gs.WHITE)
        UP2_SCORE_RECT = UP2_SCORE_TEXT.get_rect(right=gs.SCREEN_WIDTH - 20, top=250)

        # Render and position the current level text
        RND_TEXT = self.font.render("RND " + str(self.level), True, gs.WHITE)
        RND_RECT = RND_TEXT.get_rect(left=gs.SCREEN_WIDTH - 370, top=gs.SCREEN_HEIGHT - 50)

        # Calculate and draw the radar rectangle
        radar_width = (gs.COLS - 8) * self.radar_scale
        radar_height = (gs.ROWS - 8) * self.radar_scale
        radar_x = gs.SCREEN_WIDTH - radar_width  # Align to the right edge
        radar_y = 3 * (gs.SCREEN_HEIGHT - radar_height) / 4  # Center vertically
        py.draw.rect(surface, gs.BLUE, (radar_x, radar_y, radar_width, radar_height))

        # Draw objects on the radar
        for obj in self.radar_objects:
            obj_x, obj_y, color = obj
            radar_obj_x = radar_x + (obj_x * self.radar_scale) - (gs.MAZE_SIZE // 3.5)
            radar_obj_y = radar_y + (obj_y * self.radar_scale) - (gs.MAZE_SIZE // 3.5)
            py.draw.rect(surface, color, (radar_obj_x, radar_obj_y, self.radar_scale, self.radar_scale))

        # Draw the HUD elements on the surface
        surface.blit(HI_SCORE_TEXT, HI_SCORE_RECT)
        surface.blit(HI_SCORE_DISPLAY_TEXT, HI_SCORE_DISPLAY_RECT)
        surface.blit(UP1_TEXT, UP1_RECT)
        surface.blit(UP1_SCORE_TEXT, UP1_SCORE_RECT)
        if self.number_players == 2:
            surface.blit(UP2_TEXT, UP2_RECT)
            surface.blit(UP2_SCORE_TEXT, UP2_SCORE_RECT)
        surface.blit(RND_TEXT, RND_RECT)

        # Draw the life icons
        for i in range(self.lives):
            life_x = gs.SCREEN_WIDTH - 400 + 20 + i * 50  # Adjust position for each life icon
            life_y = gs.SCREEN_HEIGHT - 120
            surface.blit(self.life_image, (life_x, life_y))

        # Draw the fuel bar
        for n in range(len(self.fuel_image)):
            surface.blit(self.fuel_image[n], (gs.SCREEN_WIDTH - 328 + 20 + n * 64, 325))

        # Calculate and draw the fuel level rectangle
        max_fuel_width = len(self.fuel_image) * 64 - 20
        fuel_width = max_fuel_width * self.fuel_percentage
        fuel_x = gs.SCREEN_WIDTH - 296 - fuel_width + max_fuel_width
        fuel_bar_color = gs.RED if self.fuel_percentage <= 0.2 else gs.YELLOW
        py.draw.rect(surface, fuel_bar_color, (fuel_x, 357, fuel_width, 32))