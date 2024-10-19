from abc import ABC, abstractmethod

class MoveStrategy(ABC):
    @abstractmethod
    def move(self, unit, game_state):
        pass


class BasicMoveStrategy(MoveStrategy):
    def move(self, unit, game_state):
        new_y = unit.y + unit.delta
        new_x = unit.x
        return (new_x, new_y)

# Attack other units
class UnitMoveStrategy(MoveStrategy):
    def move(self, unit, game_state):
        new_y = unit.y + unit.delta
        new_x = unit.x
        return (new_x, new_y)