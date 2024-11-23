import random
from constants import GRID_SIZE, ROCK_COUNT

class GameWorld:
    def __init__(self):
        self.rocks = self._generate_rocks()
        self.current_stick = None
        self.collected_sticks = 0
        self.spawn_new_stick()

    def _generate_rocks(self):
        rocks = set()
        # Generate border rocks
        for x in range(GRID_SIZE):
            rocks.add((x, 0))
            rocks.add((x, GRID_SIZE-1))
            rocks.add((0, x))
            rocks.add((GRID_SIZE-1, x))

        # Generate random rocks
        rock_count = 0
        while rock_count < ROCK_COUNT:
            x = random.randint(1, GRID_SIZE-2)
            y = random.randint(1, GRID_SIZE-2)
            if (x, y) not in rocks:
                rocks.add((x, y))
                rock_count += 1
        return rocks

    def spawn_new_stick(self):
        """Spawn a single stick in a valid position"""
        while True:
            x = random.randint(1, GRID_SIZE-2)
            y = random.randint(1, GRID_SIZE-2)
            if (x, y) not in self.rocks:
                self.current_stick = (x, y)
                return

    def collect_stick(self, check_pos):
        """Try to collect a stick at the given position"""
        if check_pos == self.current_stick:
            self.collected_sticks += 1
            self.spawn_new_stick()
            return True
        return False