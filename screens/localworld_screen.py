import json
import time
import random
from rich.text import Text

from engine.audio_manager import AudioManager
from engine.game_state import GameState
from engine.loader import ObjectLoader
from engine.movement import attempt_move
from render.renderer import render_world
from render.window import WindowPanel, RowLayoutBuilder
from screens.base_screen import BaseScreen
from world.game_world import GameWorld
from world.map_loader import load_map
from utils.paths import resource_path

from render.effects_manager import (
    conceal_collapse,
    conceal_glitch,
    conceal_sprinkle,
    dim_glitch,
    full_map_alice,
    full_map_glitch,
    full_map_help_me,
    letter_glitch,
    line_glitch,
    red_glitch,
    skull_sprinkle,
)

from objects.item import Item
from objects.switch import Switch
from objects.door import Door

CHARA_FILE = "chara.json"


class LocalworldScreen(BaseScreen):
    accept_arrows = True
    accept_commands = False

    def __init__(self, map_file, change_scene_callback):
        super().__init__()

        self.map_file = map_file
        self.change_scene = change_scene_callback
        self.freeze_player = False
        self.debug_text = ""
        self.base_text = ""

        AudioManager.stop_music(fade_ms=1000)

        base_grid = load_map(map_file)

        with open(resource_path(CHARA_FILE), "r", encoding="utf-8") as f:
            char_defs = json.load(f)

        registry, player = ObjectLoader.load_objects(base_grid, char_defs)

        self.world = GameWorld(base_grid)

        for obj in registry.all_objects():
            self.world.add_object(obj)

        if not player:
            raise ValueError("No '@' found in map!")

        self.player = player
        self.pending_scene = None
        self.end_timer_start = None
        self.is_ending = False

        self._last_effect_time = time.time()
        self.min_effect_interval = 45
        self.max_effect_interval = 120

        self.is_asylum = "asylum" in self.map_file.lower()

        if self.is_asylum:
            self.min_effect_interval = 3
            self.max_effect_interval = 5

        self._effect_interval = random.uniform(
            self.min_effect_interval, self.max_effect_interval
        )

        # Asylum door logic
        if self.is_asylum:
            gs = GameState()

            if gs.check_all_items_collected():
                for obj in self.world.objects:
                    if isinstance(obj, Door):
                        obj.open(self.world, False)

                self._effect_interval = random.uniform(1000, 2000)

    # Update loop
    def update_objects(self):
        # Update world objects
        for obj in list(self.world.objects):
            if obj is self.player:
                continue
            obj.update(self.world)

        if self.pending_scene and self.end_timer_start:
            delay = 7 if self.is_ending else 3
            if time.time() - self.end_timer_start >= delay:
                scene_name, new_pos = self.pending_scene
                self.pending_scene = None
                self.change_scene(scene_name, new_pos)

        switches = [o for o in self.world.objects if isinstance(o, Switch)]
        if switches and all(s.triggered for s in switches):
            for door in [o for o in self.world.objects if isinstance(o, Door)]:
                door.open(self.world)

        self.world.update_effects()

        now = time.time()
        if now - self._last_effect_time >= self._effect_interval:
            self._last_effect_time = now
            self._effect_interval = random.uniform(
                self.min_effect_interval, self.max_effect_interval
            )

            # Doubling up message for redundancy
            if self.is_asylum and not self.is_ending:
                self.world.trigger_effect(
                    conceal_sprinkle,
                    duration=5,
                    message="TURN BACK\n\nSomething is wrong...",
                )
                self.world.trigger_effect(
                    skull_sprinkle,
                    duration=2,
                    message="TURN BACK\n\nSomething is wrong...",
                )
            elif not self.is_asylum:
                effect = random.choice(
                    [
                        conceal_sprinkle,
                        conceal_glitch,
                        full_map_glitch,
                        full_map_help_me,
                        dim_glitch,
                        red_glitch,
                        letter_glitch,
                        line_glitch,
                        conceal_glitch,
                        full_map_alice,
                    ]
                )
                self.world.trigger_effect(
                    effect,
                    duration=2,
                    message="Something feels strange...",
                )

    def update(self):
        self.update_objects()

    def handle_arrow(self, direction):
        if self.freeze_player:
            return
        attempt_move(self.world, self.player, direction)

    def interact(self):
        for obj in self.world.get_adjacent_objects(self.player):
            if hasattr(obj, "interact"):
                if isinstance(obj, Item):
                    obj.interact(self.player, self)
                else:
                    obj.interact(self.player, self.world)

    def end_level(self, item_name=""):
        self.accept_arrows = False
        self.freeze_player = True

        scene_name = self.map_file.split("/")[-1].removesuffix(".txt")

        gs = GameState()
        gs.add_collected_item(item_name, scene_name)
        gs.complete_map(scene_name)

        self.world.collapse_start_time = time.time()

        self.world.trigger_effect(
            conceal_collapse,
            duration=7.0,
            message="",
        )

        self.pending_scene = ("overworld", None)
        self.end_timer_start = time.time()

    def end_game_sequence(self):
        self.is_ending = True
        self.accept_arrows = False
        self.freeze_player = True

        self.world.collapse_start_time = time.time()

        self.world.trigger_effect(
            conceal_collapse,
            duration=7.0,
            message="",
        )

        self.pending_scene = ("ending", None)
        self.end_timer_start = time.time()

    def get_info_text(self):
        region_text = self.map_file.replace("map/maps/", "").replace(".txt", "")
        self.base_text = ""

        if region_text == "station":
            self.base_text += "Use arrow keys to move\n\n"

        if not self.is_asylum:
            self.base_text += "REGION: " + region_text.capitalize() + "\n"
            self.base_text += "POSITION: " + f"{self.player.position}" + "\n"

            locked_doors = "Open"
            switches_remaining = 0
            switches = [o for o in self.world.objects if isinstance(o, Switch)]
            switches_remaining = len([s for s in switches if s.triggered == False])
            if switches and all(s.triggered for s in switches):
                locked_doors = "Open"
            elif not switches:
                locked_doors = "Open"
            else:
                locked_doors = "Locked"
            self.base_text += "DOORS: " + locked_doors + "\n"
            self.base_text += "SWITCHES: " + f"{switches_remaining}" + "\n"
        txt = Text(style="bold white")

        msg = self.world.info_message
        if msg:
            txt.append(msg + "\n", style="magenta bold")
            return txt

        txt.append(self.base_text + "\n", style="blue")

        for name, dialogue in self.player.get_adjacent_speech(self.world):
            txt.set_length(0)
            txt.append(f"[ {name.upper()} ]\n", style="yellow bold")
            txt.append(f"{dialogue}\n", style="cyan")

        if self.debug_text:
            txt.append("\n" + self.debug_text + "\n", style="red bold")
        return txt

    def render(self):
        map_panel = WindowPanel(
            "[ GAME MAP ]",
            lambda: render_world(self.world, self.player),
            border_style="blue",
        )
        info_panel = WindowPanel(
            "[ INFORMATION ]",
            self.get_info_text,
            border_style="green",
        )
        builder = RowLayoutBuilder([info_panel, map_panel], ratios=[1, 3])
        return builder.build()

    def manual_effect_trigger(self):
        effect = random.choice(
            [
                dim_glitch,
                red_glitch,
                letter_glitch,
                line_glitch,
                full_map_glitch,
                conceal_sprinkle,
                conceal_glitch,
                full_map_help_me,
                full_map_alice,
            ]
        )
        self.world.trigger_effect(
            effect,
            duration=2,
            message="You pressed the bad key...!",
        )
