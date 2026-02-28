import os
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich import box

from global_style import get_border

console = Console()
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 30


# Prevent user from downsizing window
def too_small_panel():
    try:
        tw, th = os.get_terminal_size()
    except OSError:
        tw, th = 80, 24

    if tw < SCREEN_WIDTH or th < SCREEN_HEIGHT:
        return Panel(
            f"Terminal too small!\n\nRequired: {SCREEN_WIDTH}x{SCREEN_HEIGHT}\nCurrent: {tw}x{th}",
            box=box.DOUBLE,
            border_style="red",
            padding=(1, 2),
        )
    return None


class WindowPanel:
    def __init__(
        self, name, render_callback=None, border_style="white", panel_box=None
    ):
        self.name = name
        self.render_callback = render_callback or (lambda: "")
        self.border_style = border_style
        self.box = panel_box

    def render(self):
        return Panel(
            self.render_callback(),
            border_style=self.border_style,
            subtitle=self.name,
            title=self.name,
            box=self.box or get_border(),  # Fixes crashing
            padding=(1, 2),
            expand=True,
            title_align="center",
            subtitle_align="center",
        )


class RowLayoutBuilder:
    def __init__(self, panels, ratios=None):
        self.panels = panels
        self.ratios = ratios or [1] * len(panels)

    def build(self):

        small = too_small_panel()
        if small:
            return small
        layout = Layout()
        layout.split_row(
            *[Layout(name=p.name, ratio=r) for p, r in zip(self.panels, self.ratios)]
        )
        for panel in self.panels:
            layout[panel.name].update(panel.render())

        root_panel = Panel(
            layout,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            box=box.ROUNDED,  # outermost border stays simple.
            border_style="white",
        )
        return root_panel
