from entities.base_entity import BaseEntity

class BaseObstacle(BaseEntity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.is_blocking = True
    
    def update(self, dt: float) -> None:
        pass  # Obstacles typically don't need updates