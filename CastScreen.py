import pygame as py
import Settings as gs
import time
from Assets import Assets
from Player import Smoke_Screen

class CastScreen:
    """
    Class representing the Cast Screen, which displays various game elements
    (e.g., cars, checkpoints, and objects) with animations.

    Attributes:
        window (pygame.Surface): The surface to draw the Cast Screen on.
        assets (Assets): The game assets, including images and sounds.
        run (bool): A flag to control the screen loop.
        font (pygame.font.Font): The font used for rendering text.
        group (pygame.sprite.Group): A group for managing sprites.
        text (list): A list of text strings to display on the screen.
        objects (list): A list of objects (e.g., images) corresponding to the text.
        delay (float): The delay between animation steps.
        isAnimate (bool): A flag to control whether text is animated.
        y_offset (int): The vertical offset for positioning text.
        anim_index (int): The index of the current animation step.
        rendered_text (pygame.Surface): The currently rendered text surface.
        text_rect (pygame.Rect): The rectangle for positioning the rendered text.
    """

    def __init__(self, surface):
        """
        Initialize the CastScreen.

        :param surface: The surface to draw the Cast Screen on.
        """
        py.init()
        self.window = surface
        self.assets = Assets()  # Load game assets
        self.run = False  # Flag to control the screen loop
        self.font = py.font.Font(gs.font, 32)  # Font for rendering text
        self.group = py.sprite.Group()  # Group for managing sprites
        self.text = [
            'NEW RALLY-X',
            'CAST',
            'MY CAR',
            'RED CAR',
            'CHECK POINT',
            'SPECIAL CHECK POINT',
            'LUCKY CHECK POINT',
            'ROCK < DANGER ! >',
            'SMOKE SCREEN',
            'PRESS ENTER TO CONTINUE'
        ]  # List of text to display
        self.objects = [
            None,
            None,
            self.assets.player_car['UP'][0],
            self.assets.enemy_car['UP'][0],
            self.assets.objects['Flags'][0],
            self.assets.objects['Flags'][1],
            self.assets.objects['Flags'][2],
            create_spliced_image(self.assets.objects['Rock'], gs.SIZE),
            create_spliced_image(self.assets.objects['Smoke'], gs.SIZE),
            None
        ]  # Corresponding objects to display alongside the text
        self.delay = 0.1  # Delay for animation
        self.isAnimate = True  # Flag to control animation
        self.y_offset = 50  # Initial vertical offset for text
        self.anim_index = 0  # Index to track the current animation step

    def input(self):
        """
        Handle user input to control the Cast Screen.
        """
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()  # Quit the game
                exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    py.quit()  # Quit the game
                    exit()
                if event.key == py.K_RETURN:
                    self.run = False  # Exit the Cast Screen

    def draw(self):
        """
        Draw the Cast Screen, including text and objects.
        """
        self.window.fill(gs.LIGHT_ORANGE)  # Clear the screen with a background color

        if self.isAnimate:
            # Animate text one by one
            if self.anim_index < len(self.text):
                if self.anim_index == 0:
                    color = gs.RED  # Highlight the first text in red
                else:
                    color = gs.WHITE  # Default color for other text
                self.animate(self.text[self.anim_index], self.y_offset, color)
                self.y_offset += self.font.get_height() * 2  # Move to the next line
                self.anim_index += 1
            else:
                # Reset animation state after all text is displayed
                self.y_offset = 50
                self.isAnimate = False
        else:
            # Display all text and objects without animation
            for i in range(len(self.text)):
                if i == 0:
                    color = gs.RED  # Highlight the first text in red
                else:
                    color = gs.WHITE  # Default color for other text

                t_box = self.font.render(self.text[i], True, color)
                if i >= 2:
                    t_box_rect = t_box.get_rect(midleft=(gs.SCREEN_WIDTH / 2 - 200, self.y_offset))
                else:
                    t_box_rect = t_box.get_rect(center=(gs.SCREEN_WIDTH / 2, self.y_offset))

                # Draw the corresponding object if available
                if self.objects[i] is not None:
                    obj_rect = self.objects[i].get_rect(midright=(t_box_rect.left - 50, t_box_rect.centery))
                    self.window.blit(self.objects[i], obj_rect)

                self.window.blit(t_box, t_box_rect)
                self.y_offset += self.font.get_height() * 2
            self.y_offset = 50  # Reset vertical offset
        py.display.flip()  # Update the display

    def animate(self, s, y_cord, color):
        """
        Animate the display of a single line of text.

        :param s: The string to animate.
        :param y_cord: The vertical position to draw the text.
        :param color: The color of the text.
        """
        for i in range(len(s) + 1):
            self.window.fill(gs.LIGHT_ORANGE)  # Clear the screen

            # Draw previously animated text
            y_offset = 50
            for j in range(self.anim_index):
                if j == 0:
                    prev_color = gs.RED  # Highlight the first text in red
                else:
                    prev_color = gs.WHITE  # Default color for other text
                prev_text = self.font.render(self.text[j], True, prev_color)
                if j >= 2:
                    prev_text_rect = prev_text.get_rect(midleft=(gs.SCREEN_WIDTH / 2 - 200, y_offset))
                else:
                    prev_text_rect = prev_text.get_rect(center=(gs.SCREEN_WIDTH / 2, y_offset))

                # Draw the corresponding object if available
                if self.objects[j] is not None:
                    obj_rect = self.objects[j].get_rect(midright=(prev_text_rect.left - 50, prev_text_rect.centery))
                    self.window.blit(self.objects[j], obj_rect)

                self.window.blit(prev_text, prev_text_rect)
                y_offset += self.font.get_height() * 2

            # Render the current text
            self.rendered_text = self.font.render(s[:i], True, color)
            if self.anim_index >= 2:
                self.text_rect = self.rendered_text.get_rect(midleft=(gs.SCREEN_WIDTH / 2 - 200, y_cord))
            else:
                self.text_rect = self.rendered_text.get_rect(center=(gs.SCREEN_WIDTH / 2, y_cord))

            # Draw the corresponding object if available
            if self.objects[self.anim_index] is not None:
                obj_rect = self.objects[self.anim_index].get_rect(
                    midright=(self.text_rect.left - 50, self.text_rect.centery))
                self.window.blit(self.objects[self.anim_index], obj_rect)

            self.window.blit(self.rendered_text, self.text_rect)
            py.display.flip()  # Update the display
            time.sleep(self.delay)  # Pause for animation effect

        # Ensure the full text is rendered after the loop
        self.rendered_text = self.font.render(s, True, color)
        if self.anim_index >= 2:
            self.text_rect = self.rendered_text.get_rect(midleft=(gs.SCREEN_WIDTH / 2 - 200, y_cord))
        else:
            self.text_rect = self.rendered_text.get_rect(center=(gs.SCREEN_WIDTH / 2, y_cord))

        # Draw the corresponding object if available
        if self.objects[self.anim_index] is not None:
            obj_rect = self.objects[self.anim_index].get_rect(
                midright=(self.text_rect.left - 50, self.text_rect.centery))
            self.window.blit(self.objects[self.anim_index], obj_rect)

        self.window.blit(self.rendered_text, self.text_rect)
        py.display.flip()  # Update the display

    def runscreen(self):
        """
        Run the Cast Screen loop, handling input and drawing the screen.
        """
        while self.run:
            self.input()  # Handle user input
            self.draw()  # Draw the screen

def create_spliced_image(images, block_size):
    """
    Create a spliced image from a list of images.

    :param images: List of images to splice together.
    :param block_size: The size of each block.
    :return: A spliced and scaled image.
    """
    merged_image = py.Surface((block_size * 2, block_size * 2), py.SRCALPHA)
    merged_image.blit(images[0], (0, 0))
    merged_image.blit(images[1], (block_size, 0))
    merged_image.blit(images[2], (0, block_size))
    merged_image.blit(images[3], (block_size, block_size))
    crop_rect = py.Rect(32, 0, 96, 96)  # Define the cropping rectangle
    scaled_image = py.transform.scale(merged_image.subsurface(crop_rect), (64, 64))  # Scale the cropped image
    return scaled_image