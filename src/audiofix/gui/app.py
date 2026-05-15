"""Tkinter GUI entry point.

The GUI is intentionally thin. Conversion planning and ffmpeg execution belong
in audiofix.core so the same behavior can later be reused by tests or a CLI.
"""

import os
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, filedialog
from tkinter import ttk

from audiofix import __version__
from audiofix.core.config import (
    DEFAULT_DB_INTERVAL,
    DEFAULT_INITIAL_GAIN_DB_TEXT,
    DEFAULT_MIN_DB,
    DEFAULT_PEAK_MARGIN_DB,
    get_runtime_paths,
)
from audiofix.core.ffmpeg import (
    FfmpegOptions,
    AudioInfo,
    build_ffmpeg_command,
    check_ffmpeg_tools,
    convert_plan_item,
    gain_to_peak_margin_db,
    measure_max_volume_db,
    probe_audio_info,
)
from audiofix.core.planning import (
    build_output_plan,
    calculate_step_count,
)
from audiofix.gui.theme import DEFAULT_THEME, THEMES, apply_theme


def build_menu(root: tk.Tk, theme_var: tk.StringVar) -> tk.Menu:
    menu_bar = tk.Menu(root)

    view_menu = tk.Menu(menu_bar, tearoff=False)
    theme_menu = tk.Menu(view_menu, tearoff=False)
    for theme_name in THEMES:
        theme_menu.add_radiobutton(
            label=theme_name.title(),
            variable=theme_var,
            value=theme_name,
        )
    view_menu.add_cascade(label="Theme", menu=theme_menu)
    menu_bar.add_cascade(label="View", menu=view_menu)

    help_menu = tk.Menu(menu_bar, tearoff=False)
    help_menu.add_command(
        label="About AudioFix",
        command=lambda: messagebox.showinfo(
            title="About AudioFix",
            message=(
                f"AudioFix {__version__}\n\n"
                "Batch loudness converter for generating quieter game audio variants."
            ),
        ),
    )
    menu_bar.add_cascade(label="Help", menu=help_menu)

    return menu_bar


