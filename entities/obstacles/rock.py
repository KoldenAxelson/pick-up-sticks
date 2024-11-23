from entities.obstacles.base_obstacle import BaseObstacle
from constants import GRAY

class Rock(BaseObstacle):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        
    def get_render_data(self) -> dict:
        return {
            'color': GRAY,
            'position': self.position,
            'type': 'rectangle'
        }