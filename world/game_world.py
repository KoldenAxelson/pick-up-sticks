import random
from typing import Dict, List, Optional, Set, Tuple
from constants import GRID_SIZE, ROCK_COUNT
from entities.base_entity import BaseEntity
from entities.items import BaseItem, Stick
from entities.obstacles import BaseObstacle, Rock
from .path_finder import PathFinder, PathFinderCache

class GameWorld:
    def __init__(self):
        self.obstacles: List[BaseObstacle] = []
        self.items: List[BaseItem] = []
        self.collected_items = 0
        self.path_cache = PathFinderCache()
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

    def _get_rock_positions(self) -> Set[Tuple[int, int]]:
        """Get set of current rock positions"""
        return {(obstacle.x, obstacle.y) for obstacle in self.obstacles}

    def _is_position_blocked(self, pos: Tuple[int, int], player_pos: Optional[Tuple[int, int]] = None) -> bool:
        """Check if a position is blocked by any entity or the player"""
        return pos in self.grid or pos == player_pos

    def get_valid_spawn_position(self, player_pos: Optional[Tuple[int, int]] = None) -> Optional[Tuple[int, int]]:
        """Get a random position that's not occupied by any entity or the player"""
        attempts = 100
        while attempts > 0:
            x = random.randint(1, GRID_SIZE-2)
            y = random.randint(1, GRID_SIZE-2)
            pos = (x, y)
            if not self._is_position_blocked(pos, player_pos):
                return pos
            attempts -= 1
        return None

    def _generate_rocks(self) -> None:
        """Generate initial rocks including borders"""
        # Generate border rocks
        for x in range(GRID_SIZE):
            for pos in [(x, 0), (x, GRID_SIZE-1), (0, x), (GRID_SIZE-1, x)]:
                rock = Rock(pos[0], pos[1])
                self.obstacles.append(rock)
                self.add_to_grid(rock)

        # Generate interior rocks
        rocks_placed = 0
        rock_positions = self._get_rock_positions()

        while rocks_placed < ROCK_COUNT:
            pos = self.get_valid_spawn_position()
            if pos and PathFinder.is_map_accessible(rock_positions, pos):
                x, y = pos
                rock = Rock(x, y)
                self.obstacles.append(rock)
                self.add_to_grid(rock)
                rocks_placed += 1

    def spawn_new_rock(self, player_pos: Tuple[int, int]) -> bool:
        """
        Try to spawn a new rock avoiding the player position.
        Now tries all available positions if necessary.
        """
        # Get all valid positions
        empty_positions = [
            (x, y) 
            for x in range(1, GRID_SIZE-1)
            for y in range(1, GRID_SIZE-1)
            if not self._is_position_blocked((x, y), player_pos)
        ]
        
        if not empty_positions:
            return False
            
        # Shuffle positions for randomness
        random.shuffle(empty_positions)
        rocks = self._get_rock_positions()
        
        # Try each empty position
        for pos in empty_positions:
            # Check cache first
            cached_result = self.path_cache.get(rocks, pos)
            if cached_result is not None:
                accessible = cached_result
            else:
                accessible = PathFinder.is_map_accessible(rocks, pos)
                self.path_cache.set(rocks, pos, accessible)

            if accessible:
                x, y = pos
                rock = Rock(x, y)
                self.obstacles.append(rock)
                self.add_to_grid(rock)
                return True
                
        return False

    def spawn_new_stick(self) -> None:
        """Spawn a new stick in a valid position"""
        pos = self.get_valid_spawn_position()
        if pos:
            x, y = pos
            stick = Stick(x, y)
            self.items.append(stick)
            self.add_to_grid(stick)

    def check_collection(self, position: Tuple[int, int]) -> None:
        """Check if there's an item to collect and handle collection"""
        entity = self.get_entity_at(position)
        if isinstance(entity, BaseItem) and entity.is_collectible:
            entity.on_collect()
            self.items.remove(entity)
            self.remove_from_grid(position)
            self.collected_items += 1
            if isinstance(entity, Stick):
                self.spawn_new_stick()
                # Spawn a new rock when stick is collected
                player_pos = position  # Use collection position as player position
                self.spawn_new_rock(player_pos)

    def update(self, dt: float) -> None:
        """Update all entities in the world"""
        for obstacle in self.obstacles:
            obstacle.update(dt)
        for item in self.items:
            item.update(dt)