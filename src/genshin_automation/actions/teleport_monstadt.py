from abc import ABC, abstractmethod
from dataclasses import dataclass

from genshin_automation.actions.action_types import ActionType
from genshin_automation.actions.base import register_action, BaseTeleportAction
from genshin_automation.config import AFTER_TELEPORT_PAUSE, BETWEEN_CLICK_PAUSE
from genshin_automation.core.context import RunContext
from genshin_automation.core.input_controller import sleep, click_percent, click_to_teleport_button, open_map


class BaseTeleportMondstadtAction(BaseTeleportAction, ABC):

    @abstractmethod
    def after_focus_on_mondstadt(self, ctx: RunContext) -> None:
        ...

    def run(self, ctx: RunContext) -> None:
        open_map()

        click_percent(ctx.window_rect, 0.94, 0.94)
        sleep(BETWEEN_CLICK_PAUSE)

        click_percent(ctx.window_rect, 0.78, 0.1578)
        sleep(BETWEEN_CLICK_PAUSE)

        self.after_focus_on_mondstadt(ctx)
        sleep(BETWEEN_CLICK_PAUSE)

        click_to_teleport_button(ctx.window_rect)
        sleep(AFTER_TELEPORT_PAUSE)


@register_action
@dataclass
class TeleportMondstadtWindwailAction(BaseTeleportMondstadtAction):

    @staticmethod
    def type_name() -> str:
        return ActionType.TELEPORT_MONDSTADT_WINDWAIL

    def after_focus_on_mondstadt(self, ctx: RunContext) -> None:
        click_percent(ctx.window_rect, 0.438, 0.705)


@register_action
@dataclass
class TeleportMondstadtWolvendomAction(BaseTeleportMondstadtAction):

    @staticmethod
    def type_name() -> str:
        return ActionType.TELEPORT_MONDSTADT_WOLVENDOM

    def after_focus_on_mondstadt(self, ctx: RunContext) -> None:
        click_percent(ctx.window_rect, 0.428, 0.55)


@register_action
@dataclass
class TeleportMondstadtWindriseAction(BaseTeleportMondstadtAction):

    @staticmethod
    def type_name() -> str:
        return ActionType.TELEPORT_MONDSTADT_WINDRISE

    def after_focus_on_mondstadt(self, ctx: RunContext) -> None:
        click_percent(ctx.window_rect, 0.5785, 0.668)

@register_action
@dataclass
class TeleportMondstadtStormterrorLeft(BaseTeleportMondstadtAction):

    @staticmethod
    def type_name() -> str:
        return ActionType.TELEPORT_MONDSTADT_STORM_TERROR_LAIR_LEFT

    def after_focus_on_mondstadt(self, ctx: RunContext) -> None:
        click_percent(ctx.window_rect, 0.25, 0.35)