from moviepy.editor import VideoFileClip
import os


def extract_audio(video_path, output_dir):
    """
    Extract audio from video file and save as WAV.
    
    Args:
        video_path: Path to video file
        output_dir: Directory to save audio file
    
    Returns:
        str: Path to extracted audio file, or None if no audio
    
    Raises:
        Exception: If extraction fails for other reasons
    """
    os.makedirs(output_dir, exist_ok=True)

    audio_path = os.path.join(output_dir, "audio.wav")

    try:
        print(f"🎬 Loading video: {video_path}")
        video = VideoFileClip(video_path)
        
        # Check if video has audio - HANDLE THIS GRACEFULLY
        if video.audio is None:
            print("⚠️  Video has no audio track")
            video.close()
            
            # Return None instead of crashing
            return None
        
        print(f"🔊 Extracting audio to: {audio_path}")
        
        # Write audio to file with minimal verbosity
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        # Close the video file
        video.close()
        
        print(f"✅ Audio extracted successfully: {audio_path}")
        return audio_path
    
    except Exception as e:
        print(f"❌ Error extracting audio: {str(e)}")
        raise