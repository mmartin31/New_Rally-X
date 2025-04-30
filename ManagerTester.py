import pygame as py
from StartScreen import MainMenu
from GameScreen import NewRallyX
from InstructionsScreen import Instructions
from CastScreen import CastScreen
from ScreenManager import ScreenManager
from ChallengeStage import ChallengeScreen
from HiScoreScreen import HiScoreScreen
import Settings as gs

def main():
    py.init()  # Initialize Pygame
    window = py.display.set_mode((gs.SCREEN_WIDTH, gs.SCREEN_HEIGHT))
    clock = py.time.Clock()
    running = True

    screen_manager = ScreenManager(window)
    main_menu = MainMenu(window)
    instructions = Instructions(window)
    cast_screen = CastScreen(window)
    challenge_screen = ChallengeScreen(window)
    game = None

    screen_manager.add_screen('main_menu', main_menu)
    screen_manager.add_screen('instructions', instructions)
    screen_manager.add_screen('cast_screen', cast_screen)
    screen_manager.add_screen('challenge_screen', challenge_screen)
    screen_manager.set_screen('main_menu')

    try:
        while running:
            running = screen_manager.handle_events()

            if not main_menu.run and screen_manager.current_screen == main_menu:
                screen_manager.set_screen('instructions')

            if not instructions.run and screen_manager.current_screen == instructions:
                screen_manager.set_screen('cast_screen')

            if not cast_screen.run and screen_manager.current_screen == cast_screen:
                game = NewRallyX(window)
                screen_manager.add_screen('game', game)
                screen_manager.set_screen('game')
                #screen_manager.current_screen.isPause = False

            if not game.run and screen_manager.current_screen == game:
                player_score = game.send_player_score()
                score_screen = HiScoreScreen(window, player_score)
                screen_manager.add_screen('scores_screen', score_screen)
                screen_manager.set_screen('scores_screen')

            if not score_screen.run and screen_manager.current_screen == score_screen:

                screen_manager.set_screen('main_menu')

            clock.tick(60)
    finally:
        py.quit()  # Ensure Pygame quits properly

main()