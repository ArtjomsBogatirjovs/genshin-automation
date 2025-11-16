from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Any, Type

from genshin_automation.core.context import RunContext

ACTION_REGISTRY: Dict[str, Type["Action"]] = {}


def register_action(cls: Type["Action"]) -> Type["Action"]:
    ACTION_REGISTRY[cls.type_name()] = cls
    return cls


class Action(ABC):

    @staticmethod
    @abstractmethod
    def type_name() -> str:
        ...

    @abstractmethod
    def run(self, ctx: RunContext) -> None:
        ...

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        ...

    @staticmethod
    @abstractmethod
    def from_dict(data: Dict[str, Any]) -> "Action":
        ...


class BaseTeleportAction(Action, ABC):

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.type_name()}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseTeleportAction":
        return cls()
