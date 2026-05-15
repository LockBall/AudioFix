# Tools

Maintenance scripts for local development and release prep.

## Check ffmpeg

```powershell
python tools/check_ffmpeg.py
```

Checks whether `ffmpeg.exe` and `ffprobe.exe` are available from the bundled
vendor path or system `PATH`.

## Install ffmpeg

```powershell
python tools/install_ffmpeg.py
```

Downloads a Windows ffmpeg release zip and copies `ffmpeg.exe` and
`ffprobe.exe` into:

```text
vendor/ffmpeg/win-x64/bin/
```

Use `--force` to replace existing binaries.
