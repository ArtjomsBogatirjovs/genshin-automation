# **Genshin Automation**

A modular, extensible desktop automation tool for creating and executing custom routes in *Genshin Impact*.
Designed with clean architecture, OOP principles, and a plugin-like action system.

The tool provides:

* A GUI for building automation routes (clicks, movement, key presses, teleports, camera adjustments).
* A runtime engine that executes routes relative to the game window.
* A debug panel for testing input, clicks, and mouse movement.
* JSON-based route storage.
* Extensible action definitions via Python classes.

---

## **Features**

### ✔ Route Builder (Editor Tab)

* Create, edit, reorder, and update actions.
* Insert actions at any position.
* Auto-generated editor fields based on action metadata.
* Save routes to JSON.
* Load existing routes for modification.

### ✔ Route Runner (Routes Tab)

* Select game window (Genshin Impact).
* Choose aspect ratio or resolution (optional).
* Select one or multiple routes to run sequentially.
* Automatically focus the game window before execution.

### ✔ Debug Tools (Debug Tab)

* Click tester (percentage-based).
* Relative mouse movement tester.
* Camera rotation tester.
* Visual click markers.

### ✔ Action System

Actions are implemented as Python classes, each registered automatically:

* `ClickPointAction`
* `PressKeyAction`
* `MoveAction`
* `MoveCameraAction`
* `TeleportMondstadtAction`
* (Your custom actions can be easily added)

Each action implements:

```python
run(ctx: RunContext) -> None
type_name() -> str
to_dict() -> dict
from_dict(data) -> Action
```

---

## **Project Structure**

```
genshin-automation/
│
├─ routes/                       # Saved JSON routes
│
├─ src/
│   └─ genshin_automation/
│       ├─ __init__.py
│       ├─ __main__.py          # Entry point for python -m genshin_automation
│       ├─ main.py              # run_app()
│       ├─ core/
│       │   ├─ input_controller.py
│       │   ├─ window.py
│       │   ├─ route.py
│       │   ├─ context.py
│       │   └─ paths.py
│       ├─ ui/
│       │   ├─ app.py
│       │   ├─ editor_tab.py
│       │   ├─ routes_tab.py
│       │   └─ debug_tab.py
│       └─ actions/
│           ├─ action_types.py
│           ├─ base.py
│           ├─ click_point.py
│           ├─ press_key.py
│           ├─ move.py
│           ├─ move_camera.py
│           └─ teleport.py
│
├─ pyproject.toml
├─ requirements.txt
└─ README.md
```

---

## **Installation**

### 1. Clone the repository

```bash
git clone https://github.com/ArtjomsBogatirjovs/genshin-automation
cd genshin-automation
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate it

**PowerShell:**

```bash
.\.venv\Scripts\Activate.ps1
```

**CMD:**

```bash
.\.venv\Scripts\activate.bat
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Install the package in editable mode

```bash
pip install -e .
```

---

## **Running the Application**

### GUI launch

```bash
python -m genshin_automation
```

---

## **Creating a Route**

1. Open **Route Editor** tab
2. Enter a route name
3. Select an action type
4. Fill its parameters
5. Press **Add action**
6. Reorder actions (Move Up / Move Down) if needed
7. Press **Save**

Your route will appear in:

```
/routes/<route_name>.json
```

---

## **Executing a Route**

1. Open **Routes** tab
2. Select the Genshin window (recognized automatically by title)
3. Choose one or multiple routes
4. Press **Start**

The engine will:

* focus the game window
* execute each action sequentially
* respect timing and relative screen percentages

---

## **Extending the System**

To add a new action:

1. Create a new class in `src/genshin_automation/actions/`
2. Inherit from `Action`
3. Place `@register_action` decorator above the class
4. Implement required methods
5. Add UI definition in `ACTION_UI_DEFS`

Example:

```python
@register_action
@dataclass
class MyAction(Action):
    value: int

    @staticmethod
    def type_name() -> str:
        return ActionType.MY_ACTION

    def run(self, ctx: RunContext) -> None:
        print("Do something", self.value)
```

---

## **Important Notes**

* This tool uses only legal desktop automation (no memory editing, no injection).
* It simulates clicks and keyboard input like a macro recorder.
* Use responsibly.
