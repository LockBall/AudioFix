# AudioFix
Generate multiple quieter versions of an audio file for game audio tuning.

## Table of Contents

- [Purpose](#purpose)
- [Design](#design)
- [Project Structure](#project-structure)
- [Run the GUI](#run-the-gui)
- [MVP Scope](#mvp-scope)
- [Example](#example)
- [Words are Words](#words-are-words)
- [Levels](#levels)
- [Tools](#tools)
- [Vendor Resources](#vendor-resources)

## Purpose
- Take one source audio file and export multiple files with different volume reductions.
- Support manual analysis: the user determines the needed starting offset in a separate program and enters that value into AudioFix.
- Let the user choose how many output files to generate and the dB interval between each output.
- Generate a log file that records the source file, output files, and dB levels used.

## Design
- WoW's files are Ogg Vorbis, so the initial target output format is Ogg Vorbis.
- Use a Python Tkinter GUI frontend to control ffmpeg.
- Provide basic dependency-free light and dark GUI themes.
- Keep the first version free of third-party Python runtime dependencies.
- Prefer bundled `ffmpeg` and `ffprobe` binaries under `vendor/ffmpeg` so users do not need to install them manually.
- User-entered parameters:
  - dB offset
  - number of output files / steps
  - dB interval between files
  - output folder
- Output files use unique numbered names: `filename_0.ogg`, `filename_1.ogg`, `filename_2.ogg`, etc.
- Each run writes a log file as a reference for the dB levels used.

## Project Structure
- `src/audiofix/gui/`: Tkinter interface.
- `src/audiofix/core/`: conversion planning, naming, ffmpeg command generation, and logging logic.
- `vendor/ffmpeg/`: bundled ffmpeg/ffprobe resources.
- `tools/`: maintenance scripts for bundled resources and release prep.
- `docs/`: project notes that are more detailed than the README.
- `tests/`: focused tests for planning, naming, and command construction.

## Run the GUI
From the project root:

```powershell
python run_gui.py
```

## MVP Scope
- Batch loudness conversion first.
- The user handles audio analysis manually for now.
- The app applies deterministic dB gain changes and exports numbered files.
- Advanced restoration, clipping repair, compression repair, and generative audio features are future ideas tracked in `docs/ideas.md`.

## Example
- Example/source: https://www.wowhead.com/sound=8960/readycheck  
The infamous "Your dungeon is ready" sound that is much louder than desired.

## Words are Words
Audio (data) or (physical) Sound ?  
A microphone converts sound into audio, and a speaker converts audio into sound.

## Levels
- Use dB gain changes for the first version.
- Most WoW sound files appear to be volume maximized already, so the initial workflow assumes the source is loud enough and generates quieter variants.
- LUFS normalization and perceived-loudness workflows are out of scope for the first version.

## Tools

Utility scripts for maintaining bundled resources belong under `tools/`.

Planned scripts:

- download or update ffmpeg/ffprobe for supported platforms
- verify bundled binary versions
- prepare standalone release artifacts

## Vendor Resources

AudioFix is intended to be a mostly standalone utility. Third-party runtime
tools that users should not have to install manually belong here.

### ffmpeg

Expected layout for Windows builds:

```text
vendor/
  ffmpeg/
    win-x64/
      bin/
        ffmpeg.exe
        ffprobe.exe
```

Do not commit downloaded archives unless there is a deliberate release reason.
The app should prefer bundled binaries first and can later fall back to system
`ffmpeg` during development.
