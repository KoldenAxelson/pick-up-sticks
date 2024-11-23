import pygame
from constants import *
from typing import Tuple

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

    def draw_entity(self, render_data: dict, camera_offset: Tuple[float, float], surface: pygame.Surface) -> None:
        """Draw an entity based on its render data"""
        if render_data['type'] == 'rectangle':
            position = render_data['position']
            screen_x = position[0] * CELL_SIZE - camera_offset[0]
            screen_y = position[1] * CELL_SIZE - camera_offset[1]
            
            if 0 <= screen_x < GAME_WINDOW_SIZE and 0 <= screen_y < GAME_WINDOW_SIZE:
                if 'is_player' in render_data:
                    # Special handling for player
                    screen_x = GAME_WINDOW_SIZE // 2 - CELL_SIZE // 2
                    screen_y = GAME_WINDOW_SIZE // 2 - CELL_SIZE // 2
                    pygame.draw.rect(surface, render_data['color'],
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
                    pygame.draw.circle(surface,
                                     GREEN if render_data['is_running'] else WHITE,
                                     (int(indicator_x), int(indicator_y)), 5)
                else:
                    pygame.draw.rect(surface, render_data['color'],
                                   (screen_x, screen_y, CELL_SIZE-CELL_MARGIN, CELL_SIZE-CELL_MARGIN))

    def render(self, game_world, player, stats):
        self.screen.fill(BLACK)
        
        # Calculate camera offset based on player's pixel position
        camera_x = player.pixel_pos[0] - GAME_WINDOW_SIZE // 2
        camera_y = player.pixel_pos[1] - GAME_WINDOW_SIZE // 2
        camera_offset = (camera_x, camera_y)
        
        # Draw game elements with offset for stats bar
        game_surface = pygame.Surface((GAME_WINDOW_SIZE, GAME_WINDOW_SIZE))
        game_surface.fill(BLACK)
        
        # Draw game elements on the game surface
        for obstacle in game_world.obstacles:
            self.draw_entity(obstacle.get_render_data(), camera_offset, game_surface)
        
        for item in game_world.items:
            self.draw_entity(item.get_render_data(), camera_offset, game_surface)
        
        self.draw_entity(player.get_render_data(), camera_offset, game_surface)
        
        # Blit game surface onto main screen with offset for stats bar
        self.screen.blit(game_surface, (STATS_WIDTH, 0))
        
        # Draw stats
        self.render_stats(stats, game_world)
        
        pygame.display.flip()

    def render_stats(self, stats, world):
        # Draw stats background
        stats_rect = pygame.Rect(0, 0, STATS_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, LIGHT_GRAY, stats_rect)
        pygame.draw.line(self.screen, GRAY, 
                        (STATS_WIDTH, 0), 
                        (STATS_WIDTH, WINDOW_HEIGHT), 2)

        # Render stats text - adjusted positions
        x_offset = 10  # Moved left
        y_offset = 20  # Moved up
        line_height = 30  # Reduced line height
        
        stats_texts = [
            f"Moves: {stats.tiles_moved}",
            f"Sticks: {stats.sticks_collected}",
            f"Rocks: {stats.rocks_spawned}",
            f"Empty: {stats.empty_cells}"
        ]

        for i, text in enumerate(stats_texts):
            text_surface = self.font.render(text, True, BLACK)
            self.screen.blit(text_surface, (x_offset, y_offset + (i * line_height)))
