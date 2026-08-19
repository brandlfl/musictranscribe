from abc import ABC, abstractmethod
from AMT.Handler import AbstractHandler
from AMT.Piece import Piece
from pathlib import Path
from mido import MidiFile, MidiTrack, MetaMessage

import logging
logger = logging.getLogger(__name__)

class ITranscriber(AbstractHandler, ABC):
    @abstractmethod
    def audio_to_midi(self, input_path: str) -> str:
        pass

    def handle(self, request: Piece) -> str:
        if request.is_transcribed is False:
            logger.debug(f"Attempting to transcribe \nPath: {request.path}\nStems: {request.stems}")
            if request.is_separated and (len(request.stems) > 0):
                logger.debug(f"About to transcribe {request.stems}")
                midi_files = []
                for stem in request.stems:
                    midi_stem = self.audio_to_midi(stem)
                    midi_files.append(str(midi_stem)) # str conversion required to store value not reference!
                logger.debug(f"Midi files: {midi_files}")
                request.midi_stems.extend(midi_files)
                # combine midi stems. TODO: The Piece class should maybe do that by itself
                midi_out = str(Path(request.path).parent / (Path(request.path).stem + ".mid"))
                request.midi = request.combine_midis(request.midi_stems, midi_out)
                request.is_transcribed = True
            else:
                midi = self.audio_to_midi(request.path)
                request.set_midi(midi)
                request.is_transcribed = True
        return super().handle(request)
