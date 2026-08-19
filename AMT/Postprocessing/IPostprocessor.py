from abc import ABC, abstractmethod
from AMT.Handler import AbstractHandler
from AMT.Piece import Piece

class IPostprocessor(AbstractHandler, ABC):
    """Interface for postprocessing the generated MIDI files."""
    @abstractmethod
    def process_midi(self, input_path: str) -> str:
        """Process a MIDI file.

        Parameters
        ----------
        input_path : str
            Path to the input midi file.

        Returns
        -------
        str
            Path to the output file.
        """
        raise NotImplementedError

    def handle(self, request: Piece) -> str:
        if request.is_postprocessed is False:
            new_midi = self.process_midi(request.path)
            request.midi = new_midi
            request.is_postprocessed = True
        return super().handle(request)
