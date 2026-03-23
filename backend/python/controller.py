from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_cors import CORS
import game
import os

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

user_id = None



@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

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

@app.route('/api/end-session', methods=['POST'])
def end_session():
    global user_id
    tmp_user_id = request.json.get("userId")
    if user_id != tmp_user_id:
        return jsonify({"error": "User ID not avaiable!"}), 400
    user_id = None
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
