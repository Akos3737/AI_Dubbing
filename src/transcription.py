import whisper

# Whisper 모델을 사용하여 음성을 텍스트로 변환하는 함수
def transcribe_audio(audio_path: str, model_size: str = "base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path, language='en')
    return result["text"]
