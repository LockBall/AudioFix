from dataclasses import dataclass
from pathlib import Path


APP_NAME = "AudioFix"
DEFAULT_OUTPUT_EXTENSION = ".ogg"
DEFAULT_MIN_DB = -60.0
DEFAULT_INITIAL_GAIN_DB_TEXT = ""
DEFAULT_DB_INTERVAL = 3.0
DEFAULT_PEAK_MARGIN_DB = 0.0


@dataclass(frozen=True)
class RuntimePaths:
    project_root: Path
    vendor_root: Path
    ffmpeg_root: Path


def get_runtime_paths(project_root: Path | None = None) -> RuntimePaths:
    root = project_root or Path(__file__).resolve().parents[3]
    vendor_root = root / "vendor"
    return RuntimePaths(
        project_root=root,
        vendor_root=vendor_root,
        ffmpeg_root=vendor_root / "ffmpeg",
    )
