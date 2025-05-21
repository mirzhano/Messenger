from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    # Генерируем room_id, если не передан в URL
    room_id = request.args.get('room', str(uuid.uuid4()))
    return render_template('index.html', room_id=room_id)

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('message', {'sender': 'System', 'text': f"{data['username']} joined the chat"}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    emit('message', data, room=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)