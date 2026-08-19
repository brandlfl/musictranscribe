from AMT.Transcription.ITranscriber import ITranscriber

import subprocess
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

DEFAULT_BP_OUTPUT_PATH = "transcribed/basicpitch"
FALLBACK_BP_COMMAND = ["uvx", "--python", "3.11", "--from", "git+https://github.com/brandlfl/basic-pitch-env.git", "basic-pitch"]
INSTALLED_BP_COMMAND = ["basic-pitch"]

class BasicPitchTranscriber(ITranscriber):
    """Implementation of the audio_to_midi transcription using the Basic Pitch Model from 2022. 
    This model can deal with various instruments and vocals but expects a single instrument. For multi-instruments use MuScriptor or a MT3 model."""
    
    def __init__(self) -> None:
        super().__init__()
        self.config = {}
        self.use_fallback = False
    
    def help(self):
        """Prints the help message for the Basic Pitch model."""
        try:
            subprocess.run([*INSTALLED_BP_COMMAND, "--help"], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.warning(f"installed basic-pitch command failed or not found. Attempting fallback. Error: {e}")
            self.use_fallback = True
            try:
                subprocess.run([*FALLBACK_BP_COMMAND, "--help"], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                logger.error(f"basic-pitch fallback command failed. Please check your installation. Error: {e}")
    
    def audio_to_midi(self, input_path: str, output_path: str = DEFAULT_BP_OUTPUT_PATH, apply_config: bool = True, *basic_pitch_args) -> str:
        in_path = Path(input_path)
        if not in_path.exists():
            raise FileNotFoundError(f"Input file not found: {in_path}")
        if in_path.is_dir():
            raise FileNotFoundError(f"Please select a single file for transcription not a directory: {in_path}")
        #     audio_paths = [str(ap) for ap in in_path.iterdir() if ap.is_file()]
        # else:
        #     audio_paths = [str(in_path)]

        if output_path == DEFAULT_BP_OUTPUT_PATH:
            out_path = Path(output_path) / in_path.parent.stem
        else:
            out_path = Path(output_path)
        Path(out_path).mkdir(parents=True, exist_ok=True)

        try:
            logger.debug(f"Attempting to run basic-pitch {str(out_path)} {str(in_path)}")
            if apply_config:
                args = self._generate_basic_pitch_args()
            else:
                args = list(basic_pitch_args)
            # try installed basic-pitch first, fall back to uvx invocation
            try:
                subprocess.run([*INSTALLED_BP_COMMAND, *args, str(out_path), str(in_path)], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                logger.warning(f"Installed basic-pitch failed or not found. Falling back to uvx. Error: {e}")
                try:
                    subprocess.run([*FALLBACK_BP_COMMAND, *args, str(out_path), str(in_path)], check=True)
                except (subprocess.CalledProcessError, FileNotFoundError) as e:
                    raise RuntimeError(f"Error occurred while transcribing audio to MIDI: {e}")
        except Exception as e:
            raise RuntimeError(f"Error occurred while transcribing audio to MIDI: {e}")
        
        if not out_path.exists():
            raise FileNotFoundError(f"Output directory not found: {out_path.as_posix()}")

        output_paths = [str(stem) for stem in out_path.iterdir() if stem.is_file()]
        # after full demucs separation there should be 4 stems: bass, drums, other, vocals
        # now find the right file
        the_right_file = ""
        for stem in output_paths:
            if stem.find(in_path.stem) != -1 and stem.endswith(".mid"):
                the_right_file = str(stem)
                break
        # TODO: basic pitch is made for passing directories and converting a batch of files 
        # muscriptor however expects one file in and one file out
        return the_right_file
 
    def configure(self, 
                  model_path: str | None = None,
                  model_serialization: str | None = "onnx",
                  save_midi: bool = True,
                  sonify_midi: bool = False, 
                  save_notes: bool = False, 
                  onset_threshold: float = 0.5, 
                  frame_threshold: float = 0.3, 
                  minimum_note_length: float = 127.7, 
                  minimum_frequency: float | None = None, 
                  maximum_frequency: float | None = None, 
                  no_melodia: bool = True,
                  midi_tempo: float = 120): 
        """Configure the Basic Pitch model with the given parameters.
        usage: basic-pitch [-h] [--model-path MODEL_PATH] [--model-serialization {tf,coreml,tflite,onnx}] [--save-midi] [--sonify-midi] [--save-model-outputs] [--save-note-events] [--onset-threshold ONSET_THRESHOLD]
                   [--frame-threshold FRAME_THRESHOLD] [--minimum-note-length MINIMUM_NOTE_LENGTH] [--minimum-frequency MINIMUM_FREQUENCY] [--maximum-frequency MAXIMUM_FREQUENCY] [--multiple-pitch-bends]
                   [--sonification-samplerate SONIFICATION_SAMPLERATE] [--midi-tempo MIDI_TEMPO] [--debug-file DEBUG_FILE] [--no-melodia]
                   output_dir audio_paths [audio_paths ...]

    Predict midi from audio.

    positional arguments:
    output_dir            directory to save outputs
    audio_paths           Space separated paths to the input audio files.

    options:
    -h, --help            show this help message and exit
    --model-path MODEL_PATH
                            path to the saved model directory. Defaults to a ICASSP 2022 model. The preferred model is determined by the first library available in [tensorflow, coreml, tensorflow-lite, onnx]
    --model-serialization {tf,coreml,tflite,onnx}
                            If used, --model-path is ignored and instead the model serialization typespecified is used.
    --save-midi           Create a MIDI file.
    --sonify-midi         Create an audio .wav file which sonifies the MIDI outputs.
    --save-model-outputs  Save the raw model output as an npz file.
    --save-note-events    Save the predicted note events as a csv file.
    --onset-threshold ONSET_THRESHOLD
                            The minimum likelihood for an onset to occur, between 0 and 1.
    --frame-threshold FRAME_THRESHOLD
                            The minimum likelihood for a frame to sustain, between 0 and 1.
    --minimum-note-length MINIMUM_NOTE_LENGTH
                            The minimum allowed note length, in miliseconds.
    --minimum-frequency MINIMUM_FREQUENCY
                            The minimum allowed note frequency, in Hz.
    --maximum-frequency MAXIMUM_FREQUENCY
                            The maximum allowed note frequency, in Hz.
    --multiple-pitch-bends
                            Allow overlapping notes in midi file to have pitch bends. Note: this will map each pitch to its own instrument
    --sonification-samplerate SONIFICATION_SAMPLERATE
                            The samplerate for sonified audio files.
    --midi-tempo MIDI_TEMPO
                            The tempo for the midi file.
    --debug-file DEBUG_FILE
                            Optional file for debug output for inference.
    --no-melodia          Skip the melodia trick.
    """
        self.config = { 
            "model_path": model_path,
            "model_serialization": model_serialization,
            "save_midi": save_midi,
            "sonify_midi": sonify_midi,
            "save_notes": save_notes,
            "onset_threshold": onset_threshold, 
            "frame_threshold": frame_threshold,
            "minimum_note_length": minimum_note_length,
            "minimum_frequency": minimum_frequency,
            "maximum_frequency": maximum_frequency,
            "no_melodia": no_melodia,
            "midi_tempo": midi_tempo
        }

    def _generate_basic_pitch_args(self) -> list[str]:
        """Generate command-line arguments for the Basic Pitch model based on the current configuration."""
        args = []
        if self.config.get("model_path") is not None:
            args.extend(["--model-path", self.config["model_path"]])
        if self.config.get("model_serialization") is not None:
            args.extend(["--model-serialization", self.config["model_serialization"]])
        if self.config.get("save_midi"):
            args.append("--save-midi")
        if self.config.get("sonify_midi"):
            args.append("--sonify-midi")
        if self.config.get("save_notes"):
            args.append("--save-notes")
        if self.config.get("onset_threshold") is not None:
            args.extend(["--onset-threshold", str(self.config["onset_threshold"])])
        if self.config.get("frame_threshold") is not None:
            args.extend(["--frame-threshold", str(self.config["frame_threshold"])])
        if self.config.get("minimum_note_length") is not None:
            args.extend(["--minimum-note-length", str(self.config["minimum_note_length"])])
        if self.config.get("minimum_frequency") is not None:
            args.extend(["--minimum-frequency", str(self.config["minimum_frequency"])])
        if self.config.get("maximum_frequency") is not None:
            args.extend(["--maximum-frequency", str(self.config["maximum_frequency"])])
        if self.config.get("no_melodia"):
            args.append("--no-melodia")
        if self.config.get("midi_tempo") is not None:
            args.extend(["--midi-tempo", str(self.config["midi_tempo"])])
        
        return args
    
    def load_config(self, json_path: str):
        """Load configuration from a JSON file."""
        import json
        with open(json_path, 'r') as f:
            self.config = json.load(f)
    
    def save_config(self, json_path: str):
        """Save the current configuration to a JSON file."""
        import json
        with open(json_path, 'w') as f:
            json.dump(self.config, f, indent=4)
    