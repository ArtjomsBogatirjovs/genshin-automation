from dataclasses import dataclass
from typing import Dict, Any, List

from genshin_automation.actions.action_types import ActionType
from genshin_automation.actions.base import Action, register_action
from genshin_automation.config import BETWEEN_CLICK_PAUSE
from genshin_automation.core.context import RunContext
from genshin_automation.core.input_controller import key_press, sleep, click_percent, type_text
from genshin_automation.core.paths import PROMO_CODES_FILE, PROMO_ACTIVATED_CODES_FILE


def _ensure_activated_file_exists() -> None:
    PROMO_ACTIVATED_CODES_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not PROMO_ACTIVATED_CODES_FILE.exists():
        PROMO_ACTIVATED_CODES_FILE.touch()


def _load_promo_codes() -> List[str]:
    if not PROMO_CODES_FILE.exists():
        return []

    codes: List[str] = []
    with PROMO_CODES_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            raw = line.strip()
            if not raw:
                continue
            if raw.startswith("#"):
                continue
            codes.append(raw)
    return codes


def _load_activated() -> set[str]:
    try:
        return {
            line.strip()
            for line in PROMO_ACTIVATED_CODES_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
    except FileNotFoundError:
        return set()


@register_action
@dataclass
class PromoCodesAction(Action):
    def __init__(self):
        _ensure_activated_file_exists()
        self._activated = _load_activated()
        self._codes = _load_promo_codes()

    @staticmethod
    def type_name() -> str:
        return ActionType.PROMO_CODES

    def run(self, ctx: RunContext) -> None:
        if not self._codes:
            return
        key_press("esc")
        sleep(BETWEEN_CLICK_PAUSE * 5)
        click_percent(ctx.window_rect, 0.0465, 0.76)
        sleep(BETWEEN_CLICK_PAUSE * 5)
        click_percent(ctx.window_rect, 0.07, 0.53)
        sleep(BETWEEN_CLICK_PAUSE)

        for code in self._codes:
            if self.is_activated(code):
                continue
            click_percent(ctx.window_rect, 0.915, 0.26)
            sleep(BETWEEN_CLICK_PAUSE)
            click_percent(ctx.window_rect, 0.45, 0.475)
            sleep(BETWEEN_CLICK_PAUSE)
            type_text(code)
            sleep(BETWEEN_CLICK_PAUSE)
            click_percent(ctx.window_rect, 0.523, 0.68)
            sleep(5)
            click_percent(ctx.window_rect, 0.5, 0.725)
            sleep(BETWEEN_CLICK_PAUSE)
            key_press("esc")
            sleep(BETWEEN_CLICK_PAUSE)
            self.mark_activated(code)

        key_press("esc")
        sleep(BETWEEN_CLICK_PAUSE * 5)
        key_press("esc")

    def mark_activated(self, code: str) -> None:
        if code not in self._activated:
            self._activated.add(code)
            PROMO_ACTIVATED_CODES_FILE.write_text(
                "\n".join(sorted(self._activated)),
                encoding="utf-8"
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type_name(),
        }

    def is_activated(self, code: str) -> bool:
        return code in self._activated

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PromoCodesAction":
        return PromoCodesAction()
