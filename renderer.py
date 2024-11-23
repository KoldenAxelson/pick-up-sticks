import pygame
from constants import CELL_SIZE, CELL_MARGIN, WINDOW_SIZE, BLACK, WHITE, GREEN
from typing import Tuple

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def draw_entity(self, render_data: dict, camera_offset: Tuple[float, float]) -> None:
        """Draw an entity based on its render data"""
        if render_data['type'] == 'rectangle':
            position = render_data['position']
            screen_x = position[0] * CELL_SIZE - camera_offset[0]
            screen_y = position[1] * CELL_SIZE - camera_offset[1]
            
            if 0 <= screen_x < WINDOW_SIZE and 0 <= screen_y < WINDOW_SIZE:
                if 'is_player' in render_data:
                    # Special handling for player
                    screen_x = WINDOW_SIZE // 2 - CELL_SIZE // 2
                    screen_y = WINDOW_SIZE // 2 - CELL_SIZE // 2
                    pygame.draw.rect(self.screen, render_data['color'],
                                   (screen_x + (CELL_SIZE//2),
                                    screen_y + (CELL_SIZE//2),
                                    CELL_SIZE-CELL_MARGIN, CELL_SIZE-CELL_MARGIN))
                    
                    # Calculate center of the player's cell
                    center_x = screen_x + CELL_SIZE
                    center_y = screen_y + CELL_SIZE

                    # Draw direction indicator
                    direction = render_data['direction']
                    indicator_x = center_x - (CELL_MARGIN // 2) + direction[0] * (CELL_SIZE - 2 * CELL_MARGIN) * 0.5
                    indicator_y = center_y - (CELL_MARGIN // 2) + direction[1] * (CELL_SIZE - 2 * CELL_MARGIN) * 0.5
                    pygame.draw.circle(self.screen,
                                     GREEN if render_data['is_running'] else WHITE,
                                     (int(indicator_x), int(indicator_y)), 5)
                else:
                    pygame.draw.rect(self.screen, render_data['color'],
                                   (screen_x, screen_y, CELL_SIZE-CELL_MARGIN, CELL_SIZE-CELL_MARGIN))

    def render(self, game_world, player):
        self.screen.fill(BLACK)
        
        # Calculate camera offset based on player's pixel position
        camera_x = player.pixel_pos[0] - WINDOW_SIZE // 2
        camera_y = player.pixel_pos[1] - WINDOW_SIZE // 2
        camera_offset = (camera_x, camera_y)
        
        # Draw obstacles
        for obstacle in game_world.obstacles:
            self.draw_entity(obstacle.get_render_data(), camera_offset)
        
        # Draw items
        for item in game_world.items:
            self.draw_entity(item.get_render_data(), camera_offset)
        
        # Draw player
        self.draw_entity(player.get_render_data(), camera_offset)
        
        # Draw collected items counter
        counter = self.font.render(f'Sticks: {game_world.collected_items}', True, WHITE)
        self.screen.blit(counter, (10, 10))
        
        pygame.display.flip()
