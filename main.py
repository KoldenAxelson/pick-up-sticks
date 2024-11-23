import pygame
import random

# Initialize PyGame
pygame.init()

# Constants
CELL_SIZE = 30
GRID_SIZE = 20
WINDOW_SIZE = CELL_SIZE * 11  # Visible area is 11x11 with player in center
WORLD_SIZE = GRID_SIZE * CELL_SIZE
PLAYER_POS = [GRID_SIZE // 2, GRID_SIZE // 2]  # Start in middle
PLAYER_DIR = [0, -1]  # Start facing up
ROCK_COUNT = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)

# Setup display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Pick Up Sticks')
clock = pygame.time.Clock()

def spawn_stick(rocks, player_pos):
    """Spawn a single stick in a valid position"""
    while True:
        x = random.randint(1, GRID_SIZE-2)  # Keep away from borders
        y = random.randint(1, GRID_SIZE-2)
        if (x, y) not in rocks and (x, y) != tuple(player_pos):
            return (x, y)

# Generate border rocks
rocks = set()
for x in range(GRID_SIZE):
    rocks.add((x, 0))  # Top border
    rocks.add((x, GRID_SIZE-1))  # Bottom border
    rocks.add((0, x))  # Left border
    rocks.add((GRID_SIZE-1, x))  # Right border

# Generate random rock positions (interior rocks)
rock_count = 0
while rock_count < ROCK_COUNT:
    x = random.randint(1, GRID_SIZE-2)
    y = random.randint(1, GRID_SIZE-2)
    if (x, y) != tuple(PLAYER_POS) and (x, y) not in rocks:
        rocks.add((x, y))
        rock_count += 1

# Spawn initial stick
current_stick = spawn_stick(rocks, PLAYER_POS)
collected_sticks = 0
running = True

def draw_grid_object(surface, color, grid_pos, camera_offset):
    """Draw an object aligned to the grid with the camera offset"""
    screen_x = grid_pos[0] * CELL_SIZE - camera_offset[0]
    screen_y = grid_pos[1] * CELL_SIZE - camera_offset[1]
    if 0 <= screen_x < WINDOW_SIZE and 0 <= screen_y < WINDOW_SIZE:
        pygame.draw.rect(surface, color,
                        (screen_x, screen_y, CELL_SIZE-2, CELL_SIZE-2))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Movement
            new_pos = PLAYER_POS.copy()
            if event.key == pygame.K_w:
                new_pos[1] -= 1
                PLAYER_DIR = [0, -1]
            elif event.key == pygame.K_s:
                new_pos[1] += 1
                PLAYER_DIR = [0, 1]
            elif event.key == pygame.K_a:
                new_pos[0] -= 1
                PLAYER_DIR = [-1, 0]
            elif event.key == pygame.K_d:
                new_pos[0] += 1
                PLAYER_DIR = [1, 0]
            
            # Check if move is valid (not hitting rocks, borders, or sticks)
            new_pos_tuple = tuple(new_pos)
            if (0 < new_pos[0] < GRID_SIZE-1 and 
                0 < new_pos[1] < GRID_SIZE-1 and 
                new_pos_tuple not in rocks and
                new_pos_tuple != current_stick):  # Add stick collision check
                PLAYER_POS = new_pos
            
            # Stick collection
            if event.key == pygame.K_SPACE:
                check_pos = (PLAYER_POS[0] + PLAYER_DIR[0], 
                           PLAYER_POS[1] + PLAYER_DIR[1])
                if check_pos == current_stick:
                    collected_sticks += 1
                    current_stick = spawn_stick(rocks, PLAYER_POS)

    # Drawing
    screen.fill(BLACK)
    
    # Calculate camera offset to center player
    camera_x = PLAYER_POS[0] * CELL_SIZE - WINDOW_SIZE // 2
    camera_y = PLAYER_POS[1] * CELL_SIZE - WINDOW_SIZE // 2
    camera_offset = (camera_x, camera_y)
    
    # Draw rocks
    for rock in rocks:
        draw_grid_object(screen, GRAY, rock, camera_offset)
    
    # Draw current stick
    draw_grid_object(screen, BROWN, current_stick, camera_offset)
    
    # Draw player (centered on grid)
    player_screen_pos = (WINDOW_SIZE // 2 - CELL_SIZE // 2, 
                        WINDOW_SIZE // 2 - CELL_SIZE // 2)
    pygame.draw.rect(screen, RED,
                    (player_screen_pos[0]+(CELL_SIZE//2), player_screen_pos[1]+(CELL_SIZE//2), 
                     CELL_SIZE-2, CELL_SIZE-2))
    
    # Draw direction indicator
    indicator_x = player_screen_pos[0] + PLAYER_DIR[0] * CELL_SIZE * 0.3 + CELL_SIZE
    indicator_y = player_screen_pos[1] + PLAYER_DIR[1] * CELL_SIZE * 0.3 + CELL_SIZE
    pygame.draw.circle(screen, WHITE, (int(indicator_x), int(indicator_y)), 5)
    
    # Draw stick counter
    font = pygame.font.Font(None, 36)
    counter = font.render(f'Sticks: {collected_sticks}', True, WHITE)
    screen.blit(counter, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()