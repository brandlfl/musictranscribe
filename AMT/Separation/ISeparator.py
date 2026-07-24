from abc import ABC, abstractmethod
from AMT.Handler import AbstractHandler
from AMT.Piece import Piece
from pathlib import Path

class ISeparator(AbstractHandler, ABC):
    """Interface for audio separation implementations."""
    @abstractmethod
    def separate_stems(self, input_path: str) -> list[str]:
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
        if request.is_separated is False:
            stems = self.separate_stems(request.path)
            request.stems.extend(stems)
            request.is_separated = True
        return super().handle(request)
