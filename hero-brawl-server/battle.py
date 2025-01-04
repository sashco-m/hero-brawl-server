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

# Handle client message
def handle_client_message(client_id, message):
    event = json.loads(message)
    event_type = event.get('type') 
    data = event.get('data')

    if event_type == 'unit_placed':
        with state_lock:
            # Assume data includes unit placement info
            board_state.place_unit(
                client_id, 
                mini_pekka.MiniPekka(data['id'], data['x'], data['y'])
            )
    print(f"Handled action from player {client_id}: {message}")

# Thread for handling WebSocket messages from each client
def handle_ws_messages(ws, client_id):
    try:
        while ws.connected:
            message = ws.receive()
            if message:
                handle_client_message(client_id, message)
    except Exception as e:
        print(f"Error receiving message from client {client_id}: {e}")
    finally:
        print(f"Client {client_id} disconnected")


@sock.route('/battle')
def battle(ws):
    # Add the client to the list of connected clients
    clients.append(ws)

    print("IN BATTLE")
    # Set the client ID
    client_id = ws.receive()
    print("Client ID:", client_id)
    with state_lock:
        board_state.add_player(client_id)

    # Start thread for handling WebSocket messages
    threading.Thread(target=handle_ws_messages, args=(ws, client_id), daemon=True).start()

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
    # TODO add back once we need rest
    # app.register_blueprint(bp)