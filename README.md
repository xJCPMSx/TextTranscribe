# TextTranscribe

## English

This project transcribes audio/video files using the `faster-whisper` library with CPU-friendly INT8 and optional streaming segment processing to keep memory usage low. It now supports saving outputs in plain text (TXT), SubRip subtitles (SRT), or JSON via command-line options.

### Versions

*   **transcrever.py**: Initial version of the script using `faster-whisper` basics.
*   **transcrever2.0.py**: Improved iteration/printing of segments for better readability on console.
*   **transcrever2.1.py**: Saves the transcription to `transcricao.txt` while streaming segments as they are produced.
*   **transcrever3.0.py**: Adds a command-line interface to choose output format (txt, srt, json) and output path, writing incrementally to avoid loading all segments in memory at once.

### Requirements

*   Python 3
*   `faster-whisper` (CTranslate2-based Whisper implementation with PyAV decoding; no system-wide FFmpeg required).

Install dependencies with pip:

```bash
pip install faster-whisper
```

### How to Use

1.  Ensure there is an input media file such as `audio.mp4` in the project root (an example `audio.mp4` is included for demonstration).
2.  For the latest version with format selection:

    ```bash
    # TXT (default)
    python transcrever3.0.py audio.mp4

    # Explicit TXT
    python transcrever3.0.py audio.mp4 --format txt --output transcricao.txt

    # SRT (SubRip)
    python transcrever3.0.py audio.mp4 --format srt --output transcricao.srt

    # JSON (streamed writing)
    python transcrever3.0.py audio.mp4 --format json --output transcricao.json
    ```
    The SRT writer uses standard HH:MM:SS,mmm timestamps derived from segment start/end times, compatible with common video players and editors.

### Notes and Tips

*   `segments` is a generator; writing each segment directly to the target file keeps memory in check on long audios without materializing all segments in a list.
*   If running on CPU, consider using `compute_type="int8"` and limiting threads (e.g., `cpu_threads` and `OMP_NUM_THREADS`) to stabilize performance and memory footprint.
*   Choose a model size that fits your machine: “turbo”/“medium”/“small” trade accuracy vs. speed/memory; smaller or INT8-quantized models reduce RAM usage compared to “large”.

---

## Português

Este projeto transcreve arquivos de áudio/vídeo utilizando a biblioteca `faster-whisper` com quantização INT8 para CPU e processamento em fluxo dos segmentos para baixo uso de memória. Agora permite salvar a saída em texto simples (TXT), legendas SubRip (SRT) ou JSON via opções na linha de comando.

### Versões

*   **transcrever.py**: Versão inicial do script com uso básico do `faster-whisper`.
*   **transcrever2.0.py**: Iteração/impressão dos segmentos aprimorada para melhor leitura no console.
*   **transcrever2.1.py**: Salva a transcrição em `transcricao.txt` enquanto processa os segmentos em fluxo.
*   **transcrever3.0.py**: Adiciona interface de linha de comando para escolher formato (txt, srt, json) e caminho de saída, gravando de forma incremental para não carregar todos os segmentos na memória.

### Requisitos

*   Python 3
*   `faster-whisper` (implementação baseada em CTranslate2 com decodificação via PyAV; não requer FFmpeg instalado no sistema).

Instalação com pip:

```bash
pip install faster-whisper
```

### Como Usar

1.  Garanta um arquivo de mídia de entrada como `audio.mp4` no diretório raiz (um `audio.mp4` de exemplo está incluído para demonstração).
2.  Para a versão mais recente com seleção de formato:

    ```bash
    # TXT (padrão)
    python transcrever3.0.py audio.mp4

    # TXT explícito
    python transcrever3.0.py audio.mp4 --format txt --output transcricao.txt

    # SRT (SubRip)
    python transcrever3.0.py audio.mp4 --format srt --output transcricao.srt

    # JSON (gravação em fluxo)
    python transcrever3.0.py audio.mp4 --format json --output transcricao.json
    ```
    O gerador de SRT usa timestamps no padrão HH:MM:SS,mmm a partir de start/end de cada segmento, compatível com players e editores comuns.

### Notas e Dicas

*   `segments` é um gerador; escrever cada segmento diretamente no arquivo destino mantém a memória baixa em áudios longos sem precisar converter para lista.
*   Em CPU, utilize `compute_type="int8"` e limite threads (`cpu_threads` e `OMP_NUM_THREADS`) para estabilizar o consumo de memória e o desempenho.
*   Escolha o tamanho do modelo conforme sua máquina: “turbo”/“medium”/“small” equilibram acurácia, velocidade e memória; modelos menores ou INT8 costumam consumir menos RAM que “large”.

Referências: `faster-whisper` (features, streaming, PyAV/FFmpeg embutido), guia de formatação SRT e boas práticas de parametrização.
