import tkinter as tk
from tkinter import ttk

from genshin_automation.ui.routes_tab import RoutesRunTab
from genshin_automation.ui.editor_tab import RouteEditorTab
from genshin_automation.ui.debug_tab import DebugTab


def run_app() -> None:
    root = tk.Tk()
    root.title("Genshin Automation")

    notebook = ttk.Notebook(root)

    tab_run = RoutesRunTab(notebook)
    tab_edit = RouteEditorTab(notebook)
    tab_debug = DebugTab(notebook)

    notebook.add(tab_run, text="Run routes")
    notebook.add(tab_edit, text="Route editor")
    notebook.add(tab_debug, text="Debug")

    notebook.pack(fill="both", expand=True)
    root.geometry("1200x600")

    # -------- tab change handling --------
    def on_tab_changed(event: tk.Event) -> None:
        widget = event.widget
        current = widget.nametowidget(widget.select())

        if isinstance(current, RoutesRunTab):
            current.refresh_routes()
            current.refresh_windows()

        elif isinstance(current, DebugTab):
            current.refresh_windows()


    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    root.mainloop()
