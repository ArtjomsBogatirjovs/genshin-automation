from dataclasses import dataclass
from typing import Dict, Any

from genshin_automation.actions.base import Action, register_action
from genshin_automation.actions.action_types import ActionType
from genshin_automation.core.context import RunContext
from genshin_automation.core.input_controller import sleep


@register_action
@dataclass
class WaitAction(Action):
    duration_s: float = 1.0

    @staticmethod
    def type_name() -> str:
        return ActionType.WAIT

    def run(self, ctx: RunContext) -> None:
        sleep(self.duration_s)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type_name(),
            "duration_s": self.duration_s,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "WaitAction":
        return WaitAction(duration_s=float(data.get("duration_s", 1.0)))
