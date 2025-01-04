from abc import ABC, abstractproperty, abstractmethod
from json import JSONEncoder

class Unit(ABC):
    def __init__(self, id, x, y):
        # UUID
        self.id = id
        # Current X/Y
        self.x = x
        self.y = y
        # unit or tower, move or attack
        self.target = None

    # movement delta for tick
    @property
    @abstractmethod
    def delta(self):
        pass

    # move strategy
    @property
    @abstractmethod
    def move_strategy(self):
        pass

    def move(self, state):
        new_x, new_y = self.move_strategy.move(self, state)
        self.x = new_x
        self.y = new_y
