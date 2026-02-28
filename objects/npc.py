import random
from objects.base_object import GameObject


class NPC(GameObject):
    DELTAS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(
        self, position=(0, 0), character="1-9, A-Z", name="NPC", dialogue="Hello"
    ):
        super().__init__(
            position,
            character,
            name=name,
            dialogue=dialogue,
            color="light_sky_blue3",
        )
        self.start = position
        self.range = 2

    def update(self, world):
        # Do nothing if object is adjacent. Should prevent clipping issues.
        for obj in world.get_adjacent_objects(self):
            if obj:
                return

        if random.random() < 0.95:
            return

        random.shuffle(self.DELTAS)
        sr, sc = self.start

        for dr, dc in self.DELTAS:
            nr, nc = self.position[0] + dr, self.position[1] + dc

            # Thanks google.
            if abs(nr - sr) > self.range or abs(nc - sc) > self.range:
                continue

            if world.is_walkable((nr, nc)) and not world.get_object_at((nr, nc)):
                world.move_object(self, (nr, nc))
                break
