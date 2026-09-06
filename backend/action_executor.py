# TODO (from PLAN.pdf Section 5/9 - orb/Windows side, not Team 1's scope)
#
# Interface first, FakeActionExecutor for Linux dev, WindowsActionExecutor
# (pyautogui) built later by whoever tests on Windows.

class ActionExecutor:
    def click(self, x: int, y: int) -> None:
        raise NotImplementedError

    def type_text(self, text: str) -> None:
        raise NotImplementedError

    def open_app(self, name: str) -> None:
        raise NotImplementedError

    def screenshot(self) -> bytes:
        raise NotImplementedError


class FakeActionExecutor(ActionExecutor):
    """Logs calls instead of executing them - what you develop/test against."""

    def click(self, x: int, y: int) -> None:
        print(f"[FAKE] click({x}, {y})")

    def type_text(self, text: str) -> None:
        print(f"[FAKE] type_text({text!r})")

    def open_app(self, name: str) -> None:
        print(f"[FAKE] open_app({name!r})")

    def screenshot(self) -> bytes:
        print("[FAKE] screenshot()")
        return b""
