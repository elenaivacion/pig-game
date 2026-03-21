from flask import Flask, jsonify, request
from flask_cors import CORS
import game

app = Flask(__name__)
CORS(app)



@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({"message": "It Works!"})

@app.route('/api/init', methods=['POST'])
def init_game():
    return jsonify(game.init())

@app.route('/api/roll', methods=['POST'])
def roll_dice():
    return jsonify(game.roll_dice())

@app.route('/api/hold', methods=['POST'])
def hold_score():
    return jsonify(game.hold_score())


# ---------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
