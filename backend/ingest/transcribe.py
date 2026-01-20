from faster_whisper import WhisperModel
import os

# Load once (CPU-friendly)
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

def transcribe_audio(audio_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    segments, info = model.transcribe(audio_path)

    full_text = []
    segment_list = []

    for seg in segments:
        full_text.append(seg.text)
        segment_list.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text
        })

    transcript_text = " ".join(full_text)

    transcript_path = os.path.join(output_dir, "transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    return transcript_path, segment_list
