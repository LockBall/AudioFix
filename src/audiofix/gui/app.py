"""Tkinter GUI entry point.

The GUI is intentionally thin. Conversion planning and ffmpeg execution belong
in audiofix.core so the same behavior can later be reused by tests or a CLI.
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk

from audiofix import __version__
from audiofix.core.config import get_runtime_paths
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

    ttk.Label(frame, text="AudioFix").grid(row=0, column=0, sticky="w")
    theme_var.trace_add("write", on_theme_changed)

    ttk.Label(
        frame,
        text="Select a source audio file to begin.",
        style="Muted.TLabel",
    ).grid(row=1, column=0, sticky="w", pady=(8, 0))

    file_path_var = tk.StringVar(value="")
    media_dir = get_runtime_paths().project_root / "media"

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
            file_path_var.set(path)

    picker_frame = ttk.Frame(frame)
    picker_frame.grid(row=3, column=0, sticky="ew", pady=(12, 0))
    picker_frame.columnconfigure(1, weight=1)

    browse_btn = ttk.Button(picker_frame, text="Browse...", command=browse_file)
    browse_btn.grid(row=0, column=0, sticky="w")

    entry = ttk.Entry(picker_frame, textvariable=file_path_var, justify="left")
    entry.grid(row=0, column=1, sticky="ew", padx=(8, 0))

    root.mainloop()


if __name__ == "__main__":
    main()
