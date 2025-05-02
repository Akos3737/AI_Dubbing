import os
import numpy as np
import soundfile as sf
from scipy.signal import resample
from TTS.api import TTS
import torch

# TTS 모델을 로드하는 함수
def load_tts_model(model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2") -> TTS:
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA가 감지되지 않았습니다. 이 코드는 CUDA 환경에서만 실행됩니다.")
    print(f"사용 중인 장치: {torch.cuda.get_device_name(0)}")

    print("XTTS 모델 로딩 중...")
    tts = TTS(model_name=model_name)
    tts.to(torch.device("cuda"))
    print(f"모델 로딩 완료! (모델: {model_name})")
    return tts

# TTS 모델을 사용하여 텍스트를 음성으로 변환하는 함수
def process_batch(tts: TTS, texts, durations, idxs, output_dir, reference_wav):
    print(f"{idxs[0]:03d}~{idxs[-1]:03d}번 TTS 시작 ({len(texts)}개 batch)")
    wavs = []
    for text in texts:
        try:
            audio = tts.tts(
                text=text,
                speaker_wav=reference_wav,
                language="ko",
                speed=1.0,
                temperature=0.3,
                repetition_penalty=5.0,
                length_penalty=1.0
            )
            wavs.append(audio)
            print(f"텍스트 생성 성공: {text[:50]}...")
        except Exception as e:
            print(f"오류 발생 - 텍스트: {text}\n에러: {str(e)}")
            wavs.append(np.zeros(44100))  # 1초 무음

    for audio, duration, id in zip(wavs, durations, idxs):
        try:
            original_len = len(audio)
            target_len = max(int(44100 * duration), 1)
            if original_len > 0:
                audio = resample(audio, target_len)
                audio = np.clip(audio, -1.0, 1.0)
                audio = (audio * 32767).astype(np.int16)
                output_path = os.path.join(output_dir, f"line_{id:03d}.wav")
                sf.write(output_path, audio, 44100)
                print(f"저장 완료: {output_path}")
            else:
                print(f"경고: {id:03d}번 오디오 길이가 0입니다.")
        except Exception as e:
            print(f"오디오 처리 중 오류 발생 - ID: {id}\n에러: {str(e)}")
