@REM Install uv, ffmpeg and MusescoreStudio with winget
winget install --id=astral-sh.uv  -e
winget install -e --id Gyan.FFmpeg
winget install -e --id Musescore.Musescore
@REM Install C++ build tools for using madmom and demucs
@REM XXX TODO: This step is manual!!! See README.md for instructions
@REM Install tools with uv
uv tool install git+https://github.com/brandlfl/demucs
@REM uv tool install --python 3.11 --with-executables-from basic-pitch git+https://github.com/brandlfl/basicpitchuv.git
uv tool install --python cp311 git+https://github.com/brandlfl/basic-pitch-env --force
uv tool install muscriptor
@REM You need an account on HuggingFace to download the muscriptor model. See README.md for more instructions. 
@REM Login to HuggingFace and accept the muscriptor model license at https://huggingface.co/MuScriptor/muscriptor-medium 
uvx hf auth login