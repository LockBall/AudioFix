# Dependencies

## Runtime

- Python 3.11 or newer
- Tkinter from the Python standard library, using basic app-owned light/dark themes
- ffmpeg and ffprobe, preferably bundled under `vendor/ffmpeg`

The first version should avoid third-party Python packages. That keeps the app
easy to run and makes future standalone packaging simpler.

## Packaging Direction

The likely packaging path is PyInstaller or a similar freezer once the MVP is
stable. At that point, bundled `ffmpeg.exe` and `ffprobe.exe` should be included
as application data.

## Future Updating

Resource updating should be handled by explicit maintenance tooling, not silent
runtime downloads. The app can later expose an update check, but conversion
should not depend on network access.
