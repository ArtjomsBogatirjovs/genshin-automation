import tkinter as tk
from tkinter import ttk, messagebox

from genshin_automation.actions import TeleportMondstadtWolvendomAction
from genshin_automation.actions.action_types import ActionType
from genshin_automation.actions.click_point import ClickPointAction
from genshin_automation.actions.move import MoveAction
from genshin_automation.actions.move_camera import MoveCameraAction
from genshin_automation.actions.press_key import PressKeyAction
from genshin_automation.actions.teleport_monstadt import TeleportMondstadtWindwailAction
from genshin_automation.core.paths import ROUTES_DIR
from genshin_automation.core.route import Route, save_route, load_route

ACTION_UI_DEFS = {
    ActionType.CLICK: {
        "cls": ClickPointAction,
        "label": "Click at point",
        "fields": [
            {"name": "x_frac", "label": "X (0..1)", "type": "float", "default": "0.5"},
            {"name": "y_frac", "label": "Y (0..1)", "type": "float", "default": "0.5"},
        ],
    },
    ActionType.PRESS: {
        "cls": PressKeyAction,
        "label": "Press keyboard key",
        "fields": [
            {"name": "key", "label": "Key (e.g. 'f')", "type": "str", "default": "f"},
        ],
    },
    ActionType.MOVE: {
        "cls": MoveAction,
        "label": "Move in direction for seconds",
        "fields": [
            {
                "name": "direction",
                "label": "Direction",
                "type": "choice",
                "choices": ["forward", "backward", "left", "right"],
                "default": "forward",
            },
            {
                "name": "duration_s",
                "label": "Duration (s)",
                "type": "float",
                "default": "1.0",
            },
        ],
    },
    ActionType.MOVE_CAMERA: {
        "cls": MoveCameraAction,
        "label": "Rotate camera",
        "fields": [
            {
                "name": "direction",
                "label": "Direction",
                "type": "choice",
                "choices": ["left", "right"],
                "default": "right",
            },
            {
                "name": "iterations",
                "label": "Iterations",
                "type": "int",
                "default": "1",
            },
        ],
    },
    ActionType.TELEPORT_MONDSTADT_WINDWAIL: {
        "cls": TeleportMondstadtWindwailAction,
        "label": "Teleport to Mondstadt Windwail Highland Statue",
        "fields": [],
    },
    ActionType.TELEPORT_MONDSTADT_WOLVENDOM: {
        "cls": TeleportMondstadtWolvendomAction,
        "label": "Teleport to Mondstadt Wolvendom teleporter",
        "fields": [],
    },
}


