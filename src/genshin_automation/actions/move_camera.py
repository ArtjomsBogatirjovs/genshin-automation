from dataclasses import dataclass
from typing import Dict, Any, Literal

from genshin_automation.actions.base import Action, register_action
from genshin_automation.actions.action_types import ActionType
from genshin_automation.core.context import RunContext
from genshin_automation.core import input_controller as ic

Direction = Literal["left", "right"]

@register_action
@dataclass
class MoveCameraAction(Action):
    direction: Direction
    pixels: int
    duration_s: float

    @staticmethod
    def type_name() -> str:
        return ActionType.MOVE_CAMERA

    def run(self, ctx: RunContext) -> None:
        if self.direction == "left":
            ic.mouse_look_left(pixels=self.pixels, duration=self.duration_s)
        else:
            ic.mouse_look_right(pixels=self.pixels, duration=self.duration_s)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type_name(),
            "direction": self.direction,
            "pixels": self.pixels,
            "duration_s": self.duration_s,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MoveCameraAction":
        return MoveCameraAction(
            direction=str(data["direction"]),
            pixels=int(data["pixels"]),
            duration_s=float(data["duration_s"]),
        )
