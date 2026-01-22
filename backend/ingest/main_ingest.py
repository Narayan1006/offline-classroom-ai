import json
import os
import sys

from backend.ingest.extract_audio import extract_audio
from backend.ingest.transcribe import transcribe_audio
from backend.ingest.topics import extract_topics
from backend.ingest.structure_lesson import structure_lesson


BASE_DIR = "backend/data"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
LESSON_DIR = os.path.join(BASE_DIR, "lessons")


def ingest_lesson(video_path):
    """
    Process a video file into a structured lesson.
    
    Args:
        video_path: Path to video file
    
    Returns:
        str: Path to structured lesson JSON, or None if processing failed
    """
    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.makedirs(LESSON_DIR, exist_ok=True)

    print("🎥 Video selected:", video_path)

    # Extract audio from video
    audio_path = extract_audio(video_path, AUDIO_DIR)
    
    # HANDLE NO AUDIO CASE
    if audio_path is None:
        print("❌ Cannot process video without audio track")
        return None
    
    print("🔊 Audio extracted")

    # Transcribe audio to text
    try:
        transcript, segments = transcribe_audio(audio_path)
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        return None
    
    print("🧠 Transcription complete")

    # Extract main topics from transcript
    try:
        topics = extract_topics(transcript)
        print("🏷 Topics:", topics)
    except Exception as e:
        print(f"⚠️  Topic extraction failed: {e}")
        topics = ["General"]  # Fallback to general topic

    # Build lesson JSON
    lesson = {
        "transcript": transcript,
        "segments": segments,
        "topics": topics
    }

    lesson_path = os.path.join(LESSON_DIR, "lecture.json")
    try:
        with open(lesson_path, "w", encoding="utf-8") as f:
            json.dump(lesson, f, indent=2, ensure_ascii=False)
        print("📄 lesson.json written")
    except Exception as e:
        print(f"❌ Error saving lesson.json: {e}")
        return None

    # Structure the lesson
    try:
        structured_path = structure_lesson(lesson_path)
        print("✅ Structured lesson created:", structured_path)
        return structured_path
    except Exception as e:
        print(f"❌ Error structuring lesson: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python -m backend.ingest.main_ingest <video_path>")
        sys.exit(1)

    result = ingest_lesson(sys.argv[1])
    if result:
        print(f"✅ Success: {result}")
    else:
        print("❌ Failed to process video")