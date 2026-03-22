import random


game = {}

def init():
    global game
    game = {
        "scores": [0, 0],
        "currentScore": 0,
        "activePlayer": 0,
        "dice": None,
        "winner": None
    }    
    return {**game, "action": "new"}

def roll_dice():
    dice = random.randint(1, 6)
    game["dice"] = dice

    if dice == 1:
        game["currentScore"] = 0
        game["activePlayer"] = 1 - game["activePlayer"]
        action = "switch"
    else:
        game["currentScore"] += dice
        action = "update"

    return {**game, "action": action}

def hold_score():
    p = game["activePlayer"]
    game["scores"][p] += game["currentScore"]
    game["currentScore"] = 0
    if game["scores"][p] >= 100:
        game["winner"] = p
        action = "winner"
    else:
        game["activePlayer"] = 1 - p
        action = "switch"

    return {**game, "action": action}