def main() -> None:
    root = tk.Tk()
    root.title("AudioFix")
    root.minsize(720, 420)
    apply_theme(root, DEFAULT_THEME)

    frame = ttk.Frame(root, padding=16)
    frame.grid(row=0, column=0, sticky="nsew")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(2, weight=1)

    theme_var = tk.StringVar(value=DEFAULT_THEME)
    root.configure(menu=build_menu(root, theme_var))

    def on_theme_changed(*_: object) -> None:
        apply_theme(root, theme_var.get())

    def clear_entry_focus(event: tk.Event) -> None:
        widget = event.widget
        if isinstance(widget, (tk.Entry, ttk.Entry, tk.Text)):
            return
        root.focus_set()

    theme_var.trace_add("write", on_theme_changed)
    root.bind("<Button-1>", clear_entry_focus, add="+")

    runtime_paths = get_runtime_paths()
    media_dir = runtime_paths.project_root / "media"

    file_path_var = tk.StringVar(value="")
    min_db_var = tk.StringVar(value=f"{DEFAULT_MIN_DB:.2f}")
    initial_gain_db_var = tk.StringVar(value=DEFAULT_INITIAL_GAIN_DB_TEXT)
    db_interval_var = tk.StringVar(value=f"{DEFAULT_DB_INTERVAL:.2f}")
    peak_margin_db_var = tk.StringVar(value=f"{DEFAULT_PEAK_MARGIN_DB:.2f}")
    step_count_var = tk.StringVar(value="")
    output_folder_var = tk.StringVar(value="")
    audio_info_var = tk.StringVar(value="Audio info: select an input file.")
    overwrite_var = tk.BooleanVar(value=False)
    status_var = tk.StringVar(value="Ready.")
    ffmpeg_status_var = tk.StringVar(value="")
    ffprobe_status_var = tk.StringVar(value="")
    command_preview_var = tk.StringVar(value="ffmpeg command preview unavailable.")
    last_audio_info: list[AudioInfo | None] = [None]
    last_output_folder: list[Path | None] = [None]

    def refresh_tool_status() -> None:
        tool_status = check_ffmpeg_tools()
        ffmpeg_status_var.set(tool_status.ffmpeg.display_text())
        ffprobe_status_var.set(tool_status.ffprobe.display_text())

    def format_audio_info(info: AudioInfo) -> str:
        bit_rate = f"{round(info.bit_rate / 1000)} kbps" if info.bit_rate else "unknown bitrate"
        sample_rate = f"{info.sample_rate} Hz" if info.sample_rate else "unknown sample rate"
        channels = f"{info.channels} ch" if info.channels else "unknown channels"
        return f"Audio info: {info.codec_name}, {bit_rate}, {sample_rate}, {channels}"

    def get_audio_info(source_path: Path) -> AudioInfo | None:
        tool_status = check_ffmpeg_tools()
        ffmpeg_status_var.set(tool_status.ffmpeg.display_text())
        ffprobe_status_var.set(tool_status.ffprobe.display_text())
        if not tool_status.ffprobe.available or tool_status.ffprobe.path is None:
            error = tool_status.ffprobe.error or "ffprobe not found"
            audio_info_var.set(f"Audio info: {error}.")
            return None
        try:
            info = probe_audio_info(tool_status.ffprobe.path, source_path)
        except (RuntimeError, ValueError) as error:
            audio_info_var.set(f"Audio info: {error}")
            last_audio_info[0] = None
            return None
        audio_info_var.set(format_audio_info(info))
        last_audio_info[0] = info
        return info

    def update_step_count(*_: object) -> None:
        try:
            step_count = calculate_step_count(
                min_db=float(min_db_var.get()),
                db_interval=float(db_interval_var.get()),
            )
        except ValueError:
            step_count_var.set("Invalid")
            return
        step_count_var.set(str(step_count))

    def update_command_preview(*_: object) -> None:
        source_text = file_path_var.get().strip()
        output_text = output_folder_var.get().strip()
        if not source_text or not output_text:
            command_preview_var.set("ffmpeg command preview unavailable.")
            return

        tool_status = check_ffmpeg_tools()
        if not tool_status.ffmpeg.available or tool_status.ffmpeg.path is None:
            command_preview_var.set("ffmpeg command preview unavailable: ffmpeg missing.")
            return

        try:
            initial_gain_db = float(initial_gain_db_var.get())
        except ValueError:
            command_preview_var.set("ffmpeg command preview unavailable: enter Initial dB.")
            return

        try:
            db_interval = float(db_interval_var.get())
        except ValueError:
            command_preview_var.set("ffmpeg command preview unavailable: enter dB interval.")
            return

        source_path = Path(source_text)
        output_dir = Path(output_text)
        plan = build_output_plan(
            source_path=source_path,
            output_dir=output_dir,
            db_offset=initial_gain_db,
            step_count=1,
            db_interval=-abs(db_interval),
        )
        command = build_ffmpeg_command(
            ffmpeg_path=tool_status.ffmpeg.path,
            source_path=source_path,
            item=plan[0],
            options=FfmpegOptions(
                audio_bitrate=(
                    f"{last_audio_info[0].bit_rate}"
                    if last_audio_info[0] and last_audio_info[0].bit_rate
                    else None
                ),
                sample_rate=last_audio_info[0].sample_rate if last_audio_info[0] else None,
                channels=last_audio_info[0].channels if last_audio_info[0] else None,
                overwrite=overwrite_var.get(),
            ),
        )
        command_preview_var.set(" ".join(f'"{part}"' if " " in part else part for part in command))

    def format_decimal_var(value_var: tk.StringVar) -> None:
        try:
            value_var.set(f"{float(value_var.get()):.2f}")
        except ValueError:
            return

    def on_peak_margin_focus_out() -> None:
        if not peak_margin_db_var.get().strip():
            peak_margin_db_var.set("0.00")
        format_decimal_var(peak_margin_db_var)
        status_var.set("Peak margin changed. Click Analyze peak to recalculate Initial dB.")

    def browse_file() -> None:
        path = filedialog.askopenfilename(
            title="Select input audio file",
            initialdir=str(media_dir),
            filetypes=(
                ("Audio files", "*.wav *.mp3 *.flac *.ogg *.m4a"),
                ("All files", "*.*"),
            ),
        )
        if path:
            input_path = Path(path)
            file_path_var.set(str(input_path))
            output_folder_var.set(str(input_path.with_name(f"{input_path.stem}_out")))
            last_audio_info[0] = None
            last_output_folder[0] = None
            open_output_button.state(["disabled"])
            get_audio_info(input_path)
            update_command_preview()

    def browse_output_folder() -> None:
        path = filedialog.askdirectory(
            title="Select output folder",
            initialdir=str(media_dir),
        )
        if path:
            output_folder_var.set(str(Path(path)))
            last_output_folder[0] = None
            open_output_button.state(["disabled"])
            update_command_preview()

    def analyze_peak() -> None:
        source_text = file_path_var.get().strip()
        if not source_text:
            status_var.set("Select an input file before analyzing peak.")
            return

        source_path = Path(source_text)
        if not source_path.is_file():
            status_var.set("Select a valid input file before analyzing peak.")
            return

        tool_status = check_ffmpeg_tools()
        ffmpeg_status_var.set(tool_status.ffmpeg.display_text())
        ffprobe_status_var.set(tool_status.ffprobe.display_text())
        if not tool_status.ffmpeg.available or tool_status.ffmpeg.path is None:
            status_var.set("ffmpeg unavailable; cannot analyze peak.")
            return

        status_var.set("Analyzing peak...")
        root.update_idletasks()
        try:
            max_volume_db = measure_max_volume_db(tool_status.ffmpeg.path, source_path)
            peak_margin_db = float(peak_margin_db_var.get())
        except ValueError:
            status_var.set("Enter a valid peak margin dB value.")
            return
        except RuntimeError as error:
            status_var.set(f"Peak analysis failed: {error}")
            return

        initial_gain_db = gain_to_peak_margin_db(max_volume_db, peak_margin_db)
        initial_gain_db_var.set(f"{initial_gain_db:.2f}")
        target_peak_db = -abs(peak_margin_db)
        status_var.set(
            f"Peak analysis: max {max_volume_db:.2f} dB, target {target_peak_db:.2f} dB, "
            f"initial gain {initial_gain_db:.2f} dB."
        )
        update_command_preview()

    def open_output_folder() -> None:
        output_dir = last_output_folder[0]
        if output_dir is None or not output_dir.is_dir():
            status_var.set("No generated output folder to open.")
            open_output_button.state(["disabled"])
            return
        os.startfile(str(output_dir))

    def run_conversion() -> None:
        try:
            source_text = file_path_var.get().strip()
            output_text = output_folder_var.get().strip()
            min_db = float(min_db_var.get())
            db_interval = float(db_interval_var.get())
            step_count = calculate_step_count(min_db=min_db, db_interval=db_interval)
        except ValueError as error:
            status_var.set(f"Invalid settings: {error}")
            return

        try:
            initial_gain_db = float(initial_gain_db_var.get())
        except ValueError:
            status_var.set("Enter the initial dB value determined in GoldWave.")
            return

        if not source_text:
            status_var.set("Select an input file.")
            return
        if not output_text:
            status_var.set("Select an output folder.")
            return

        source_path = Path(source_text)
        output_dir = Path(output_text)
        if not source_path.is_file():
            status_var.set("Select a valid input file.")
            return
        last_output_folder[0] = None
        open_output_button.state(["disabled"])
        audio_info = get_audio_info(source_path)
        if audio_info is None:
            status_var.set("Cannot read input audio settings with ffprobe.")
            return
        if audio_info.bit_rate is None:
            status_var.set("Input audio bitrate is unknown; conversion stopped to avoid changing it.")
            return

        tool_status = check_ffmpeg_tools()
        ffmpeg_status_var.set(tool_status.ffmpeg.display_text())
        ffprobe_status_var.set(tool_status.ffprobe.display_text())
        if not tool_status.available or tool_status.ffmpeg.path is None:
            status_var.set(
                "ffmpeg/ffprobe unavailable. Add both under "
                "vendor/ffmpeg/win-x64/bin or install them on PATH."
            )
            return

        output_dir.mkdir(parents=True, exist_ok=True)
        plan = build_output_plan(
            source_path=source_path,
            output_dir=output_dir,
            db_offset=initial_gain_db,
            step_count=step_count,
            db_interval=-abs(db_interval),
        )
        existing_outputs = [item.output_path for item in plan if item.output_path.exists()]
        if existing_outputs and not overwrite_var.get():
            status_var.set(
                f"{len(existing_outputs)} output files already exist. Enable overwrite or choose a new folder."
            )
            return
        options = FfmpegOptions(
            audio_bitrate=f"{audio_info.bit_rate}",
            sample_rate=audio_info.sample_rate,
            channels=audio_info.channels,
            overwrite=overwrite_var.get(),
        )

        for item in plan:
            status_var.set(f"Converting {item.output_path.name}...")
            root.update_idletasks()
            result = convert_plan_item(
                ffmpeg_path=tool_status.ffmpeg.path,
                source_path=source_path,
                item=item,
                options=options,
            )
            if result.returncode != 0:
                error_text = result.stderr.strip() or result.stdout.strip()
                status_var.set(f"ffmpeg failed on {item.output_path.name}: {error_text}")
                return

        last_output_folder[0] = output_dir
        open_output_button.state(["!disabled"])
        status_var.set(f"Generated {len(plan)} files in {output_dir}.")

    ttk.Label(
        frame,
        text="Select input, adjust settings, then choose an output folder.",
        style="Muted.TLabel",
    ).grid(row=0, column=0, sticky="w")
    tools_frame = ttk.Frame(frame)
    tools_frame.grid(row=0, column=0, sticky="e")
    ttk.Label(tools_frame, textvariable=ffmpeg_status_var, style="Status.TLabel").grid(
        row=0,
        column=0,
        sticky="e",
    )
    ttk.Label(tools_frame, textvariable=ffprobe_status_var, style="Status.TLabel").grid(
        row=0,
        column=1,
        sticky="e",
        padx=(8, 0),
    )

    input_frame = ttk.Frame(frame)
    input_frame.grid(row=1, column=0, sticky="ew", pady=(16, 0))
    input_frame.columnconfigure(1, weight=1)

    ttk.Label(input_frame, text="Input file").grid(row=0, column=0, sticky="w")
    ttk.Entry(input_frame, textvariable=file_path_var, justify="left").grid(
        row=0,
        column=1,
        sticky="ew",
        padx=(8, 8),
    )
    browse_btn = ttk.Button(input_frame, text="Browse...", command=browse_file)
    browse_btn.grid(row=0, column=2, sticky="e")

    settings_frame = ttk.Frame(frame)
    settings_frame.grid(row=2, column=0, sticky="new", pady=(20, 0))
    for column in range(5):
        settings_frame.columnconfigure(column, weight=1, uniform="settings")

    min_db_frame = ttk.Frame(settings_frame)
    min_db_frame.grid(row=0, column=0, sticky="w", padx=(0, 12))
    ttk.Label(min_db_frame, text="Minimum dB").grid(row=0, column=0, sticky="w")
    min_db_entry = ttk.Entry(
        min_db_frame,
        textvariable=min_db_var,
        width=12,
        justify="right",
    )
    min_db_entry.grid(
        row=1,
        column=0,
        sticky="w",
        pady=(4, 0),
    )
    min_db_entry.bind("<FocusOut>", lambda _event: format_decimal_var(min_db_var))

    initial_gain_db_frame = ttk.Frame(settings_frame)
    initial_gain_db_frame.grid(row=0, column=1, sticky="w", padx=(0, 12))
    ttk.Label(initial_gain_db_frame, text="Initial dB").grid(row=0, column=0, sticky="w")
    initial_gain_db_entry = ttk.Entry(
        initial_gain_db_frame,
        textvariable=initial_gain_db_var,
        width=12,
        justify="right",
    )
    initial_gain_db_entry.grid(row=1, column=0, sticky="w", pady=(4, 0))
    initial_gain_db_entry.bind("<FocusOut>", lambda _event: format_decimal_var(initial_gain_db_var))
    ttk.Button(
        initial_gain_db_frame,
        text="Analyze peak",
        command=analyze_peak,
    ).grid(row=2, column=0, sticky="w", pady=(6, 0))

    peak_margin_db_frame = ttk.Frame(settings_frame)
    peak_margin_db_frame.grid(row=0, column=2, sticky="w", padx=(0, 12))
    ttk.Label(peak_margin_db_frame, text="Peak margin dB").grid(row=0, column=0, sticky="w")
    peak_margin_db_entry = ttk.Entry(
        peak_margin_db_frame,
        textvariable=peak_margin_db_var,
        width=12,
        justify="right",
    )
    peak_margin_db_entry.grid(row=1, column=0, sticky="w", pady=(4, 0))
    peak_margin_db_entry.bind("<FocusOut>", lambda _event: on_peak_margin_focus_out())

    db_interval_frame = ttk.Frame(settings_frame)
    db_interval_frame.grid(row=0, column=3, sticky="w", padx=(0, 12))
    ttk.Label(db_interval_frame, text="dB interval").grid(row=0, column=0, sticky="w")
    db_interval_entry = ttk.Entry(
        db_interval_frame,
        textvariable=db_interval_var,
        width=12,
        justify="right",
    )
    db_interval_entry.grid(row=1, column=0, sticky="w", pady=(4, 0))
    db_interval_entry.bind("<FocusOut>", lambda _event: format_decimal_var(db_interval_var))

    step_count_frame = ttk.Frame(settings_frame)
    step_count_frame.grid(row=0, column=4, sticky="w")
    ttk.Label(step_count_frame, text="Number of files").grid(row=0, column=0, sticky="w")
    ttk.Label(step_count_frame, textvariable=step_count_var).grid(
        row=1,
        column=0,
        sticky="w",
        pady=(8, 0),
    )

    min_db_var.trace_add("write", update_step_count)
    db_interval_var.trace_add("write", update_step_count)
    db_interval_var.trace_add("write", update_command_preview)
    initial_gain_db_var.trace_add("write", update_command_preview)
    overwrite_var.trace_add("write", update_command_preview)
    update_step_count()
    update_command_preview()

    audio_frame = ttk.Frame(frame)
    audio_frame.grid(row=3, column=0, sticky="ew", pady=(20, 0))
    audio_frame.columnconfigure(0, weight=1)

    ttk.Label(audio_frame, textvariable=audio_info_var, style="Muted.TLabel").grid(
        row=0,
        column=0,
        sticky="w",
    )
    ttk.Checkbutton(
        audio_frame,
        text="Overwrite existing files",
        variable=overwrite_var,
    ).grid(row=0, column=1, sticky="e")

    command_frame = ttk.Frame(frame)
    command_frame.grid(row=4, column=0, sticky="ew", pady=(16, 0))
    command_frame.columnconfigure(0, weight=1)

    ttk.Label(command_frame, text="FFmpeg command").grid(row=0, column=0, sticky="w")
    ttk.Entry(
        command_frame,
        textvariable=command_preview_var,
        justify="left",
        state="readonly",
    ).grid(row=1, column=0, sticky="ew", pady=(4, 0))

    output_frame = ttk.Frame(frame)
    output_frame.grid(row=5, column=0, sticky="ew", pady=(20, 0))
    output_frame.columnconfigure(1, weight=1)

    ttk.Label(output_frame, text="Output folder").grid(row=0, column=0, sticky="w")
    ttk.Entry(
        output_frame,
        textvariable=output_folder_var,
        justify="left",
    ).grid(row=0, column=1, sticky="ew", padx=(8, 8))
    ttk.Button(
        output_frame,
        text="Browse...",
        command=browse_output_folder,
    ).grid(row=0, column=2, sticky="e")

    action_frame = ttk.Frame(frame)
    action_frame.grid(row=6, column=0, sticky="ew", pady=(16, 0))
    action_frame.columnconfigure(0, weight=1)

    ttk.Label(action_frame, textvariable=status_var, style="Muted.TLabel").grid(
        row=0,
        column=0,
        sticky="w",
    )
    ttk.Button(action_frame, text="Run conversion", command=run_conversion).grid(
        row=0,
        column=1,
        sticky="e",
        padx=(8, 0),
    )
    open_output_button = ttk.Button(
        action_frame,
        text="Open output folder",
        command=open_output_folder,
    )
    open_output_button.grid(
        row=0,
        column=2,
        sticky="e",
        padx=(8, 0),
    )
    open_output_button.state(["disabled"])

    refresh_tool_status()

    root.mainloop()


if __name__ == "__main__":
    main()
