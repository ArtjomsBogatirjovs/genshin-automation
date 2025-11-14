import time
from typing import Tuple
import pydirectinput

def click(x: int, y: int) -> None:
    pydirectinput.click(x, y)

def key_press(key: str) -> None:
    pydirectinput.press(key)

def key_down(key: str):
    pydirectinput.keyDown(key)

def key_up(key: str):
    pydirectinput.keyUp(key)

def sleep(seconds: float) -> None:
    time.sleep(seconds)


def click_percent(rect: Tuple[int, int, int, int], x_frac: float, y_frac: float) -> None:
    left, top, width, height = rect
    x = int(left + x_frac * width)
    y = int(top + y_frac * height)
    click(x, y)

def click_to_teleport_button(rect: Tuple[int, int, int, int]) -> None:
    click_percent(rect, 0.88, 0.93)

# -------------------------
# Smooth mouse movement (relative)
# -------------------------

def move_mouse_relative_smooth(
        delta_x: int,
        delta_y: int = 0,
        duration: float = 0.2,
        steps: int = 30,
) -> None:
    """
    Smooth relative mouse movement by (delta_x, delta_y) using moveRel.
    """
    steps = max(1, steps)
    step_delay = duration / steps

    step_dx = delta_x / steps
    step_dy = delta_y / steps

    for _ in range(steps):
        pydirectinput.moveRel(step_dx, step_dy)
        time.sleep(step_delay)


def mouse_look_left(pixels: int = 200, duration: float = 0.15) -> None:
    """
    Rotate camera left by moving mouse left (no buttons).
    """
    move_mouse_relative_smooth(delta_x=-abs(pixels), duration=duration)


def mouse_look_right(pixels: int = 200, duration: float = 0.15) -> None:
    """
    Rotate camera right by moving mouse right (no buttons).
    """
    move_mouse_relative_smooth(delta_x=abs(pixels), duration=duration)
