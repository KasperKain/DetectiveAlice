# engine/input.py

import threading
from time import sleep

import readchar


class InputHandler:

    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.running = True
        self.input_lock = threading.Lock()
        self.command_lock = threading.Lock()

    def start(self):
        t = threading.Thread(target=self._input_loop, daemon=True)
        t.start()

    def stop(self):
        self.running = False

    # Main loop
    def _input_loop(self):
        while self.running:
            try:
                key = self._read_key()
                screen = self.scene_manager.get_screen()

                # Any-key screens (intro)
                if getattr(screen, "accept_any", False):
                    screen.handle_any_key(key)
                    continue

                # Arrow-style keys & special keys
                if self._handle_special_keys(screen, key):
                    continue

                # Command mode (text input)
                if self._handle_command_keys(screen, key):
                    continue

            except Exception as e:
                import traceback

                print("\n[InputHandler] Exception in input loop:")
                traceback.print_exc()
                sleep(0.2)

    def _read_key(self):
        with self.input_lock:
            return readchar.readkey()

    def _handle_special_keys(self, screen, key):
        arrow_keys = {
            readchar.key.UP: "UP",
            readchar.key.DOWN: "DOWN",
            readchar.key.LEFT: "LEFT",
            readchar.key.RIGHT: "RIGHT",
        }

        if key == readchar.key.ESC:
            self.scene_manager.change_scene("overworld")
            return True

        if key == readchar.key.TAB:
            if hasattr(screen, "interact"):
                screen.interact()
            return True

        if key == "d" and hasattr(screen, "manual_effect_trigger"):
            screen.manual_effect_trigger()
            screen.manual_effect_trigger()
            return True

        if key in arrow_keys and getattr(screen, "accept_arrows", False):
            direction = arrow_keys[key]
            screen.handle_arrow(direction)
            return True

        return False

    def _handle_command_keys(self, screen, key):
        if not getattr(screen, "accept_commands", False):
            return False

        if key in (readchar.key.ENTER, "\r", "\n"):
            with self.command_lock:
                cmd = screen.command_buffer
                screen.command_buffer = ""
            self.scene_manager.handle_command(cmd)
            return True

        if key in (readchar.key.BACKSPACE, "\x7f", "\b"):
            with self.command_lock:
                screen.add_char_to_buffer("\x7f")
            return True

        if isinstance(key, str) and len(key) == 1 and 32 <= ord(key) <= 126:
            with self.command_lock:
                screen.add_char_to_buffer(key)
            return True

        return False
