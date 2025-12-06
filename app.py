import os
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
import uuid

app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

rooms = {}
players = {}

def get_sid():
    from flask import request
    return getattr(request, 'sid', None)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@socketio.on('connect')
def handle_connect():
    sid = get_sid()
    players[sid] = {'room': None, 'symbol': None}

@socketio.on('disconnect')
def handle_disconnect():
    sid = get_sid()
    if sid in players:
        room_id = players[sid].get('room')
        if room_id and room_id in rooms:
            room = rooms[room_id]
            if room['host'] == sid:
                if room['guest']:
                    emit('opponent_left', to=room['guest'])
                del rooms[room_id]
                broadcast_rooms()
            elif room['guest'] == sid:
                room['guest'] = None
                room['status'] = 'waiting'
                emit('opponent_left', to=room['host'])
                broadcast_rooms()
        del players[sid]

@socketio.on('get_rooms')
def handle_get_rooms():
    available = []
    for room_id, room in rooms.items():
        if room['status'] == 'waiting':
            available.append({
                'id': room_id,
                'host_name': room['host_name']
            })
    emit('room_list', available)

@socketio.on('create_room')
def handle_create_room(data):
    sid = get_sid()
    room_id = str(uuid.uuid4())[:8]
    host_name = data.get('name', 'Player')
    rooms[room_id] = {
        'host': sid,
        'host_name': host_name,
        'guest': None,
        'guest_name': None,
        'status': 'waiting',
        'board': {},
        'current_turn': 'X',
        'host_symbol': 'X',
        'guest_symbol': 'O'
    }
    players[sid]['room'] = room_id
    players[sid]['symbol'] = 'X'
    join_room(room_id)
    emit('room_created', {'room_id': room_id})
    broadcast_rooms()

@socketio.on('join_room')
def handle_join_room(data):
    sid = get_sid()
    room_id = data.get('room_id')
    guest_name = data.get('name', 'Player')
    
    if room_id not in rooms:
        emit('join_error', {'message': 'Room not found'})
        return
    
    room = rooms[room_id]
    if room['status'] != 'waiting':
        emit('join_error', {'message': 'Room is full'})
        return
    
    room['guest'] = sid
    room['guest_name'] = guest_name
    room['status'] = 'playing'
    players[sid]['room'] = room_id
    players[sid]['symbol'] = 'O'
    join_room(room_id)
    
    emit('game_start', {
        'symbol': 'X',
        'opponent_name': guest_name,
        'your_turn': True
    }, to=room['host'])
    
    emit('game_start', {
        'symbol': 'O',
        'opponent_name': room['host_name'],
        'your_turn': False
    }, to=sid)
    
    broadcast_rooms()

@socketio.on('make_move')
def handle_make_move(data):
    sid = get_sid()
    if sid not in players:
        return
    
    room_id = players[sid].get('room')
    if not room_id or room_id not in rooms:
        return
    
    room = rooms[room_id]
    symbol = players[sid]['symbol']
    
    if room['current_turn'] != symbol:
        return
    
    gx = data.get('gx')
    gy = data.get('gy')
    key = f"{gx},{gy}"
    
    if key in room['board']:
        return
    
    room['board'][key] = symbol
    room['current_turn'] = 'O' if symbol == 'X' else 'X'
    
    emit('move_made', {
        'gx': gx,
        'gy': gy,
        'symbol': symbol
    }, to=room_id)

@socketio.on('game_won')
def handle_game_won(data):
    sid = get_sid()
    if sid not in players:
        return
    
    room_id = players[sid].get('room')
    if not room_id or room_id not in rooms:
        return
    
    winner = data.get('winner')
    emit('game_over', {'winner': winner}, to=room_id)

@socketio.on('request_rematch')
def handle_rematch():
    sid = get_sid()
    if sid not in players:
        return
    
    room_id = players[sid].get('room')
    if not room_id or room_id not in rooms:
        return
    
    room = rooms[room_id]
    room['board'] = {}
    room['host_symbol'], room['guest_symbol'] = room['guest_symbol'], room['host_symbol']
    room['current_turn'] = 'X'
    
    players[room['host']]['symbol'] = room['host_symbol']
    if room['guest']:
        players[room['guest']]['symbol'] = room['guest_symbol']
    
    emit('rematch_start', {
        'symbol': room['host_symbol'],
        'your_turn': room['host_symbol'] == 'X'
    }, to=room['host'])
    
    if room['guest']:
        emit('rematch_start', {
            'symbol': room['guest_symbol'],
            'your_turn': room['guest_symbol'] == 'X'
        }, to=room['guest'])

@socketio.on('leave_game')
def handle_leave_game():
    sid = get_sid()
    if sid not in players:
        return
    
    room_id = players[sid].get('room')
    if not room_id or room_id not in rooms:
        return
    
    room = rooms[room_id]
    leave_room(room_id)
    
    if room['host'] == sid:
        if room['guest']:
            emit('opponent_left', to=room['guest'])
        del rooms[room_id]
    elif room['guest'] == sid:
        room['guest'] = None
        room['guest_name'] = None
        room['status'] = 'waiting'
        room['board'] = {}
        room['current_turn'] = 'X'
        emit('opponent_left', to=room['host'])
    
    players[sid]['room'] = None
    players[sid]['symbol'] = None
    broadcast_rooms()

def broadcast_rooms():
    available = []
    for room_id, room in rooms.items():
        if room['status'] == 'waiting':
            available.append({
                'id': room_id,
                'host_name': room['host_name']
            })
    socketio.emit('room_list', available)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
