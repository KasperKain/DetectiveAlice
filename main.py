import os
import random
import time

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import sys
import traceback

from engine.audio_manager import AudioManager
from engine.scene_manager import SceneManager
from engine.input import InputHandler
from engine.core import GameEngine
from engine.game_state import GameState
from utils.paths import resource_path

from config.game_config import (
    PLAYER,
    LOCATIONS,
    REFRESH_RATE,
    TICK_DELAY,
)


# Doesn't work as well as I'd like, but it's helpful
def excepthook(exc_type, exc_value, exc_traceback):
    print("\n=== UNCAUGHT EXCEPTION ===")
    traceback.print_exception(exc_type, exc_value, exc_traceback)


sys.excepthook = excepthook


def load_audio_assets():
    # I preload sounds, but not music files. Why I do this?
    sounds = {
        "speak": "audio/speak.wav",
        "open": "audio/open.wav",
        "trigger": "audio/trigger.wav",
        "push": "audio/push.wav",
        "collect": "audio/collect.wav",
        "end": "audio/end.wav",
        "arrow": "audio/arrow.wav",
    }

    for key, path in sounds.items():
        AudioManager.load_sound(key, resource_path(path))


# ----------------------------------------------------------
# Game initialization
# ----------------------------------------------------------
def create_engine():
    # Persistent game state
    game_state = GameState()
    scene_manager = SceneManager(PLAYER, LOCATIONS)
    input_handler = InputHandler(scene_manager)
    engine = GameEngine(
        scene_manager=scene_manager,
        input_handler=input_handler,
        refresh_rate=REFRESH_RATE,
        tick_delay=TICK_DELAY,
    )

    return engine


def fake_loading_bar(duration=3.0, width=30):
    start = time.time()
    last = 0

    while True:
        elapsed = time.time() - start
        progress = min(elapsed / duration, 1.0)

        filled = int(progress * width)
        bar = "█" * filled + "░" * (width - filled)

        percent = int(progress * 100)
        sys.stdout.write(f"\rLoading [{bar}] {percent}%")
        sys.stdout.flush()

        if progress >= 1:
            break
        time.sleep(random.uniform(0.03, 0.12))

    print()


def main():
    print("Initializing engine...\n")  # fake. Just for show

    load_audio_assets()

    fake_loading_bar(duration=4.5, width=32)
    engine = create_engine()
    AudioManager.play_music(resource_path("audio/end.wav"), volume=1, loops=0)
    engine.start()


if __name__ == "__main__":
    main()
