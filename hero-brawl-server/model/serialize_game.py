from json import JSONEncoder
from ..units import unit
from .model import Model, Player

# Keep up to date with everything in the model
class Serializer(JSONEncoder):
    def default(self, o):
        if isinstance(o, Model):
            # serialize model
            return {
                "players": o.players
            }
        
        if isinstance(o, Player):
            # serialize player
            return {
                "id": o.id,
                "pieces": o.pieces
            }

        if isinstance(o, unit.Unit):
            # serialize pieces
            return {
                "id": o.id,
                "x": o.x,
                "y": o.y
            }

        return super().default(o)
