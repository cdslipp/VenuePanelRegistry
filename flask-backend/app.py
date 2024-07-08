# flask-backend/app.py

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import threading
import time
import requests
import dimmer_control
import kasa_control
import asyncio

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

showMode = False

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello from Flask!")

@app.route('/api/companion/<int:page>/<int:button>', methods=['GET'])
def send_companion_command(page, button):
    try:
        response = requests.get(f'http://host.docker.internal:8000/press/bank/{page}/{button}')
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify(error=str(e)), 500

@app.route('/api/set_light_level/<string:light_set>/<int:level>', methods=['POST'])
def set_light_level(light_set, level):
    dimmer_control.set_light_level(light_set, level)
    return jsonify(success=True)

@app.route('/api/get_light_level/<string:light_set>', methods=['GET'])
def get_light_level(light_set):
    level = dimmer_control.get_light_level(light_set)
    return jsonify(level=level)

@app.route('/api/tplight/turn_on', methods=['POST'])
def turn_on_tplight():
    result = asyncio.run(kasa_control.turn_on_work_lights())
    if result:
        return jsonify(error=result), 500
    return jsonify(success=True)

@app.route('/api/tplight/turn_off', methods=['POST'])
def turn_off_tplight():
    result = asyncio.run(kasa_control.turn_off_work_lights())
    if result:
        return jsonify(error=result), 500
    return jsonify(success=True)

@app.route('/api/tplight/state', methods=['GET'])
def tplight_state():
    state, error = asyncio.run(kasa_control.get_work_lights_state())
    if error:
        return jsonify(error=error), 500
    return jsonify(is_on=state)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('show_mode', {'showMode': showMode})
    emit('light_levels', dimmer_control.current_levels)

@socketio.on('toggle_show_mode')
def toggle_show_mode():
    global showMode
    showMode = not showMode
    emit('show_mode', {'showMode': showMode}, broadcast=True)

def broadcast_light_levels():
    while True:
        socketio.emit('light_levels', dimmer_control.current_levels)
        time.sleep(0.5)

if __name__ == '__main__':
    threading.Thread(target=broadcast_light_levels, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=4999, debug=True)
