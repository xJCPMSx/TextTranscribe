import os
import argparse
import json
from faster_whisper import WhisperModel

def format_timestamp(seconds):
    """Formats a timestamp in HH:MM:SS,mmm format."""
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio/video files using faster-whisper.")
    parser.add_argument("input_file", help="Path to the input audio/video file (e.g., audio.mp4).")
    parser.add_argument("--format", choices=["txt", "srt", "json"], default="txt",
                        help="Output format (txt, srt, json). Default is txt.")
    parser.add_argument("--output", help="Output file path. Defaults to 'transcricao.<format>'.")
    parser.add_argument("--model", default="turbo",
                        help="Whisper model to use (e.g., 'turbo', 'medium', 'small', 'distil-large-v3').")
    parser.add_argument("--device", default="cpu", help="Device to use for inference (e.g., 'cpu', 'cuda').")
    parser.add_argument("--compute_type", default="int8", help="Compute type (e.g., 'int8', 'float16').")
    parser.add_argument("--cpu_threads", type=int, default=4, help="Number of CPU threads for inference.")

    args = parser.parse_args()

    # Set OMP_NUM_THREADS if cpu_threads is specified
    if args.device == "cpu" and args.cpu_threads:
        os.environ["OMP_NUM_THREADS"] = str(args.cpu_threads)

    model = WhisperModel(
        args.model,
        device=args.device,
        compute_type=args.compute_type,
        cpu_threads=args.cpu_threads if args.device == "cpu" else None
    )

    segments, info = model.transcribe(
        args.input_file,
        beam_size=1,
        vad_filter=True,
        condition_on_previous_text=False
    )

    output_filename = args.output
    if not output_filename:
        output_filename = f"transcricao.{args.format}"

    print(f"Idioma: {info.language} (p={info.language_probability:.2f})")

    with open(output_filename, "w", encoding="utf-8") as f:
        if args.format == "txt":
            f.write(f"Idioma: {info.language} (p={info.language_probability:.2f})\n")
            for seg in segments:
                line = f"[{seg.start:.2f}s -> {seg.end:.2f}s] {seg.text}"
                print(line)
                f.write(line + "\n")
        elif args.format == "srt":
            for i, seg in enumerate(segments):
                f.write(f"{i + 1}\n")
                f.write(f"{format_timestamp(seg.start)} --> {format_timestamp(seg.end)}\n")
                f.write(f"{seg.text}\n\n")
        elif args.format == "json":
            # For JSON, we'll write segments as they come, but wrap in a list structure
            # This is a simplified streaming JSON output. A more robust solution might
            # involve writing a JSON array incrementally or using a custom JSON encoder.
            f.write("{\"language\": \"" + info.language + "\", \"language_probability\": " + str(info.language_probability) + ", \"segments\": [")
            first_segment = True
            for seg in segments:
                if not first_segment:
                    f.write(", ")
                json.dump({
                    "id": seg.id,
                    "seek": seg.seek,
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text,
                    "tokens": seg.tokens,
                    "temperature": seg.temperature,
                    "avg_logprob": seg.avg_logprob,
                    "compression_ratio": seg.compression_ratio,
                    "no_speech_prob": seg.no_speech_prob
                }, f, ensure_ascii=False)
                first_segment = False
            f.write("]}")

    print(f"Transcrição salva em {output_filename}")

if __name__ == "__main__":
    main()