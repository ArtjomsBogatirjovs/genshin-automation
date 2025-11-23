from dataclasses import dataclass
from typing import Callable, List, Optional

from genshin_automation.actions.promo_codes import PromoCodesAction
from genshin_automation.core.route import Route


@dataclass(frozen=True)
class BuiltinRouteDef:
    id: str
    display_name: str
    factory: Callable[[], Route]


def _build_promo_codes_route() -> Route:
    actions = [
        PromoCodesAction(),
    ]
    return Route(name="promo_codes", actions=actions)


_BUILTIN_ROUTES: List[BuiltinRouteDef] = [
    BuiltinRouteDef(
        id="promo_codes",
        display_name="Promo codes input",
        factory=_build_promo_codes_route,
    ),
]


def list_display_names() -> list[str]:
    return [r.display_name for r in _BUILTIN_ROUTES]


def find_by_display_name(name: str) -> Optional[BuiltinRouteDef]:
    for r in _BUILTIN_ROUTES:
        if r.display_name == name:
            return r
    return None


def build_route_by_display_name(name: str) -> Route:
    route_def = find_by_display_name(name)
    if route_def is None:
        raise ValueError(f"Unknown built-in route: {name}")
    return route_def.factory()
