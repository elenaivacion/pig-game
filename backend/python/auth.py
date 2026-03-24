import uuid
import datetime
import jwt

# we should move this into an environment variable/configuration file
SECRET_KEY = "change-this-in-production"


users = {}

def start_session(user_id):
    if user_id not in users:
        users[user_id] = str(uuid.uuid4())

    game_id = users[user_id]

    token = jwt.encode(
        {
            "user_id": user_id,
            "game_id": game_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    return token

def end_session(game_id):
    for key, value in list(users.items()):
        if value == game_id:
            del users[key]
            break

def verify_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload["game_id"]
