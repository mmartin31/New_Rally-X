import time
import pygame
import Settings as gs
from Player import Player, Smoke_Screen, Character
from Assets import Assets
from HUD import HUD
from Maze import Maze
from Flags import Flag, Point
from Scoring import Scoring
from Enemy import Enemy, Crash
import random
import math

window = pygame.display.set_mode((gs.SCREEN_WIDTH, gs.SCREEN_HEIGHT))

class NewRallyX:
    """
    Class representing the New Rally X game, including game logic, rendering, and player interactions.

    Attributes:
        groups (dict): A dictionary of sprite groups for managing game objects (e.g., player, flags, blocks).
        window (pygame.Surface): The surface to draw the game on.
        clock (pygame.time.Clock): The game clock for managing frame rate.
        start_time (int): The time when the game started, used for tracking elapsed time.
        run (bool): A flag to control the main game loop.
        font (pygame.font.Font): The font used for rendering text in the game.
        assets (Assets): The game assets, including images and sounds.
        scoring (Scoring): The scoring system for the game.
        HUD (HUD): The heads-up display for showing game information (e.g., score, fuel).
        Maze (Maze): The maze object representing the current level layout.
        player_start_x (int): The starting x-coordinate for the player.
        player_start_y (int): The starting y-coordinate for the player.
        Player (Player): The player object controlled by the user.
        enemies (list): A list of enemy objects in the game.
        flags (list): A list of flag objects placed in the maze.
        current_player (int): The ID of the current player (1 or 2).
        isPause (bool): A flag indicating whether the game is paused.
        crash_handled (bool): A flag to track whether a crash event has been handled.
        level_complete (bool): A flag indicating whether the current level is complete.
        game_over (bool): A flag indicating whether the game is over.
        camera_offset (tuple): The offset for the camera to follow the player.
    """

    def __init__(self, surface):
        """
        Initialize the game.

        :param surface: The surface to draw the game on.
        """
        pygame.init()
        self.groups = {
            "player": pygame.sprite.Group(),
            "flags": pygame.sprite.Group(),
            "blocks": pygame.sprite.Group(),
            "points": pygame.sprite.Group(),
            "objects": pygame.sprite.Group(),
            "enemy": pygame.sprite.Group()
        }

        self.window = surface
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.run = True
        self.font = pygame.font.Font(gs.font, 32)
        self.assets = Assets()
        self.scoring = Scoring()
        self.HUD = HUD(self.assets, 1)
        self.HUD.hi_score_display = self.scoring.get_top_score()
        self.Maze = Maze(self.groups["blocks"], self.assets, gs.maze1, 1)

        # Initialize player starting position
        self.player_start_x = 11 * gs.MAZE_SIZE + (gs.SIZE // 1.5)
        self.player_start_y = 19 * gs.MAZE_SIZE + (gs.SIZE // 1.5)
        self.Player = Player(self.groups["player"], self.player_start_x, self.player_start_y, self.assets, 1)

        # Initialize enemies and flags
        self.enemies = []
        self.generate_enemies()
        self.Maze.build_maze()
        self.flags = []
        self.place_flags()
        self.determine_flag_type()

        # Game state variables
        self.current_player = 1
        self.isPause = False
        self.crash_handled = False
        self.level_complete = False
        self.game_over = False

    def input(self):
        """
        Handle user input for controlling the game and player actions.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_1:
                    self.Player.ID = 1
                    self.HUD.number_players = 1
                if event.key == pygame.K_2:
                    self.Player.ID = 2
                    self.HUD.number_players = 2
                if event.key == pygame.K_p:
                    self.isPause = not self.isPause
                if event.key == pygame.K_SPACE and not self.isPause:
                    # Create a smoke screen and reduce fuel
                    self.Player.create_smoke_screen(self.groups['objects'], self.assets, self.Maze.maze_matrix)
                    self.HUD.fuel_percentage -= 0.01
        if self.isPause:
            return
        # Handle player movement and interactions
        self.Player.input(self.groups['blocks'], self.groups['objects'], self.assets, self.Maze.maze_matrix)

    def generate_enemies(self):
        """
        Generate enemy cars based on the current level.
        """
        enemies = 0
        if self.HUD.level == 1:
            enemies = 1
        elif self.HUD.level == 2:
            enemies = 2
        elif self.HUD.level in [3, 4]:
            enemies = 3
        elif self.HUD.level in [5, 6]:
            enemies = 4
        elif self.HUD.level in [7, 8]:
            enemies = 5
        elif self.HUD.level in [9, 10]:
            enemies = 6
        else:
            enemies = 7

        for n in range(enemies):
            # Set enemy starting positions
            enemy_start_x = gs.enemy_Car_starts[n][0] * gs.MAZE_SIZE + (gs.SIZE // 1.5)
            enemy_start_y = gs.enemy_Car_starts[n][1] * gs.MAZE_SIZE + (gs.SIZE // 1.5)

            enemy = Enemy(self.groups["enemy"], enemy_start_x, enemy_start_y, self.assets)
            if n in [5, 6]:
                enemy.image = self.assets.enemy_car['LEFT'][0]
            self.enemies.append(enemy)

    def update(self):
        """
        Update the game state, including player, enemies, flags, and HUD.
        """
        self.input()
        if not self.isPause:
            # Update player and enemies
            self.Player.auto_move(self.Maze.maze_matrix, self.groups['blocks'])
            self.Player.animate_turn()
            for enemy_car in self.enemies:
                enemy_car.chase_player(self.Player, self.groups['blocks'])
                enemy_car.auto_move(self.Maze.maze_matrix, self.groups['blocks'])
                enemy_car.animate_turn()

            # Update flags, radar, and fuel
            self.update_flags()
            self.update_radar()
            self.update_fuel()

            # Update HUD and scores
            self.HUD.update_score(self.Player)
            if self.Player.score > self.HUD.hi_score_display:
                self.HUD.hi_score_display = self.Player.score

            # Update points and objects
            for point in self.groups['points']:
                point.update()
            for object in self.groups['objects']:
                object.update()

    def update_radar(self):
        """
        Update the radar with the positions of flags, the player, and enemies.
        """
        radar_objects = []
        for flag in self.flags:
            if not flag.isCollected:
                if flag.isSpec:
                    radar_objects.append((flag.rect.x // gs.MAZE_SIZE, flag.rect.y // gs.MAZE_SIZE, gs.GREEN))
                else:
                    radar_objects.append((flag.rect.x // gs.MAZE_SIZE, flag.rect.y // gs.MAZE_SIZE, gs.YELLOW))
        radar_objects.append((self.Player.rect.x // gs.MAZE_SIZE, self.Player.rect.y // gs.MAZE_SIZE, gs.WHITE))
        for enemy in self.groups['enemy']:
            radar_objects.append((enemy.rect.x // gs.MAZE_SIZE, enemy.rect.y // gs.MAZE_SIZE, gs.RED))
        self.HUD.update_radar(radar_objects)

    def update_fuel(self):
        """
        Update the player's fuel level and adjust speed based on remaining fuel.
        """
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000  # Convert milliseconds to seconds

        # Reduce fuel based on elapsed time
        fuel = self.HUD.fuel_percentage
        self.HUD.fuel_percentage -= 0.01 * elapsed_time
        self.scoring.fuel_remaining = self.HUD.fuel_percentage

        # Adjust player speed based on fuel level
        if self.HUD.fuel_percentage > 0 and not self.isPause:
            self.Player.speed = 6 + (2 * self.HUD.fuel_percentage)
        elif self.HUD.fuel_percentage == 0:
            self.complete_level()
        elif not self.isPause:
            self.HUD.fuel_percentage = 0
            self.Player.speed = 0
        if self.isPause:
            self.HUD.fuel_percentage = fuel

        # Reset the start time for the next update
        self.start_time = current_time

    def update_flags(self):
        """
        Handle flag collection and scoring logic.
        """
        if self.flags:
            for flag in self.flags:
                if flag.isCollected:
                    if flag.isSpec:
                        self.scoring.isMultiplier = True
                    self.flags.remove(flag)
                    self.scoring.flags_remaining = len(self.flags)
                    point_x, point_y = flag.positions
                    point_sprite = Point(self.groups['points'], point_x, point_y, self.assets,
                                         self.scoring.flags_started - len(self.flags), self.scoring.isMultiplier)
                    self.groups['points'].add(point_sprite)
                    if flag.isLucky:
                        if len(self.flags) >= 1:
                            self.pause()
        else:
            self.drain_fuel_and_update_score()
            self.HUD.fuel_percentage = 0
            self.complete_level()

    def draw(self, countdown=None):
        """
        Render all game elements on the screen, with an optional countdown overlay.

        :param countdown: The countdown value to display (if any).
        """
        self.window.fill(gs.LIGHT_ORANGE)

        # Calculate camera offset based on player position
        self.camera_offset = self.camera_offset_player_position(self.Player.rect.center)
        self.window.scroll(self.camera_offset[0], self.camera_offset[1])

        # Draw blocks, objects, player, enemies, flags, and points
        for group_name in ["blocks", "objects", "player", "enemy", "flags", "points"]:
            for sprite in self.groups[group_name]:
                adjusted_rect = sprite.rect.move(-self.camera_offset[0], -self.camera_offset[1])
                self.window.blit(sprite.image, adjusted_rect)

        # Display game over text if applicable
        if self.game_over:
            GAME = self.font.render('GAME', True, gs.WHITE)
            GAME_RECT = GAME.get_rect(center=(gs.SCREEN_WIDTH / 2, gs.SCREEN_HEIGHT / 2))
            OVER = self.font.render('OVER', True, gs.WHITE)
            OVER_RECT = OVER.get_rect(center=(gs.SCREEN_WIDTH / 2, gs.SCREEN_HEIGHT / 2 + 32))
            self.window.blit(GAME, GAME_RECT)
            self.window.blit(OVER, OVER_RECT)

        # Display countdown overlay if provided
        if countdown is not None:
            countdown_text = self.font.render(str(countdown), True, gs.WHITE)
            countdown_rect = countdown_text.get_rect(center=(gs.SCREEN_WIDTH / 2, gs.SCREEN_HEIGHT / 2))
            self.window.blit(countdown_text, countdown_rect)

        # Update HUD and flip the display
        self.HUD.update(self.window)
        pygame.display.flip()

    def camera_offset_player_position(self, player_pos):
        """
        Calculate the camera offset based on the player's position.

        :param player_pos: The player's position.
        :return: The camera offset.
        """
        camera_offset = (
            player_pos[0] - (gs.SCREEN_WIDTH - self.HUD.HUD_WIDTH) // 2,
            player_pos[1] - gs.SCREEN_HEIGHT // 2
        )

        camera_offset = (
            max(0, min(camera_offset[0], gs.MAZE_WIDTH - (gs.SCREEN_WIDTH - self.HUD.HUD_WIDTH))),
            max(0, min(camera_offset[1], gs.MAZE_HEIGHT - gs.SCREEN_HEIGHT))
        )
        return camera_offset

    def place_flags(self):
        """
        Place flags in the maze at random positions within a grid, ensuring only one flag per grid cell.

        Flags are distributed across the maze in a grid-like structure, avoiding the player's starting grid cell.
        Each grid cell can contain at most one flag, and the positions are chosen randomly within the cell.
        """
        maze = self.Maze.maze_matrix
        grid_positions = []
        grid_col_size = gs.COLS // 4  # Divide the maze into 4x4 grid cells horizontally
        grid_row_size = gs.ROWS // 4  # Divide the maze into 4x4 grid cells vertically

        # Calculate the player's starting grid cell
        start_x = 11 * gs.MAZE_SIZE + (gs.SIZE // 1.5)
        start_y = 19 * gs.MAZE_SIZE + (gs.SIZE // 1.5)
        player_start_grid_x = start_x // gs.MAZE_SIZE // grid_col_size
        player_start_grid_y = start_y // gs.MAZE_SIZE // grid_row_size

        # Divide the maze into a grid and collect possible positions for flags
        for y in range(0, gs.ROWS, grid_row_size):
            for x in range(0, gs.COLS, grid_col_size):
                cell_positions = []
                grid_x = x // grid_col_size
                grid_y = y // grid_row_size
                if grid_x == player_start_grid_x and grid_y == player_start_grid_y:
                    continue  # Skip the player's starting grid cell
                for cell_y in range(y, y + grid_row_size):
                    for cell_x in range(x, x + grid_col_size):
                        if cell_y < gs.ROWS and cell_x < gs.COLS and maze[cell_y][cell_x] == " ":
                            cell_positions.append((cell_x, cell_y))
                if cell_positions:
                    grid_positions.append(cell_positions)

        # Randomly select one position from each grid cell for the flags
        for flag in range(10):  # Place up to 10 flags
            if not grid_positions:
                break  # Stop if there are no more valid grid positions
            cell_positions = random.choice(grid_positions)
            pos = random.choice(cell_positions)
            grid_positions.remove(cell_positions)  # Ensure only one flag per grid cell
            flag_x = pos[0] * gs.MAZE_SIZE + (gs.MAZE_SIZE // 2)
            flag_y = pos[1] * gs.MAZE_SIZE + (gs.MAZE_SIZE // 2)
            flag = Flag(self.groups['flags'], flag_x, flag_y, self.assets)
            self.flags.append(flag)

    def determine_flag_type(self):
        """
        Determine the type of each flag (Normal, Special, or Lucky).

        Two flags are randomly selected to be Special and Lucky. The rest remain Normal.
        """
        selected_indices = set()
        while len(selected_indices) < 2:
            selected_indices.add(random.randint(0, 9))  # Randomly select two unique indices

        spec_flag, lucky_flag = selected_indices
        self.flags[spec_flag].change_type('Special')  # Set one flag as Special
        self.flags[lucky_flag].change_type('Lucky')  # Set another flag as Lucky

    def drain_fuel_and_update_score(self):
        """
        Gradually drain the player's fuel and update the score.

        This function animates the fuel depletion and increments the player's score based on the remaining fuel.
        """
        initial_fuel = self.HUD.fuel_percentage  # Store the initial fuel level
        points_per_frame = self.scoring.add_points()  # Points to add per frame
        frames = int(initial_fuel * 100)  # Number of frames for the animation

        for frame in range(frames):
            self.HUD.fuel_percentage -= 1 / 100  # Decrease fuel gradually
            self.Player.score += points_per_frame  # Increment the player's score
            self.HUD.update_score(self.Player)  # Update the HUD with the new score
            self.draw()  # Redraw the screen to reflect changes
            self.clock.tick(gs.FPS // 3)  # Slow down the animation for visual effect

        # Restore the initial fuel level and update the scoring system
        self.HUD.fuel_percentage = initial_fuel
        self.scoring.fuel_remaining = initial_fuel
        self.isPause = False  # Resume the game after the animation

    def pause(self):
        """
        Pause the game and drain fuel while updating the score.

        This function is triggered when the player collects a Lucky flag.
        """
        self.Player.speed = 0  # Stop the player's movement
        self.isPause = True  # Set the game to paused state
        self.drain_fuel_and_update_score()  # Drain fuel and update the score

    def crash(self, enemy):
        """
        Handle the crash event when the player collides with an enemy.

        :param enemy: The enemy object the player collided with.
        """
        if not self.crash_handled:  # Check if the crash has already been handled
            self.isPause = True  # Pause the game
            self.Crash = Crash(self.groups['objects'], enemy.rect.x + 48, enemy.rect.y + 48, self.assets)
            for all_enemies in self.enemies:
                all_enemies.kill()  # Remove all enemies from the game
            self.Player.image = pygame.Surface((0, 0))  # Set the player's image to an empty surface
            self.Player.is_crashed = True  # Set a flag to indicate the player has crashed
            if self.Player.lives > 0:
                self.Player.lives -= 1  # Decrement the player's lives
                self.HUD.get_player_lives(self.Player)  # Update the HUD with the remaining lives
            if self.Player.lives == 0:
                self.game_over = True  # End the game if no lives are left
            self.crash_handled = True  # Set the flag to indicate the crash has been handled

            if not self.game_over:
                # Draw the crash animation
                self.draw()
                pygame.display.flip()
                pygame.time.delay(3000)  # Delay to show the crash animation for 3 seconds
                self.isPause = False  # Resume the game
            else:
                # Draw the game over screen
                self.draw()
                pygame.display.flip()
                pygame.time.delay(3000)  # Delay to show the game over screen for 3 seconds
                self.run = False  # Stop the game loop

    def crash_reset(self):
        """
        Reset the game state after a crash.

        This function resets the player's position, image, and speed, regenerates enemies,
        and restores the fuel and radar. It ensures the game can continue after a crash.
        """
        pygame.event.clear()
        self.Crash.kill()  # Remove the crash effect
        self.Player.animating = False
        self.Player.image = self.assets.player_car['RIGHT'][0]  # Reset player image
        self.Player.direction = 'RIGHT'  # Reset player direction
        self.Player.speed = 6
        self.Player.rect.center = (self.player_start_x, self.player_start_y)  # Reset player position
        self.Player.snap_to_grid()
        self.enemies = []  # Clear the list of enemies
        for enemy in self.groups['enemy']:
            enemy.kill()  # Remove all enemy sprites
        self.generate_enemies()  # Regenerate enemies
        self.HUD.fuel_percentage = 1.00  # Restore full fuel
        self.update_radar()  # Update the radar with new positions
        self.Player.is_crashed = False  # Reset crash flag
        self.isPause = False  # Resume the game
        self.scoring.get_flags_at_start(len(self.flags))  # Update scoring with remaining flags
        self.scoring.isMultiplier = False  # Reset score multiplier

    def complete_level(self):
        """
        Handle the completion of a level.

        This function stops the player and enemies, pauses the game, and prepares for the next level.
        """
        self.Player.speed = 0  # Stop the player
        for enemy in self.groups['enemy']:
            enemy.kill()  # Remove all enemy sprites
        self.isPause = True  # Pause the game
        for enemy in self.enemies:
            enemy.speed = 0  # Stop all enemies
        self.crash_handled = False  # Reset crash flag
        if not self.level_complete:
            self.level_complete = True  # Mark the level as complete

    def new_level(self):
        """
        Initialize a new level.

        This function resets the player's position, regenerates enemies and flags, and updates the HUD.
        """
        pygame.event.clear()

        # Select the maze based on the current level
        if self.HUD.level % 2 == 1:
            maze_layout = gs.maze2  # Use maze2 for even levels
            maze_ID = 2
        else:
            maze_layout = gs.maze1  # Use maze1 for odd levels
            maze_ID = 1

        # Clear the blocks group to remove the old maze
        for block in self.groups['blocks']:
            block.kill()

        # Update the Maze object with the new layout
        self.Maze = Maze(self.groups['blocks'], self.assets, maze_layout, maze_ID)
        self.Maze.build_maze()

        # Reset player position and attributes
        self.Player.animating = False
        self.Player.image = self.assets.player_car['RIGHT'][0]
        self.Player.direction = 'RIGHT'
        self.Player.speed = 8
        self.Player.rect.center = (self.player_start_x, self.player_start_y)
        self.Player.snap_to_grid()


        # Increment the level and regenerate enemies and flags
        self.HUD.level += 1
        self.enemies = []
        for enemy in self.groups['enemy']:
            enemy.kill()
        self.generate_enemies()

        # Restore fuel and place new flags
        self.HUD.fuel_percentage = 1.00
        self.flags = []
        self.place_flags()
        self.determine_flag_type()

        # Reset game state
        self.isPause = False
        self.scoring.isMultiplier = False
        self.countdown(3)

    def countdown(self, seconds):
        """
        Display a countdown timer on the screen.

        :param seconds: The number of seconds for the countdown.
        """
        for i in range(seconds, 0, -1):
            self.draw(countdown=i)  # Pass the countdown value to the draw method
            pygame.time.delay(1000)  # Wait for 1 second

        # Ensure the player moves right after the countdown
        self.Player.direction = 'RIGHT'
        self.Player.image = self.assets.player_car['RIGHT'][0]
    def send_player_score(self):
        """
        Send the player's score to the high score screen.

        :return: The player's current score.
        """
        return self.Player.score

    def runscreen(self):
        """
        Run the main game loop.

        This function handles input, updates the game state, checks for collisions, and renders the game.
        """
        self.countdown(3)  # Display a countdown before starting the game
        while self.run:
            self.input()  # Handle user input
            self.Player.check_flag_collision(self.flags, self.scoring.calculate_points())  # Check flag collisions
            for enemy in self.enemies:
                enemy.check_smoke_collision(self.groups['objects'])  # Check if enemies collide with smoke
                if enemy.check_player_collision(self.Player):  # Check if an enemy collides with the player
                    self.crash(enemy)  # Handle the crash
                    self.crash_reset()  # Reset the game state after the crash

            self.update()  # Update the game state
            self.draw()  # Render the game
            self.clock.tick(gs.FPS)  # Limit the frame rate
            if not self.isPause:
                self.crash_handled = False  # Reset crash flag when the game is not paused
            if self.level_complete:
                self.new_level()  # Start a new level
                self.level_complete = False
        if self.game_over:
            self.run = False  # Stop the game loop if the game is over