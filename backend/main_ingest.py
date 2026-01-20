from backend.ingest.extract_audio import extract_audio
from backend.ingest.transcribe import transcribe_audio
from backend.ingest.segment import extract_topics

import json
import os

def ingest_video(video_path):
    base_name = os.path.splitext(os.path.basename(video_path))[0]

    audio_path = extract_audio(
        video_path,
        "backend/data/transcripts"
    )

    transcript_path, segments = transcribe_audio(
        audio_path,
        "backend/data/transcripts"
    )

    with open(transcript_path, "r", encoding="utf-8") as f:
        text = f.read()

    topics = extract_topics(text)

    lesson = {
        "video": video_path,
        "transcript": text,
        "topics": topics,
        "segments": segments
    }

    os.makedirs("backend/data/lessons", exist_ok=True)
    lesson_path = f"backend/data/lessons/{base_name}.json"

    with open(lesson_path, "w", encoding="utf-8") as f:
        json.dump(lesson, f, indent=2)

    return lesson_path


if __name__ == "__main__":
    path = ingest_video("backend/data/videos/lecture.mp4")
    print("Lesson created:", path)
