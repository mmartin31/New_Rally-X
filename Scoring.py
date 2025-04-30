class Scoring:
    """
    Class to manage scoring and high scores for the game.

    This class handles the calculation of points, management of flags and fuel,
    and loading/saving of high scores from a file.

    Attributes:
        flag_points (int): Points awarded per flag collected.
        flags_started (int): The number of flags at the start of the game.
        flags_remaining (int): The number of flags remaining in the game.
        fuel_remaining (int): The amount of fuel remaining for the player.
        isMultiplier (bool): Indicates if a score multiplier is active.
        file (str): The file path where high scores are stored.
        high_scores (list): A list of high scores as tuples (score, initials).
        top_score (int): The highest score from the high scores list.
    """

    def __init__(self, file_path='Scores.txt'):
        """
        Initialize the Scoring object.

        :param file_path: The path to the file where high scores are stored.
        """
        self.flag_points = 100  # Points awarded per flag
        self.flags_started = 10  # Number of flags at the start of the game
        self.flags_remaining = 10  # Number of flags remaining
        self.fuel_remaining = 100  # Amount of fuel remaining
        self.isMultiplier = False  # Flag to indicate if a score multiplier is active
        self.file = file_path  # File path for high scores
        self.high_scores = self.load_scores()  # Load high scores from the file
        self.top_score = self.get_top_score()  # Get the top score from the high scores

    def calculate_points(self):
        """
        Calculate the points based on flags collected and multipliers.

        :return: The total points calculated.
        """
        multiplier = self.flags_started + 1 - self.flags_remaining  # Calculate the multiplier
        if self.isMultiplier:  # Double the multiplier if the multiplier flag is active
            multiplier *= 2
        return self.flag_points * multiplier  # Return the total points

    def add_points(self):
        """
        Add points based on whether a multiplier is active.

        :return: The points to be added.
        """
        if self.isMultiplier:  # Return higher points if the multiplier is active
            return 20
        else:  # Return standard points otherwise
            return 10

    def get_flags_at_start(self, start_flags):
        """
        Set the number of flags at the start of the game.

        :param start_flags: The number of flags at the start.
        """
        self.flags_started = start_flags

    def load_scores(self):
        """
        Load high scores from the file.

        :return: A list of high scores as tuples (score, initials).
        """
        high_scores = []
        with open(self.file, 'r') as file:  # Open the file in read mode
            for line in file.readlines():  # Read each line in the file
                score, initial = line.strip().split(', ')  # Split the line into score and initials
                high_scores.append((int(score), initial))  # Append the score and initials as a tuple
        return high_scores

    def save_scores(self):
        """
        Save the high scores to the file.
        """
        with open(self.file, 'w') as file:  # Open the file in write mode
            for score, initial in self.high_scores:  # Write each high score to the file
                file.write(f"{score}, {initial}\n")

    def get_top_score(self):
        """
        Get the top score from the high scores list.

        :return: The highest score.
        """
        return self.high_scores[0][0]  # Return the first score in the sorted high scores list

    def check_high_score(self, player_score):
        """
        Check if the player's score is a new high score and update the list.

        :param player_score: The player's score to check.
        :return: A tuple (is_high_score, position) where:
                 - is_high_score: True if the score is a new high score, False otherwise.
                 - position: The position of the new high score in the list, or -1 if not a high score.
        """
        for n in range(len(self.high_scores)):  # Iterate through the high scores
            if player_score > self.high_scores[n][0]:  # Check if the player's score is higher
                new_score = (player_score, self.high_scores[-1][1])  # Create a new score entry
                self.high_scores.insert(n, new_score)  # Insert the new score at the correct position
                self.high_scores.pop()  # Remove the lowest score to maintain the list size
                self.save_scores()  # Save the updated high scores to the file
                return True, n  # Return True and the position of the new high score
        return False, -1  # Return False if the score is not a high score