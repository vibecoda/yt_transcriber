# YouTube Audio Transcriber

Transcribe speech from a local video/audio file with OpenAI Whisper.

This repo also supports a YouTube URL input, but the quickest way to try it is with a video already in this repo.

## Prerequisites

- Python 3.10+ recommended
- `ffmpeg` installed and available on `PATH`
- `uv` installed ([official install docs](https://docs.astral.sh/uv/getting-started/installation/))
- Internet access on first run (Whisper downloads model weights once)

### Install ffmpeg

macOS (Homebrew):

```bash
brew install ffmpeg
```

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y ffmpeg
```

Verify:

```bash
ffmpeg -version
```

## Quick Start (with repo video)

Clone and enter the repository:

```bash
git clone https://github.com/vibecoda/yt_transcriber.git
cd yt_transcriber
```

Create venv and install deps with `uv`:

If `uv` is not installed yet, install it first:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
uv venv .venv
uv pip install -r requirements.txt
```

Run transcription against the local video in `data/`:

```bash
.venv/bin/python src/main.py data/jNQXAC9IVRw.mp4 --model tiny --output data/jNQXAC9IVRw.transcript.txt
```

Transcript will be written to:

```bash
data/jNQXAC9IVRw.transcript.txt
```

## Usage

General command:

```bash
.venv/bin/python src/main.py <file_path_or_youtube_url> [options]
```

Options:

- `--model`: `tiny`, `base`, `small`, `medium`, `large` (default: `base`)
- `--output`: output text file path
- `--keep-audio`: keep downloaded file when input is a URL

Local file example:

```bash
.venv/bin/python src/main.py ./data/my_video.mp4 --model tiny --output ./data/my_video.txt
```

YouTube URL example:

```bash
.venv/bin/python src/main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --model tiny --keep-audio
```

## Troubleshooting

- `ffmpeg` not found:
  install `ffmpeg` and rerun.
- Slow run or high memory usage:
  use `--model tiny` or `--model base`.
- First run takes longer:
  Whisper model download happens only once per model size.
