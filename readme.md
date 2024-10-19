## Activate the venv
source server_env/bin/activate

## starting the server
flask --app hero-brawl-server run

## connecting to server from emulator
10.0.2.2:5000

## Connecting to server from physical device
1. chrome://inspect/#devices
2. enable port forwarding to localhost:5000

### Connection troubleshooting
- If unable to connect to server from physical device, confirm you can reach localhost:5000 in device browser

## Starting a dummy client
python -m websockets ws://localhost:8001/
