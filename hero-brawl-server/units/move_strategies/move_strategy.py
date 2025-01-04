from abc import ABC, abstractmethod

class MoveStrategy(ABC):
    def __init__(self):
        self.board_width = 480
        # x/y pixel valeus
        self.left_bridge = (73, 479)
        self.right_bridge = (403, 479)
        self.enemy_left_tower = (73, 641)
        self.enemy_right_tower = (403, 641)

    @abstractmethod
    def move(self, unit, game_state):
        pass


class BasicMoveStrategy(MoveStrategy):
    def move(self, unit, game_state):
        on_left_side = unit.x < self.board_width / 2
        # move to bridge
        if on_left_side:
            target = self.left_bridge
        else:
            target = self.right_bridge
        
        # if past bridge move to tower
        if unit.y >= self.left_bridge[1] and on_left_side:
            target = self.enemy_left_tower
        elif unit.y >= self.left_bridge[1]:
            target = self.enemy_right_tower
        
        # Calculate movement delta for both x and y
        new_x = self.move_towards(unit.x, target[0], unit.delta)
        new_y = self.move_towards(unit.y, target[1], unit.delta)

        return new_x, new_y

    def move_towards(self, current, target, delta):
        # TODO update to calculate distance with direction 
        if current < target:
            return min(current + delta, target)
        elif current > target:
            return max(current - delta, target)
        return current
        