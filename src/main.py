import argparse
import os
import sys
from urllib.parse import urlparse

# Ensure we can import modules from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from downloader import download_audio
from transcriber import transcribe_audio


def is_http_url(value):
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe a local media file or download audio from YouTube and transcribe it."
    )
    parser.add_argument("source", help="Local media file path or YouTube video URL")
    parser.add_argument(
        "--model",
        default="base",
        help="Whisper model size (tiny, base, small, medium, large)",
    )
    parser.add_argument("--output", help="Output text file path")
    parser.add_argument(
        "--keep-audio",
        action="store_true",
        help="Keep downloaded audio file (URL mode only)",
    )

    args = parser.parse_args()

    print(f"Processing {args.source}...")

    audio_path = None
    downloaded_audio = False

    if is_http_url(args.source):
        # 1. Download for URL mode
        print("Downloading audio...")
        audio_path = download_audio(args.source)
        downloaded_audio = True

        if not audio_path:
            print("Failed to download audio.")
            sys.exit(1)

        print(f"Audio downloaded to: {audio_path}")
    else:
        # 1. Use local file path directly
        audio_path = os.path.abspath(args.source)
        if not os.path.exists(audio_path):
            print(f"Input file not found: {args.source}", file=sys.stderr)
            sys.exit(1)

        print(f"Using local media file: {audio_path}")

    # 2. Transcribe
    print("Transcribing audio (this may take a while)...")
    text, lang = transcribe_audio(audio_path, model_name=args.model)

    if text is None:
        print("Transcription failed.")
        if downloaded_audio and not args.keep_audio and os.path.exists(audio_path):
            os.remove(audio_path)
        sys.exit(1)

    # 3. Output
    print("-" * 40)
    print(f"Detected Language: {lang}")
    print("-" * 40)
    print(text)
    print("-" * 40)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(f"Language: {lang}\n\n")
                f.write(text)
            print(f"Transcription saved to {args.output}")
        except Exception as e:
            print(f"Error saving output: {e}")

    # Cleanup downloaded files only
    if downloaded_audio and not args.keep_audio:
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
                print("Temporary audio file removed.")
        except OSError as e:
            print(f"Error removing audio file: {e}")
    elif downloaded_audio:
        print(f"Audio file kept at {audio_path}")


if __name__ == "__main__":
    main()
