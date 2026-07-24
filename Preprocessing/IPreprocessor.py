from abc import ABC, abstractmethod
from AMT.Handler import AbstractHandler
from AMT.Piece import Piece

class ISeparator(AbstractHandler, ABC):
    """Interface for audio separation implementations."""
    @abstractmethod
    def process_wav(self, input_path: str) -> str:
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
        if request.is_preprocessed is False:
            new_audio = self.process_wav(request.path)
            request.path = new_audio
            request.is_preprocessed = True
        return super().handle(request)
