import json
import random

def load_structured_lesson(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_questions(structured_path, per_concept=5):
    data = load_structured_lesson(structured_path)
    concepts = data.get("concepts", [])

    all_questions = []

    for concept in concepts:
        name = concept["name"]
        keywords = concept.get("keywords", [])

        questions = [
            f"What is {name}?",
            f"Explain {name} in your own words.",
            f"Why is {name} important?",
            f"Give an example related to {name}.",
            f"Where is {name} used in real life?"
        ]

        # Add keyword-based questions
        for kw in random.sample(keywords, min(2, len(keywords))):
            questions.append(
                f"How is '{kw}' related to {name}?"
            )

        all_questions.append({
            "concept": name,
            "questions": questions[:per_concept]
        })

    return all_questions


if __name__ == "__main__":
    questions = generate_questions(
        "backend/data/lessons/lecture_structured.json"
    )

    for block in questions:
        print(f"\n📘 Concept: {block['concept']}")
        for q in block["questions"]:
            print(" -", q)
