import random
from typing import Dict, List, Optional, Set, Tuple
from constants import GRID_SIZE, ROCK_COUNT
from entities.base_entity import BaseEntity
from entities.items import BaseItem, Stick
from entities.obstacles import BaseObstacle, Rock
from .path_finder import PathFinder, PathFinderCache
from stats import GameStats

class GameWorld:
    def __init__(self, stats):
        self.obstacles: List[BaseObstacle] = []
        self.items: List[BaseItem] = []
        self.collected_items = 0
        self.path_cache = PathFinderCache()
        self.grid: Dict[Tuple[int, int], BaseEntity] = {}
        self.stats = stats
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
                
        # Update stats with initial rocks
        if hasattr(self, 'stats'):  # In case stats hasn't been set yet
            self.stats.set_initial_rocks(rocks_placed)

    def spawn_new_rock(self, player_pos: Tuple[int, int], stats: GameStats) -> bool:
        """
        Try to spawn a new rock avoiding the player position.
        Only rocks block accessibility, but we won't place on players or items.
        """
        # Get current rock positions
        rocks = self._get_rock_positions()
        
        # Get candidate positions (excluding player and items)
        blocked_for_placement = {player_pos}  # Initial positions we can't place on
        blocked_for_placement.update((item.x, item.y) for item in self.items)
        
        # Try all valid positions that aren't blocked for initial placement
        candidates = PathFinder.VALID_POSITIONS - blocked_for_placement
        
        for pos in candidates:
            # Skip if there's already a rock here
            if pos in rocks:
                continue
                
            # Check if placing a rock here maintains accessibility
            if PathFinder.is_map_accessible(rocks, pos):
                x, y = pos
                rock = Rock(x, y)
                self.obstacles.append(rock)
                self.add_to_grid(rock)
                stats.rock_spawned()
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

    def try_remove_rock(self, position: Tuple[int, int], stats: GameStats) -> bool:
        """
        Try to remove a rock by spending a stick point.
        Returns True if rock was removed, False otherwise.
        """
        entity = self.get_entity_at(position)
        if isinstance(entity, Rock) and stats.sticks_collected > 0:
            # Don't allow removing border rocks
            x, y = position
            if x == 0 or x == GRID_SIZE-1 or y == 0 or y == GRID_SIZE-1:
                return False
                
            # Remove the rock
            self.obstacles.remove(entity)
            self.remove_from_grid(position)
            # Spend a stick point
            stats.spend_stick()
            # Update empty cells count
            stats.rock_removed()
            return True
        return False

    def check_collection(self, position: Tuple[int, int], stats: GameStats) -> None:
        """Check if there's an item to collect"""
        entity = self.get_entity_at(position)
        if isinstance(entity, BaseItem) and entity.is_collectible:
            entity.on_collect()
            self.items.remove(entity)
            self.remove_from_grid(position)
            if isinstance(entity, Stick):
                stats.stick_collected()
                self.spawn_new_rock(position, stats)
                self.spawn_new_stick()

    def update(self, dt: float) -> None:
        """Update all entities in the world"""
        for obstacle in self.obstacles:
            obstacle.update(dt)
        for item in self.items:
            item.update(dt)