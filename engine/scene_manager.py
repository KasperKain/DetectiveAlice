# engine/scene_manager.py

from global_style import cycle_border
from screens.end_screen import EndingScreen
from screens.help_screen import HelpScreen
from screens.intro_screen import IntroScreen
from screens.localworld_screen import LocalworldScreen
from screens.overworld_screen import OverworldScreen


class SceneManager:

    def __init__(self, player, locations):
        self.player = player
        self.locations = locations
        self.screen = IntroScreen(change_scene_callback=self.change_scene)

    def get_screen(self):
        return self.screen

    def handle_command(self, cmd: str):
        cmd_lower = (cmd or "").strip().lower()
        if not cmd_lower:
            return

        # GLOBAL QUIT COMMAND
        if cmd_lower in ("quit", "exit"):
            print("\nExiting game…")
            self.screen.should_quit = True
            return

        if cmd_lower == "style":
            cycle_border()
            return

        if cmd_lower == "help" and isinstance(self.screen, OverworldScreen):
            self.screen = HelpScreen()
            return

        if hasattr(self.screen, "handle_command"):
            self.screen.handle_command(cmd)

    def change_scene(self, scene_name, new_pos=None):

        if scene_name == "ending":
            self.screen = EndingScreen()
            return

        if isinstance(self.screen, HelpScreen):
            self.screen = OverworldScreen(
                start_pos=self.player["position"],
                change_scene_callback=self.change_scene,
            )
            return

        if scene_name == "overworld":
            if new_pos is not None:
                self.player["position"] = new_pos
            self.screen = OverworldScreen(
                start_pos=self.player["position"],
                change_scene_callback=self.change_scene,
            )
            return

        if scene_name in self.locations:

            if new_pos is not None:
                self.player["position"] = new_pos
            self.screen = LocalworldScreen(
                map_file=f"map/maps/{scene_name}.txt",
                change_scene_callback=self.change_scene,
            )
            return
