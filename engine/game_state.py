# engine/game_state.py


class GameState:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.reset()
        return cls._instance

    # Core reset
    def reset(self):
        self.inventory = set()
        self.collected_items = []
        self.completed_maps = {}
        self.collected_all_items = False

    def add_collected_item(self, item_name, map_name):
        if map_name.endswith(".txt"):
            scene_name = map_name.removesuffix(".txt")
        else:
            scene_name = map_name

        if item_name not in self.inventory:
            self.inventory.add(item_name)
            self.collected_items.append({"name": item_name, "location": scene_name})

    def has_item(self, item_name):
        return item_name in self.inventory

    def complete_map(self, map_name):
        self.completed_maps[map_name] = True

    def is_map_completed(self, map_name):
        return self.completed_maps.get(map_name, False)

    def check_all_items_collected(self):
        return len(self.inventory) >= 7

    def get_collected_items(self):
        """Return a copy of collected items list."""
        return list(self.collected_items)

    def clear(self):
        self.reset()

    def enable_debug(self):
        self.debug_mode = True

    def check_debug(self):
        if hasattr(self, "debug_mode"):
            return True
        else:
            return False
