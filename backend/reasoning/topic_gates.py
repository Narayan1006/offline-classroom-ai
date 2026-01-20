import json

def load_concepts(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["concepts"]

def is_question_allowed(question, concepts):
    question = question.lower()

    for concept in concepts:
        if concept["name"].lower() in question:
            return True, concept

        for kw in concept["keywords"]:
            if kw.lower() in question:
                return True, concept

    return False, None
