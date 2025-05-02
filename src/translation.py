import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# nllb-200 모델을 사용하여 영어를 한국어로 번역하는 함수
def translate_text_nllb(english_text: str, model_name: str = "facebook/nllb-200-distilled-600M") -> str:
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.config.forced_bos_token_id = tokenizer.convert_tokens_to_ids("kor_Hang")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    inputs = tokenizer(english_text, return_tensors="pt", truncation=True, padding=True).to(device)
    outputs = model.generate(**inputs, max_length=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
