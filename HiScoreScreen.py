import pygame as py
import Settings as gs
from Scoring import Scoring

class HiScoreScreen:
    """
    Represents the high score screen where the top 5 scores are displayed.
    Allows the player to input their initials if they achieve a new high score.

    Attributes:
        window (pygame.Surface): The surface to draw the high score screen on.
        run (bool): A flag to control the screen loop.
        font (pygame.font.Font): The font used for rendering text.
        text (str): The title text for the high score screen.
        rank (list): A list of rank labels (e.g., '1st', '2nd', etc.).
        Scores (Scoring): The scoring object to manage high scores.
        isNewScore (bool): Indicates if the player's score is a new high score.
        new_score_rank (int): The rank position of the new high score.
        scores_nums (list): A list of scores to display.
        names (list): A list of names/initials corresponding to the scores.
        y_offset (int): The vertical offset for positioning text.
        blink (bool): A flag to control the blinking effect for new high score input.
        blink_timer (int): The timestamp for managing the blinking effect.
        initials (str or None): The player's initials for a new high score (None if not applicable).
    """

    def __init__(self, surface, player_score):
        """
        Initialize the high score screen.

        :param surface: The surface to draw the high score screen on.
        :param player_score: The player's score to check against the high scores.
        """
        py.init()
        self.window = surface  # The game window surface
        self.run = True  # Flag to control the screen loop
        self.font = py.font.Font(gs.font, 32)  # Font for rendering text
        self.text = 'THE TOP 5 DRIVERS'  # Title text for the high score screen
        self.rank = ['RANK', '1st', '2nd', '3rd', '4th', '5th']  # Rank labels
        self.Scores = Scoring()  # Scoring object to manage high scores
        self.isNewScore, self.new_score_rank = self.Scores.check_high_score(player_score)  # Check if the score is a new high score
        self.scores_nums = ['Score'] + [score for score, initial in self.Scores.high_scores]  # List of scores
        self.names = ['Name'] + [initial for score, initial in self.Scores.high_scores]  # List of names/initials
        self.y_offset = 100  # Vertical offset for drawing text
        self.blink = True  # Flag for blinking effect
        self.blink_timer = py.time.get_ticks()  # Timer for blinking effect
        self.initials = '' if self.isNewScore else None  # Player initials (empty if new high score)

    def input(self):
        """
        Handle user input for navigating the high score screen and entering initials.
        """
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()  # Quit the game if the window is closed
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    py.quit()  # Quit the game if the Escape key is pressed
                if event.key == py.K_RETURN:
                    # Save initials and exit if Enter is pressed
                    if self.isNewScore and len(self.initials) == 3:
                        self.Scores.high_scores[self.new_score_rank] = (self.Scores.high_scores[self.new_score_rank][0], self.initials)
                        self.Scores.save_scores()  # Save the updated high scores
                        self.run = False
                    elif not self.isNewScore:
                        self.run = False  # Exit if not a new high score
                if self.isNewScore and event.unicode.isalpha() and len(self.initials) < 3:
                    self.initials += event.unicode.upper()  # Add a letter to the initials
                if self.isNewScore and event.key == py.K_BACKSPACE:
                    self.initials = self.initials[:-1]  # Remove the last letter from the initials

    def draw(self):
        """
        Render the high score screen, including the title, ranks, scores, and names.
        """
        self.window.fill(gs.LIGHT_ORANGE)  # Clear the screen with a background color
        y_offset = self.y_offset  # Start drawing from the vertical offset

        # Draw the main title text
        t_box = self.font.render(self.text, True, gs.RED)
        t_box_rect = t_box.get_rect(center=(gs.SCREEN_WIDTH / 2, y_offset))
        self.window.blit(t_box, t_box_rect)
        y_offset += self.font.get_height() * 2  # Add spacing below the title

        # Draw the rank, scores, and names
        for i in range(len(self.rank)):
            rank_color = gs.RED  # Color for rank labels
            score_color = gs.RED if i == 0 else gs.WHITE  # Color for scores
            name_color = gs.RED if i == 0 else gs.WHITE  # Color for names

            # Render and display the rank text
            rank_text = self.font.render(str(self.rank[i]), True, rank_color)
            rank_rect = rank_text.get_rect(midleft=(gs.SCREEN_WIDTH / 2 - 200, y_offset))
            self.window.blit(rank_text, rank_rect)

            if i < len(self.scores_nums):
                # Handle blinking effect for new high score
                if self.isNewScore and i == self.new_score_rank + 1:  # Adjust for header
                    current_time = py.time.get_ticks()
                    if current_time - self.blink_timer > 500:  # Toggle blink every 500ms
                        self.blink = not self.blink
                        self.blink_timer = current_time
                    if self.blink:
                        score_color = gs.YELLOW  # Highlight the new score
                        name_color = gs.YELLOW
                    else:
                        score_color = gs.WHITE
                        name_color = gs.WHITE

                # Render and display the score and name text
                score_text = self.font.render(str(self.scores_nums[i]), True, score_color)
                name_text = self.font.render(str(self.names[i]), True, name_color)

                # Handle initials input for new high score
                if self.isNewScore and i == self.new_score_rank + 1:
                    name_text = ''
                    for j in range(3):
                        if j < len(self.initials):
                            name_text += self.initials[j]  # Add entered initials
                        else:
                            if self.blink and j == len(self.initials):
                                name_text += '_'  # Add blinking underscore for the next letter
                            else:
                                name_text += ' '

                    name_text = self.font.render(name_text, True, name_color)

                # Position and display the score and name
                score_rect = score_text.get_rect(midright=(gs.SCREEN_WIDTH / 2 + 67, y_offset))
                name_rect = name_text.get_rect(midright=(gs.SCREEN_WIDTH / 2 + 200, y_offset))

                self.window.blit(score_text, score_rect)
                self.window.blit(name_text, name_rect)

            y_offset += self.font.get_height() * 2  # Add spacing between rows

        py.display.flip()  # Update the display

    def runscreen(self):
        """
        Run the high score screen loop, handling input and rendering.
        """
        while self.run:
            self.input()  # Handle user input
            self.draw()  # Render the screen