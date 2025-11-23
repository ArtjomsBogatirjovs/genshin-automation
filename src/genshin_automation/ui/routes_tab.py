import tkinter as tk
from tkinter import ttk, messagebox

from genshin_automation.config import AFTER_ROUTE_PAUSE
from genshin_automation.core import builtin_routes
from genshin_automation.core.context import RunContext
from genshin_automation.core.input_controller import open_map, scroll_up, scroll_down, sleep
from genshin_automation.core.paths import ROUTES_DIR
from genshin_automation.core.route import load_route
from genshin_automation.core.window import GameWindow

map_adjusted = False


def setup_map():
    global map_adjusted
    if map_adjusted:
        return
    open_map()
    for _ in range(61):
        scroll_down()
    for _ in range(19):
        scroll_up()
    open_map()
    map_adjusted = True


class RoutesRunTab(ttk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master)

        # list of routes
        self.routes_list = tk.Listbox(self, height=10, selectmode=tk.EXTENDED)

        self.btn_refresh_routes = ttk.Button(
            self, text="Refresh routes", command=self.refresh_routes
        )
        self.btn_run = ttk.Button(
            self, text="Run selected routes", command=self.run_selected
        )

        # game window selection
        self.window_title_var = tk.StringVar()
        self.aspect_var = tk.StringVar(value="16:9")

        ttk.Label(self, text="Routes:").grid(
            row=0, column=0, sticky="w", padx=5, pady=(5, 0)
        )
        self.routes_list.grid(
            row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5
        )

        self.btn_refresh_routes.grid(
            row=2, column=0, sticky="ew", padx=5, pady=(0, 5)
        )
        self.btn_run.grid(
            row=2, column=1, sticky="ew", padx=5, pady=(0, 5)
        )

        # game window block
        ttk.Label(self, text="Game window (Genshin / GI):").grid(
            row=3, column=0, sticky="w", padx=5
        )

        self.window_combo = ttk.Combobox(
            self,
            textvariable=self.window_title_var,
            state="readonly",
            width=40,
        )
        self.window_combo.grid(
            row=3, column=1, sticky="ew", padx=5, pady=(0, 5)
        )

        btn_refresh_windows = ttk.Button(
            self, text="Refresh windows", command=self.refresh_windows
        )
        btn_refresh_windows.grid(
            row=3, column=2, sticky="ew", padx=5, pady=(0, 5)
        )

        # aspect ratio (for future scaling logic)
        ttk.Label(self, text="Aspect ratio:").grid(
            row=4, column=0, sticky="w", padx=5
        )
        aspect_combo = ttk.Combobox(
            self,
            textvariable=self.aspect_var,
            state="readonly",
            values=["16:9", "21:9", "4:3"],
            width=8,
        )
        aspect_combo.grid(
            row=4, column=1, sticky="w", padx=5, pady=(0, 5)
        )

        # layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(1, weight=1)

        self.refresh_routes()
        self.refresh_windows()

    def refresh_routes(self):
        self.routes_list.delete(0, tk.END)
        ROUTES_DIR.mkdir(parents=True, exist_ok=True)
        for path in sorted(ROUTES_DIR.glob("*.json")):
            self.routes_list.insert(tk.END, path.stem)
        for display_name in builtin_routes.list_display_names():
            self.routes_list.insert(tk.END, display_name)

    def refresh_windows(self):
        titles = GameWindow.list_candidate_titles()
        self.window_combo["values"] = titles
        if titles:
            current = self.window_title_var.get()
            if current not in titles:
                self.window_title_var.set(titles[0])
        else:
            self.window_title_var.set("")

    def run_selected(self):
        selections = self.routes_list.curselection()
        if not selections:
            messagebox.showwarning(
                "No routes selected", "Select one or more routes to run."
            )
            return

        window_title = self.window_title_var.get().strip()
        if not window_title:
            messagebox.showwarning(
                "No game window",
                "Select a Genshin / GI window in the dropdown.",
            )
            return

        names = [self.routes_list.get(i) for i in selections]

        gw = GameWindow(title=window_title)
        gw.find_and_focus()
        rect = gw.get_rect()
        width, height = rect[2], rect[3]

        ctx = RunContext(
            window_rect=rect,
            resolution=(width, height)
        )

        setup_map()

        for i, name in enumerate(names):
            builtin_def = builtin_routes.find_by_display_name(name)
            if builtin_def is not None:
                route = builtin_def.factory()
            else:
                route_path = ROUTES_DIR / f"{name}.json"
                try:
                    route = load_route(route_path)
                except Exception as e:
                    messagebox.showerror(
                        "Load error",
                        f"Failed to load route '{name}':\n{e}",
                    )
                    return

            try:
                route.run(ctx)
                if i < len(names) - 1:
                    sleep(AFTER_ROUTE_PAUSE)
            except Exception as e:
                messagebox.showerror(
                    "Execution error",
                    f"Error while running route '{name}':\n{e}",
                )
                return

        messagebox.showinfo(
            "Done",
            "Routes executed:\n" + "\n".join(names),
        )
