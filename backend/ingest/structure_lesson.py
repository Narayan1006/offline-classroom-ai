import json
import re
from collections import defaultdict


def extract_keywords(segment_text, topic):
    """
    Extract relevant keywords from segment text.
    Looks for capitalized words and terms that might be important.
    """
    # Find capitalized words (likely proper nouns/important terms)
    capitalized = re.findall(r'\b[A-Z][a-z]+\b', segment_text)
    
    # Also get longer words (4+ chars) that appear frequently
    words = re.findall(r'\b[a-z]{4,}\b', segment_text.lower())
    
    # Combine and deduplicate
    all_terms = list(set(capitalized + words))
    
    # Remove the topic itself from keywords
    all_terms = [t for t in all_terms if t.lower() != topic.lower()]
    
    # Return top 8 keywords
    return all_terms[:8]


def structure_lesson(lesson_json_path):
    """
    Structure lesson into concepts with segments and keywords.
    Creates a _structured.json file for use by the QA system.
    """
    try:
        with open(lesson_json_path, "r", encoding="utf-8") as f:
            lesson = json.load(f)
    except Exception as e:
        print(f"Error loading lesson: {e}")
        return None

    segments = lesson.get("segments", [])
    topics = lesson.get("topics", [])

    if not segments or not topics:
        print("Warning: No segments or topics found in lesson")

    concept_map = defaultdict(list)

    # Map segments to concepts
    for seg in segments:
        text = seg.get("text", "").lower()
        for topic in topics:
            if topic.lower() in text:
                concept_map[topic].append(seg)

    # Build structured output
    structured = {
        "concepts": []
    }

    for topic in topics:
        segs = concept_map.get(topic, [])
        all_text = " ".join([s.get("text", "") for s in segs])
        
        structured["concepts"].append({
            "name": topic,
            "segments": segs,
            "keywords": extract_keywords(all_text, topic),
            "allowed": True
        })

    # Write structured JSON
    out_path = lesson_json_path.replace(".json", "_structured.json")
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(structured, f, indent=2, ensure_ascii=False)
        print(f"✅ Structured lesson saved: {out_path}")
    except Exception as e:
        print(f"❌ Error saving structured lesson: {e}")
        return None

    return out_path