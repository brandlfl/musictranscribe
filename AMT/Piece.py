from pathlib import Path
import music21
from mido import MidiFile, MidiTrack

#TODO: Should this class also handle the separation, transcription, etc.? Or should it just be a container for the audio file and the stems are handled by the separator?

class Piece:
    """Gathers music information like audio, tempo, beats and key for one piece."""
    
    def __init__(
        self,
        audio_path: str,
        stems: list = [], 
        bpm: float = 80,
        time_signature: str = '4/4',
        key: str = 'C'
    ):
        """
        Initialize a Piece with audio and optional stem information.
        
        Args:
            audio_path: Path to the audio file of the whole piece.
            stems: List of audio file paths for separated stems. (optional)
            bpm: Beats per minute of the piece. (default: 80)
            time_signature: Time signature of the piece. (default: '4/4')
            key: Key of the piece. A capital letter for a major key and a lowercase letter for a minor key. Use # for sharps and - for flats.(default: 'C')
        """
        self.path = Path(audio_path) # Using self.path instead of self._path uses the setter function of the property
        if not self._path.exists():
            raise FileNotFoundError(f"Audio file not found: {self._path}")

        self.stems: list[str] = []
        if len(stems) > 0:
            for stem in stems:
                new_stem = Path(stem)
                if not new_stem.exists():
                    raise FileNotFoundError(f"Stem file not found: {new_stem}")
                else:
                    self.stems.append(new_stem.as_posix())
            is_separated = True
        else:
            is_separated = False
        
        self.midi: str | None = None
        self.midi_stems: list[str] = []

        self.bpm = bpm
        self.time_signature = music21.meter.TimeSignature(time_signature) # get as string with time_signature.ratioString
        self.key = music21.key.Key(key)
        self.beatmap = None

        self.is_separated = is_separated
        self.is_preprocessed = False
        self.is_transcribed = False
        self.is_postprocessed = False

    @property
    def path(self):
        """Return the path of the audio file as string."""
        return str(self._path)
    
    @path.setter
    def path(self, new_path: str | Path):
        """Set a new path for the audio file."""
        new_path_obj = Path(new_path)
        if not new_path_obj.exists():
            raise FileNotFoundError(f"Audio file not found: {new_path_obj}")
        self._path = new_path_obj

    def set_midi(self, new_midi: str):
        self.midi = new_midi

    def set_beatmap(self, beatmap):
        self.beatmap = beatmap
    
    def combine_midis(self, midi_files: list[str], output_file: str | None = None) -> str:
        """Combine multiple MIDI files into one."""
        # this could be done with music21 too but mido is simpler for this low level task

        combined_midi = MidiFile()
        for midi_file in midi_files:
            stem_midi = MidiFile(midi_file)
            for track in stem_midi.tracks:
                combined_midi.tracks.append(track)
        
        if output_file is not None:
            out_file = output_file
        else:
            out_file = str(Path(midi_files[0]).parent / "combined.mid")
        combined_midi.save(out_file)
        return out_file