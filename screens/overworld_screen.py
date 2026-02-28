import json
import inspect
from rich.text import Text
from rich.style import Style

from engine.audio_manager import AudioManager
from engine.game_state import GameState
from render.renderer import render_overworld
from render.window import WindowPanel, RowLayoutBuilder
from screens.base_screen import BaseScreen
from global_style import get_border
from utils.paths import resource_path

DEFAULT_ASCII_MAP = "map/maps/overworld.txt"
DESC_FILE = "desc.json"


class OverworldScreen(BaseScreen):
    accept_commands = True

    def __init__(
        self,
        start_pos=(0, 0),
        desc_file=DESC_FILE,
        change_scene_callback=None,
    ):
        super().__init__()
        self.debug_text = ""
        self.change_scene = change_scene_callback
        AudioManager.play_music(
            resource_path("audio/bg_music.wav"), volume=0.8, loops=-1
        )

        # debug string to display in the info panel
        self.debug_info = f"OverworldScreen loaded from: {inspect.getfile(type(self))}"

        with open(resource_path(DEFAULT_ASCII_MAP), "r", encoding="utf-8") as f:
            self.map_grid = [list(line.rstrip("\n")) for line in f.readlines()]

        # Load region descriptions. Should work correctly now
        with open(resource_path(desc_file), "r", encoding="utf-8") as f:
            self.descriptions = json.load(f)

            self.key_map = {
                key.lower().replace(" ", "_"): key for key in self.descriptions.keys()
            }

            keys = list(self.key_map.keys())
            self.grid_size = int(len(keys) ** 0.5 + 0.999)

            self.region_grid = [
                keys[i * self.grid_size : (i + 1) * self.grid_size]
                for i in range(self.grid_size)
            ]

        # Selected region start position. Should probably keep it centered.
        self.selected_region = [
            min(start_pos[0], self.grid_size - 1),
            min(start_pos[1], self.grid_size - 1),
        ]

        self.command_buffer = ""

    # ----- movement via commands -----
    def handle_command(self, cmd: str):
        cmd = (cmd or "").strip().lower()
        self.last_command = cmd

        if cmd in ("north", "n"):
            self.selected_region[0] = max(0, self.selected_region[0] - 1)
            AudioManager.play("arrow", 0.3)
        elif cmd in ("south", "s"):
            self.selected_region[0] = min(
                self.grid_size - 1, self.selected_region[0] + 1
            )
            AudioManager.play("arrow", 0.3)
        elif cmd in ("west", "w"):
            self.selected_region[1] = max(0, self.selected_region[1] - 1)
            AudioManager.play("arrow", 0.3)
        elif cmd in ("east", "e"):
            self.selected_region[1] = min(
                self.grid_size - 1, self.selected_region[1] + 1
            )
            AudioManager.play("arrow", 0.3)
        elif cmd == "enter":
            self._enter_region()

        elif cmd == "quit":
            self.should_quit = True
        # "help" handled globally by SceneManager. Sloppy solution but it works
        elif cmd == "debug_all_items":
            gs = GameState()
            gs.reset()

            for i in range(7):
                item_name = f"Item {i + 1}"
                location = f"debug_{i + 1}"
                gs.add_collected_item(item_name, location)

            self.debug_text = "[DEBUG] Full item set"
        elif cmd == "debug":
            gs = GameState()
            gs.enable_debug()
            self.debug_text = "[DEBUG] Wall collisions disabled"

    def _enter_region(self):
        y, x = self.selected_region
        raw = self.region_grid[y][x]
        region_name = raw.lower().replace(" ", "_")

        gs = GameState()
        region_key = (
            region_name.removesuffix(".txt")
            if region_name.endswith(".txt")
            else region_name
        )

        # If an item is already collected, the region should be locked.
        if any(
            item["location"].lower() == region_key for item in gs.get_collected_items()
        ):
            self.last_command = f"Item already collected in {region_key}."
            return
        if self.change_scene:
            self.debug_text = f"Entering region: {region_name}"
            self.change_scene(region_name, self.selected_region)

    def add_char_to_buffer(self, ch: str):
        if ch == "\x7f":
            self.command_buffer = self.command_buffer[:-1]
        else:
            self.command_buffer += ch

    def _get_current_description(self):
        y, x = self.selected_region
        try:
            loc_name = self.region_grid[y][x]
        except IndexError:
            return "Unknown region."

        gs = GameState()
        region_key = loc_name.lower().removesuffix(".txt")

        for item in gs.get_collected_items():
            if item["location"].lower() == region_key:
                return "Item collected in this region!"

        original_key = self.key_map.get(loc_name)
        if not original_key:
            return "No description available for this area."  # If this prints, something is wrong

        return self.descriptions.get(original_key, "No description available.")

    def get_info_text(self):
        gs = GameState()
        txt = Text(style="bold white")

        txt.append(
            f"{self._get_current_description()}\n",
            style=Style(color="yellow", italic=True),
        )

        txt.append(
            "\nCOMMANDS: north, east, south, west, enter, quit, help, style\n",
            style="bold green",
        )

        txt.append(
            f"> {self.command_buffer}\n",
            style=Style(color="white", italic=True, bold=True),
        )

        txt.append(self.debug_text, style="bold cyan")
        collected = gs.get_collected_items()
        if not collected:
            txt.append("\n(no items)\n", style="dim")
        else:
            txt.append("\n")
            for item in collected:
                txt.append(f"  • {item['name']}\n", style="white bold")
        return txt

    def render(self):
        border = get_border()
        map_panel = WindowPanel(
            "[ WORLD MAP ]",
            lambda: render_overworld(
                self.map_grid, self.selected_region, self.grid_size, self.grid_size
            ),
            border_style="bright_blue",
            panel_box=border,
        )
        info_panel = WindowPanel(
            "[ INFORMATION ]",
            self.get_info_text,
            border_style="green",
            panel_box=border,
        )
        builder = RowLayoutBuilder([map_panel, info_panel], ratios=[3, 1])
        return builder.build()
