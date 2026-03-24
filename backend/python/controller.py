from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from functools import wraps
import game, auth
import os
import jwt

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
        if not token:
            return jsonify({"error": "Missing auth token!"}), 401
        try:
            game_id = auth.verify_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Expired token!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        return f(game_id, *args, **kwargs)
    return decorated

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({"message": "It Works!"})

@app.route('/api/start-session', methods=['POST'])
def start_session():
    user_id = request.json.get("userId")
    if not user_id:
        return jsonify({"error": "User ID not avaiable!"}), 400
    token = auth.start_session(user_id)
    return jsonify({"token": token}), 200

@app.route('/api/end-session', methods=['POST'])
@require_auth
def end_session(game_id):
    auth.end_session(game_id)
    return jsonify({"status": "ok"}), 200

@app.route('/api/init', methods=['POST'])
def init_game():
    token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
    try:
        game_id = auth.verify_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return jsonify({"action": "login"}), 200

    state = game.init(game_id)
    return jsonify(state), 200

@app.route('/api/roll', methods=['POST'])
@require_auth
def roll_dice(game_id):
    return jsonify(game.roll_dice(game_id))

@app.route('/api/hold', methods=['POST'])
@require_auth
def hold_score(game_id):
    return jsonify(game.hold_score(game_id))


# ---------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
