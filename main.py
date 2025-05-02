from src.audio_utils import extract_audio_from_video
from src.transcription import transcribe_audio
from src.translation import translate_text_nllb
from src.srt_utils import save_text, save_single_srt
from src.tts_utils import process_batch
from src.video_merge import merge_video_audio
from src.srt_to_csv import srt_to_csv     
import argparse
from TTS.api import TTS
import os, csv

# TTS 모델을 로드하는 부분
tts = TTS(model_name="tts_models.multilingual.multi-dataset.xtts_v2", gpu=True)

# 항상 YES로 설정
os.environ["COQUI_TOS_AGREED"] = "1"

# 중복된 디렉토리를 피하기 위한 함수
def get_unique_save_dir(base_dir):
    if not os.path.exists(base_dir):
        return base_dir
    i = 1
    while True:
        new_dir = f"{base_dir}({i})"
        if not os.path.exists(new_dir):
            return new_dir
        i += 1

if __name__ == "__main__":
    # 비디오 파일 경로와 HuggingFace 토큰을 인자로 받기 위한 argparse 설정
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", type=str, required=True, help="입력 비디오 파일 경로")
    args = parser.parse_args()

    video_path = args.video_path
    absolute_path = os.path.abspath(video_path)


    reference_wav = "sample_voice.wav"
    absolute_ref_path = os.path.abspath(reference_wav)

    base_name = os.path.splitext(os.path.basename(absolute_path))[0]
    base_save_dir = os.path.join("outputs", base_name)
    save_dir = get_unique_save_dir(base_save_dir)
    os.makedirs(save_dir, exist_ok=True)

    audio_path, duration = extract_audio_from_video(absolute_path, os.path.join(save_dir, "audio.wav"))
    english_text = transcribe_audio(audio_path)
    korean_text = translate_text_nllb(english_text)

    save_text(english_text, os.path.join(save_dir, "english.txt"))
    save_text(korean_text, os.path.join(save_dir, "korean.txt"))

    save_single_srt(english_text, duration, os.path.join(save_dir, "subtitle_en.srt"))
    save_single_srt(korean_text, duration, os.path.join(save_dir, "subtitle_ko.srt"))

    # TTS
    srt_path = os.path.join(save_dir, "subtitle_ko.srt")
    csv_path = os.path.join(save_dir, "timing_script.csv")
    srt_to_csv(srt_path, csv_path)
    
    output_dir = os.path.join(save_dir, "tts_segments")
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(save_dir, "timing_script.csv"), mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        texts, durations, idxs = [], [], []
        for idx, row in enumerate(reader):
            text = row["text"].strip()
            start = float(row["start_time"])
            end = float(row["end_time"])
            duration = end - start
            if not text or duration <= 0:
                continue
            texts.append(text)
            durations.append(duration)
            idxs.append(idx)
            if len(texts) == 2:
                process_batch(tts, texts, durations, idxs, output_dir, absolute_ref_path)
                texts, durations, idxs = [], [], []
        if texts:
            process_batch(tts, texts, durations, idxs, output_dir, absolute_ref_path)

    merge_video_audio(absolute_path, os.path.join(output_dir, "line_000.wav"), os.path.join(save_dir, "output_dubbed.mp4"))
