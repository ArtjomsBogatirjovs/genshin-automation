from dataclasses import dataclass
from typing import Dict, Any

from genshin_automation.actions.action_types import ActionType
from genshin_automation.actions.base import Action, register_action
from genshin_automation.core.context import RunContext
from genshin_automation.core.input_controller import key_down, sleep, key_up

DIRECTION_TO_KEY = {
    "forward": "w",
    "backward": "s",
    "left": "a",
    "right": "d",
}


@register_action
@dataclass
class MoveAction(Action):
    direction: str
    duration_s: float

    @staticmethod
    def type_name() -> str:
        return ActionType.MOVE

    def run(self, ctx: RunContext) -> None:
        key = DIRECTION_TO_KEY.get(self.direction, "w")
        key_down(key)
        try:
            sleep(self.duration_s)
        finally:
            key_up(key)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type_name(),
            "direction": self.direction,
            "duration_s": self.duration_s,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MoveAction":
        return MoveAction(
            direction=str(data["direction"]),
            duration_s=float(data["duration_s"]),
        )


@register_action
@dataclass
class RunAction(Action):
    direction: str
    duration_s: float

    @staticmethod
    def type_name() -> str:
        return ActionType.RUN

    def run(self, ctx: RunContext) -> None:
        key = DIRECTION_TO_KEY.get(self.direction, "w")
        key_down(key)
        key_down("shift")
        try:
            sleep(self.duration_s)
        finally:
            key_up("shift")
            key_up(key)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type_name(),
            "direction": self.direction,
            "duration_s": self.duration_s,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "RunAction":
        return RunAction(
            direction=str(data["direction"]),
            duration_s=float(data["duration_s"]),
        )
