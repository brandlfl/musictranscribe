from pathlib import Path
import librosa

import logging
logger = logging.getLogger(__name__)

class Stem:
    """Represents audio featuring a single instrument."""
    
    def __init__(self, audio_path: str, instrument_name: str = None):
        """
        Initialize a Stem object.
        
        Args:
            audio_path (str or Path): Path to the audio file.
            instrument_name (str, optional): Name of the instrument. Defaults to None.
        """
        self.audio_path = Path(audio_path)
        if not self.audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {self.audio_path}")
        
        self.audio_data, self.sample_rate = librosa.load(self.audio_path, sr=None)

        if instrument_name is None:
            self.instrument_name = self.audio_path.stem.capitalize()
        else:
            self.instrument_name = instrument_name
        
        logger.debug(f"Initialized Stem: {self.instrument_name} from {self.audio_path}")
    
    def __repr__(self):
        return f"Stem(audio_path='{self.audio_path}', instrument_name='{self.instrument_name}')"
