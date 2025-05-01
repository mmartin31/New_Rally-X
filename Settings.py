import pygame as py



# Create a set size for the screen
SCREEN_HEIGHT = 775
SCREEN_WIDTH = 1400
MAZE_HEIGHT = 3840
MAZE_WIDTH = 6144

# Variable to hold font name
font = 'joystix.otf'

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (188, 188, 188)
LIGHT_ORANGE = (255,152,71)
YELLOW = (255, 255, 0)

# Game Matrix
SIZE = 64
MAZE_SIZE = 96
ROWS = 40
COLS = 64


FPS = 60

# Sprtie Coordinates
player_Car = {
    "RIGHT":[(0,3)],
    "LEFT": [(0,9)],
    "DOWN": [(0,6)],
    "UP": [(0,0)],
    "UP_TO_RIGHT": [(0, 0), (0, 1), (0, 2), (0, 3)],
    "RIGHT_TO_UP": [(0,3), (0,2), (0,1), (0,0)],
    "RIGHT_TO_DOWN": [(0, 3), (0, 4), (0, 5), (0, 6)],
    "DOWN_TO_RIGHT": [(0,6), (0,5), (0,4), (0,3)],
    "DOWN_TO_LEFT": [(0, 6), (0, 7), (0, 8), (0, 9)],
    "LEFT_TO_DOWN": [(0,9), (0,8), (0,7), (0,6)],
    "LEFT_TO_UP": [(0, 9), (0, 10), (0, 11), (0, 0)],
    "UP_TO_LEFT": [(0,0), (0,11), (0,10), (0,9)],
    "UP_TO_DOWN": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)],
    "DOWN_TO_UP": [(0,6), (0,5), (0,4), (0,3), (0,2), (0,1), (0,0)],
    "RIGHT_TO_LEFT": [(0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9)],
    "LEFT_TO_RIGHT": [(0,9), (0,8), (0,7), (0,6), (0,5), (0,4), (0,3)]
}

enemy_Car = {
    "RIGHT":[(1,3)],
    "LEFT": [(1,9)],
    "DOWN": [(1,6)],
    "UP": [(1,0)],
    "UP_TO_RIGHT": [(1, 0), (1, 1), (1, 2), (1, 3)],
    "RIGHT_TO_UP": [(1,3), (1,2), (1,1), (1,0)],
    "RIGHT_TO_DOWN": [(1, 3), (1, 4), (1, 5), (1, 6)],
    "DOWN_TO_RIGHT": [(1,6), (1,5), (1,4), (1,3)],
    "DOWN_TO_LEFT": [(1, 6), (1, 7), (1, 8), (1, 9)],
    "LEFT_TO_DOWN": [(1,9), (1,8), (1,7), (1,6)],
    "LEFT_TO_UP": [(1, 9), (1, 10), (1, 11), (1, 0)],
    "UP_TO_LEFT": [(1,0), (1,11), (1,10), (1,9)],
    "UP_TO_DOWN": [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)],
    "DOWN_TO_UP": [(1,6), (1,5), (1,4), (1,3), (1,2), (1,1), (1,0)],
    "RIGHT_TO_LEFT": [(1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9)],
    "LEFT_TO_RIGHT": [(1,9), (1,8), (1,7), (1,6), (1,5), (1,4), (1,3)],
    "SPIN": [(1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9), (1,10), (1,11)]
}

enemy_Car_starts = [(5, 19), (5, 21), (5, 17), (5, 23), (5, 15), (56, 19), (56, 21)]

objects = {
    "Life": [(4,12)],
    "Flags": [(4,0), (4,1), (4,2)],
    "Rock": [(5,1), (5,2), (6,1), (6,2)],
    "Smoke": [(5,4), (5,5), (6,4), (6,5)],
    "Fuel_Bar": [(2,12), (2,13), (2,14), (2,15)],
    "Points": [(0,16), (0,17), (1,16), (1,17), (2,16), (2,17), (3,16), (3,17), (4,16), (4,17), (0,18)],
    "Crash": [(5, 0), (5, 1), (6, 0), (6, 1)]
}

boundary_blocks = {
    "Maze1": [(11,10), (11, 11),(12,10),(12,11)],
    "Maze2": [(17,10), (17,11), (18,10), (18,11)]
}

