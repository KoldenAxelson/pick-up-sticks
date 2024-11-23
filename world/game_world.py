import random
from typing import List, Optional, Tuple
from constants import GRID_SIZE, ROCK_COUNT
from entities.obstacles.rock import Rock
from entities.items.stick import Stick
from entities.obstacles.base_obstacle import BaseObstacle
from entities.items.base_item import BaseItem

class GameWorld:
    def __init__(self):
        self.obstacles: List[BaseObstacle] = []
        self.items: List[BaseItem] = []
        self.collected_items = 0
        self._generate_rocks()
        self.spawn_new_stick()

    def _generate_rocks(self) -> None:
        # Generate border rocks
        for x in range(GRID_SIZE):
            self.obstacles.append(Rock(x, 0))
            self.obstacles.append(Rock(x, GRID_SIZE-1))
            self.obstacles.append(Rock(0, x))
            self.obstacles.append(Rock(GRID_SIZE-1, x))

        # Generate random rocks
        rock_count = 0
        while rock_count < ROCK_COUNT:
            x = random.randint(1, GRID_SIZE-2)
            y = random.randint(1, GRID_SIZE-2)
            pos = (x, y)
            if not any(obstacle.position == pos for obstacle in self.obstacles):
                self.obstacles.append(Rock(x, y))
                rock_count += 1

    def get_valid_spawn_position(self) -> Tuple[int, int]:
        """Get a random position that's not occupied by any entity"""
        while True:
            x = random.randint(1, GRID_SIZE-2)
            y = random.randint(1, GRID_SIZE-2)
            pos = (x, y)
            if (not any(obstacle.position == pos for obstacle in self.obstacles) and
                not any(item.position == pos for item in self.items)):
                return (x, y)

    def spawn_new_stick(self) -> None:
        """Spawn a new stick in a valid position"""
        x, y = self.get_valid_spawn_position()
        self.items.append(Stick(x, y))

    def check_collection(self, position: Tuple[int, int]) -> None:
        """Check if there's an item to collect at the given position"""
        for item in self.items[:]:  # Copy list to safely remove while iterating
            if item.position == position:
                item.on_collect()
                self.items.remove(item)
                self.collected_items += 1
                if isinstance(item, Stick):
                    self.spawn_new_stick()

    def update(self, dt: float) -> None:
        """Update all entities in the world"""
        for obstacle in self.obstacles:
            obstacle.update(dt)
        for item in self.items:
            item.update(dt)