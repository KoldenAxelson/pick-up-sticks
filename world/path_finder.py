# world/path_finder.py
from typing import Set, Tuple, List, FrozenSet
from constants import GRID_SIZE
from functools import lru_cache

class PathFinder:
    # Pre-calculate valid positions (not on border)
    VALID_POSITIONS = frozenset((x, y) 
                               for x in range(1, GRID_SIZE-1) 
                               for y in range(1, GRID_SIZE-1))
    
    # Pre-calculate valid neighbors for each position
    NEIGHBORS_MAP = {
        (x, y): tuple((nx, ny) 
                      for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                      if 1 <= nx < GRID_SIZE-1 and 1 <= ny < GRID_SIZE-1)
        for x, y in VALID_POSITIONS
    }

    @classmethod
    def is_position_valid(cls, pos: Tuple[int, int]) -> bool:
        """Check if a position is within bounds and not on the border"""
        return pos in cls.VALID_POSITIONS

    @classmethod
    def get_neighbors(cls, pos: Tuple[int, int]) -> Tuple[Tuple[int, int], ...]:
        """Get all valid neighboring positions"""
        return cls.NEIGHBORS_MAP.get(pos, ())

    @classmethod
    def is_map_accessible(cls, rocks: Set[Tuple[int, int]], test_pos: Tuple[int, int] = None) -> bool:
        """
        Check if the map remains fully accessible with the given rock positions.
        Uses an optimized flood fill algorithm and early exit conditions.
        """
        # Quick validation for test_pos
        if test_pos and (test_pos in rocks or test_pos not in cls.VALID_POSITIONS):
            return False

        # Create immutable set of rocks for efficient lookups
        rock_set = rocks | {test_pos} if test_pos else rocks

        # Early exit if too many rocks would make it impossible to have a path
        available_spaces = len(cls.VALID_POSITIONS - rock_set)
        if available_spaces < 2:  # Need at least 2 spaces for movement
            return False

        # Find a starting point that isn't a rock
        start = None
        for pos in cls.VALID_POSITIONS:
            if pos not in rock_set:
                start = pos
                break
        
        if start is None:
            return False

        # Use set for visited tracking - faster than dict for this use case
        visited = {start}
        queue = [start]  # Using list as a queue is fine for this size
        idx = 0  # Index into queue

        # Modified BFS that uses list index instead of pop(0)
        while idx < len(queue):
            current = queue[idx]
            idx += 1

            for neighbor in cls.NEIGHBORS_MAP[current]:
                if neighbor not in rock_set and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        # Check if all non-rock positions are accessible
        return len(visited) == available_spaces

class PathFinderCache:
    """Optional cache wrapper for path finding results"""
    def __init__(self, size: int = 1024):
        self.cache_size = size
        self._cache = {}
        self._cache_order = []

    def _make_cache_key(self, rocks: Set[Tuple[int, int]], test_pos: Tuple[int, int] = None) -> Tuple:
        """Create an immutable cache key from the parameters"""
        return (frozenset(rocks), test_pos)

    def get(self, rocks: Set[Tuple[int, int]], test_pos: Tuple[int, int] = None) -> bool:
        """Get cached result if it exists"""
        key = self._make_cache_key(rocks, test_pos)
        return self._cache.get(key)

    def set(self, rocks: Set[Tuple[int, int]], test_pos: Tuple[int, int], result: bool) -> None:
        """Cache the result with LRU eviction"""
        key = self._make_cache_key(rocks, test_pos)
        
        if key in self._cache:
            # Move to most recent
            self._cache_order.remove(key)
            self._cache_order.append(key)
            return

        if len(self._cache) >= self.cache_size:
            # Evict oldest
            old_key = self._cache_order.pop(0)
            del self._cache[old_key]

        self._cache[key] = result
        self._cache_order.append(key)