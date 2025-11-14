from dataclasses import dataclass
from typing import Dict, Any

from genshin_automation.actions.action_types import ActionType
from genshin_automation.actions.base import Action, register_action
from genshin_automation.core.context import RunContext
from genshin_automation.core.input_controller import click_percent


@register_action
@dataclass
class ClickPointAction(Action):
    x_frac: float
    y_frac: float

    @staticmethod
    def type_name() -> str:
        return ActionType.CLICK

    def run(self, ctx: RunContext) -> None:
        click_percent(ctx.window_rect, self.x_frac, self.y_frac)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type_name(),
            "x_frac": self.x_frac,
            "y_frac": self.y_frac,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ClickPointAction":
        return ClickPointAction(
            x_frac=float(data["x_frac"]),
            y_frac=float(data["y_frac"]),
        )
