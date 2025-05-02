import os
import re
import csv

# SRT 파일에 저장된 시간 형식은 'HH:MM:SS,mmm'이므로 이를 초 단위로 변환하는 함수
def time_to_seconds(time_str):
    h, m, s_ms = time_str.split(':')
    s, ms = s_ms.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
# SRT 파일을 CSV 파일로 변환하는 함수
def srt_to_csv(srt_path, csv_path):
    
    # SRT 파일이 존재하는지 확인
    if not os.path.exists(srt_path):
        raise FileNotFoundError(f"입력 파일을 찾을 수 없습니다: {srt_path}")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    # SRT 파일을 읽어오기
    with open(srt_path, 'r', encoding='utf-8') as srt_file:
        srt_content = srt_file.read()

    # SRT 파일의 각 블록을 분리
    blocks = re.split(r'\n\s*\n', srt_content.strip())
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['start_time', 'end_time', 'text'])
        for block in blocks:
            lines = block.splitlines()
            if len(lines) >= 3:
                start_time_str, end_time_str = lines[1].split(' --> ')
                text = " ".join(lines[2:]).strip()
                start = time_to_seconds(start_time_str)
                end = time_to_seconds(end_time_str)
                writer.writerow([start, end, text])
