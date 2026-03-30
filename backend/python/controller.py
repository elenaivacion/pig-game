from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flasgger import Swagger
from functools import wraps
import game, auth
import os
import jwt

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)
swagger = Swagger(app)


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
        if not token:
            return jsonify({"error": "Missing auth token!", "action": "login"}), 401
        try:
            game_id = auth.verify_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Expired token!", "action": "login"})), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!", "action": "login"}), 401
        return f(game_id, *args, **kwargs)
    return decorated

@app.route('/')
def index():
    """
    Serves the main game interface (Frontend).
    ---
    tags:
      - Static Content
    summary: Load Game UI
    description: Returns the main index.html file that initializes the Pig Game frontend application.
    responses:
      200:
        description: HTML page loaded successfully.
        schema:
          type: string
          example: "<!DOCTYPE html>..."
      404:
        description: Frontend files not found.
    """
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    """
    Check the API operational status.
    ---
    tags:
      - System
    summary: Health check endpoint
    description: Returns the current status of the API to verify if the service is up and running.
    responses:
      200:
        description: Service is operational.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "It Works!"
      503:
        description: Service Unavailable - The server is down or undergoing maintenance.
    """
    return jsonify({"message": "It Works!"}), 200

@app.route('/api/init', methods=['POST'])
@require_auth
def init_game(game_id):
    """
    Initializes or resets the game state within an active session.
    ---
    tags:
      - Game Logic
    summary: Initialize Game State
    description: >
      Resets all internal game variables (scores, current turn, dice) to their starting values.
      This should be called after 'start_session' to begin a new match within the same session.
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: 'Bearer token obtained from start_session (format: Bearer <token>)'
      - name: game_id
        in: path
        type: string
        required: true
        description: The unique ID of the game to be initialized.
    responses:
      200:
        description: Game state initialized successfully.
        schema:
          type: object
          properties:
            action:
              type: string
              example: "init"
            state:
              type: object
              description: The freshly reset game state object.
      401:
        description: 'Unauthorized - Token is invalid or expired. Action: login'
        schema:
          type: object
          properties:
            action:
              type: string
              example: "login"
            error:
              type: string
              example: "Invalid or expired token"
    """    
    token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
    try:
      game_id = auth.verify_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
      return jsonify({"action": "login", "error": "Invalid or expired token"}), 401
    
    state = game.init(game_id)
    return jsonify(state), 200

@app.route('/api/start-session', methods=['POST'])
def start_session():
    """
    User login/registration and session initialization.
    ---
    tags:
      - Authentication
    summary: Starts a new game session
    description: Registers a new user or logs in an existing one, returning a security token.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - userId
          properties:
            userId:
              type: string
              example: "player_99"
              description: Unique identifier for the player (name, nickname, email, etc.).
    responses:
      200:
        description: Session started successfully. Returns a JWT token.
        schema:
          type: object
          properties:
            token:
              type: string
              example: "eyJhbGciOiJIUzI1Ni..."
      400:
        description: Bad Request - Missing JSON body or userId.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User ID is required!"
      409:
        description: Conflict - User ID already in use.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User ID already in use!"
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "User ID is required! (Missing JSON body)"}), 400
    
    user_id = data.get("userId")
    
    # Validation logic
    if not user_id:
        return jsonify({"error": "User ID is required!"}), 400
        
    token = auth.start_session(user_id)
    if token is None:
        return jsonify({"error": "User ID already in use!"}), 409
    
    return jsonify({"token": token}), 200

@app.route('/api/end-session', methods=['POST'])
@require_auth
def end_session(game_id):
    """
    Terminates the current game session and releases the User ID.
    ---
    tags:
      - Authentication
    summary: Ends the active session
    description: >
      Closes the game session associated with the provided Bearer Token. 
      This will remove the User ID from the active list, allowing it to be used again for a new login.
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: 'JWT token (format: "Bearer <token>")'
      - name: game_id
        in: path
        type: string
        required: true
        description: The ID of the game session to terminate.
    responses:
      200:
        description: Session ended successfully and resources were cleared.
        schema:
          type: object
          properties:
            status:
              type: string
              example: "ok"
      401:
        description: Unauthorized - The token is missing, invalid, or expired.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid token!"
      500:
        description: Internal Server Error.
    """
    token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()

    user_id = None
    try:
        # extract user_id from the token
        payload = auth.get_payload(token)
        user_id = payload.get("user_id")
    except Exception as e:
        # something went wrong
        pass
    
    auth.end_session(game_id, user_id)

    return jsonify({"status": "ok"}), 200

@app.route('/api/roll', methods=['POST'])
@require_auth
def roll_dice(game_id):
    """
    Roll the dice for the current player.
    ---
    tags:
      - Game Play
    summary: Roll the dice
    description: >
      Triggers a dice roll for the active player in the specified game. 
      If the dice is 1, the turn score is reset and the turn passes to the next player.
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: 'JWT token (format: "Bearer <token>")'
      - name: game_id
        in: path
        type: string
        required: true
        description: The unique ID of the ongoing game.
    responses:
      200:
        description: Dice rolled successfully.
        schema:
          type: object
          properties:
            scores:
              type: integer
              example: 12
            currentScore:
              type: integer
              example: 25
            activePlayer:
              type: integer
              example: 1
            dice:
              type: integer
              example: 4
            winner:
              type: integer
              example: 0
            action:
              type: string
              example: "update"
      401:
        description: Unauthorized - Bearer token is missing or invalid.
      404:
        description: Not Found - Game ID does not exist.
      400:
        description: Bad Request - Game is already finished or invalid state.
    """
    return jsonify(game.roll_dice(game_id))

@app.route('/api/hold', methods=['POST'])
@require_auth
def hold_score(game_id):
    """
    Save the current turn score to the global score.
    ---
    tags:
      - Game Play
    summary: Hold current score
    description: >
      Adds the accumulated turn score to the player's total score and switches the turn to the next player.
      If the total score reaches the target, the player is declared the winner.
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: 'JWT token (format: "Bearer <token>")'
      - name: game_id
        in: path
        type: string
        required: true
        description: The unique ID of the active game session.
    responses:
      200:
        description: Score held successfully.
        schema:
          type: object
          properties:
            global_score:
              type: integer
              example: 45
            next_player:
              type: string
              example: "Player 2"
            is_winner:
              type: boolean
              example: false
      401:
        description: Unauthorized - Bearer token is missing or invalid.
      404:
        description: Not Found - Game ID does not exist.
      400:
        description: Bad Request - Action not allowed (e.g., no points to hold).
    """
    # Note for QA: Ensure game_id is extracted from the request body before calling the logic
    return jsonify(game.hold_score(game_id))

# ---------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
