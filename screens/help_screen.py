from rich.text import Text
from rich.style import Style
from render.window import WindowPanel, RowLayoutBuilder
from screens.base_screen import BaseScreen

from objects.player import Player
from objects.npc import NPC
from objects.block import Block
from objects.switch import Switch
from objects.door import Door
from objects.item import Item


class HelpScreen(BaseScreen):
    accept_commands = True
    accept_arrows = False

    def __init__(self):
        super().__init__()

        self.objects = [Player(), Block(), Switch(), Door(), Item(), NPC()]

    def _goal_text(self):
        txt = Text()
        txt.append("GOAL\n", Style(color="yellow", bold=True))
        txt.append(
            "Good evening, Detective Alice.\n\n"
            "As usual in this diminished city, another case has surfaced. A young woman has been found dead, and there is no one else to assign it to. You are the only detective willing to follow these threads to their end.\n\n"
            "This case feels different because of the weight it carries. Something about her death refuses to stay neatly filed away. Your task is simple in structure. Travel between regions, observe what remains, and collect the items tied to each place. Each one represents a piece of the process.\n\n"
            "The asylum, located to the north-center of the map, draws your attention more than the others. You feel its presence even from a distance. Still, something prevents you from entering it just yet. Perhaps certain matters must be addressed first.\n\n"
            "When all necessary evidence has been gathered, you may confront what waits there.\n\n"
            "Proceed carefully. This investigation is less about discovering new truths, and more about acknowledging the ones already in front of you."
        )
        return txt

    def _commands_text(self):
        txt = Text()

        commands = [
            ("north / n", "Move north"),
            ("south / s", "Move south"),
            ("west / w", "Move west"),
            ("east / e", "Move east"),
            ("enter", "Enter region"),
            ("help", "Show help screen"),
            ("quit", "Exit game"),
            ("style", "Cycle borders"),
        ]

        keybinds = [
            ("TAB", "Interact"),
            ("ESC", "Back to Overworld"),
            ("ARROWS", "Move player"),
            ("ENTER", "Enter Command"),
        ]

        txt.append("COMMANDS\n", Style(color="yellow", bold=True))
        for cmd, desc in commands:
            txt.append(f"  {cmd:<12}", Style(color="cyan", bold=True))
            txt.append(f" {desc}\n", Style(color="white"))
        txt.append("\nKEYBINDS\n", Style(color="yellow", bold=True))
        for keys, desc in keybinds:
            txt.append(f"  {keys:<12}", Style(color="cyan", bold=True))
            txt.append(f" {desc}\n", Style(color="white"))

        txt.append("\nLEGEND\n", Style(color="yellow", bold=True))
        for item in self.objects:
            txt.append(f"  {item.name:<12}", Style(color="cyan"))
            txt.append(f" {item.character}\n", Style(color=item.color))
        return txt

    def render(self):
        left = WindowPanel("[ GOAL ]", self._goal_text, border_style="bright_yellow")
        right = WindowPanel(
            "[ COMMANDS ]", self._commands_text, border_style="bright_cyan"
        )
        row = RowLayoutBuilder([left, right], ratios=[2, 1])
        return row.build()
