from AMT.Piece import Piece
from AMT.Separation.demucs_separator import DemucsSeparator
from AMT.Transcription.basicpitch_transcriber import BasicPitchTranscriber, DEFAULT_BP_OUTPUT_PATH
from AMT.Transcription.muscriptor_transcriber import MuscriptorTranscriber, DEFAULT_MUSCRIPTOR_OUTPUT_PATH
from AMT.Beattracking.beat_this_beattracker import BeatThisBeattracker

from pathlib import Path
import music21

import logging
import logging.config
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "standard",
            "level": "DEBUG",
            "filename": "AutoTranscribe.log"
        }
    },
    "loggers": {
        "": {  # Root logger
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
    }
}
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def test_demucs_handler():
    dem = DemucsSeparator()
    score = Piece("audio/ac_short.wav")
    dem.handle(score)
    print(len(score.stems))

def test_transcribers_direct(audio_file):
    separator = DemucsSeparator()
    stem_paths = separator.separate_stems(audio_file)#, "--two-stems=drums")
    print("Separated stems:")
    for path in stem_paths:
        print(f"  {path}")
    
    stem_dir = Path(stem_paths[0]).parent.as_posix()

    transcriber = BasicPitchTranscriber()
    midi_stems = []
    for stem in stem_paths:
        midi_stem = transcriber.audio_to_midi(stem, DEFAULT_BP_OUTPUT_PATH)
        print(f"Transcribed {stem} to {midi_stem}")
        midi_stems.append(midi_stem)
    midi_bp_combined = combine_midis(midi_stems, str(Path(stem_dir) / "combined_basicpitch.mid"))

    # or use new Muscriptor for multi-instrumental transcription
    transcriber = MuscriptorTranscriber()
    midi_muscriptor = transcriber.audio_to_midi(audio_file)

    score_bp = music21.converter.parse(midi_bp_combined)
    score_muscriptor = music21.converter.parse(midi_muscriptor[0])
    score_bp.show()
    score_muscriptor.show()

def main():
    logger.debug("Starting main.")
    
    # audio_file = "audio/ac_short.wav"
    audio_file = "examples/tsynth_112.wav"
    piece = Piece(audio_file)

    separator = DemucsSeparator(model="htdemucs")
    beattracker = BeatThisBeattracker()
    transcriber_bp = BasicPitchTranscriber()
    transcriber_mu = MuscriptorTranscriber()

    # handle with basic pitch
    separator.set_next(beattracker).set_next(transcriber_bp)
    separator.handle(piece)
    print("Chain: demucs > beat_this > basic pitch\n", "Result at", piece.midi)
    score_bp = music21.converter.parse(str(piece.midi))
    score_bp.show()

    # reset piece
    piece = Piece(audio_file)
    # handle with muscriptor
    transcriber_mu.handle(piece)
    print("Chain: muscriptor\n", "Result at", piece.midi)
    score_mu = music21.converter.parse(str(piece.midi))
    score_mu.show()

    # or export to pdf with MuseScore Studio installed
    # import subprocess
    # subprocess.run(["mscore", "-o",  "'My Score.pdf'", "'My Score.mscz'"])

def combine_midis(midi_files: list[str], output_file: str | None = None) -> str:
    """Combine multiple MIDI files into one."""
    # this could be done with music21 too but mido is simpler for this low level task
    from mido import MidiFile, MidiTrack

    combined_midi = MidiFile()
    for midi_file in midi_files:
        stem_midi = MidiFile(midi_file)
        for track in stem_midi.tracks:
            combined_midi.tracks.append(track)
    
    if output_file is not None:
        combined_midi.save(output_file)
    else:
        output_file = str(Path(midi_files[0]).parent / "combined.mid")
        combined_midi.save(output_file)
    return output_file

if __name__ == "__main__":
    main()
