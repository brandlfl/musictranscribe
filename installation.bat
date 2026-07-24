@REM Install uv and ffmpeg with winget
winget install --id=astral-sh.uv  -e
winget install -e --id Gyan.FFmpeg
@REM Install C++ build tools for using madmom and demucs
@REM XXX TODO: This step is manual!!! See README.md for instructions
@REM Install tools with uv
uv tool install muscriptor
@REM uv tool install git+https://github.com/brandlfl/demucs
@REM uv tool install --python 3.11 --with-executables-from basic-pitch git+https://github.com/brandlfl/basicpitchuv.git