import yt_dlp
import os
import sys

def download_audio(url, output_dir="downloads"):
    """
    Downloads audio from a YouTube URL.
    Returns the path to the downloaded audio file.
    """
    # Ensure local bin is in PATH for ffmpeg
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    bin_path = os.path.join(project_root, 'bin')
    if os.path.exists(bin_path) and bin_path not in os.environ["PATH"]:
        os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Output template
    output_template = os.path.join(output_dir, '%(id)s.%(ext)s')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            video_id = info['id']
            # After conversion, the extension is mp3
            filename = os.path.join(output_dir, f"{video_id}.mp3")
            return filename
        except Exception as e:
            print(f"Error downloading {url}: {e}", file=sys.stderr)
            return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = download_audio(sys.argv[1])
        if path:
            print(f"Downloaded to: {path}")
        else:
            print("Download failed.")
