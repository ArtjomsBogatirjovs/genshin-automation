import tkinter as tk
from tkinter import ttk, messagebox

from genshin_automation.actions import MoveCameraAction
from genshin_automation.core import input_controller as ic
from genshin_automation.core.context import RunContext
from genshin_automation.core.window import GameWindow


class DebugTab(ttk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master)

        self.window_title_var = tk.StringVar()

        # click test
        self.x_frac_var = tk.StringVar(value="0.5")
        self.y_frac_var = tk.StringVar(value="0.5")

        # camera test
        self.camera_direction_var = tk.StringVar(value="right")
        self.camera_iterations_var = tk.StringVar(value="1")

        self._build_ui()
        self.refresh_windows()

    # -------------------------------------------------------------
    # UI BUILD
    # -------------------------------------------------------------
    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)

        # ---------------------------------------------------------
        # Window selector
        # ---------------------------------------------------------
        frame_window = ttk.LabelFrame(self, text="Game window")
        frame_window.grid(row=0, column=0, sticky="ew", padx=8, pady=8)

        ttk.Label(frame_window, text="Genshin window:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )

        self.window_combo = ttk.Combobox(
            frame_window,
            textvariable=self.window_title_var,
            state="readonly",
            width=40,
        )
        self.window_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        frame_window.columnconfigure(1, weight=1)

        ttk.Button(
            frame_window,
            text="Refresh",
            command=self.refresh_windows,
        ).grid(row=0, column=2, padx=5)

        # ---------------------------------------------------------
        # Click test
        # ---------------------------------------------------------
        frame_click = ttk.LabelFrame(self, text="Click tester")
        frame_click.grid(row=1, column=0, sticky="ew", padx=8, pady=8)

        ttk.Label(frame_click, text="X (0..1):").grid(
            row=0, column=0, padx=5, pady=2, sticky="w"
        )
        ttk.Entry(frame_click, textvariable=self.x_frac_var, width=10).grid(
            row=0, column=1, padx=5, pady=2, sticky="w"
        )

        ttk.Label(frame_click, text="Y (0..1):").grid(
            row=1, column=0, padx=5, pady=2, sticky="w"
        )
        ttk.Entry(frame_click, textvariable=self.y_frac_var, width=10).grid(
            row=1, column=1, padx=5, pady=2, sticky="w"
        )

        ttk.Button(
            frame_click,
            text="Click",
            command=self._debug_click,
        ).grid(row=2, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        self.pixel_label = ttk.Label(frame_click, text="Screen coords: - , -")
        self.pixel_label.grid(row=3, column=0, columnspan=3, sticky="w", padx=5)

        # ---------------------------------------------------------
        # Camera rotation test (same pattern as MoveCameraAction)
        # ---------------------------------------------------------
        frame_camera = ttk.LabelFrame(self, text="Camera rotation (Alt + drag)")
        frame_camera.grid(row=2, column=0, sticky="ew", padx=8, pady=8)

        ttk.Label(frame_camera, text="Direction:").grid(
            row=0, column=0, padx=5, pady=2, sticky="w"
        )
        direction_combo = ttk.Combobox(
            frame_camera,
            textvariable=self.camera_direction_var,
            state="readonly",
            values=["left", "right"],
            width=10,
        )
        direction_combo.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(frame_camera, text="Iterations:").grid(
            row=1, column=0, padx=5, pady=2, sticky="w"
        )
        ttk.Entry(frame_camera, textvariable=self.camera_iterations_var, width=10).grid(
            row=1, column=1, padx=5, pady=2, sticky="w"
        )

        ttk.Button(
            frame_camera,
            text="Rotate camera",
            command=self._debug_camera_rotate,
        ).grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    # -------------------------------------------------------------
    # WINDOW LIST
    # -------------------------------------------------------------
    def refresh_windows(self) -> None:
        titles = GameWindow.list_candidate_titles()
        self.window_combo["values"] = titles
        if titles:
            current = self.window_title_var.get()
            if current not in titles:
                self.window_title_var.set(titles[0])
        else:
            self.window_title_var.set("")

    # -------------------------------------------------------------
    # CLICK TEST
    # -------------------------------------------------------------
    def _debug_click(self) -> None:
        title = self.window_title_var.get().strip()
        if not title:
            messagebox.showwarning("Game window", "Select a game window.")
            return

        try:
            x_frac = float(self.x_frac_var.get())
            y_frac = float(self.y_frac_var.get())
        except ValueError:
            messagebox.showwarning("Invalid values", "X and Y must be floats.")
            return

        if not (0.0 <= x_frac <= 1.0 and 0.0 <= y_frac <= 1.0):
            messagebox.showwarning("Range error", "X and Y must be in range 0..1.")
            return

        gw = GameWindow(title=title)
        gw.find_and_focus()

        ic.move_mouse_to(gw.get_rect(), x_frac, y_frac)
        x, y = ic.get_x_y(gw.get_rect(), x_frac, y_frac)
        self.pixel_label.config(text=f"Screen coords: {x}, {y}")

        self._show_marker(x, y)

    # -------------------------------------------------------------
    # CAMERA ROTATION TEST
    # -------------------------------------------------------------
    def _debug_camera_rotate(self) -> None:
        title = self.window_title_var.get().strip()
        if not title:
            messagebox.showwarning("Game window", "Select a game window.")
            return

        direction = self.camera_direction_var.get()
        if direction not in ("left", "right"):
            messagebox.showwarning("Direction", "Direction must be 'left' or 'right'.")
            return

        try:
            iterations = int(self.camera_iterations_var.get())
        except ValueError:
            messagebox.showwarning("Iterations", "Iterations must be an integer.")
            return

        iterations = max(1, iterations)

        gw = GameWindow(title=title)
        gw.find_and_focus()
        rect = gw.get_rect()

        # Same logic as MoveCameraAction
        move_action = MoveCameraAction(direction=direction, iterations=iterations)
        move_action.run(RunContext(window_rect=rect, resolution=(16, 9)))

    # -------------------------------------------------------------
    # MARKER
    # -------------------------------------------------------------
    def _show_marker(self, x: int, y: int) -> None:
        size = 20
        top = tk.Toplevel(self)
        top.overrideredirect(True)
        top.geometry(f"{size}x{size}+{x - size // 2}+{y - size // 2}")
        try:
            top.attributes("-topmost", True)
            top.attributes("-alpha", 0.6)
        except tk.TclError:
            pass

        canvas = tk.Canvas(top, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_rectangle(0, 0, size, size, outline="red", width=2)

        top.after(4000, top.destroy)
