import pygame as py
import Settings as gs
import time

class Instructions:
    """
    Represents the instructions screen in the game.

    Attributes:
        window (pygame.Surface): The surface to draw the instructions screen on.
        run (bool): A flag to control the instructions screen loop.
        font (pygame.font.Font): The font used for rendering text.
        text (list): A list of instruction lines to display on the screen.
        delay (float): The delay between each character animation.
        isAnimate (bool): A flag to control whether the text is animated.
        y_offset (int): The vertical offset for positioning text.
        anim_index (int): The index of the current line being animated.
        rendered_text (pygame.Surface): The currently rendered text surface.
        text_rect (pygame.Rect): The rectangle for positioning the rendered text.
    """

    def __init__(self, surface):
        """
        Initialize the instructions screen.

        :param surface: The surface to draw the instructions screen on.
        """
        py.init()
        self.window = surface  # The game window surface
        self.run = False  # Flag to control the instructions screen loop
        self.font = py.font.Font(gs.font, 32)  # Font for rendering text
        self.text = [  # List of instruction lines to display
            'INSTRUCTIONS',
            'BY DODGING RED CARS',
            'AND ROCKS.',
            'CLEAR 10 FLAGS',
            'BEFORE FUEL RUNS OUT.',
            'ARROW KEYS TO MOVE',
            'SPACE KEY TO DEPLOY SMOKE',
            'PRESS ENTER TO CONTINUE'
        ]
        self.delay = 0.1  # Delay between each character animation
        self.isAnimate = True  # Flag to control text animation
        self.y_offset = 100  # Vertical offset for drawing text
        self.anim_index = 0  # Index of the current line being animated

    def input(self):
        """
        Handle user input to navigate the instructions screen.
        """
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()  # Quit pygame
                exit()  # Exit the program to prevent further execution
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    py.quit()  # Quit pygame
                    exit()  # Exit the program
                if event.key == py.K_RETURN:
                    self.run = False  # Exit the instructions screen if Enter is pressed

    def draw(self):
        """
        Draw the instructions screen, including animated or static text.
        """
        self.window.fill(gs.LIGHT_ORANGE)  # Clear the screen with a background color

        if self.isAnimate:
            # Animate the current line of text
            if self.anim_index < len(self.text):
                if self.anim_index == 0:
                    color = gs.RED  # Highlight the title in red
                else:
                    color = gs.WHITE  # Use white for other lines
                self.animate(self.text[self.anim_index], self.y_offset, color)
                self.y_offset += self.font.get_height() * 2  # Add spacing between lines
                self.anim_index += 1  # Move to the next line
            else:
                # Reset animation state after all lines are animated
                self.y_offset = 100
                self.isAnimate = False
        else:
            # Display all text statically after animation is complete
            for i in range(len(self.text)):
                if i == 0:
                    color = gs.RED  # Highlight the title in red
                else:
                    color = gs.WHITE  # Use white for other lines
                t_box = self.font.render(self.text[i], True, color)
                t_box_rect = t_box.get_rect(center=(gs.SCREEN_WIDTH / 2, self.y_offset))
                self.window.blit(t_box, t_box_rect)
                self.y_offset += self.font.get_height() * 2  # Add spacing between lines
            self.y_offset = 100  # Reset vertical offset for future draws
        py.display.flip()  # Update the display

    def animate(self, s, y_cord, color):
        """
        Animate a single line of text character by character.

        :param s: The string to animate.
        :param y_cord: The vertical position to draw the text.
        :param color: The color of the text.
        """
        for i in range(len(s) + 1):
            self.window.fill(gs.LIGHT_ORANGE)  # Clear the screen with a background color

            # Draw previously animated text
            y_offset = 100
            for j in range(self.anim_index):
                if j == 0:
                    prev_color = gs.RED  # Highlight the title in red
                else:
                    prev_color = gs.WHITE  # Use white for other lines
                prev_text = self.font.render(self.text[j], True, prev_color)
                prev_text_rect = prev_text.get_rect(center=(gs.SCREEN_WIDTH / 2, y_offset))
                self.window.blit(prev_text, prev_text_rect)
                y_offset += self.font.get_height() * 2  # Add spacing between lines

            # Render the current text up to the current character
            self.rendered_text = self.font.render(s[:i], True, color)
            self.text_rect = self.rendered_text.get_rect(center=(gs.SCREEN_WIDTH / 2, y_cord))
            self.window.blit(self.rendered_text, self.text_rect)
            py.display.flip()  # Update the display
            time.sleep(self.delay)  # Delay for animation effect

        # Ensure the full text is rendered after the loop
        self.rendered_text = self.font.render(s, True, color)
        self.text_rect = self.rendered_text.get_rect(center=(gs.SCREEN_WIDTH / 2, y_cord))
        self.window.blit(self.rendered_text, self.text_rect)
        py.display.flip()  # Update the display

    def runscreen(self):
        """
        Run the instructions screen loop, handling input and rendering.
        """
        while self.run:
            self.input()  # Handle user input
            self.draw()  # Render the instructions screen