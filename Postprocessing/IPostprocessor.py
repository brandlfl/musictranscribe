from abc import ABC, abstractmethod
from AMT.Handler import AbstractHandler
from AMT.Piece import Piece

class ISeparator(AbstractHandler, ABC):
    """Interface for audio separation implementations."""
    @abstractmethod
    def process_midi(self, input_path: str) -> str:
        """Separate stems from an audio file.

        Parameters
        ----------
        input_path : str
            Path to the input audio file.

        Returns
        -------
        list[str]
            Paths to the separated single-instrument output files.
        """
        raise NotImplementedError

    def handle(self, request: Piece) -> str:
        if request.is_postprocessed is False:
            new_midi = self.process_midi(request.path)
            request.midi = new_midi
            request.is_postprocessed = True
        return super().handle(request)
