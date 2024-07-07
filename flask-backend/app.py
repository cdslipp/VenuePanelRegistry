from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

showMode = False

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello from Flask!")

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('show_mode', {'showMode': showMode})

@socketio.on('toggle_show_mode')
def toggle_show_mode():
    global showMode
    showMode = not showMode
    emit('show_mode', {'showMode': showMode}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=4999, debug=True)
