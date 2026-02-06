import whisper
import warnings
import os
import sys

# Suppress specific warnings
warnings.filterwarnings("ignore")

def setup_ffmpeg_path():
    """Ensures local bin is in PATH for ffmpeg"""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    bin_path = os.path.join(project_root, 'bin')
    if os.path.exists(bin_path):
        # Check if already in path to avoid duplicate entries (simple check)
        if bin_path not in os.environ["PATH"]:
             os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]

def transcribe_audio(audio_path, model_name="base"):
    """
    Transcribes the audio file using OpenAI's Whisper model.
    Returns a tuple (text, language).
    """
    setup_ffmpeg_path()
    
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    print(f"Loading Whisper model '{model_name}'...")
    try:
        model = whisper.load_model(model_name)
    except Exception as e:
        print(f"Error loading model: {e}", file=sys.stderr)
        return None, None
    
    print(f"Transcribing '{audio_path}'...")
    try:
        # result contains 'text', 'segments', 'language' (if detected)
        # Note: language detection happens if not specified.
        result = model.transcribe(audio_path)
        
        text = result["text"]
        language = result.get("language", "unknown")
        
        return text.strip(), language
    except Exception as e:
        print(f"Error during transcription: {e}", file=sys.stderr)
        return None, None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text, lang = transcribe_audio(sys.argv[1])
        if text:
            print(f"Language: {lang}")
            print(f"Text: {text}")
