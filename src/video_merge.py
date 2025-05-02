import os
import subprocess

# 비디오와 오디오 파일을 합치는 함수
def merge_video_audio(video_path, audio_path, output_path):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"비디오 파일을 찾을 수 없습니다: {video_path}")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"오디오 파일을 찾을 수 없습니다: {audio_path}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("ffmpeg로 비디오와 오디오를 합치는 중...")
    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-ac", "2",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        output_path
    ]
    subprocess.run(command, check=True)
    print(f"합성 완료! 결과 파일: {output_path}")
