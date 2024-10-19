from . import unit
from .move_strategies import move_strategy

class MiniPekka(unit.Unit):
    move_strategy = move_strategy.BasicMoveStrategy()
    delta = 2 
