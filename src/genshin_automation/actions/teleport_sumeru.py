from abc import abstractmethod, ABC
from dataclasses import dataclass

from genshin_automation.actions.action_types import ActionType
from genshin_automation.actions.base import BaseTeleportAction, register_action
from genshin_automation.config import AFTER_TELEPORT_PAUSE
from genshin_automation.core.context import RunContext
from genshin_automation.core.input_controller import open_map, click_percent, sleep, click_to_teleport_button


class BaseTeleportSumeruAction(BaseTeleportAction, ABC):

    @abstractmethod
    def after_focus_on_sumeru(self, ctx: RunContext) -> None:
        ...

    def run(self, ctx: RunContext) -> None:
        open_map()

        click_percent(ctx.window_rect, 0.94, 0.94)
        sleep(1)

        click_percent(ctx.window_rect, 0.9, 0.255)
        sleep(1)

        self.after_focus_on_sumeru(ctx)
        sleep(1)

        click_to_teleport_button(ctx.window_rect)
        sleep(AFTER_TELEPORT_PAUSE)


@register_action
@dataclass
class TeleportAvidyaForestUpAction(BaseTeleportSumeruAction):

    @staticmethod
    def type_name() -> str:
        return ActionType.TELEPORT_AVIDYA_FOREST_UP

    def after_focus_on_sumeru(self, ctx: RunContext) -> None:
        click_percent(ctx.window_rect, 0.5469, 0.59)
