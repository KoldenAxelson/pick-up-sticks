CELL_SIZE = 30
GRID_SIZE = 10
CELL_MARGIN = 0
STATS_WIDTH = 150  # Width of the stats bar
GAME_WINDOW_SIZE = CELL_SIZE * 11  # Main game view size (11x11 with player in center)
WINDOW_WIDTH = GAME_WINDOW_SIZE + STATS_WIDTH  # Add stats width
WINDOW_HEIGHT = GAME_WINDOW_SIZE  # Keep game height
WORLD_SIZE = GRID_SIZE * CELL_SIZE

# Movement constants
MOVEMENT_DELAY = 0.15  # Seconds between movements when key is held
MOVEMENT_SPEED = 300  # Pixels per second
ROCK_COUNT = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)