maze1_blocks = {
    "Solo": [(7,12), (7,16), (11, 12),(11,16)],
    "Penn_UP":[(7,18), (7,19), (8,18), (8,19)],
    "Penn_Right": [(8,19), (8,20), (9,19), (9,20)],
    "Penn_Down": [(10,18), (10,19), (11,18), (11,19)],
    "Penn_Left": [(8,16), (8,17), (9,16), (9,17)],
    "Top_Left": [(7,12), (7,13), (8,12), (8,13)],
    "Top_Middle": [(7,13), (7,14), (8,13), (8,14)],
    "Top_Right": [(7,15), (7,16), (8,15), (8,16)],
    "Middle_Left": [(9,12), (9,13), (10,12), (10,13)],
    "Middle": [(9,13), (9,14), (10,13), (10,14)],
    "Middle_Right": [(9,15), (9,16), (10,15), (10,16)],
    "Bottom_Left": [(10,12), (10,13), (11,12), (11,13)],
    "Bottom_Middle": [(10,13), (10,14), (11,13), (11,14)],
    "Bottom_Right": [(10,15), (10,16), (11,15), (11,16)],
    "Bridge_H": [(7,13), (7,14), (11,13), (11,14)],
    "Bridge_V": [(9,12), (9,16), (10,12), (10,16)]
}

maze2_blocks = {
    "Solo": [(13,12), (13,16), (17, 12),(17,16)],
    "Penn_UP":[(13,18), (13,19), (14,18), (14,19)],
    "Penn_Right": [(14,19), (14,20), (15,19), (15,20)],
    "Penn_Down": [(16,18), (16,19), (17,18), (17,19)],
    "Penn_Left": [(14,16), (14,17), (15,16), (15,17)],
    "Top_Left": [(13,12), (13,13), (14,12), (14,13)],
    "Top_Middle": [(13,13), (13,14), (14,13), (14,14)],
    "Top_Right": [(13,15), (13,16), (14,15), (14,16)],
    "Middle_Left": [(14,12), (14,13), (16,12), (16,13)],
    "Middle": [(15,13), (15,14), (16,13), (16,14)],
    "Middle_Right": [(15,15), (15,16), (16,15), (16,16)],
    "Bottom_Left": [(16,12), (16,13), (17,12), (17,13)],
    "Bottom_Middle": [(16,13), (16,14), (17,13), (17,14)],
    "Bottom_Right": [(16,15), (16,16), (17,15), (17,16)],
    "Bridge_H": [(13,13), (13,14), (17,13), (17,14)],
    "Bridge_V": [(15,12), (15,16), (16,12), (16,16)]
}

maze1 = [
    "################################################################",
    "################################################################",
    "################################################################",
    "################################################################",
    "####     XXXXX         XXXXXXXXXXXXXX            XXXX       ####",
    "#### XXX XXXXX                        XXX XXX XX       X XX ####",
    "#### XXX       XXXXXX XX XX XXXX XX X XXX XXX XXXXXXX  X XX ####",
    "####     XX XX XXXXXX XX XX XXXX XX X XXX X            X XX ####",
    "#### XX XXX XX        XX    XXXX XX X XXX X XXXXXXXX X X    ####",
    "#### XX XXX XX XX XXX XX XX      XX X     X        X X X XX ####",
    "#### XX        XX XXX    XX XXXX XX XXX XXX X X XX X X X XX ####",
    "#### XXX XX XX XX XXX XX XX XXXX XX XXX XXX X X XX X X   XX ####",
    "#### XXX XX XX XX     XX                  X X X      X X XX ####",
    "####           XX XXXXXX XX XXXX XX XXX X X X XXXXXXXX X XX ####",
    "#### XXXXXX XX    XXXX   XX XXXX XX XXX X X X          X    ####",
    "####        XX XX XXXX  XXX   XX XX XXX X X XXXXXXXXXX X XX ####",
    "#### XXXXXX XX XX       XXX X XX XX X   X              X XX ####",
    "####        XX XXXX XX           XX X XXX XXXX XX XXXX      ####",
    "#### XXXXXX XX XXXX XX  XXXXX XX XX X XXX XXXX XX XXXX      ####",
    "####                    XXXXX XX XX X XXX XXXX XX XXXXX    X####",
    "#### XXXXXX XX XX X XX                               XX XX X####",
    "####        XX XX X XX                     XXX XXXXX XX    X####",
    "#### XXXXXX XX XX X XX  XX XX XX XXXXX XX  XXX XXXXX       X####",
    "####                    XX XX XX XXXXX XX      XXXXX XXX XXX####",
    "#### XXXXXX XXXXXX XXX  XX XX XX XX    XX            XXX XXX####",
    "####               XXX           XX    XX  XXXXXXX X XXX XXX####",
    "#### XXX XXXXX XXX XXX  XXX XXXX XX XXXXX  XXX     X XXX XXX####",
    "#### XXX XXXXX XXX XXX  XXX XXXX XX XXXXX  XXX XX  X        ####",
    "####                                           XX  X X XX X ####",
    "####                                           XX  X X XX X ####",
    "####XX XX XXXX XXXXXXX  XX XXXXX XX XXX XX XXX XX  X X XX X ####",
    "####XX XX XXXX XXXXXXX  XX XXXXX XX XXX XX XXX XX  X X    X ####",
    "####   XX               XX    XX XX XXX XX XXX     X X XX X ####",
    "#### XXXX XXXXXXXX XXX  XXXXX XX XX X      XXXXXXXXX X XX X ####",
    "#### XXXX XXXXXXXX XXX  XX             XXX           X XX X ####",
    "####                       XXXXXXXXXXXXXXX  XXXXXXXX        ####",
    "################################################################",
    "################################################################",
    "################################################################",
    "################################################################"
]

