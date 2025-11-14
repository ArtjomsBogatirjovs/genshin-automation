import tkinter as tk
from tkinter import ttk, messagebox

from genshin_automation.core import input_controller as ic
from genshin_automation.core.window import GameWindow


class DebugTab(ttk.Frame):
    """
    Debug tab for testing clicks and mouse movement.
    """

    def __init__(self, master: tk.Misc):
        super().__init__(master)

        self.window_title_var = tk.StringVar()

        # click test
        self.x_frac_var = tk.StringVar(value="0.5")
        self.y_frac_var = tk.StringVar(value="0.5")

        # mouse move test (relative)
        self.delta_x_var = tk.StringVar(value="200")
        self.delta_y_var = tk.StringVar(value="0")
        self.delta_duration_var = tk.StringVar(value="0.2")

        # camera look test
        self.camera_pixels_var = tk.StringVar(value="300")
        self.camera_duration_var = tk.StringVar(value="0.2")

        # layout
        self._build_ui()
        self.refresh_windows()

    # -------------------------------------------------------------
    # UI BUILD
    # -------------------------------------------------------------
    def _build_ui(self):
        self.columnconfigure(0, weight=1)

        # ---------------------------------------------------------
        # Window selector
        # ---------------------------------------------------------
        frame_window = ttk.LabelFrame(self, text="Game window")
        frame_window.grid(row=0, column=0, sticky="ew", padx=8, pady=8)

        ttk.Label(frame_window, text="Genshin window:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

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
            command=self.refresh_windows
        ).grid(row=0, column=2, padx=5)

        # ---------------------------------------------------------
        # Click test
        # ---------------------------------------------------------
        frame_click = ttk.LabelFrame(self, text="Click tester")
        frame_click.grid(row=1, column=0, sticky="ew", padx=8, pady=8)

        ttk.Label(frame_click, text="X (0..1):").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        ttk.Entry(frame_click, textvariable=self.x_frac_var, width=10).grid(row=0, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(frame_click, text="Y (0..1):").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        ttk.Entry(frame_click, textvariable=self.y_frac_var, width=10).grid(row=1, column=1, padx=5, pady=2, sticky="w")

        ttk.Button(
            frame_click,
            text="Click",
            command=self._debug_click
        ).grid(row=2, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        self.pixel_label = ttk.Label(frame_click, text="Screen coords: - , -")
        self.pixel_label.grid(row=3, column=0, columnspan=3, sticky="w", padx=5)

        # ---------------------------------------------------------
        # Relative mouse movement
        # ---------------------------------------------------------
        frame_move = ttk.LabelFrame(self, text="Mouse movement (relative)")
        frame_move.grid(row=2, column=0, sticky="ew", padx=8, pady=8)

        ttk.Label(frame_move, text="Delta X:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        ttk.Entry(frame_move, textvariable=self.delta_x_var, width=10).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame_move, text="Delta Y:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        ttk.Entry(frame_move, textvariable=self.delta_y_var, width=10).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(frame_move, text="Duration (s):").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        ttk.Entry(frame_move, textvariable=self.delta_duration_var, width=10).grid(row=2, column=1, padx=5, pady=2)

        ttk.Button(
            frame_move,
            text="Move mouse",
            command=self._debug_move_mouse
        ).grid(row=3, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        # ---------------------------------------------------------
        # Camera movement using relative mouse movement
        # ---------------------------------------------------------
        frame_camera = ttk.LabelFrame(self, text="Camera rotation")
        frame_camera.grid(row=3, column=0, sticky="ew", padx=8, pady=8)

        ttk.Label(frame_camera, text="Pixels:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        ttk.Entry(frame_camera, textvariable=self.camera_pixels_var, width=10).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame_camera, text="Duration (s):").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        ttk.Entry(frame_camera, textvariable=self.camera_duration_var, width=10).grid(row=1, column=1, padx=5, pady=2)

        btn_left = ttk.Button(frame_camera, text="Rotate Left", command=self._debug_camera_left)
        btn_right = ttk.Button(frame_camera, text="Rotate Right", command=self._debug_camera_right)

        btn_left.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        btn_right.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    # -------------------------------------------------------------
    # WINDOW LIST
    # -------------------------------------------------------------
    def refresh_windows(self):
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
    def _debug_click(self):
        title = self.window_title_var.get().strip()
        if not title:
            messagebox.showwarning("Game window", "Select a game window.")
            return

        x_frac = float(self.x_frac_var.get())
        y_frac = float(self.y_frac_var.get())

        gw = GameWindow(title=title)
        gw.find_and_focus()
        left, top, w, h = gw.get_rect()

        x = int(left + x_frac * w)
        y = int(top + y_frac * h)

        self.pixel_label.config(text=f"Screen coords: {x}, {y}")

        ic.click(x, y)
        self._show_marker(x, y)

    # -------------------------------------------------------------
    # RELATIVE MOUSE MOVEMENT
    # -------------------------------------------------------------
    def _debug_move_mouse(self):
        dx = int(self.delta_x_var.get())
        dy = int(self.delta_y_var.get())
        duration = float(self.delta_duration_var.get())

        ic.move_mouse_relative_smooth(dx, dy, duration=duration)

    # -------------------------------------------------------------
    # CAMERA MOVEMENT
    # -------------------------------------------------------------
    def _debug_camera_left(self):
        px = int(self.camera_pixels_var.get())
        duration = float(self.camera_duration_var.get())
        ic.mouse_look_left(pixels=px, duration=duration)

    def _debug_camera_right(self):
        px = int(self.camera_pixels_var.get())
        duration = float(self.camera_duration_var.get())
        ic.mouse_look_right(pixels=px, duration=duration)

    # -------------------------------------------------------------
    # MARKER
    # -------------------------------------------------------------
    def _show_marker(self, x: int, y: int):
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

        top.after(400, top.destroy)
