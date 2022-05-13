from pygame.math import Vector2 as vec

# screen settings
BOTTOM_PANEL = 750
WIDTH, HEIGHT = 600, 600
START_TEXT_SIZE = 25
START_FONT = 'verdana'
CENTER = (WIDTH // 2 - 100, HEIGHT // 2 - 290)
BACKGROUND_CENTER = (WIDTH // 2 - 350, HEIGHT // 2 - 400)
TOP_BOTTOM_BUFFER = 50

# colour settings
GREEN = (170, 255, 58)
RED = (200, 0, 0)
BLACK = (0, 0, 70)
WHITE = (255, 250, 250)
MAZE_IMAGE = 'road_Dark.png'

# player settings
PLAYER_STATIC_POS = (30, 320)
PLAYER_START_POS = vec(30, 320)
PLAYER_RADIUS = 200
PLAYER_NAME = 'Venom'

# enemy settings
ENEMY_STATIC_POS = (400, 330)
ENEMY_START_POS = vec(400, 330)
ENEMY_RADIUS = 180
ENEMY_NAME = 'Spider-man'
