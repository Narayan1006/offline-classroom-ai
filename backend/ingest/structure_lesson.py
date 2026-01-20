import json
import os
import re
from collections import defaultdict

def structure_lesson(lesson_path):
    with open(lesson_path, "r", encoding="utf-8") as f:
        lesson = json.load(f)

    transcript = lesson["transcript"]
    segments = lesson["segments"]
    raw_topics = lesson.get("topics", [])

    concept_map = defaultdict(lambda: {
        "segments": [],
        "keywords": set()
    })

    for seg in segments:
        text = seg["text"].lower()
        for topic in raw_topics:
            if topic.lower() in text:
                concept_map[topic]["segments"].append({
                    "start": seg["start"],
                    "end": seg["end"]
                })
                concept_map[topic]["keywords"].update(
                    re.findall(r"[a-zA-Z]{4,}", text)
                )

    concepts = []
    for topic, data in concept_map.items():
        if len(data["segments"]) == 0:
            continue

        concepts.append({
            "name": topic,
            "definition": "",
            "segments": data["segments"],
            "keywords": list(data["keywords"]),
            "allowed": True
        })

    structured = {
        "concepts": concepts,
        "raw_topics": raw_topics
    }

    out_path = lesson_path.replace(".json", "_structured.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(structured, f, indent=2)

    return out_path


if __name__ == "__main__":
    path = structure_lesson("backend/data/lessons/lecture.json")
    print("Structured lesson created:", path)
