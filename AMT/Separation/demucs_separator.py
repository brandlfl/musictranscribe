# maybe make alternate version with no pip install, only uvx command
import subprocess

from AMT.Separation.ISeparator import ISeparator
from pathlib import Path


class DemucsSeparator(ISeparator):

    _demucs_models = ["htdemucs", "htdemucs_ft", "htdemucs_6s", "hdemucs_mmi", "mdx", "mdx_extra"]
    DEFAULT_OUTPUT_PATH = "separated"

    def __init__(self, model: str = "htdemucs"):
        if DemucsSeparator._demucs_models.count(model) == 0:
            raise ValueError(f"Invalid model name: {model}. Must be one of {DemucsSeparator._demucs_models}")
        self.model = model
    
    def separate_stems(self, input_path: str, *demucs_args) -> list[str]:
        """Separate stems from an audio file using Demucs.

        Parameters
        ----------
        input_path : str
            Path to the input audio file.

        Returns
        -------
        list[str]
            Paths to the separated single-instrument output files.
        """
        in_path = Path(input_path)
        if not in_path.exists():
            raise FileNotFoundError(f"Input file not found: {in_path}")

        if len(demucs_args) < 2:
            out_path = Path(DemucsSeparator.DEFAULT_OUTPUT_PATH)
        else:
            # Passing an output path as argument is not yet implemented. 
            out_path = Path(DemucsSeparator.DEFAULT_OUTPUT_PATH)
        Path(out_path).mkdir(parents=True, exist_ok=True)

        # Call Demucs to separate stems
        # a) use demucs in Python directly (requires pip install demucs)
        # demucs.separate.main(["--model", self.model, str(input_path)])
        # b) use demucs via uv (requieres uv, nothing else)
        #    The official demucs repo is missing a numpy import, which is fixed in the provided fork.
        try:
            subprocess.run(["uvx", "--from", "git+https://github.com/brandlfl/demucs", "demucs", "-n", self.model, "-o", str(out_path), *demucs_args, str(in_path)], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error occurred while separating stems: {e}")

        # The output directory is created in the same directory as the input file
        # demucs creates the structure "modelname/inputstem/"
        output_dir = Path(f"separated/{self.model}/{in_path.stem}")
        if not output_dir.exists():
            raise FileNotFoundError(f"Output directory not found: {output_dir.as_posix()}")

        # Collect paths to separated stems
        stem_paths = [str(stem) for stem in output_dir.iterdir() if stem.is_file()]
        
        return stem_paths