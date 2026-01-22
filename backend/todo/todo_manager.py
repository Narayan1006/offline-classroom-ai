import json
import os

TODO_FILE = "backend/data/todo.json"


def load_tasks(lesson_id="lecture"):
    if not os.path.exists(TODO_FILE):
        return []

    with open(TODO_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get(lesson_id, [])


def save_tasks(lesson_id, tasks):
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    data[lesson_id] = tasks

    os.makedirs(os.path.dirname(TODO_FILE), exist_ok=True)
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
