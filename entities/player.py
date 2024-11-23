import pygame
from entities.base_entity import BaseEntity
from constants import CELL_SIZE, GRID_SIZE, MOVEMENT_SPEED, BLUE, RED

class Player(BaseEntity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.pixel_pos = [x * CELL_SIZE, y * CELL_SIZE]
        self.direction = [0, -1]  # Start facing up
        self.is_moving = False
        self.is_running = False
        self.target_pixel_pos = None

    def try_move(self, direction, game_world) -> bool:
        """Attempt to move in the given direction"""
        new_x = self.x + direction[0]
        new_y = self.y + direction[1]
        new_pos = (new_x, new_y)
        self.direction = direction
        
        # Quick boundary check
        if not (0 < new_x < GRID_SIZE-1 and 0 < new_y < GRID_SIZE-1):
            return False
            
        # Check if the target cell is blocked
        entity = game_world.get_entity_at(new_pos)
        if entity and entity.is_blocking:
            return False
        
        if not self.is_moving:
            self.target_pixel_pos = [new_x * CELL_SIZE, new_y * CELL_SIZE]
            self.is_moving = True
            self.x, self.y = new_x, new_y
            return True
        return False

    def update(self, dt: float) -> None:
        """Update smooth movement between cells"""
        if self.is_moving and self.target_pixel_pos:
            dx = self.target_pixel_pos[0] - self.pixel_pos[0]
            dy = self.target_pixel_pos[1] - self.pixel_pos[1]

            base_speed = MOVEMENT_SPEED if self.is_running else (MOVEMENT_SPEED / 2)
            speed = base_speed * dt

            if abs(dx) <= speed and abs(dy) <= speed:
                self.pixel_pos = self.target_pixel_pos.copy()
                self.is_moving = False
                self.target_pixel_pos = None
            else:
                distance = (dx * dx + dy * dy) ** 0.5
                move_x = (dx / distance) * speed if distance > 0 else 0
                move_y = (dy / distance) * speed if distance > 0 else 0
                
                self.pixel_pos[0] += move_x
                self.pixel_pos[1] += move_y

    def get_render_data(self) -> dict:
        return {
            'color': BLUE if self.is_moving else RED,
            'position': self.position,
            'type': 'rectangle',
            'is_player': True,
            'direction': self.direction,
            'is_running': self.is_running,
            'pixel_pos': self.pixel_pos
        }