# pip install faster-whisper
import os
os.environ["OMP_NUM_THREADS"] = "4"  # opcional, reforça limite de threads

from faster_whisper import WhisperModel

model = WhisperModel(
    "turbo",              # ou "medium"/"small"/"distil-large-v3"
    device="cpu",
    compute_type="int8",  # mantém o pico de RAM baixo
    cpu_threads=4
)

segments, info = model.transcribe(
    "audio.mp4",
    beam_size=1,                 # greedy
    vad_filter=True,             # ignora silêncios longos
    condition_on_previous_text=False
)

# imprime na tela e salva em TXT no mesmo loop (segments é um generator)
print(f"Idioma: {info.language} (p={info.language_probability:.2f})")
with open("transcricao.txt", "w", encoding="utf-8") as f:
    f.write(f"Idioma: {info.language} (p={info.language_probability:.2f})\n")
    for seg in segments:  # não converta para list(...)
        linha = f"[{seg.start:.2f}s -> {seg.end:.2f}s] {seg.text}"
        print(linha)
        f.write(linha + "\n")

print("Transcrição salva em transcricao.txt")
