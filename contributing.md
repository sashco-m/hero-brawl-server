## Design Doc
Handles logic for the mobile app.

Ideal Flow
1. Load app data from DB on startup via REST
2. Send user a request to play
3. If accepted, start listening on a new port for the game
4. handle all game logic, send data via websocket

V0
Single game socket for two devices to connect to