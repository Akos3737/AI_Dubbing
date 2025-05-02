import os
from moviepy.video.io.VideoFileClip import VideoFileClip

# 입력된 비디오에서 오디오를 추출하는 함수
def extract_audio_from_video(video_path: str, audio_path: str = "extracted.wav"):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, codec='pcm_s16le')
    return audio_path, video.duration
