# src/genshin_automation/core/route.py
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Type

from genshin_automation.actions.base import Action, ACTION_REGISTRY
from genshin_automation.core.context import RunContext


@dataclass
class Route:
    name: str
    actions: List[Action] = field(default_factory=list)

    def run(self, ctx: RunContext) -> None:
        for action in self.actions:
            action.run(ctx)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "actions": [a.to_dict() for a in self.actions],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Route":
        actions: List[Action] = []
        for a_data in data["actions"]:
            type_name = a_data["type"]
            action_cls: Type[Action] = ACTION_REGISTRY[type_name]
            actions.append(action_cls.from_dict(a_data))
        return cls(name=data["name"], actions=actions)


def save_route(route: Route, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(route.to_dict(), f, ensure_ascii=False, indent=2)


def load_route(path: Path) -> Route:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return Route.from_dict(data)
