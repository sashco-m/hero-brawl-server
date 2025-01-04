from abc import ABC
from uuid import uuid4

class Tower(ABC):
    def __init__(self, hp):
        # UUID
        self.id = uuid4()
        self.hp = hp

class KingTower(Tower):
    def __init__(self):
        super().__init__(4000)   
        self.is_active = False


class PrincessTower(Tower):
    def __init__(self):
        super().__init__(2000)
