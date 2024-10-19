from . import sock
from flask import Blueprint, request
import json
import threading
import time
#units
from .units import mini_pekka
# state
from .model import serialize_game, model

from pprint import pprint

# TODO move to own class
# BOARD STATE
board_state = model.Model()

# Lock for synchronizing access to the board state
state_lock = threading.Lock()

# List to keep track of connected WebSocket clients
clients = []

# BATTLE SOCKET
# Streams game state to client

@sock.route('/battle')
def battle(ws):
    # Add the client to the list of connected clients
    clients.append(ws)

    # ping back connection opened, ready to accept player ID
    ws.send("success")

    print("IN BATTLE")
    # Set the client ID
    client_id = ws.receive()
    print("Client ID:", client_id)
    with state_lock:
        board_state.add_player(client_id)

    try:
        while True:
            with state_lock:
                # Broadcast the board state to all clients
                for client in clients:
                    # better encoding?
                    client.send(json.dumps(board_state, cls=serialize_game.Serializer))
                    pass

            time.sleep(0.1)  # Adjust the interval as needed
    except Exception as e:
        print("Error:", e)
    finally:
        # Remove the client from the list of connected clients
        clients.remove(ws)

# ADD PIECE ENDPOINT
bp = Blueprint('battle', __name__, url_prefix='/battle')

@bp.route('/add-piece', methods=['POST'])
def battle():
    data = request.get_json()
    print("input: ", data)
    
    with state_lock:
        # TODO add based on type
        piece_type = data['type']
        player_id = request.headers['PlayerId']

        board_state.place_unit(
            player_id, 
            mini_pekka.MiniPekka(data['id'], data['x'], data['y'])
        )

        print("Board state updated:", board_state)


    return {
        "status": "ok"
    }


# Background thread for game logic

def update_pieces():
    while True:
        with state_lock:
            # Update the position of each piece
            for player in board_state.players.values():
                for piece in player.pieces:
                    # TODO make class for each unit?
                    piece.move(board_state)
                    pass
                        
        # Wait for a short period before updating again
        time.sleep(0.1)  # Adjust the interval as needed

def init_app(app):
    # Start the background thread to update piece positions
    updater_thread = threading.Thread(target=update_pieces)
    updater_thread.daemon = True
    updater_thread.start()
    
    # Register the blueprint
    app.register_blueprint(bp)