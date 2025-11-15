from dataclasses import dataclass
from typing import Dict, Any, Literal

from genshin_automation.actions.action_types import ActionType
from genshin_automation.actions.base import Action, register_action
from genshin_automation.core import input_controller as ic
from genshin_automation.core.context import RunContext

Direction = Literal["left", "right"]


@register_action
@dataclass
class MoveCameraAction(Action):
    direction: Direction
    iterations: int = 1

    @staticmethod
    def type_name() -> str:
        return ActionType.MOVE_CAMERA

    def run(self, ctx: RunContext) -> None:
        ic.key_down("alt")
        ic.sleep(0.1)

        start_x_frac = 0.1
        if self.direction == "left":
            start_x_frac = 0.9

        iterations = max(1, self.iterations)

        for _ in range(iterations):
            ic.move_camera_horizontal(
                rect=ctx.window_rect,
                start_x_frac=start_x_frac,
                start_y_frac=0.65,
                right=self.direction == "right",
            )
            ic.sleep(0.05)
        ic.key_up("alt")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type_name(),
            "direction": self.direction,
            "iterations": self.iterations,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MoveCameraAction":
        return MoveCameraAction(
            direction=str(data["direction"]),
            iterations=int(data.get("iterations", 1))
        )
