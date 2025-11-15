from dataclasses import dataclass
from typing import Dict, Any

from genshin_automation.actions.action_types import ActionType
from genshin_automation.actions.base import Action, register_action
from genshin_automation.config import AFTER_TELEPORT_PAUSE
from genshin_automation.core.context import RunContext
from genshin_automation.core.input_controller import key_press, sleep, click_percent, click_to_teleport_button


@register_action
@dataclass
class TeleportMondstadtWindwailAction(Action):

    @staticmethod
    def type_name() -> str:
        return ActionType.TELEPORT_MONDSTADT_WINDWAIL

    def run(self, ctx: RunContext) -> None:
        key_press("m")
        sleep(1)

        click_percent(ctx.window_rect, 0.94, 0.94)
        sleep(1)

        click_percent(ctx.window_rect, 0.78, 0.2)
        sleep(1)

        click_percent(ctx.window_rect, 0.422, 0.757)
        sleep(1)

        click_to_teleport_button(ctx.window_rect)
        sleep(AFTER_TELEPORT_PAUSE)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type_name(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "TeleportMondstadtWindwailAction":
        return TeleportMondstadtWindwailAction()
