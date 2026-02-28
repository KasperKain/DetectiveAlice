# world/game_world.py

import time
from engine.audio_manager import AudioManager
from engine.game_state import GameState
from objects.player import Player
from render.effects_manager import EffectsManager


class GameWorld:
    def __init__(self, base_grid):
        self.base_grid = [row[:] for row in base_grid]
        self.height = len(self.base_grid)
        self.width = len(self.base_grid[0]) if self.height else 0

        self.objects = []
        self._pos_lookup = {}

        self.effects_manager = EffectsManager()

        self.info_message = ""
        self._effect_end_time = 0.0

    def trigger_effect(self, effect_fn, duration=2.0, message=None):

        self.effects_manager.add_effect(effect_fn, duration)

        if message:
            self.info_message = message
            self._effect_end_time = time.time() + duration

    def update_effects(self):
        self.effects_manager.update()

        if self.info_message and time.time() >= self._effect_end_time:
            self.info_message = ""

    def add_object(self, obj):
        self.objects.append(obj)
        self._pos_lookup[obj.position] = obj

    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)
        self._pos_lookup.pop(obj.position, None)

    def get_object_at(self, pos):
        return self._pos_lookup.get(tuple(pos))

    def get_adjacent_objects(self, obj):
        y, x = obj.position
        neighbors = []
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < self.height and 0 <= nx < self.width:
                target = self.get_object_at((ny, nx))
                if target:
                    neighbors.append(target)
        return neighbors

    def is_walkable(self, pos):
        r, c = pos
        tile = self.base_grid[r][c]
        return tile not in ["#", "^", "!", "|"]  # walls, spikes, etc.

    def move_object(self, obj, new_pos):
        gs = GameState()
        new_pos = tuple(new_pos)
        old_pos = obj.position

        # Block movement if tile or object is blocking
        if not self.is_walkable(new_pos) and gs.check_debug() == False:
            return False
        if new_pos in self._pos_lookup:
            return False
        # Move
        self._pos_lookup.pop(old_pos, None)
        self._pos_lookup[new_pos] = obj
        obj.position = new_pos
        return True
