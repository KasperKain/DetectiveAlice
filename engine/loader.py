# engine/loader.py

from inspect import signature

from objects.base_object import GameObject
from objects.block import Block
from objects.door import Door
from objects.final_item import FinalItem
from objects.item import Item
from objects.npc import NPC
from objects.player import Player
from objects.switch import Switch


CLASS_MAP = {
    "player": Player,
    "npc": NPC,
    "block": Block,
    "switch": Switch,
    "door": Door,
    "item": Item,
    "final_item": FinalItem,
}


class ObjectRegistry:
    def __init__(self):
        self.by_pos = {}

    def all_objects(self):
        return list(self.by_pos.values())

    def set_position(self, pos, obj):
        self.by_pos[tuple(pos)] = obj

    def remove(self, obj):
        pos = obj.position
        if self.by_pos.get(pos) is obj:
            del self.by_pos[pos]

    def clear_positions(self):
        self.by_pos.clear()


class ObjectLoader:
    @staticmethod
    def load_objects(base_grid, char_defs):
        registry = ObjectRegistry()
        player = None

        char_lookup = {
            data.get("character"): data
            for data in char_defs.values()
            if data.get("character") is not None
        }

        for row_idx, row in enumerate(base_grid):
            for col_idx, symbol in enumerate(row):
                pos = (row_idx, col_idx)

                # PLAYER
                if symbol == "@":
                    player = Player(position=pos)
                    registry.set_position(player.position, player)
                    base_grid[row_idx][col_idx] = " "
                    continue

                # OTHER OBJECTS
                if symbol in char_lookup:
                    data = char_lookup[symbol]
                    obj_type = data.get("type")
                    obj_class = CLASS_MAP.get(obj_type, GameObject)

                    ctor = signature(obj_class.__init__).parameters
                    kwargs = {}
                    if "position" in ctor:
                        kwargs["position"] = pos
                    if "character" in ctor:
                        kwargs["character"] = symbol

                    obj = obj_class(**kwargs)

                    if "name" in data:
                        obj.name = data["name"]
                    if "dialogue" in data:
                        obj.dialogue = data["dialogue"]

                    registry.set_position(obj.position, obj)

                    # Hacky solution for eliminating ghost objects
                    base_grid[row_idx][col_idx] = " "

        return registry, player
