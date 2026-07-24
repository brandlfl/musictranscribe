# Installation

1. Install `uv`. On Windows use the command ```winget install --id=astral-sh.uv  -e```. For other systems refer to `uv`s [Installation page](https://docs.astral.sh/uv/getting-started/installation/).
2. (optional) To support audio formats other than .wav install `ffmpeg` on Windows with ```winget install -e --id Gyan.FFmpeg``` or refer to the [Installation page](https://ffmpeg.org/download.html).
3. It is highly recommended to install a Notation tool for view scores and convert them to pdf. I recommend MuseScore Studio. Install directly ```winget install -e --id Musescore.Musescore``` or download [here](https://musescore.org/en).
4. Test the environment by opening a terminal in the same directory as this README file and execute ```uv run main.py```
5. If `madmom` is not working: 
    1. Install C++ Build Tools version >= 14 to properly use the `Cython` package. From the [Installation page](https://visualstudio.microsoft.com/de/visual-cpp-build-tools/) download and execute the installer. 
    2. In the menu choose what to install or change the installation to match what is described in [this issue](https://github.com/CPJKU/madmom/issues/478). 
    3. Open a PowerShell in this projects folder (the same folder this README file is in) and execute the following four lines: 
    ```SET DISTUTILS_USE_SDK=1```
    ```& 'C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvarsall.bat' x64``` change the path if you use a different version. 
    4. Rerun the test ```uv run main.py```
6. If some other package fails to install mentioning hardlinks try ```uv cache clean```
7. For troubleshooting it can be helpful to clear the virtual environment with ```uv venv``` or reinstall it with ```uv sync```.
8. Setting up MuScriptor. This is a huge leap in transcription accuracy and worth the extra setup. The model is hosted on HuggingFace and gated behind a license.
    1. Create a free account on HuggingFace at [this page](https://huggingface.co/join). 
    2. Accept the model license at https://huggingface.co/MuScriptor/muscriptor-medium
    3. Run ```uvx hf auth login``` and follow the instructions. 

# Usage 

Check out main.py and its tests. Run it with ```uv run main.py```. Then build your own chains of transcription tools. 

# TODO

- Keep up to date with the latest AMT developments
- Make a stable fallback environment for MuScriptor
- Find a way to install the secondary executables from the fixed demucs and basic-pitch environments