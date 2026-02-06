import os
import sys
import unittest
from unittest.mock import patch

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import main


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.test_audio = os.path.abspath("test_audio.mp3")
        ret = os.system(
            f"ffmpeg -y -f lavfi -i 'sine=frequency=1000:duration=1' {self.test_audio} > /dev/null 2>&1"
        )
        if ret != 0:
            raise RuntimeError("ffmpeg failed to create dummy audio")

    def tearDown(self):
        if os.path.exists(self.test_audio):
            os.remove(self.test_audio)

    @patch("main.transcribe_audio")
    @patch("main.download_audio")
    def test_local_file_flow_skips_download(self, mock_download, mock_transcribe):
        mock_transcribe.return_value = ("hello world", "en")

        with patch.object(sys, "argv", ["main.py", self.test_audio, "--keep-audio"]):
            try:
                main.main()
            except SystemExit as e:
                if e.code != 0:
                    self.fail(f"main exited with code {e.code}")

        mock_download.assert_not_called()
        mock_transcribe.assert_called_once_with(self.test_audio, model_name="base")

    @patch("main.transcribe_audio")
    @patch("main.download_audio")
    def test_url_flow_downloads_audio(self, mock_download, mock_transcribe):
        mock_download.return_value = self.test_audio
        mock_transcribe.return_value = ("hello world", "en")

        with patch.object(sys, "argv", ["main.py", "https://example.com/watch?v=abc", "--model", "tiny", "--keep-audio"]):
            try:
                main.main()
            except SystemExit as e:
                if e.code != 0:
                    self.fail(f"main exited with code {e.code}")

        mock_download.assert_called_once_with("https://example.com/watch?v=abc")
        mock_transcribe.assert_called_once_with(self.test_audio, model_name="tiny")

    def test_missing_local_file_exits_nonzero(self):
        missing = os.path.abspath("does_not_exist.mp4")

        with patch.object(sys, "argv", ["main.py", missing]):
            with self.assertRaises(SystemExit) as ctx:
                main.main()

        self.assertEqual(ctx.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
