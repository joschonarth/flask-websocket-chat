from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
socketio = SocketIO(app)

connected_users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("Usuário conectado!")

@socketio.on('disconnect')
def handle_disconnect():
    username = connected_users.pop(request.sid, None)
    if username:
        emit('message', {
            'msg': f"{username} saiu do chat.",
            'time': datetime.now().strftime('%H:%M'),
            'system': True
        }, broadcast=True)

@socketio.on('set_username')
def set_username(data):
    username = data.get('username', 'Usuário Anônimo')
    connected_users[request.sid] = username
    emit('message', {
        'msg': f"{username} entrou no chat.",
        'time': datetime.now().strftime('%H:%M'),
        'system': True
    }, broadcast=True)

@socketio.on('message')
def handle_message(data):
    username = connected_users.get(request.sid, 'Anônimo')
    msg = data.get('msg', '')
    timestamp = datetime.now().strftime('%H:%M')

    emit('message', {
        'username': username,
        'msg': msg,
        'time': timestamp
    }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)