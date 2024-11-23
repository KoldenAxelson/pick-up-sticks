import pygame
from constants import CELL_SIZE, WINDOW_SIZE, BLACK, GRAY, BROWN, BLUE, RED, GREEN, WHITE

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def draw_grid_object(self, color, grid_pos, camera_offset):
        """Draw an object aligned to the grid with the camera offset"""
        screen_x = grid_pos[0] * CELL_SIZE - camera_offset[0]
        screen_y = grid_pos[1] * CELL_SIZE - camera_offset[1]
        if 0 <= screen_x < WINDOW_SIZE and 0 <= screen_y < WINDOW_SIZE:
            pygame.draw.rect(self.screen, color,
                           (screen_x, screen_y, CELL_SIZE-2, CELL_SIZE-2))

    def render(self, game_world, player):
        self.screen.fill(BLACK)
        
        # Calculate camera offset based on pixel position
        camera_x = player.pixel_pos[0] - WINDOW_SIZE // 2
        camera_y = player.pixel_pos[1] - WINDOW_SIZE // 2
        camera_offset = (camera_x, camera_y)
        
        # Draw rocks
        for rock in game_world.rocks:
            self.draw_grid_object(GRAY, rock, camera_offset)
        
        # Draw current stick
        self.draw_grid_object(BROWN, game_world.current_stick, camera_offset)
        
        # Draw player
        player_screen_x = WINDOW_SIZE // 2 - CELL_SIZE // 2
        player_screen_y = WINDOW_SIZE // 2 - CELL_SIZE // 2
        
        player_color = BLUE if player.is_moving else RED
        pygame.draw.rect(self.screen, player_color,
                        (player_screen_x+(CELL_SIZE//2), player_screen_y+(CELL_SIZE//2), 
                         CELL_SIZE-2, CELL_SIZE-2))
        
        # Draw direction indicator
        indicator_x = player_screen_x + player.direction[0] * CELL_SIZE * 0.3 + CELL_SIZE
        indicator_y = player_screen_y + player.direction[1] * CELL_SIZE * 0.3 + CELL_SIZE
        pygame.draw.circle(self.screen, GREEN if player.is_running else WHITE, 
                         (int(indicator_x), int(indicator_y)), 5)
        
        # Draw stick counter
        counter = self.font.render(f'Sticks: {game_world.collected_sticks}', True, WHITE)
        self.screen.blit(counter, (10, 10))
        
        pygame.display.flip()