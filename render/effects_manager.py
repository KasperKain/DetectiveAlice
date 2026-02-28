import random
from rich.style import Style
import time

from engine.audio_manager import AudioManager


class EffectsManager:
    def __init__(self):
        self.effects = []
        self.tick = 0

    def update(self):
        self.tick += 1
        now = time.time()
        # Should remove expired effects.
        self.effects = [
            (effect, start, duration)
            for effect, start, duration in self.effects
            if duration is None or now - start < duration
        ]

    def add_effect(self, effect_callable, duration=None):
        self.effects.append((effect_callable, time.time(), duration))

    def apply(self, pos, char, style, player, world):
        now = time.time()
        active_effects = [
            (effect, start, duration)
            for effect, start, duration in self.effects
            if duration is None or now - start < duration
        ]
        # I don't remember how or why this works. Removing the params breaks the game though, so leave this alone future me!
        for effect, start, duration in active_effects:
            char, style = effect(pos, char, style, player, self.tick, world)
        return char, style


# EFFECT METHODS: AI helped a lot with these. Math isn't my strongest skill...But I did build the system itself, so yay!
def full_map_glitch(pos, char, style, player, tick, world):
    """Randomly replace most tiles with glitch symbols/colors."""
    if random.random() < 0.05:
        char = random.choice(["#", "h", "e", "l", "p", "m", "e"])
        style = Style(
            color=random.choice(["red", "magenta", "white", "cyan"]), bold=True
        )
    return char, style


def full_map_help_me(pos, char, style, player, tick, world):
    """Overwrite rows with a repeating 'HELP ME ' pattern"""
    help_str = "HELP ME "
    world_width = getattr(world, "width", None) or 80
    r, c = pos
    row_str = (help_str * ((world_width // len(help_str)) + 1))[:world_width]
    char = row_str[c % world_width]
    style = Style(color="red", bold=True)
    return char, style


def full_map_alice(pos, char, style, player, tick, world):
    """Overwrite rows with a repeating 'HELP ME ' pattern"""
    help_str = "A L I C E "
    world_width = getattr(world, "width", None) or 80
    r, c = pos
    row_str = (help_str * ((world_width // len(help_str)) + 1))[:world_width]
    char = row_str[c % world_width]
    style = Style(color="BLUE", bold=True)
    return char, style


def conceal_glitch(pos, char, style, player, tick, world):
    """Conceal all tiles"""
    style = Style(conceal=True)
    return char, style


def dim_glitch(pos, char, style, player, tick, world):
    style = Style(dim=True, italic=True)
    return char, style


def red_glitch(pos, char, style, player, tick, world):
    style = Style(dim=True, color="red")
    return char, style


def letter_glitch(pos, char, style, player, rick, world):
    char = random.choice(["A", "L", "I", "C", "E"])
    style = Style(color="white", dim=True)
    return char, style


def line_glitch(pos, char, style, player, tick, world):
    """Conceal random tiles"""
    if random.random() < 0.3:  # might up this later, might not.
        char = "-"
        style = style
    return char, style


def conceal_sprinkle(pos, char, style, player, tick, world):
    """Conceal random tiles"""
    if random.random() < 0.1:  # might up this later, might not.
        char = " "
        style = Style(color="white", bold=True)
    return char, style


def conceal_collapse(pos, char, style, player, tick, world):

    DURATION = 7.0

    elapsed = time.time() - getattr(world, "collapse_start_time", 0)
    progress = min(max(elapsed / DURATION, 0.0), 1.0)

    # Thanks google
    probability = progress**2

    if random.random() < probability:
        char = " "
        style = Style(color="black")

    return char, style


def skull_sprinkle(pos, char, style, player, tick, world):
    if random.random() < 0.001:
        char = "GO 💀 BACK"  # breaks the grid.... but it looks cooler that way so I'm keeping it.
        style = Style(color=random.choice(["white", "red", "magenta"]), bold=True)
    return char, style
