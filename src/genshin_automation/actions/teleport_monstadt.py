from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any

from genshin_automation.actions.action_types import ActionType
from genshin_automation.actions.base import Action, register_action
from genshin_automation.config import AFTER_TELEPORT_PAUSE
from genshin_automation.core.context import RunContext
from genshin_automation.core.input_controller import sleep, click_percent, click_to_teleport_button, open_map


class BaseTeleportMondstadtAction(Action, ABC):

    @staticmethod
    @abstractmethod
    def type_name() -> str:
        ...

    @abstractmethod
    def after_focus_on_mondstadt(self, ctx: RunContext) -> None:
        ...

    def run(self, ctx: RunContext) -> None:
        open_map()

        click_percent(ctx.window_rect, 0.94, 0.94)
        sleep(1)

        click_percent(ctx.window_rect, 0.78, 0.2)
        sleep(1)

        self.after_focus_on_mondstadt(ctx)
        sleep(1)

        click_to_teleport_button(ctx.window_rect)
        sleep(AFTER_TELEPORT_PAUSE)

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.type_name()}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseTeleportMondstadtAction":
        return cls()


@register_action
@dataclass
class TeleportMondstadtWindwailAction(BaseTeleportMondstadtAction):

    @staticmethod
    def type_name() -> str:
        return ActionType.TELEPORT_MONDSTADT_WINDWAIL

    def after_focus_on_mondstadt(self, ctx: RunContext) -> None:
        click_percent(ctx.window_rect, 0.438, 0.705)
        sleep(1)


@register_action
@dataclass
class TeleportMondstadtWolvendomAction(BaseTeleportMondstadtAction):

    @staticmethod
    def type_name() -> str:
        return ActionType.TELEPORT_MONDSTADT_WOLVENDOM

    def after_focus_on_mondstadt(self, ctx: RunContext) -> None:
        click_percent(ctx.window_rect, 0.428, 0.55)
        sleep(1)
