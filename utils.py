import os
import json

NOTES_FILE = "notes.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as file:
            return json.load(file)
    else:
        return {"r_cheatsheet": {}}

def save_notes(notes):
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, indent=4)
