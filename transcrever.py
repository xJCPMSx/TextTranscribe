# pip install faster-whisper
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cpu", compute_type="int8")  # ou device="cuda", compute_type="float16"
segments, info = model.transcribe("audio.mp4", beam_size=5)
print(f"Idioma detectado: {info.language} (p={info.language_probability:.2f})")
for seg in segments:
    print(f"[{seg.start:.2f}s -> {seg.end:.2f}s] {seg.text}")
