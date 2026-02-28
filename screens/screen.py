from typing import Text
from render.window import RowLayoutBuilder, WindowPanel


class ScreenBase:
    accept_commands = True
    accept_arrows = False

    def __init__(self, screens=None):

        # Unused fallback. Keeping it here just incase.
        if screens is None:
            screens = [
                {"name": "Map", "ratio": 3, "render_func": lambda: Text("No map")},
                {"name": "Info", "ratio": 1, "render_func": lambda: Text("No info")},
            ]
        self.screens = screens
        self.selected_region = [0, 0]

    def render(self):
        panels = []
        for screen in self.screens:
            panels.append(
                WindowPanel(
                    f"[ {screen['name']} ]",
                    screen.get("render_func", lambda: Text("No content")),
                    border_style="bright_yellow",
                )
            )
        builder = RowLayoutBuilder(panels, ratios=[s["ratio"] for s in self.screens])
        return builder.build()