class RouteEditorTab(ttk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master)

        self.route_name_var = tk.StringVar(value="new_route")
        self.actions_list = tk.Listbox(self, height=10)

        self.action_type_var = tk.StringVar()
        self._field_vars: dict[str, tk.StringVar] = {}
        self._current_actions: list[dict] = []

        self.routes_combo_var = tk.StringVar()
        self.routes_combo: ttk.Combobox | None = None

        # top: route name
        top = ttk.Frame(self)
        ttk.Label(top, text="Route name:").pack(side=tk.LEFT, padx=(5, 2))
        ttk.Entry(top, textvariable=self.route_name_var, width=30).pack(
            side=tk.LEFT, padx=2, pady=5
        )
        ttk.Button(
            top,
            text="New route",
            command=self.new_route,
        ).pack(side=tk.LEFT, padx=5)
        top.grid(row=0, column=0, columnspan=2, sticky="ew")

        # left: actions list
        ttk.Label(self, text="Actions in route:").grid(
            row=1, column=0, sticky="w", padx=5
        )
        self.actions_list.grid(
            row=2, column=0, rowspan=3, sticky="nsew", padx=5, pady=5
        )
        self.actions_list.bind("<<ListboxSelect>>", self._on_action_selected)

        # right: existing routes selector
        right_top = ttk.Frame(self)
        right_top.grid(row=1, column=1, sticky="ew", padx=5, pady=(5, 0))

        ttk.Label(right_top, text="Existing routes:").grid(
            row=0, column=0, sticky="w"
        )
        self.routes_combo = ttk.Combobox(
            right_top,
            textvariable=self.routes_combo_var,
            state="readonly",
            width=20,
        )
        self.routes_combo.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        btn_load = ttk.Button(
            right_top, text="Load", command=self.load_selected_route
        )
        btn_load.grid(row=0, column=2, sticky="w", padx=(5, 0))

        right_top.columnconfigure(1, weight=1)

        # right: dynamic action editor
        self.editor_frame = ttk.LabelFrame(self, text="Action editor")
        self.editor_frame.grid(
            row=2, column=1, rowspan=2, sticky="nsew", padx=5, pady=5
        )

        # bottom operations
        bottom = ttk.Frame(self)
        bottom.grid(row=5, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 5))

        btn_remove = ttk.Button(
            bottom, text="Remove selected", command=self.remove_selected
        )
        btn_move_up = ttk.Button(
            bottom, text="Move up", command=self.move_up
        )
        btn_move_down = ttk.Button(
            bottom, text="Move down", command=self.move_down
        )
        btn_save = ttk.Button(
            bottom, text="Save route", command=self.save_route_json
        )

        btn_remove.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        btn_move_up.grid(row=0, column=1, sticky="ew", padx=(0, 5))
        btn_move_down.grid(row=0, column=2, sticky="ew", padx=(0, 5))
        btn_save.grid(row=0, column=3, sticky="ew")

        bottom.columnconfigure(0, weight=0)
        bottom.columnconfigure(1, weight=0)
        bottom.columnconfigure(2, weight=0)
        bottom.columnconfigure(3, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        # initial state
        if ACTION_UI_DEFS:
            self.action_type_var.set(next(iter(ACTION_UI_DEFS.keys())))
        self._build_action_editor()
        self.refresh_available_routes()

    # ----------------- routes (file level) -----------------

    def refresh_available_routes(self) -> None:
        ROUTES_DIR.mkdir(parents=True, exist_ok=True)
        routes = sorted(p.stem for p in ROUTES_DIR.glob("*.json"))
        self.routes_combo["values"] = routes
        if routes and not self.routes_combo_var.get():
            self.routes_combo_var.set(routes[0])

    def load_selected_route(self) -> None:
        name = self.routes_combo_var.get().strip()
        if not name:
            messagebox.showwarning("Route", "Select a route to load.")
            return

        path = ROUTES_DIR / f"{name}.json"
        if not path.exists():
            messagebox.showerror("Load error", f"File not found:\n{path}")
            return

        try:
            route = load_route(path)
        except Exception as e:
            messagebox.showerror("Load error", f"Failed to load route:\n{e}")
            return

        self.route_name_var.set(route.name or name)
        self._current_actions.clear()

        for action in route.actions:
            cls = action.__class__
            type_name = cls.type_name()
            if type_name not in ACTION_UI_DEFS:
                messagebox.showwarning(
                    "Unknown action",
                    f"Action type '{type_name}' is not supported in editor. Skipped.",
                )
                continue

            ui_def = ACTION_UI_DEFS[type_name]
            a_dict: dict[str, object] = {"type": type_name}
            for field_def in ui_def["fields"]:
                fname = field_def["name"]
                a_dict[fname] = getattr(action, fname)
            self._current_actions.append(a_dict)

        self._rebuild_actions_list()

    # ----------------- editor UI -----------------

    def _build_action_editor(self) -> None:
        for child in self.editor_frame.winfo_children():
            child.destroy()
        self._field_vars.clear()

        ttk.Label(self.editor_frame, text="Action type:").grid(
            row=0, column=0, sticky="w", padx=5, pady=(5, 0)
        )
        type_combo = ttk.Combobox(
            self.editor_frame,
            textvariable=self.action_type_var,
            state="readonly",
            values=list(ACTION_UI_DEFS.keys()),
            width=100,
        )
        type_combo.grid(row=0, column=1, sticky="w", padx=5, pady=(5, 0))
        type_combo.bind("<<ComboboxSelected>>", lambda e: self._on_action_type_changed())

        ui_def = ACTION_UI_DEFS[self.action_type_var.get()]
        ttk.Label(self.editor_frame, text=ui_def["label"]).grid(
            row=1, column=0, columnspan=2, sticky="w", padx=5, pady=(2, 5)
        )

        row = 2
        for field_def in ui_def["fields"]:
            name = field_def["name"]
            label = field_def["label"]
            f_type = field_def["type"]
            default = str(field_def.get("default", ""))

            var = tk.StringVar(value=default)
            self._field_vars[name] = var

            ttk.Label(self.editor_frame, text=f"{label}:").grid(
                row=row, column=0, sticky="w", padx=5, pady=2
            )

            if f_type == "choice":
                choices = field_def["choices"]
                cb = ttk.Combobox(
                    self.editor_frame,
                    textvariable=var,
                    state="readonly",
                    values=choices,
                    width=15,
                )
                cb.grid(row=row, column=1, sticky="w", padx=5, pady=2)
            else:
                ttk.Entry(self.editor_frame, textvariable=var, width=15).grid(
                    row=row, column=1, sticky="w", padx=5, pady=2
                )
            row += 1

        btn_add = ttk.Button(
            self.editor_frame, text="Add action", command=self.add_action
        )
        btn_add.grid(
            row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 2)
        )

        btn_update = ttk.Button(
            self.editor_frame, text="Update selected", command=self.update_selected
        )
        btn_update.grid(
            row=row + 1, column=0, columnspan=2, sticky="ew", padx=5, pady=(2, 5)
        )

    def _on_action_type_changed(self) -> None:
        self._build_action_editor()

    # ----------------- actions list operations -----------------

    def _rebuild_actions_list(self) -> None:
        self.actions_list.delete(0, tk.END)
        for idx, action in enumerate(self._current_actions, start=1):
            summary_fields = [
                f"{k}={v}"
                for k, v in action.items()
                if k != "type"
            ]
            summary = ", ".join(summary_fields) if summary_fields else "(no params)"
            self.actions_list.insert(
                tk.END, f"{idx}. {action['type']}: {summary}"
            )

    def _collect_editor_values(self) -> dict | None:
        type_name = self.action_type_var.get()
        ui_def = ACTION_UI_DEFS[type_name]

        values: dict[str, object] = {"type": type_name}

        for field_def in ui_def["fields"]:
            name = field_def["name"]
            f_type = field_def["type"]
            raw = self._field_vars[name].get()

            try:
                if f_type == "float":
                    value = float(raw)
                elif f_type == "int":
                    value = int(raw)
                else:
                    value = str(raw)
            except ValueError:
                messagebox.showwarning(
                    "Invalid value",
                    f"Field '{name}' must be {f_type}.",
                )
                return None

            if name in ("x_frac", "y_frac") and f_type == "float":
                if not (0.0 <= value <= 1.0):
                    messagebox.showwarning(
                        "Range error",
                        f"{name} must be in range 0..1.",
                    )
                    return None

            values[name] = value

        return values

    def add_action(self) -> None:
        values = self._collect_editor_values()
        if values is None:
            return

        sel = self.actions_list.curselection()
        if sel:
            insert_index = sel[0] + 1
        else:
            insert_index = len(self._current_actions)

        self._current_actions.insert(insert_index, values)
        self._rebuild_actions_list()

        self.actions_list.selection_clear(0, tk.END)
        self.actions_list.selection_set(insert_index)
        self.actions_list.see(insert_index)

    def update_selected(self) -> None:
        sel = self.actions_list.curselection()
        if not sel:
            messagebox.showwarning("Update", "Select an action to update.")
            return

        index = sel[0]
        values = self._collect_editor_values()
        if values is None:
            return

        self._current_actions[index] = values
        self._rebuild_actions_list()
        self.actions_list.selection_clear(0, tk.END)
        self.actions_list.selection_set(index)
        self.actions_list.see(index)

    def remove_selected(self) -> None:
        sel = self.actions_list.curselection()
        if not sel:
            return
        index = sel[0]
        del self._current_actions[index]
        self._rebuild_actions_list()

        if self._current_actions:
            new_index = min(index, len(self._current_actions) - 1)
            self.actions_list.selection_set(new_index)
            self.actions_list.see(new_index)

    def move_up(self) -> None:
        sel = self.actions_list.curselection()
        if not sel:
            return
        index = sel[0]
        if index == 0:
            return

        self._current_actions[index - 1], self._current_actions[index] = (
            self._current_actions[index],
            self._current_actions[index - 1],
        )
        self._rebuild_actions_list()
        self.actions_list.selection_set(index - 1)
        self.actions_list.see(index - 1)

    def move_down(self) -> None:
        sel = self.actions_list.curselection()
        if not sel:
            return
        index = sel[0]
        if index >= len(self._current_actions) - 1:
            return

        self._current_actions[index + 1], self._current_actions[index] = (
            self._current_actions[index],
            self._current_actions[index + 1],
        )
        self._rebuild_actions_list()
        self.actions_list.selection_set(index + 1)
        self.actions_list.see(index + 1)

    # ----------------- selection → editor sync -----------------

    def _on_action_selected(self, _event) -> None:
        sel = self.actions_list.curselection()
        if not sel:
            return
        index = sel[0]
        if index >= len(self._current_actions):
            return

        action = self._current_actions[index]
        type_name = action["type"]

        if type_name not in ACTION_UI_DEFS:
            return

        # set type, rebuild editor for this type, then populate fields
        self.action_type_var.set(type_name)
        self._build_action_editor()

        ui_def = ACTION_UI_DEFS[type_name]
        for field_def in ui_def["fields"]:
            name = field_def["name"]
            if name in action and name in self._field_vars:
                self._field_vars[name].set(str(action[name]))

    # ----------------- save -----------------

    def save_route_json(self) -> None:
        if not self._current_actions:
            messagebox.showwarning("Empty route", "Add at least one action.")
            return

        name = self.route_name_var.get().strip()
        if not name:
            messagebox.showwarning("Route name", "Route name cannot be empty.")
            return

        actions = []
        for a in self._current_actions:
            type_name = a["type"]
            ui_def = ACTION_UI_DEFS[type_name]
            cls = ui_def["cls"]
            kwargs = {k: v for k, v in a.items() if k != "type"}
            action_obj = cls(**kwargs)
            actions.append(action_obj)

        route = Route(name=name, actions=actions)

        ROUTES_DIR.mkdir(parents=True, exist_ok=True)
        path = ROUTES_DIR / f"{name}.json"

        try:
            save_route(route, path)
        except Exception as e:
            messagebox.showerror("Save error", f"Failed to save route:\n{e}")
            return

        messagebox.showinfo("Saved", f"Route saved to:\n{path}")
        self.refresh_available_routes()

    def new_route(self) -> None:
        """
        Clear current route state and start a new route.
        """
        self.route_name_var.set("New route")

        self._current_actions.clear()
        self.actions_list.delete(0, tk.END)
        self.actions_list.selection_clear(0, tk.END)

        # reset editor to defaults for current action type
        if ACTION_UI_DEFS and not self.action_type_var.get():
            self.action_type_var.set(next(iter(ACTION_UI_DEFS.keys())))
        self._build_action_editor()
