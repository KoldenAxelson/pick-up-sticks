import pygame
import random
import time

# Initialize PyGame
pygame.init()

# Constants
CELL_SIZE = 30
GRID_SIZE = 20
WINDOW_SIZE = CELL_SIZE * 11  # Visible area is 11x11 with player in center
WORLD_SIZE = GRID_SIZE * CELL_SIZE
PLAYER_POS = [GRID_SIZE // 2, GRID_SIZE // 2]  # Grid position
PLAYER_PIXEL_POS = [PLAYER_POS[0] * CELL_SIZE, PLAYER_POS[1] * CELL_SIZE]  # Actual pixel position
PLAYER_DIR = [0, -1]  # Start facing up
ROCK_COUNT = 10
MOVEMENT_DELAY = 0.15  # Seconds between movements when key is held
MOVEMENT_SPEED = 300  # Pixels per second

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)

# Setup display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Pick Up Sticks')
clock = pygame.time.Clock()

running = True

def spawn_stick(rocks, player_pos):
    """Spawn a single stick in a valid position"""
    while True:
        x = random.randint(1, GRID_SIZE-2)
        y = random.randint(1, GRID_SIZE-2)
        if (x, y) not in rocks and (x, y) != tuple(player_pos):
            return (x, y)

# Generate border rocks
rocks = set()
for x in range(GRID_SIZE):
    rocks.add((x, 0))
    rocks.add((x, GRID_SIZE-1))
    rocks.add((0, x))
    rocks.add((GRID_SIZE-1, x))

# Generate random rock positions
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
last_movement_time = time.time()
is_moving = False
is_running = False
target_pixel_pos = None

def draw_grid_object(surface, color, grid_pos, camera_offset):
    """Draw an object aligned to the grid with the camera offset"""
    screen_x = grid_pos[0] * CELL_SIZE - camera_offset[0]
    screen_y = grid_pos[1] * CELL_SIZE - camera_offset[1]
    if 0 <= screen_x < WINDOW_SIZE and 0 <= screen_y < WINDOW_SIZE:
        pygame.draw.rect(surface, color,
                        (screen_x, screen_y, CELL_SIZE-2, CELL_SIZE-2))

def try_move(direction):
    """Attempt to move in the given direction"""
    global PLAYER_POS, PLAYER_DIR, target_pixel_pos, is_moving
    new_pos = [PLAYER_POS[0] + direction[0], PLAYER_POS[1] + direction[1]]
    PLAYER_DIR = direction
    
    # Check if move is valid
    new_pos_tuple = tuple(new_pos)
    if (0 < new_pos[0] < GRID_SIZE-1 and 
        0 < new_pos[1] < GRID_SIZE-1 and 
        new_pos_tuple not in rocks and
        new_pos_tuple != current_stick and
        not is_moving):  # Only start new movement if not already moving
        
        # Set target position in pixels
        target_pixel_pos = [new_pos[0] * CELL_SIZE, new_pos[1] * CELL_SIZE]
        is_moving = True
        PLAYER_POS = new_pos
        return True
    return False

def update_movement():
    """Update smooth movement between cells"""
    global PLAYER_PIXEL_POS, is_moving, is_running, target_pixel_pos
    
    if is_moving and target_pixel_pos:
        dx = target_pixel_pos[0] - PLAYER_PIXEL_POS[0]
        dy = target_pixel_pos[1] - PLAYER_PIXEL_POS[1]

        # Base speed in pixels per second (not per frame)
        base_speed = MOVEMENT_SPEED if is_running else (MOVEMENT_SPEED / 2)
        
        # Convert speed to pixels per frame using delta time
        dt = clock.get_time() / 1000.0  # Convert milliseconds to seconds
        speed = base_speed * dt

        # Calculate movement this frame
        if abs(dx) <= speed and abs(dy) <= speed:
            # Close enough to snap to target
            PLAYER_PIXEL_POS = target_pixel_pos.copy()
            is_moving = False
            target_pixel_pos = None
        else:
            # Calculate direction vector
            distance = (dx * dx + dy * dy) ** 0.5
            move_x = (dx / distance) * speed if distance > 0 else 0
            move_y = (dy / distance) * speed if distance > 0 else 0
            
            # Move towards target
            PLAYER_PIXEL_POS[0] += move_x
            PLAYER_PIXEL_POS[1] += move_y

while running:
    current_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not is_moving:
            if event.key == pygame.K_SPACE:
                check_pos = (PLAYER_POS[0] + PLAYER_DIR[0], 
                           PLAYER_POS[1] + PLAYER_DIR[1])
                if check_pos == current_stick:
                    collected_sticks += 1
                    current_stick = spawn_stick(rocks, PLAYER_POS)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                is_running = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                is_running = False
    
    # Handle continuous movement
    if not is_moving and current_time - last_movement_time >= MOVEMENT_DELAY:
        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_w]:
            moved = try_move([0, -1])
        elif keys[pygame.K_s]:
            moved = try_move([0, 1])
        elif keys[pygame.K_a]:
            moved = try_move([-1, 0])
        elif keys[pygame.K_d]:
            moved = try_move([1, 0])
        
        if moved:
            last_movement_time = current_time
    
    # Update movement
    update_movement()
    
    # Drawing
    screen.fill(BLACK)
    
    # Calculate camera offset based on pixel position
    camera_x = PLAYER_PIXEL_POS[0] - WINDOW_SIZE // 2
    camera_y = PLAYER_PIXEL_POS[1] - WINDOW_SIZE // 2
    camera_offset = (camera_x, camera_y)
    
    # Draw rocks
    for rock in rocks:
        draw_grid_object(screen, GRAY, rock, camera_offset)
    
    # Draw current stick
    draw_grid_object(screen, BROWN, current_stick, camera_offset)
    
    # Draw player with smooth position
    player_screen_x = WINDOW_SIZE // 2 - CELL_SIZE // 2
    player_screen_y = WINDOW_SIZE // 2 - CELL_SIZE // 2
    
    # Change color based on movement state
    player_color = BLUE if is_moving else RED
    
    pygame.draw.rect(screen, player_color,
                    (player_screen_x+(CELL_SIZE//2), player_screen_y+(CELL_SIZE//2), 
                     CELL_SIZE-2, CELL_SIZE-2))
    
    # Draw direction indicator
    indicator_x = player_screen_x + PLAYER_DIR[0] * CELL_SIZE * 0.3 + CELL_SIZE
    indicator_y = player_screen_y + PLAYER_DIR[1] * CELL_SIZE * 0.3 + CELL_SIZE
    pygame.draw.circle(screen, GREEN if is_running else WHITE, (int(indicator_x), int(indicator_y)), 5)
    
    # Draw stick counter
    font = pygame.font.Font(None, 36)
    counter = font.render(f'Sticks: {collected_sticks}', True, WHITE)
    screen.blit(counter, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()