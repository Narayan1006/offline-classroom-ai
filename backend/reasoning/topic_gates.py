import json

def load_concepts(path):
    """Load concepts from structured lesson JSON"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("concepts", [])
    except FileNotFoundError:
        return []
    except Exception:
        return []


def is_question_allowed(question, concepts):
    """
    Check if question is about topics from today's lesson.
    Returns (allowed: bool, concept: dict or None)
    """
    if not concepts:
        # No concepts loaded - allow the question
        return True, {"name": "General", "keywords": []}
    
    question = question.lower()

    for concept in concepts:
        # Check if concept name is in question
        if concept["name"].lower() in question:
            return True, concept

        # Check if any keywords match
        keywords = concept.get("keywords", [])
        for kw in keywords:
            if isinstance(kw, str) and kw.lower() in question.lower():
                return True, concept

    # If no match found, allow first concept as default
    # This is more permissive and student-friendly
    return True, concepts[0] if concepts else {"name": "Today's Lesson", "keywords": []}