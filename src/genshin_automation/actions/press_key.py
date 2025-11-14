from dataclasses import dataclass
from typing import Dict, Any

from genshin_automation.actions.action_types import ActionType
from genshin_automation.actions.base import Action, register_action
from genshin_automation.core.context import RunContext
from genshin_automation.core.input_controller import key_press


@register_action
@dataclass
class PressKeyAction(Action):
    key: str

    @staticmethod
    def type_name() -> str:
        return ActionType.PRESS

    def run(self, ctx: RunContext) -> None:
        key_press(self.key)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type_name(),
            "key": self.key,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PressKeyAction":
        return PressKeyAction(key=str(data["key"]))
