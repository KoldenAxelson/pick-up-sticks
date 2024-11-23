from constants import GRID_SIZE

class GameStats:
    def __init__(self):
        self.tiles_moved = 0
        self.sticks_collected = 0
        self.rocks_spawned = 0
        self.empty_cells = (GRID_SIZE - 2) * (GRID_SIZE - 2)  # Initial empty cells (inner area)
    
    def move_made(self):
        self.tiles_moved += 1
    
    def stick_collected(self):
        self.sticks_collected += 1
    
    def rock_spawned(self):
        self.rocks_spawned += 1
        self.empty_cells -= 1

    def rock_removed(self):
        """Called when a rock is removed by spending a stick"""
        self.rocks_spawned -= 1
        self.empty_cells += 1

    def spend_stick(self):
        """Spend a stick point to remove a rock"""
        if self.sticks_collected > 0:
            self.sticks_collected -= 1
            return True
        return False

    def set_initial_rocks(self, rock_count: int):
        """Call this after generating initial rocks"""
        self.rocks_spawned = rock_count
        self.empty_cells -= rock_count