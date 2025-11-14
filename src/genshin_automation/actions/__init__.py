from .base import Action, ACTION_REGISTRY
from .click_point import ClickPointAction
from .move_camera import MoveCameraAction
from .press_key import PressKeyAction
from .move import MoveAction
from .teleport_monstadt import TeleportMondstadtWindwailAction

__all__ = [
    "Action",
    "ACTION_REGISTRY",
    "ClickPointAction",
    "PressKeyAction",
    "MoveAction",
    "TeleportMondstadtWindwailAction",
    "MoveCameraAction",
]
