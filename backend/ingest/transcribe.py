from faster_whisper import WhisperModel
import os

# Load Whisper model once (small model for CPU)
model = WhisperModel("small", device="cpu", compute_type="int8")


def transcribe_audio(audio_path):
    """
    Transcribe audio file to text using Whisper.
    
    Args:
        audio_path: Path to audio file (WAV, MP3, etc.)
    
    Returns:
        tuple: (full_transcript_text, list_of_segments)
        where segments = [{"start": float, "end": float, "text": str}, ...]
    """
    try:
        print(f"🗣️ Transcribing: {audio_path}")
        
        # Run Whisper transcription
        segments, info = model.transcribe(audio_path)
        
        transcript_list = []
        segment_list = []
        
        # Collect segments and build full transcript
        for seg in segments:
            transcript_list.append(seg.text)
            segment_list.append({
                "start": seg.start,
                "end": seg.end,
                "text": seg.text
            })
        
        # Join all text into one transcript
        full_transcript = " ".join(transcript_list)
        
        print(f"✅ Transcription complete: {len(full_transcript)} characters")
        
        return full_transcript, segment_list
    
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        raise