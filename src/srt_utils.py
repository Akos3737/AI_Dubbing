import os

# 텍스트를 파일에 저장하는 함수
def save_text(text: str, filename: str):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text.strip())

# 시간 단위를 포맷팅하는 함수
def format_timestamp(seconds: float):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

# 시작과 끝 시간을 받아 SRT 형식으로 저장하는 함수
def save_single_srt(text: str, duration: float, filename: str):
    start = format_timestamp(0)
    end = format_timestamp(duration)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"1\n{start} --> {end}\n{text.strip()}\n\n")
