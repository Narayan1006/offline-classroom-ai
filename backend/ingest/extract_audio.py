from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def extract_audio(video_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    audio_path = os.path.join(output_dir, "audio.wav")

    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, logger=None)

    return audio_path
