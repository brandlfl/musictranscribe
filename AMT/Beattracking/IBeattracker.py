from abc import ABC, abstractmethod
from AMT.Handler import AbstractHandler
from AMT.Piece import Piece

class IBeattracker(AbstractHandler, ABC):
    DEFAULT_OUTPUT_PATH = "beat_tracked"
    @abstractmethod
    def track_beats(self, input_path: str, output_path: str) -> str:
        pass

    def handle(self, request: Piece) -> str:
        if request.beatmap is None:
            beat_file = self.track_beats(request.path)
        return super().handle(request)