import random
from typing import List, Optional, Tuple, Dict
from constants import GRID_SIZE, ROCK_COUNT
from entities import *
from entities.items import *
from entities.obstacles import *

class GameWorld:
    def __init__(self):
        self.obstacles: List[BaseObstacle] = []
        self.items: List[BaseItem] = []
        self.collected_items = 0
        # Dictionary storing all entities by their grid position
        self.grid: Dict[Tuple[int, int], BaseEntity] = {}
        self._generate_rocks()
        self.spawn_new_stick()

    def add_to_grid(self, entity: BaseEntity) -> None:
        """Add an entity to the grid"""
        self.grid[entity.position] = entity

    def remove_from_grid(self, position: Tuple[int, int]) -> None:
        """Remove an entity from the grid"""
        if position in self.grid:
            del self.grid[position]

    def get_entity_at(self, position: Tuple[int, int]) -> Optional[BaseEntity]:
        """Get entity at a specific position"""
        return self.grid.get(position)

    def _generate_rocks(self) -> None:
        # Generate border rocks
        for x in range(GRID_SIZE):
            for pos in [(x, 0), (x, GRID_SIZE-1), (0, x), (GRID_SIZE-1, x)]:
                rock = Rock(pos[0], pos[1])
                self.obstacles.append(rock)
                self.add_to_grid(rock)

        # Generate random rocks
        rock_count = 0
        while rock_count < ROCK_COUNT:
            x = random.randint(1, GRID_SIZE-2)
            y = random.randint(1, GRID_SIZE-2)
            if (x, y) not in self.grid:
                rock = Rock(x, y)
                self.obstacles.append(rock)
                self.add_to_grid(rock)
                rock_count += 1

    def get_valid_spawn_position(self) -> Tuple[int, int]:
        """Get a random position that's not occupied by any entity"""
        while True:
            x = random.randint(1, GRID_SIZE-2)
            y = random.randint(1, GRID_SIZE-2)
            if (x, y) not in self.grid:
                return (x, y)

    def spawn_new_stick(self) -> None:
        """Spawn a new stick in a valid position"""
        x, y = self.get_valid_spawn_position()
        stick = Stick(x, y)
        self.items.append(stick)
        self.add_to_grid(stick)

    def check_collection(self, position: Tuple[int, int]) -> None:
        """Check if there's an item to collect at the given position"""
        entity = self.get_entity_at(position)
        if isinstance(entity, BaseItem) and entity.is_collectible:
            entity.on_collect()
            self.items.remove(entity)
            self.remove_from_grid(position)
            self.collected_items += 1
            if isinstance(entity, Stick):
                self.spawn_new_stick()

    def update(self, dt: float) -> None:
        """Update all entities in the world"""
        for obstacle in self.obstacles:
            obstacle.update(dt)
        for item in self.items:
            item.update(dt)