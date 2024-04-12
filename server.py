from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_cors import CORS
import redis
import uuid


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Redis setup
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Global variables
lobby_players = set()
current_match_id = 1
player_cards = {}  # Dictionary to store card faces for each player

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    # Remove player from player_cards dictionary upon disconnection
    player_id = request.sid
    if player_id in player_cards:
        del player_cards[player_id]

@socketio.on('join_lobby')
def handle_join_lobby():
    print('Player Joined')
    join_room('lobby')
    lobby_players.add(request.sid)
    emit('lobby_update', list(lobby_players), room='lobby')

@socketio.on('start_game')
def handle_start_game():
    global current_match_id
    match_id = str(uuid.uuid4())
    for player in lobby_players:
        player_cards[player] = 'X'  # Set a default card face for each player (replace 'X' with actual face)
        emit('match_found', {'match_id': match_id, 'player_cards': player_cards}, room=player)
        leave_room('lobby', sid=player)
    current_match_id += 1
    lobby_players.clear()

if __name__ == '__main__':
    socketio.run(app, debug=True)