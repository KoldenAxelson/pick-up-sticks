import pygame
from constants import CELL_SIZE, GRID_SIZE, MOVEMENT_SPEED

class Player:
    def __init__(self):
        self.grid_pos = [GRID_SIZE // 2, GRID_SIZE // 2]
        self.pixel_pos = [self.grid_pos[0] * CELL_SIZE, self.grid_pos[1] * CELL_SIZE]
        self.direction = [0, -1]  # Start facing up
        self.is_moving = False
        self.is_running = False
        self.target_pixel_pos = None

    def try_move(self, direction, rocks, current_stick):
        """Attempt to move in the given direction"""
        new_pos = [self.grid_pos[0] + direction[0], self.grid_pos[1] + direction[1]]
        self.direction = direction
        
        new_pos_tuple = tuple(new_pos)
        if (0 < new_pos[0] < GRID_SIZE-1 and 
            0 < new_pos[1] < GRID_SIZE-1 and 
            new_pos_tuple not in rocks and
            new_pos_tuple != current_stick and
            not self.is_moving):
            
            self.target_pixel_pos = [new_pos[0] * CELL_SIZE, new_pos[1] * CELL_SIZE]
            self.is_moving = True
            self.grid_pos = new_pos
            return True
        return False

    def update(self, dt):
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