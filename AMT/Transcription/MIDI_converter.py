import mido
from mido.midifiles.midifiles import DEFAULT_TICKS_PER_BEAT


class MIDISynthesizer(mido.MidiFile):
    """An implementation of a MIDI synthesizer that converts MIDI files to audio files. 
    
    In the future, this class may be extended to use random instruments and more to create augmented syntehsized datasets.
    
    At this stage, simply use the save(filename) method provided to this class by mido.MidiFile to synthesize a MIDI. See https://mido.readthedocs.io/en/stable/api.html#standard-midi-files for more info."""
    def __init__(self, filename=None, file=None, type=1, ticks_per_beat=DEFAULT_TICKS_PER_BEAT, charset='latin1', debug=False, clip=False, tracks=None):
        super().__init__(filename, file, type, ticks_per_beat, charset, debug, clip, tracks)