import random

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

game = {}

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({"message": "It Works!"})


@app.route('/api/init', methods=['POST'])
def init_game():
    global game
    game = {
        "scores": [0, 0],
        "currentScore": 0,
        "activePlayer": 0,
        "dice": None,
        "winner": None
    }    
    return jsonify(**game)


@app.route('/api/roll', methods=['POST'])
def roll_dice():
    dice = random.randint(1, 6)
    game["dice"] = dice

    if dice == 1:
        game["currentScore"] = 0
        game["activePlayer"] = 1 - game["activePlayer"]
    else:
        game["currentScore"] += dice

    return jsonify(**game)


@app.route('/api/hold', methods=['POST'])
def hold_score():
    p = game["activePlayer"]
    game["scores"][p] += game["currentScore"]
    game["currentScore"] = 0
    if game["scores"][p] >= 100:
        game["winner"] = p
    else:
        game["activePlayer"] = 1 - p

    return jsonify(**game)


# ---------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
