# world/path_finder.py
from typing import Set, Tuple, List, FrozenSet
from constants import GRID_SIZE
from functools import lru_cache

class PathFinder:
    # Pre-calculate valid positions (not on border)
    VALID_POSITIONS = frozenset((x, y) 
                               for x in range(1, GRID_SIZE-1) 
                               for y in range(1, GRID_SIZE-1))
    
    # Pre-calculate neighbors for each position
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
    def find_all_accessible_positions(cls, rocks: Set[Tuple[int, int]], start_pos: Tuple[int, int]) -> Set[Tuple[int, int]]:
        """
        Find all positions that can be reached from the start position.
        Only rocks block movement in accessibility checking.
        Args:
            rocks: Set of current rock positions
            start_pos: Starting position for the flood fill
        Returns:
            Set of all accessible positions
        """
        visited = set()
        to_visit = {start_pos}
        
        while to_visit:
            current = to_visit.pop()
            if current not in visited and current not in rocks:
                visited.add(current)
                # Add all unvisited neighbors
                to_visit.update(
                    neighbor for neighbor in cls.NEIGHBORS_MAP[current]
                    if neighbor not in visited and neighbor not in rocks
                )
        
        return visited

    @classmethod
    def is_map_accessible(cls, rocks: Set[Tuple[int, int]], test_pos: Tuple[int, int] = None) -> bool:
        """
        Check if all non-rock positions remain accessible with the given rock configuration.
        Only rocks (and the test_pos) are considered as blocking for accessibility.
        """
        # Quick validation for test_pos
        if test_pos and (test_pos in rocks or test_pos not in cls.VALID_POSITIONS):
            return False

        # Create set of rocks including test position
        rock_set = rocks | {test_pos} if test_pos else rocks

        # Find a valid starting position that isn't a rock
        start_pos = None
        for pos in cls.VALID_POSITIONS:
            if pos not in rock_set:
                start_pos = pos
                break

        if start_pos is None:  # No empty spaces
            return False

        # Get all accessible positions from this starting point
        accessible = cls.find_all_accessible_positions(rock_set, start_pos)
        
        # Compare with total available positions
        all_open_positions = cls.VALID_POSITIONS - rock_set
        
        # The map is fully accessible if we can reach all non-rock positions
        return accessible == all_open_positions

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