import random


# game_id -> game session data
games = {}
NOT_INITIALIZED = {"scores": None, "currentScore": None, "activePlayer": None, "dice": None, "winner": None, "action": "init"}

def init(game_id):
    games[game_id] = {
        "scores": [0, 0],
        "currentScore": 0,
        "activePlayer": 0,
        "dice": None,
        "winner": None
    }    
    return {**games[game_id], "action": "new"}

def roll_dice(game_id):
    state = games.get(game_id)
    if state is None:
        return NOT_INITIALIZED
        
    dice = random.randint(1, 6)
    state["dice"] = dice

    if dice == 1:
        state["currentScore"] = 0
        state["activePlayer"] = 1 - state["activePlayer"]
        action = "switch"
    else:
        state["currentScore"] += dice
        action = "update"

    return {**state, "action": action}

def hold_score(game_id):
    state = games.get(game_id)
    if state is None:
        return NOT_INITIALIZED
        
    p = state["activePlayer"]
    state["scores"][p] += state["currentScore"]
    state["currentScore"] = 0
    if state["scores"][p] >= 100:
        state["winner"] = p
        action = "winner"
    else:
        state["activePlayer"] = 1 - p
        action = "switch"

    return {**state, "action": action}

