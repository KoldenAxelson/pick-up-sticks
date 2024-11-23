from entities.items.base_item import BaseItem
from constants import BROWN

class Stick(BaseItem):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.is_blocking = True 
    
    def get_render_data(self) -> dict:
        return {
            'color': BROWN,
            'position': self.position,
            'type': 'rectangle'
        }
    
    def on_collect(self) -> None:
        super().on_collect()