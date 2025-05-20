from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '91ac3e562f54b63fc55aa576c716f503398c6a8a10d9e605')  # Безопасный ключ из переменной окружения
socketio = SocketIO(app, cors_allowed_origins="*")  # Разрешить CORS для WebSocket

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)