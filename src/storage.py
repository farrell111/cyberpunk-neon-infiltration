import json
import os

SAVE_PATH = os.path.join("data", "save_data.json")

DEFAULT_DATA = {
    "credits": 0,
    "highest_level": 1,
    "unlocked_chars": ["Specter"],
    "active_char": "Specter"
}

def load_game_data() -> dict:
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(SAVE_PATH):
        save_game_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()
    try:
        with open(SAVE_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATA.copy()

def save_game_data(data: dict):
    if not os.path.exists("data"):
        os.makedirs("data")
    with open(SAVE_PATH, "w") as f:
        json.dump(data, f, indent=4)