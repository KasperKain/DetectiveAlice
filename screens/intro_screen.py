import os
import time
from utils.paths import resource_path
from render.renderer import render_intro
from render.window import WindowPanel, RowLayoutBuilder
from screens.base_screen import BaseScreen


class IntroScreen(BaseScreen):
    accept_any = True

    FRAME_DELAY = 0.1

    def __init__(self, change_scene_callback):
        super().__init__()
        self.change_scene = change_scene_callback

        base_path = os.path.join("map", "maps", "frames")
        self.frames = []
        for i in range(8):
            file_path = os.path.join(base_path, f"intro_{i}.txt")
            with open(resource_path(file_path), "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
                if lines:
                    self.frames.append(lines)

        if not self.frames:
            raise ValueError("No intro frames found!")

        self.index = 0
        self.last_time = time.time()
        self.finished = False

    def update(self):
        if self.finished:
            return

        now = time.time()
        if now - self.last_time > self.FRAME_DELAY:
            self.last_time = now
            self.index += 1
            if self.index >= len(self.frames):
                self.index = len(self.frames) - 1
                self.finished = True

    def handle_any_key(self, _key=None):
        if self.finished:
            self.change_scene("station")
        else:
            self.index = len(self.frames) - 1
            self.finished = True

    def render(self):
        frame_index = min(self.index, len(self.frames) - 1)
        frame_content = self.frames[frame_index]

        panel = WindowPanel(
            "[ DETECTIVE ALICE ]",
            lambda: render_intro(frame_content),
            border_style="bright_blue",
        )
        builder = RowLayoutBuilder([panel])
        return builder.build()
