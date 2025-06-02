import json
import os

SCORE_FILE = "highscores.json"

def load_high_scores():
    if not os.path.exists(SCORE_FILE):
        return {"easy": 0, "hard": 0}
    with open(SCORE_FILE, "r") as f:
        return json.load(f)

def save_high_scores(high_scores):
    with open(SCORE_FILE, "w") as f:
        json.dump(high_scores, f)
