from typing import Tuple, List

import pyautogui
import pygetwindow as gw

_GI_KEYWORDS = ["Genshin Impact"]


def _matches_genshin(title: str) -> bool:
    return any(k in title for k in _GI_KEYWORDS)

class GameWindow:
    def __init__(self, title: str | None = None):
        self.title = title or ""
        self._window: gw.Win32Window | None = None

    @staticmethod
    def list_candidate_titles() -> List[str]:
        titles: list[str] = []
        for w in gw.getAllWindows():
            title = (w.title or "").strip()
            if not title:
                continue
            if title == "Genshin Impact":
                return [title]
            if _matches_genshin(title):
                if title not in titles:
                    titles.append(title)
        return titles

    def _find_window(self) -> None:
        if not self.title:
            return
        for w in gw.getAllWindows():
            title = (w.title or "").strip()
            if title == self.title:
                self._window = w
                return

    def find_and_focus(self) -> None:
        if self._window is None:
            self._find_window()
        if self._window is None:
            return
        try:
            self._window.activate()
        except Exception:
            pass

    def get_rect(self) -> Tuple[int, int, int, int]:
        if self._window is None:
            self._find_window()
        if self._window is not None:
            try:
                return (
                    self._window.left,
                    self._window.top,
                    self._window.width,
                    self._window.height,
                )
            except Exception:
                pass

        width, height = pyautogui.size()
        return 0, 0, width, height
