import json
import os

NOTES_FILE = "backend/data/notes.json"

def load_notes(lesson_id="lecture"):
    if not os.path.exists(NOTES_FILE):
        return ""

    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get(lesson_id, {}).get("notes", "")


def save_notes(lesson_id, text):
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    data[lesson_id] = {"notes": text}

    os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
