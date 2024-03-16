from flask import Flask, jsonify
import json
##import pandas as pd

app = Flask(__name__)

# Load events data from JSON file
with open('..\data\events_data.json', 'r') as f:
    events_data = json.load(f)

# Load players data from JSON file
with open('..\data\players_data.json', 'r') as f:
    players_data = json.load(f)

# API endpoint to get events data
@app.route('/api/events', methods=['GET'])
def get_events_data():
    return jsonify(events_data)

# API endpoint to get players data
@app.route('/api/players', methods=['GET'])
def get_players_data():
    return jsonify(players_data)

if __name__ == '__main__':
    app.run(debug=True)