
# TODO
# Send a playerID or infer it from the socket connection (socketID?)
# use this socketId as the player key for the pieces
# store the pieces exactly as each client sends

# LIMITATIONS
# Only support 1 game at a time for now
# To improve, keep map of gameID to model (state)
# update client array to include the gameID/State

class Player():
    def __init__(self, id):
        self.id = id
        self.pieces = []
    
    def add_unit(self, unit):
        self.pieces.append(unit)

class Model():
    # TODO map a game_ID to a model? probably using a database
    # Map of player ID to data
    players = {}

    def add_player(self, id):
        if len(self.players) >= 2:
            raise Exception("Already at 2 players")

        self.players[id] = Player(id)

    def place_unit(self, player_id, unit):
        self.players[player_id].add_unit(unit)
