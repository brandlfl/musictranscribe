from AMT.Transcription.ITranscriber import ITranscriber

import subprocess
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

DEFAULT_MUSCRIPTOR_OUTPUT_PATH = "transcribed/muscriptor"
FALLBACK_MUSCRIPTOR_COMMAND = ["uvx", "muscriptor"]
INSTALLED_MUSCRIPTOR_COMMAND = ["muscriptor"]

class MuscriptorTranscriber(ITranscriber):
    """Implementation of the audio_to_midi transcription using the Muscriptor Model from 2026. 
    This model is the state of the art at its release and can deal with multi-instrumental input. No need for stem separation."""
    
    def __init__(self) -> None:
        self.config = {} # unused for now
    
    def audio_to_midi(self, input_path: str, output_path: str = DEFAULT_MUSCRIPTOR_OUTPUT_PATH, *muscriptor_args) -> str:
        """Transcribe audio to MIDI using the Muscriptor model.
        About the transcription arguments:
        
 Usage: muscriptor transcribe [OPTIONS] {audio_file}

 Transcribe an audio file to MIDI.

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    audio_file      <path>  Input audio file (wav, mp3, flac, …) [required]                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output       -o      <path>             Output file path. Use '-' to write to stdout (all progress / timing info   │
│                                           is sent to stderr in that case). Default: <audio_file>.<ext> where ext     │
│                                           matches --format.                                                          │
│ --format       -f      <midi|json|jsonl>  Output format: midi (default), json (single array of events), or jsonl     │
│                                           (one event per line, streamed as transcription progresses)                 │
│                                           [default: midi]                                                            │
│ --notes                                   Print decoded events to stdout                                             │
│ --sampling                                Use temperature sampling instead of greedy decoding                        │
│ --temperature  -t      <float>            Sampling temperature (only with --sampling) [default: 1.0]                 │
│ --cfg-coef             <float>            Classifier-free guidance coefficient [default: 1.0]                        │
│ --model        -m      <str>              Model size ('small', 'medium', 'large'; default: medium), a local          │
│                                           safetensors path, or an hf:// / http(s):// URL                             │
│ --device       -d      <str>              Device: 'auto', 'cpu', 'cuda', 'cuda:0', … [default: auto]                 │
│ --batch-size   -b      <int>              Batch size for generation (default: 1 on CPU, 4 on GPU)                    │
│ --strict-eos                              Raise an error if a chunk fails to emit EOS within the generation budget   │
│                                           (default: downgrade to a warning)                                          │
│ --beam-size            <int>              Beam search width (1 = greedy/sampling, ≥2 enables beam search)            │
│                                           [default: 1]                                                               │
│ --auralize             <path>             Write a stereo auralization (L=original audio, R=MIDI synthesis) to this   │
│                                           path. Requires fluidsynth on PATH. Extension determines format: .wav       │
│                                           (default) or .mp3. Only valid with --format midi.                          │
│ --soundfont            <path>             Path to a .sf2 SoundFont for auralization. Defaults to                     │
│                                           MuseScore_General.sf2, downloaded once and cached locally.                 │
│ --instruments          <str>              Comma-separated list of expected instrument group names. Case-insensitive; │
│                                           unambiguous abbreviations are accepted (e.g. 'timp,cello,dist'). Run       │
│                                           'muscriptor list-instruments' to see all available names.                  │
│ --help                                    Show this message and exit.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

"""
        in_path = Path(input_path)
        if not in_path.exists():
            raise FileNotFoundError(f"Input file not found: {in_path}")
        if in_path.is_dir():
            raise FileNotFoundError(f"Please select a single file for transcription not a directory: {in_path}")
        #     audio_paths = [str(ap) for ap in in_path.iterdir() if ap.is_file()]
        # else:
        #     audio_paths = [str(in_path)]

        if output_path == DEFAULT_MUSCRIPTOR_OUTPUT_PATH:
            out_path = Path(output_path) / (in_path.stem + ".mid")
        else:
            out_path = Path(output_path)
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)

        try:
            logger.debug(f"Attempting to run muscriptor with {str(in_path)} and saving to {str(out_path)}")
            subprocess.run([*INSTALLED_MUSCRIPTOR_COMMAND, "transcribe", str(in_path), "--output", str(out_path), *muscriptor_args], check=True)
        except subprocess.CalledProcessError as e:
            try:
                logger.warning(f"Installed Muscriptor command failed. Error: {e}. Attempting fallback with uvx")
                logger.debug(f"Attempting to run muscriptor with {str(in_path)} and saving to {str(out_path)}")
                subprocess.run([*FALLBACK_MUSCRIPTOR_COMMAND, "transcribe", str(in_path), "--output", str(out_path), *muscriptor_args], check=True)
                # subprocess.run(["uvx", "muscriptor", "transcribe", str(in_path), "--output", str(out_path), *muscriptor_args], check=True)
            except subprocess.CalledProcessError as e:
                logger.error(f"Muscriptor command failed. Please check your installation. Error: {e}")
                raise RuntimeError(f"Error occurred while transcribing audio to MIDI: {e}")
        
        if not out_path.exists():
            raise FileNotFoundError(f"Output file or directory not found: {out_path.as_posix()}")
        # output_paths = [str(stem) for stem in out_path.iterdir() if stem.is_file()]
        return str(out_path)

    def help(self):
        """Prints the help message for the Muscriptor model:
        
 Usage: muscriptor [OPTIONS] COMMAND [ARGS]...

 muscriptor — audio-to-MIDI transcription

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ transcribe        Transcribe an audio file to MIDI.                                                                  │
│ serve             Run the HTTP transcription server (POST /transcribe → SSE event stream).                           │
│ list-instruments  List the instrument group names accepted by --instruments.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

"""
        try:
            subprocess.run([*INSTALLED_MUSCRIPTOR_COMMAND, "--help"], check=True)
        except subprocess.CalledProcessError as e:
            try:
                logger.warning(f"Installed Muscriptor command failed. Error: {e}. Attempting fallback with uvx")
                subprocess.run([*FALLBACK_MUSCRIPTOR_COMMAND, "--help"], check=True)
            except subprocess.CalledProcessError as e:
                logger.error(f"Muscriptor command failed. Please check your installation. Error: {e}")
                raise RuntimeError(f"Error occurred while trying to get help for Muscriptor: {e}")
    
