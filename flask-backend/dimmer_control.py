# flask-backend/dimmer_control.py

import requests
import time
import threading
from xml.etree import ElementTree as ET

dimmer_racks = [
    '192.168.0.3',
    '192.168.0.4',
    '192.168.0.5'
]

lights = {
    'house': [72],
    'front': [25, 26, 27, 21, 20, 19],
    'sides': [31, 37, 8, 2, 9, 3],
    'tops': [7, 13, 1, 14, 15, 16]
}

api_config = {
    'min_delay_between_calls': 0.1  # in seconds
}

last_call_timestamp = 0
last_sent_values = {}
current_levels = {}

def send_command(xml_command):
    responses = []
    for ip in dimmer_racks:
        try:
            response = requests.post(
                f'http://{ip}/goform/dimmertest',
                headers={'Content-Type': 'text/xml'},
                data=xml_command
            )
            responses.append(response)
        except requests.RequestException as e:
            print(f"Error sending command to {ip}: {e}")
    return responses

def rate_limited_send_command(xml_command):
    global last_call_timestamp
    now = time.time()
    if now - last_call_timestamp < api_config['min_delay_between_calls']:
        time.sleep(api_config['min_delay_between_calls'] - (now - last_call_timestamp))
    last_call_timestamp = now
    return send_command(xml_command)

def release_all_lights():
    xml_command = '<release_all space="1" />'
    rate_limited_send_command(xml_command)

def set_light_level(light_set_name, level):
    if level == 0:
        release_all_lights()
        return

    channels = lights.get(light_set_name)
    if not channels:
        print(f"No channels found for light set: {light_set_name}")
        return

    sorted_channels = sorted(channels)
    channel_key = ','.join(map(str, sorted_channels))

    if last_sent_values.get(channel_key) == level:
        return
    last_sent_values[channel_key] = level

    xml_commands = ''.join([f'<set udn="{channel}" space="1" level="{level}" side="both"/>' for channel in sorted_channels])
    xml_command = f'<setlevels>{xml_commands}</setlevels>'
    rate_limited_send_command(xml_command)

def fetch_light_levels():
    xml_command = '<setlevels><get udn="all"/></setlevels>'
    try:
        responses = rate_limited_send_command(xml_command)
        levels = {}
        for res in responses:
            tree = ET.ElementTree(ET.fromstring(res.text))
            for info in tree.findall('.//info'):
                udn = info.get('udn')
                level = info.get('level')
                levels[udn] = level
        return levels
    except Exception as e:
        print(f"Failed to fetch light levels: {e}")
        return {}

def get_light_level(light_set_name):
    channels = lights.get(light_set_name)
    if not channels:
        return 0

    all_levels = fetch_light_levels()
    relevant_levels = [int(all_levels.get(str(channel), 0)) for channel in channels]
    if not relevant_levels:
        return 0

    average_level = sum(relevant_levels) / len(relevant_levels)
    return average_level

def poll_light_levels():
    global current_levels
    while True:
        current_levels = fetch_light_levels()
        time.sleep(0.5)

polling_thread = threading.Thread(target=poll_light_levels)
polling_thread.daemon = True
polling_thread.start()
