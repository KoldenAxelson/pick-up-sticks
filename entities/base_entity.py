from abc import ABC, abstractmethod
from typing import Tuple

class BaseEntity(ABC):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        
    @property
    def position(self) -> Tuple[int, int]:
        return (self.x, self.y)
    
    @abstractmethod
    def update(self, dt: float) -> None:
        pass
    
    @abstractmethod
    def get_render_data(self) -> dict:
        """Return data needed for rendering this entity"""
        pass