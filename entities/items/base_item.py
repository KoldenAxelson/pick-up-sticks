from entities.base_entity import BaseEntity

class BaseItem(BaseEntity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.is_blocking = False
        self.is_collectible = True
    
    def update(self, dt: float) -> None:
        pass  # Items typically don't need updates
    
    def on_collect(self) -> None:
        """Called when the item is collected"""
        pass