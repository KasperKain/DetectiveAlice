# engine/core.py
import threading
import traceback
from time import sleep

from rich.live import Live


class GameEngine:

    def __init__(self, scene_manager, input_handler, refresh_rate, tick_delay):
        self.scene_manager = scene_manager
        self.input_handler = input_handler
        self.refresh_rate = refresh_rate
        self.tick_delay = tick_delay

        self.running = True
        self.screen_lock = threading.Lock()

    def _update_screen(self, screen):
        if hasattr(screen, "update_objects"):
            screen.update_objects()

        # Generic update
        if hasattr(screen, "update"):
            screen.update()

    def start(self):
        self.input_handler.start()

        first_screen = self.scene_manager.get_screen()
        with Live(
            first_screen.render(),
            refresh_per_second=self.refresh_rate,
            screen=True,
        ) as live:
            while self.running:
                try:
                    with self.screen_lock:
                        screen = self.scene_manager.get_screen()

                        # quit flag from any screen
                        if getattr(screen, "should_quit", False):
                            self.running = False
                            break

                        self._update_screen(screen)

                        rendered = screen.render()
                        live.update(rendered)

                    sleep(self.tick_delay)

                except Exception:
                    print("\n\n=== INNER LOOP EXCEPTION ===")
                    traceback.print_exc()
                    raise
