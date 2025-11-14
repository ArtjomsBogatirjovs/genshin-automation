import tkinter as tk
from tkinter import ttk, messagebox

from genshin_automation.core.input_controller import click
from genshin_automation.core.window import GameWindow


class DebugTab(ttk.Frame):
    """
    Debug tab: choose game window, enter normalized coordinates (0..1),
    send a click to the game and show a marker square at click position.
    """

    def __init__(self, master: tk.Misc):
        super().__init__(master)

        self.window_title_var = tk.StringVar()
        self.x_frac_var = tk.StringVar(value="0.5")
        self.y_frac_var = tk.StringVar(value="0.5")

        # top: window selection
        top = ttk.LabelFrame(self, text="Game window")
        top.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        ttk.Label(top, text="Genshin / GI window:").grid(
            row=0, column=0, sticky="w", padx=5, pady=(5, 2)
        )
        self.window_combo = ttk.Combobox(
            top,
            textvariable=self.window_title_var,
            state="readonly",
            width=40,
        )
        self.window_combo.grid(
            row=0, column=1, sticky="ew", padx=5, pady=(5, 2)
        )
        btn_refresh = ttk.Button(
            top, text="Refresh", command=self.refresh_windows
        )
        btn_refresh.grid(
            row=0, column=2, sticky="w", padx=5, pady=(5, 2)
        )

        top.columnconfigure(1, weight=1)

        # middle: coordinates
        mid = ttk.LabelFrame(self, text="Click position (normalized)")
        mid.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        ttk.Label(mid, text="X (0..1):").grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )
        ttk.Entry(mid, textvariable=self.x_frac_var, width=10).grid(
            row=0, column=1, sticky="w", padx=5, pady=2
        )

        ttk.Label(mid, text="Y (0..1):").grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        ttk.Entry(mid, textvariable=self.y_frac_var, width=10).grid(
            row=1, column=1, sticky="w", padx=5, pady=2
        )

        self.pixel_label = ttk.Label(mid, text="Screen coords: -,-")
        self.pixel_label.grid(
            row=2, column=0, columnspan=3, sticky="w", padx=5, pady=(4, 2)
        )

        btn_click = ttk.Button(
            mid, text="Click in game and show marker", command=self.click_and_mark
        )
        btn_click.grid(
            row=3, column=0, columnspan=3, sticky="ew", padx=5, pady=(5, 5)
        )

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.refresh_windows()

    def refresh_windows(self):
        titles = GameWindow.list_candidate_titles()
        self.window_combo["values"] = titles
        if titles:
            current = self.window_title_var.get()
            if current not in titles:
                self.window_title_var.set(titles[0])
        else:
            self.window_title_var.set("")

    def click_and_mark(self):
        title = self.window_title_var.get().strip()
        if not title:
            messagebox.showwarning(
                "Game window", "Select a Genshin / GI window first."
            )
            return

        try:
            x_frac = float(self.x_frac_var.get())
            y_frac = float(self.y_frac_var.get())
        except ValueError:
            messagebox.showwarning(
                "Invalid values", "X and Y must be float numbers."
            )
            return

        if not (0.0 <= x_frac <= 1.0 and 0.0 <= y_frac <= 1.0):
            messagebox.showwarning(
                "Range error", "X and Y must be in range 0..1."
            )
            return

        gw = GameWindow(title=title)
        gw.find_and_focus()
        left, top, width, height = gw.get_rect()

        x = int(left + x_frac * width)
        y = int(top + y_frac * height)

        self.pixel_label.config(text=f"Screen coords: {x}, {y}")

        click(x, y)

        self._show_marker(x, y)

    def _show_marker(self, x: int, y: int):
        size = 20
        top = tk.Toplevel(self)
        top.overrideredirect(True)
        try:
            top.attributes("-topmost", True)
            top.attributes("-alpha", 0.6)
        except tk.TclError:
            pass

        # position centered at (x, y)
        top.geometry(f"{size}x{size}+{x - size//2}+{y - size//2}")

        canvas = tk.Canvas(top, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_rectangle(
            0, 0, size, size, outline="red", width=2
        )

        # destroy after 500 ms
        top.after(500, top.destroy)
