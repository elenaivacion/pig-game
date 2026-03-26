import uuid
import datetime
import jwt

# we should move this into an environment variable/configuration file
SECRET_KEY = "change-this-in-production"


users = {}

def start_session(user_id):
    # check if user id is already in use
    if user_id in users:
        return None
    
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

def end_session(game_id, user_id=None):
    if user_id and user_id in users:
        if users[user_id] == game_id:
            del users[user_id]
            return True    
    
    for uid, gid in list(users.items()):
        if gid == game_id:
            del users[uid]
            return True

    return False

def verify_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = payload["user_id"]

    # check if user_id has a registered session
    if user_id in users:
        return payload["game_id"]
    else:
        # somehow a correct token was used, but there is no session for it
        raise jwt.InvalidTokenError 

def get_payload(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
