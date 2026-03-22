from flask import Flask, jsonify, request
from flask_cors import CORS
import game

app = Flask(__name__)
CORS(app)

user_id = None


@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({"message": "It Works!"})

@app.route('/api/start-session', methods=['POST'])
def start_session():
    global user_id
    user_id = request.json.get("userId")
    if not user_id:
        return jsonify({"error": "User ID not avaiable!"}), 400
    return jsonify({"status": "ok"}), 200

@app.route('/api/init', methods=['POST'])
def init_game():
    if not user_id:
        return jsonify({"-":"-", "action": "login"})
    return jsonify(game.init())

@app.route('/api/roll', methods=['POST'])
def roll_dice():
    if not user_id:
        return jsonify({"-":"-", "action": "login"})    
    return jsonify(game.roll_dice())

@app.route('/api/hold', methods=['POST'])
def hold_score():
    if not user_id:
        return jsonify({"-":"-", "action": "login"})    
    return jsonify(game.hold_score())


# ---------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
