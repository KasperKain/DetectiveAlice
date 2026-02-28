from engine.audio_manager import AudioManager
from objects.base_object import GameObject
from utils.paths import resource_path


class Block(GameObject):
    DELTAS = {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "WEST": (0, -1),
        "EAST": (0, 1),
    }

    def __init__(
        self, position=(0, 0), character="■", name="Block", color="light_green"
    ):
        super().__init__(
            position=position,
            character=character,
            name=name,
            color=color,
            dialogue="",
        )
        self.slide_direction = None

    def can_move(self):
        return True

    def interact(self, actor, world):

        ax, ay = actor.position
        bx, by = self.position

        # I forgot the math for the old block class. This works well enough for what the game is.
        if abs(ax - bx) + abs(ay - by) != 1:
            return

        AudioManager.play("push")

        # Determine push direction
        if bx < ax:
            self.slide_direction = "UP"
        elif bx > ax:
            self.slide_direction = "DOWN"
        elif by < ay:
            self.slide_direction = "WEST"
        else:
            self.slide_direction = "EAST"

    def update(self, world):
        if not self.slide_direction:
            return

        dy, dx = self.DELTAS[self.slide_direction]
        y, x = self.position

        new_y = y + dy
        new_x = x + dx
        new_position = (new_y, new_x)

        target = world.get_object_at(new_position)
        if target and hasattr(target, "trigger"):
            target.trigger(self)

        if world.is_walkable(new_position):
            self.move_to(world, new_position)
        else:
            self.slide_direction = None
