from AMT.Beattracking.IBeattracker import IBeattracker

import subprocess
from pathlib import Path

import logging
logger = logging.getLogger(__name__)


class BeatThisBeattracker(IBeattracker):
    DEFAULT_OUTPUT_PATH = IBeattracker.DEFAULT_OUTPUT_PATH + "/beat_this"
    def track_beats(self, input_path: str, output_path: str = DEFAULT_OUTPUT_PATH, *beat_this_args) -> str:
        in_path = Path(input_path)
        if not in_path.exists():
            raise FileNotFoundError(f"Input file not found: {in_path}")
        if in_path.is_dir():
            raise FileNotFoundError(f"Please select a single file for transcription not a directory: {in_path}")
        #     audio_paths = [str(ap) for ap in in_path.iterdir() if ap.is_file()] 
        # else:
        #     audio_paths = [str(in_path)]
        
        if output_path == BeatThisBeattracker.DEFAULT_OUTPUT_PATH:
            out_path = Path(output_path) / (in_path.stem + ".beats")
        else:
            out_path = Path(output_path)
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)

        try:
            logger.debug(f"Attempting to track beats of {str(in_path)} and write to {str(out_path)}")
            subprocess.run(["uvx", "--from", "git+https://github.com/brandlfl/beat_this_env", "beat_this", str(in_path), "--output", str(out_path), *beat_this_args], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error occurred while tracking beats: {e}")

        if not out_path.exists():
            raise FileNotFoundError(f"Output directory not found: {out_path.as_posix()}")
        # output_paths = [str(stem) for stem in out_path.iterdir() if stem.is_file()]
        return str(out_path)

    def help(self):
        """Prints the help message for the Beat This beattracker."""
        try:
            # run command: uvx --from git+https://github.com/brandlfl/beat_this_env beat_this --help
            subprocess.run(["uvx", "--from", "git+https://github.com/brandlfl/beat_this_env", "beat_this", "--help"], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error occurred while trying to get help for Beat This: {e}")