from dataclasses import dataclass
from typing import Tuple


@dataclass
class RunContext:
    window_rect: Tuple[int, int, int, int]
    resolution: Tuple[int, int]
