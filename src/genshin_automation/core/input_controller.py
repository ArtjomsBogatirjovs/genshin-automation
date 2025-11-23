import string
import time
from typing import Tuple

import pyautogui
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


def hold_right_click() -> None:
    pydirectinput.mouseDown(button="right")


def up_right_click() -> None:
    pydirectinput.mouseUp(button="right")


def click_percent(rect: Tuple[int, int, int, int], x_frac: float, y_frac: float) -> None:
    x, y = get_x_y(rect, x_frac, y_frac)
    click(x, y)


def move_mouse_to_cord(x: int, y: int) -> None:
    pydirectinput.moveTo(x, y)


def move_mouse_to(rect: Tuple[int, int, int, int], x_frac: float, y_frac: float) -> None:
    x, y = get_x_y(rect, x_frac, y_frac)
    move_mouse_to_cord(x, y)


def get_x_y(rect: Tuple[int, int, int, int], x_frac: float, y_frac: float) -> Tuple[int, int]:
    left, top, width, height = rect
    x = int(left + x_frac * width)
    y = int(top + y_frac * height)
    return x, y


def scroll_down() -> None:
    scroll(-1)


def scroll_up() -> None:
    scroll(1)


def scroll(clicks: int) -> None:
    pyautogui.scroll(clicks)


def click_to_teleport_button(rect: Tuple[int, int, int, int]) -> None:
    click_percent(rect, 0.88, 0.93)


def open_map() -> None:
    key_press("m")
    sleep(1.0)


def type_text(text: str) -> None:
    if not text:
        return
    for ch in text:
        if ch in string.ascii_uppercase:
            pydirectinput.keyDown("shift")
            pydirectinput.press(ch.lower())
            pydirectinput.keyUp("shift")
        else:
            pydirectinput.press(ch)


def move_camera_horizontal(
        rect: Tuple[int, int, int, int],
        start_x_frac: float,
        start_y_frac: float,
        right: bool,
) -> None:
    left, top, width, height = rect

    start_x, start_y = get_x_y(rect, start_x_frac, start_y_frac)

    delta_x = int(0.8 * width)
    if not right:
        delta_x = -delta_x
    pydirectinput.moveTo(start_x, start_y)
    time.sleep(0.01)

    pydirectinput.mouseDown()
    try:
        steps = 10
        step_dx = delta_x / steps

        for _ in range(steps):
            pydirectinput.moveRel(int(step_dx), 0)
    finally:
        pydirectinput.mouseUp()