maze2 = [
    "################################################################",
    "################################################################",
    "################################################################",
    "################################################################",
    "####                             XXXXXXXXXXXXXXXXXXXXXXXXXXX####",
    "#### X XXX XX XX XX XXXX XXX XX         X                XXX####",
    "#### X XXX XX XX XX XXXX XXX XXXXXXXXXX X XXXXXX XXXXXXX XXX####",
    "####                                    X X            X XXX####",
    "####XX XXX XX XX XX XXXXXXXX XX XX XXXX X X XXXXXXXXXX X XXX####",
    "####XX XXX XX XX XX X     XX XX XX XXXX X X X        X X XXX####",
    "####   XXX          X     XX XX XX        X    XXXX         ####",
    "#### XXXXX XX XX XX X XX           XXXX X X X        X X X  ####",
    "#### XXX   XX XX XX X XX  XX XXXXX XXXX X X XXXXXXXXXX X X  ####",
    "####     X          X     XX XXXXX XXXX X X            X X  ####",
    "#### XXXXX XXXXX XX X XXXXXX     X XXXX X XXXXXX XXXXXXX X  ####",
    "####                  XXXXXX XXX X      X                X  ####",
    "#### XXXXXXX  XXX XXX XXXXXX XXX   XXXX XXXXXXXX XXXXXXXXX  ####",
    "####          XXX XXX XXXXXX XXX X XXXX                     ####",
    "#### XXXXXXX  XXX                X XXXXXX XXXX XXXX XXXXX X ####",
    "####                          XXXX                        X ####",
    "#### XXXXXXX  X X                X XXXXXX XXXX XXXX XXXXX X ####",
    "####          X X XXXXXXX XXXXXX X XXXXXX XXXX XXXX       X ####",
    "#### XXXXXXX  X X XXXXXXX XXXXXX   XXX              XXXXX X ####",
    "####          X X XXXXXXX XXXXXX   XXX XX XXXX XXXX         ####",
    "#### XXXXXXX  X X XXXX       XXX   XXX XX XXXX XXXX XX XX X ####",
    "####                   XX XX                        XX XX X ####",
    "#### XX X XXX X XXX XX       XXX  XXXX XX XXXX XXXX XX XX X ####",
    "####  X X XXX X XXX XXXXX XXXXXX  XXXX XX X       X    XX   ####",
    "####X X X XXX X   X XXXXX XXXXXX  XXXX    X XX XX X XX XX X ####",
    "####X X       X X X               XXXX XX X X   X X XX XX X ####",
    "####X X X XXX X X X XXXXX XXXXXX       XX X X X X X         ####",
    "####X X X XXX X X X XXXXX XXXXXX  XXXX XX X X X X X XX XX X ####",
    "####    X XXX X   X XX       XXX  XXXX XX X X X X X XX XX X ####",
    "####    X     XXX X XX XXXXX XXX                       XX   ####",
    "####XXX X XXX XXX X XX XXXXX XXX  XXXXXXX XXXXXXXXX XXXXX XX####",
    "####XXX   XXX                                             XX####",
    "################################################################",
    "################################################################",
    "################################################################",
    "################################################################"
]
