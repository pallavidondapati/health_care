import whisper

model = whisper.load_model("medium")

# Check all language probabilities, not just the top one
import numpy as np

audio = whisper.load_audio(r"c:/Users/pallavi/OneDrive/New folder/Mental Health Triage/test_converted.wav")
audio_clip = whisper.pad_or_trim(audio)
mel = whisper.log_mel_spectrogram(audio_clip).to(model.device)
_, probs = model.detect_language(mel)

# Print top 5 detected languages
top5 = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:5]
for lang, prob in top5:
    print(f"{lang}: {prob:.3f}")